from __future__ import annotations

from sqlalchemy import text

from python.etl.inventory_sources import utc_now_iso
from python.etl.metric_mapping import MAPPING_SCHEMA_SQL_PATH, default_metric_alias_rows, normalize_metric_key


def execute_metric_mapping_schema(engine) -> None:
    script = MAPPING_SCHEMA_SQL_PATH.read_text(encoding="utf-8")
    statements = [statement.strip() for statement in script.split(";") if statement.strip()]
    with engine.begin() as connection:
        for statement in statements:
            connection.exec_driver_sql(statement)


def seed_metric_alias_map(connection) -> None:
    connection.execute(text("DELETE FROM metric_alias_map"))
    connection.execute(
        text(
            """
            INSERT INTO metric_alias_map (
                normalized_metric_key,
                standard_metric_name,
                is_active
            ) VALUES (
                :normalized_metric_key,
                :standard_metric_name,
                :is_active
            )
            """
        ),
        default_metric_alias_rows(),
    )


def fetch_metric_alias_map(connection) -> dict[str, str]:
    rows = connection.execute(
        text(
            """
            SELECT normalized_metric_key, standard_metric_name
            FROM metric_alias_map
            WHERE is_active = 1
            """
        )
    ).fetchall()
    return {row.normalized_metric_key: row.standard_metric_name for row in rows}


def fetch_integrated_rows(connection) -> list[dict]:
    rows = connection.execute(
        text(
            """
            SELECT
                integrated_observation_id,
                company_key,
                raw_metric_name,
                period_type,
                fiscal_year,
                fiscal_quarter,
                date_raw,
                selected_source_group,
                selected_raw_observation_id,
                selected_value_numeric,
                selected_is_estimate
            FROM integrated_observation
            """
        )
    ).mappings().all()
    return [dict(row) for row in rows]


def build_enriched_records(integrated_rows: list[dict], metric_alias_map: dict[str, str]) -> list[dict]:
    enriched_at = utc_now_iso()
    enriched_records: list[dict] = []

    for row in integrated_rows:
        normalized_metric_key, metric_variant = normalize_metric_key(row["raw_metric_name"])
        standard_metric_name = metric_alias_map.get(normalized_metric_key)
        enriched_records.append(
            {
                "integrated_observation_id": row["integrated_observation_id"],
                "company_key": row.get("company_key"),
                "raw_metric_name": row["raw_metric_name"],
                "normalized_metric_key": normalized_metric_key,
                "standard_metric_name": standard_metric_name,
                "metric_variant": metric_variant,
                "period_type": row["period_type"],
                "fiscal_year": row.get("fiscal_year"),
                "fiscal_quarter": row.get("fiscal_quarter"),
                "date_raw": row.get("date_raw"),
                "selected_source_group": row.get("selected_source_group"),
                "selected_raw_observation_id": row.get("selected_raw_observation_id"),
                "selected_value_numeric": row.get("selected_value_numeric"),
                "selected_is_estimate": int(row.get("selected_is_estimate") or 0),
                "enriched_at": enriched_at,
            }
        )

    return enriched_records


def rebuild_integrated_observation_enriched(engine) -> int:
    execute_metric_mapping_schema(engine)

    with engine.begin() as connection:
        seed_metric_alias_map(connection)
        metric_alias_map = fetch_metric_alias_map(connection)
        integrated_rows = fetch_integrated_rows(connection)
        enriched_records = build_enriched_records(integrated_rows, metric_alias_map)

        connection.execute(text("DELETE FROM integrated_observation_enriched"))
        if enriched_records:
            connection.execute(
                text(
                    """
                    INSERT INTO integrated_observation_enriched (
                        integrated_observation_id,
                        company_key,
                        raw_metric_name,
                        normalized_metric_key,
                        standard_metric_name,
                        metric_variant,
                        period_type,
                        fiscal_year,
                        fiscal_quarter,
                        date_raw,
                        selected_source_group,
                        selected_raw_observation_id,
                        selected_value_numeric,
                        selected_is_estimate,
                        enriched_at
                    ) VALUES (
                        :integrated_observation_id,
                        :company_key,
                        :raw_metric_name,
                        :normalized_metric_key,
                        :standard_metric_name,
                        :metric_variant,
                        :period_type,
                        :fiscal_year,
                        :fiscal_quarter,
                        :date_raw,
                        :selected_source_group,
                        :selected_raw_observation_id,
                        :selected_value_numeric,
                        :selected_is_estimate,
                        :enriched_at
                    )
                    """
                ),
                enriched_records,
            )

    return len(enriched_records)
