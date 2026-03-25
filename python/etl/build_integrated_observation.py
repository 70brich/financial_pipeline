from __future__ import annotations

from collections import defaultdict
from datetime import datetime
from pathlib import Path

from sqlalchemy import text

from python.etl.inventory_sources import utc_now_iso


INTEGRATED_SCHEMA_SQL_PATH = Path(__file__).resolve().parents[2] / "sql" / "004_create_integrated_tables.sql"

SOURCE_PRIORITY = {
    "YEAR": {"QDATA": 0, "KDATA2": 1, "KDATA1": 2},
    "QUARTER": {"QDATA": 0, "KDATA1": 1, "KDATA2": 2},
    "SNAPSHOT": {"QDATA": 0, "KDATA2": 1, "KDATA1": 2},
}


def execute_integrated_schema(engine) -> None:
    script = INTEGRATED_SCHEMA_SQL_PATH.read_text(encoding="utf-8")
    statements = [statement.strip() for statement in script.split(";") if statement.strip()]
    with engine.begin() as connection:
        for statement in statements:
            connection.exec_driver_sql(statement)


def make_company_key(row: dict) -> str | None:
    for key in ("normalized_stock_code", "raw_stock_code", "raw_company_name"):
        value = row.get(key)
        if value is None:
            continue
        text_value = str(value).strip()
        if text_value:
            return text_value
    return None


def build_integrated_key(row: dict) -> tuple:
    company_key = make_company_key(row)
    period_type = row["period_type"]
    raw_metric_name = row["raw_metric_name"]
    fiscal_year = row.get("fiscal_year")
    fiscal_quarter = row.get("fiscal_quarter")
    date_raw = row.get("date_raw")

    if period_type == "YEAR":
        return (company_key, raw_metric_name, period_type, fiscal_year, None, None)
    if period_type == "QUARTER":
        return (company_key, raw_metric_name, period_type, fiscal_year, fiscal_quarter, None)
    if period_type == "SNAPSHOT":
        return (company_key, raw_metric_name, period_type, None, None, date_raw)
    raise ValueError(f"Unsupported period_type: {period_type}")


def parse_ingested_at(value: str | None) -> datetime:
    if not value:
        return datetime.min
    normalized = value.replace("Z", "+00:00")
    try:
        return datetime.fromisoformat(normalized)
    except ValueError:
        return datetime.min


def candidate_sort_key(row: dict) -> tuple:
    period_type = row["period_type"]
    source_group = row["source_group"]
    priority = SOURCE_PRIORITY[period_type].get(source_group, 999)
    is_estimate = int(row.get("is_estimate") or 0)
    value_numeric_missing = 0 if row.get("value_numeric") is not None else 1
    ingested_sort = parse_ingested_at(row.get("ingested_at"))
    raw_observation_id = int(row["raw_observation_id"])
    return (
        is_estimate,
        priority,
        value_numeric_missing,
        -int(ingested_sort.timestamp()) if ingested_sort != datetime.min else 0,
        -raw_observation_id,
    )


def selection_reason_for(row: dict) -> str:
    source_suffix = row["source_group"].lower()
    if int(row.get("is_estimate") or 0) == 0:
        return f"confirmed_{source_suffix}"
    return f"estimate_{source_suffix}_fallback"


def build_integrated_records(raw_rows: list[dict]) -> list[dict]:
    grouped_rows: dict[tuple, list[dict]] = defaultdict(list)
    for row in raw_rows:
        if not row.get("raw_metric_name"):
            continue
        grouped_rows[build_integrated_key(row)].append(row)

    integrated_at = utc_now_iso()
    integrated_records: list[dict] = []

    for integrated_key, candidates in grouped_rows.items():
        selected = sorted(candidates, key=candidate_sort_key)[0]
        company_key, raw_metric_name, period_type, fiscal_year, fiscal_quarter, date_raw = integrated_key
        integrated_records.append(
            {
                "company_key": company_key,
                "raw_metric_name": raw_metric_name,
                "period_type": period_type,
                "fiscal_year": fiscal_year,
                "fiscal_quarter": fiscal_quarter,
                "date_raw": date_raw if period_type == "SNAPSHOT" else selected.get("date_raw"),
                "period_label_std": selected.get("period_label_std"),
                "selected_raw_observation_id": selected["raw_observation_id"],
                "selected_source_file_id": selected.get("source_file_id"),
                "selected_source_group": selected["source_group"],
                "selected_value_text": selected.get("value_text"),
                "selected_value_numeric": selected.get("value_numeric"),
                "selected_is_estimate": int(selected.get("is_estimate") or 0),
                "selection_reason": selection_reason_for(selected),
                "integrated_at": integrated_at,
            }
        )

    return integrated_records


def fetch_raw_observations(connection) -> list[dict]:
    rows = connection.execute(
        text(
            """
            SELECT
                raw_observation_id,
                source_file_id,
                source_group,
                raw_company_name,
                raw_stock_code,
                normalized_stock_code,
                raw_metric_name,
                value_text,
                value_numeric,
                is_estimate,
                date_raw,
                period_type,
                fiscal_year,
                fiscal_quarter,
                period_label_std,
                ingested_at
            FROM raw_observation
            """
        )
    ).mappings().all()
    return [dict(row) for row in rows]


def rebuild_integrated_observation(engine) -> int:
    execute_integrated_schema(engine)

    with engine.begin() as connection:
        raw_rows = fetch_raw_observations(connection)
        integrated_records = build_integrated_records(raw_rows)

        connection.execute(text("DELETE FROM integrated_observation"))
        if integrated_records:
            connection.execute(
                text(
                    """
                    INSERT INTO integrated_observation (
                        company_key,
                        raw_metric_name,
                        period_type,
                        fiscal_year,
                        fiscal_quarter,
                        date_raw,
                        period_label_std,
                        selected_raw_observation_id,
                        selected_source_file_id,
                        selected_source_group,
                        selected_value_text,
                        selected_value_numeric,
                        selected_is_estimate,
                        selection_reason,
                        integrated_at
                    ) VALUES (
                        :company_key,
                        :raw_metric_name,
                        :period_type,
                        :fiscal_year,
                        :fiscal_quarter,
                        :date_raw,
                        :period_label_std,
                        :selected_raw_observation_id,
                        :selected_source_file_id,
                        :selected_source_group,
                        :selected_value_text,
                        :selected_value_numeric,
                        :selected_is_estimate,
                        :selection_reason,
                        :integrated_at
                    )
                    """
                ),
                integrated_records,
            )

    return len(integrated_records)
