from __future__ import annotations

from sqlalchemy import text

from python.etl.inventory_sources import utc_now_iso
from python.etl.metric_mapping import MAPPING_SCHEMA_SQL_PATH, normalize_metric_key
from python.etl.standard_metric_master import (
    ensure_standard_metric_runtime_columns,
    execute_standard_metric_master_schema,
    reseed_metric_name_mapping,
    sync_metric_alias_map,
    upsert_standard_metric_seed_rows,
)


def execute_metric_mapping_schema(engine) -> None:
    execute_standard_metric_master_schema(engine)
    ensure_standard_metric_runtime_columns(engine)

    script = MAPPING_SCHEMA_SQL_PATH.read_text(encoding="utf-8")
    statements = [statement.strip() for statement in script.split(";") if statement.strip()]
    with engine.begin() as connection:
        for statement in statements:
            if "idx_metric_alias_map_standard_metric_id" in statement:
                continue
            if "idx_integrated_enriched_standard_metric_id" in statement:
                continue
            connection.exec_driver_sql(statement)

    ensure_standard_metric_runtime_columns(engine)


def seed_metric_alias_map(connection) -> None:
    # v2 authoritative seed flow:
    # 1. seed standard_metric master rows
    # 2. seed metric_name_mapping rows
    # 3. mirror active rows back into legacy metric_alias_map for compatibility
    standard_metric_lookup = upsert_standard_metric_seed_rows(connection)
    reseed_metric_name_mapping(connection, standard_metric_lookup)
    sync_metric_alias_map(connection)


def fetch_metric_alias_map(connection) -> dict[str, dict]:
    rows = connection.execute(
        text(
            """
            SELECT
                normalized_metric_key,
                standard_metric_id,
                standard_metric_name,
                mapping_rule,
                mapping_confidence
            FROM metric_name_mapping
            WHERE is_active = 1
            """
        )
    ).mappings().all()
    return {row["normalized_metric_key"]: dict(row) for row in rows}


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


def build_enriched_records(integrated_rows: list[dict], metric_alias_map: dict[str, object]) -> list[dict]:
    enriched_at = utc_now_iso()
    enriched_records: list[dict] = []

    for row in integrated_rows:
        normalized_metric_key, metric_variant = normalize_metric_key(row["raw_metric_name"])
        mapping_row = metric_alias_map.get(normalized_metric_key)
        if isinstance(mapping_row, dict):
            standard_metric_id = mapping_row.get("standard_metric_id")
            standard_metric_name = mapping_row.get("standard_metric_name")
        else:
            standard_metric_id = None
            standard_metric_name = mapping_row if mapping_row else None
        enriched_records.append(
            {
                "integrated_observation_id": row["integrated_observation_id"],
                "company_key": row.get("company_key"),
                "raw_metric_name": row["raw_metric_name"],
                "normalized_metric_key": normalized_metric_key,
                "standard_metric_id": standard_metric_id,
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
                        standard_metric_id,
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
                        :standard_metric_id,
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
