from __future__ import annotations

from sqlalchemy import text

from python.etl.db_runtime import DEFAULT_SQLITE_DB_PATH, create_sqlite_engine, ensure_runtime_schema


def print_section(title: str) -> None:
    print()
    print(f"=== {title} ===")


def main() -> None:
    engine = create_sqlite_engine()
    ensure_runtime_schema(engine)

    with engine.begin() as connection:
        kdata1_files = connection.execute(
            text(
                """
                SELECT source_file_id, file_name, relative_path
                FROM source_file
                WHERE source_group = 'KDATA1'
                ORDER BY source_file_id
                """
            )
        ).fetchall()

        total_kdata1_rows = connection.execute(
            text(
                """
                SELECT COUNT(*)
                FROM raw_observation
                WHERE source_group = 'KDATA1'
                """
            )
        ).scalar_one()

        recent_rows = connection.execute(
            text(
                """
                SELECT
                    raw_observation_id,
                    source_file_id,
                    raw_metric_name,
                    value_text,
                    value_numeric,
                    date_raw,
                    fiscal_year,
                    fiscal_quarter,
                    period_label_std,
                    period_type
                FROM raw_observation
                WHERE source_group = 'KDATA1'
                ORDER BY raw_observation_id DESC
                LIMIT 20
                """
            )
        ).fetchall()

        anomaly_summary = connection.execute(
            text(
                """
                SELECT
                    SUM(CASE WHEN raw_metric_name IS NULL OR TRIM(raw_metric_name) = '' THEN 1 ELSE 0 END) AS empty_metric_name_rows,
                    SUM(CASE WHEN date_raw IS NULL OR TRIM(date_raw) = '' THEN 1 ELSE 0 END) AS empty_date_raw_rows,
                    SUM(CASE WHEN fiscal_quarter IS NULL THEN 1 ELSE 0 END) AS null_fiscal_quarter_rows,
                    SUM(CASE WHEN value_numeric IS NULL THEN 1 ELSE 0 END) AS null_value_numeric_rows
                FROM raw_observation
                WHERE source_group = 'KDATA1'
                """
            )
        ).one()

        row_counts_by_file = connection.execute(
            text(
                """
                SELECT
                    sf.source_file_id,
                    sf.file_name,
                    sf.relative_path,
                    COUNT(ro.raw_observation_id) AS raw_row_count
                FROM source_file sf
                LEFT JOIN raw_observation ro
                  ON ro.source_file_id = sf.source_file_id
                 AND ro.source_group = 'KDATA1'
                WHERE sf.source_group = 'KDATA1'
                GROUP BY sf.source_file_id, sf.file_name, sf.relative_path
                ORDER BY sf.source_file_id
                """
            )
        ).fetchall()

    print("KDATA1 load inspection")
    print(f"Database: {DEFAULT_SQLITE_DB_PATH}")

    print_section("KDATA1 source_file rows")
    if kdata1_files:
        for row in kdata1_files:
            print(f"[{row.source_file_id}] {row.file_name} | {row.relative_path}")
    else:
        print("No KDATA1 source_file rows found.")

    print_section("Raw row count by KDATA1 source_file")
    if row_counts_by_file:
        for row in row_counts_by_file:
            print(f"[{row.source_file_id}] {row.file_name} | rows={row.raw_row_count} | {row.relative_path}")
    else:
        print("No KDATA1 source_file rows found.")

    print_section("Total KDATA1 raw_observation rows")
    print(f"{int(total_kdata1_rows)}")

    print_section("Recent KDATA1 raw rows")
    if recent_rows:
        for row in recent_rows:
            print(
                f"[{row.raw_observation_id}] file_id={row.source_file_id} | "
                f"metric={row.raw_metric_name} | value_text={row.value_text} | "
                f"value_numeric={row.value_numeric} | date_raw={row.date_raw} | "
                f"fy={row.fiscal_year} | fq={row.fiscal_quarter} | "
                f"label={row.period_label_std} | period_type={row.period_type}"
            )
    else:
        print("No KDATA1 raw_observation rows found.")

    print_section("KDATA1 anomaly summary")
    print(f"empty raw_metric_name rows: {int(anomaly_summary.empty_metric_name_rows or 0)}")
    print(f"empty date_raw rows: {int(anomaly_summary.empty_date_raw_rows or 0)}")
    print(f"null fiscal_quarter rows: {int(anomaly_summary.null_fiscal_quarter_rows or 0)}")
    print(f"null value_numeric rows: {int(anomaly_summary.null_value_numeric_rows or 0)}")


if __name__ == "__main__":
    main()
