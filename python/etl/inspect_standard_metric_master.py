from __future__ import annotations

from sqlalchemy import text

from python.etl.build_integrated_observation import execute_integrated_schema
from python.etl.build_integrated_observation_enriched import execute_metric_mapping_schema
from python.etl.db_runtime import DEFAULT_SQLITE_DB_PATH, create_sqlite_engine, ensure_runtime_schema


def print_section(title: str) -> None:
    print()
    print(f"=== {title} ===")


def main() -> None:
    engine = create_sqlite_engine()
    ensure_runtime_schema(engine)
    execute_integrated_schema(engine)
    execute_metric_mapping_schema(engine)

    with engine.begin() as connection:
        summary = connection.execute(
            text(
                """
                SELECT
                    (SELECT COUNT(*) FROM standard_metric) AS standard_metric_count,
                    (SELECT COUNT(*) FROM metric_name_mapping WHERE is_active = 1) AS metric_name_mapping_count,
                    (SELECT COUNT(*) FROM metric_alias_map WHERE is_active = 1) AS metric_alias_map_count,
                    (SELECT COUNT(*) FROM integrated_observation_enriched) AS enriched_row_count,
                    (
                        SELECT COUNT(*)
                        FROM integrated_observation_enriched
                        WHERE standard_metric_id IS NOT NULL
                    ) AS mapped_enriched_row_count,
                    (
                        SELECT COUNT(*)
                        FROM integrated_observation_enriched
                        WHERE standard_metric_id IS NULL
                    ) AS unmapped_enriched_row_count,
                    (
                        SELECT COUNT(DISTINCT raw_metric_name)
                        FROM integrated_observation_enriched
                    ) AS distinct_raw_metric_name_count,
                    (
                        SELECT COUNT(DISTINCT raw_metric_name)
                        FROM integrated_observation_enriched
                        WHERE standard_metric_id IS NOT NULL
                    ) AS mapped_distinct_raw_metric_name_count
                """
            )
        ).one()

        standard_metric_counts = connection.execute(
            text(
                """
                SELECT
                    sm.standard_metric_name,
                    sm.metric_family,
                    COUNT(e.integrated_observation_enriched_id) AS row_count
                FROM standard_metric sm
                LEFT JOIN integrated_observation_enriched e
                  ON e.standard_metric_id = sm.standard_metric_id
                GROUP BY sm.standard_metric_id, sm.standard_metric_name, sm.metric_family
                ORDER BY row_count DESC, sm.standard_metric_name
                LIMIT 50
                """
            )
        ).fetchall()

        mapping_samples = connection.execute(
            text(
                """
                SELECT
                    m.normalized_metric_key,
                    m.raw_metric_name_example,
                    m.standard_metric_name,
                    m.mapping_rule,
                    m.mapping_confidence
                FROM metric_name_mapping m
                WHERE m.is_active = 1
                ORDER BY m.standard_metric_name, m.normalized_metric_key
                LIMIT 50
                """
            )
        ).fetchall()

        orphan_alias_rows = connection.execute(
            text(
                """
                SELECT
                    a.normalized_metric_key,
                    a.standard_metric_name,
                    a.standard_metric_id
                FROM metric_alias_map a
                LEFT JOIN standard_metric sm
                  ON sm.standard_metric_id = a.standard_metric_id
                WHERE a.is_active = 1
                  AND (a.standard_metric_id IS NULL OR sm.standard_metric_id IS NULL)
                ORDER BY a.normalized_metric_key
                LIMIT 50
                """
            )
        ).fetchall()

        recent_rows = connection.execute(
            text(
                """
                SELECT
                    integrated_observation_enriched_id,
                    integrated_observation_id,
                    raw_metric_name,
                    normalized_metric_key,
                    standard_metric_id,
                    standard_metric_name,
                    metric_variant,
                    period_type,
                    fiscal_year,
                    fiscal_quarter,
                    date_raw,
                    selected_source_group
                FROM integrated_observation_enriched
                ORDER BY integrated_observation_enriched_id DESC
                LIMIT 30
                """
            )
        ).fetchall()

    total_rows = int(summary.enriched_row_count or 0)
    mapped_rows = int(summary.mapped_enriched_row_count or 0)
    total_distinct = int(summary.distinct_raw_metric_name_count or 0)
    mapped_distinct = int(summary.mapped_distinct_raw_metric_name_count or 0)

    row_coverage = (mapped_rows / total_rows * 100.0) if total_rows else 0.0
    distinct_coverage = (mapped_distinct / total_distinct * 100.0) if total_distinct else 0.0

    print("Standard metric master inspection")
    print(f"Database: {DEFAULT_SQLITE_DB_PATH}")

    print_section("Master summary")
    print(f"standard_metric rows: {summary.standard_metric_count}")
    print(f"metric_name_mapping active rows: {summary.metric_name_mapping_count}")
    print(f"metric_alias_map active rows: {summary.metric_alias_map_count}")

    print_section("Coverage summary")
    print(f"integrated_observation_enriched rows: {total_rows}")
    print(f"mapped enriched rows: {mapped_rows}")
    print(f"unmapped enriched rows: {summary.unmapped_enriched_row_count}")
    print(f"row coverage ratio: {row_coverage:.2f}%")
    print(f"distinct raw_metric_name count: {total_distinct}")
    print(f"mapped distinct raw_metric_name count: {mapped_distinct}")
    print(f"distinct coverage ratio: {distinct_coverage:.2f}%")

    print_section("Standard metric row counts")
    for row in standard_metric_counts:
        print(f"{row.standard_metric_name} | family={row.metric_family} | rows={row.row_count}")

    print_section("Metric name mapping samples")
    for row in mapping_samples:
        print(
            f"{row.normalized_metric_key} -> {row.standard_metric_name} | "
            f"rule={row.mapping_rule} | confidence={row.mapping_confidence} | "
            f"example={row.raw_metric_name_example}"
        )

    print_section("Alias rows missing standard_metric link")
    if orphan_alias_rows:
        for row in orphan_alias_rows:
            print(
                f"{row.normalized_metric_key} -> {row.standard_metric_name} | "
                f"standard_metric_id={row.standard_metric_id}"
            )
    else:
        print("No orphan alias rows found.")

    print_section("Recent normalized rows")
    for row in recent_rows:
        print(
            f"[{row.integrated_observation_enriched_id}] integrated_id={row.integrated_observation_id} | "
            f"raw_metric_name={row.raw_metric_name} | normalized_metric_key={row.normalized_metric_key} | "
            f"standard_metric_id={row.standard_metric_id} | standard_metric_name={row.standard_metric_name} | "
            f"metric_variant={row.metric_variant} | period_type={row.period_type} | "
            f"fy={row.fiscal_year} | fq={row.fiscal_quarter} | date_raw={row.date_raw} | "
            f"selected_source_group={row.selected_source_group}"
        )


if __name__ == "__main__":
    main()
