from __future__ import annotations

from sqlalchemy import text

from python.etl.build_integrated_observation import execute_integrated_schema
from python.etl.db_runtime import DEFAULT_SQLITE_DB_PATH, create_sqlite_engine, ensure_runtime_schema


def print_section(title: str) -> None:
    print()
    print(f"=== {title} ===")


def main() -> None:
    engine = create_sqlite_engine()
    ensure_runtime_schema(engine)
    execute_integrated_schema(engine)

    with engine.begin() as connection:
        total_count = connection.execute(
            text("SELECT COUNT(*) FROM integrated_observation")
        ).scalar_one()

        period_type_counts = connection.execute(
            text(
                """
                SELECT period_type, COUNT(*) AS row_count
                FROM integrated_observation
                GROUP BY period_type
                ORDER BY period_type
                """
            )
        ).fetchall()

        source_group_counts = connection.execute(
            text(
                """
                SELECT selected_source_group, COUNT(*) AS row_count
                FROM integrated_observation
                GROUP BY selected_source_group
                ORDER BY selected_source_group
                """
            )
        ).fetchall()

        estimate_counts = connection.execute(
            text(
                """
                SELECT selected_is_estimate, COUNT(*) AS row_count
                FROM integrated_observation
                GROUP BY selected_is_estimate
                ORDER BY selected_is_estimate
                """
            )
        ).fetchall()

        recent_rows = connection.execute(
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
                    selected_value_text,
                    selected_value_numeric,
                    selected_is_estimate,
                    selection_reason
                FROM integrated_observation
                ORDER BY integrated_observation_id DESC
                LIMIT 30
                """
            )
        ).fetchall()

        conflict_rows = connection.execute(
            text(
                """
                WITH raw_keys AS (
                    SELECT
                        COALESCE(NULLIF(normalized_stock_code, ''), NULLIF(raw_stock_code, ''), NULLIF(raw_company_name, '')) AS company_key,
                        raw_metric_name,
                        period_type,
                        CASE WHEN period_type = 'YEAR' THEN fiscal_year
                             WHEN period_type = 'QUARTER' THEN fiscal_year
                             ELSE NULL END AS key_fiscal_year,
                        CASE WHEN period_type = 'QUARTER' THEN fiscal_quarter ELSE NULL END AS key_fiscal_quarter,
                        CASE WHEN period_type = 'SNAPSHOT' THEN date_raw ELSE NULL END AS key_date_raw,
                        COUNT(*) AS candidate_count
                    FROM raw_observation
                    GROUP BY
                        COALESCE(NULLIF(normalized_stock_code, ''), NULLIF(raw_stock_code, ''), NULLIF(raw_company_name, '')),
                        raw_metric_name,
                        period_type,
                        CASE WHEN period_type = 'YEAR' THEN fiscal_year
                             WHEN period_type = 'QUARTER' THEN fiscal_year
                             ELSE NULL END,
                        CASE WHEN period_type = 'QUARTER' THEN fiscal_quarter ELSE NULL END,
                        CASE WHEN period_type = 'SNAPSHOT' THEN date_raw ELSE NULL END
                    HAVING COUNT(*) >= 2
                )
                SELECT
                    rk.company_key,
                    rk.raw_metric_name,
                    rk.period_type,
                    rk.key_fiscal_year,
                    rk.key_fiscal_quarter,
                    rk.key_date_raw,
                    rk.candidate_count,
                    io.selected_source_group,
                    io.selected_raw_observation_id
                FROM raw_keys rk
                LEFT JOIN integrated_observation io
                  ON io.company_key IS rk.company_key
                 AND io.raw_metric_name = rk.raw_metric_name
                 AND io.period_type = rk.period_type
                 AND io.fiscal_year IS rk.key_fiscal_year
                 AND io.fiscal_quarter IS rk.key_fiscal_quarter
                 AND io.date_raw IS rk.key_date_raw
                ORDER BY rk.candidate_count DESC, rk.raw_metric_name
                LIMIT 20
                """
            )
        ).fetchall()

        anomaly_summary = connection.execute(
            text(
                """
                WITH duplicated_keys AS (
                    SELECT
                        company_key,
                        raw_metric_name,
                        period_type,
                        fiscal_year,
                        fiscal_quarter,
                        date_raw,
                        COUNT(*) AS duplicate_count
                    FROM integrated_observation
                    GROUP BY company_key, raw_metric_name, period_type, fiscal_year, fiscal_quarter, date_raw
                    HAVING COUNT(*) > 1
                )
                SELECT
                    (SELECT COUNT(*) FROM integrated_observation WHERE company_key IS NULL OR TRIM(company_key) = '') AS null_company_key_rows,
                    (SELECT COUNT(*) FROM integrated_observation WHERE raw_metric_name IS NULL OR TRIM(raw_metric_name) = '') AS empty_raw_metric_name_rows,
                    (SELECT COUNT(*) FROM integrated_observation WHERE selected_raw_observation_id IS NULL) AS null_selected_raw_observation_rows,
                    (SELECT COUNT(*) FROM integrated_observation WHERE selected_source_group IS NULL OR TRIM(selected_source_group) = '') AS null_selected_source_group_rows,
                    (SELECT COALESCE(SUM(duplicate_count), 0) FROM duplicated_keys) AS duplicated_integrated_key_rows
                """
            )
        ).one()

    print("Integrated observation inspection")
    print(f"Database: {DEFAULT_SQLITE_DB_PATH}")

    print_section("Integrated total row count")
    print(f"{int(total_count)}")

    print_section("Row count by period_type")
    for row in period_type_counts:
        print(f"{row.period_type}: {row.row_count}")

    print_section("Row count by selected_source_group")
    for row in source_group_counts:
        print(f"{row.selected_source_group}: {row.row_count}")

    print_section("Row count by selected_is_estimate")
    for row in estimate_counts:
        print(f"{row.selected_is_estimate}: {row.row_count}")

    print_section("Recent integrated rows")
    if recent_rows:
        for row in recent_rows:
            print(
                f"[{row.integrated_observation_id}] company_key={row.company_key} | metric={row.raw_metric_name} | "
                f"period_type={row.period_type} | fy={row.fiscal_year} | fq={row.fiscal_quarter} | date_raw={row.date_raw} | "
                f"selected_source_group={row.selected_source_group} | selected_raw_observation_id={row.selected_raw_observation_id} | "
                f"value_text={row.selected_value_text} | value_numeric={row.selected_value_numeric} | "
                f"is_estimate={row.selected_is_estimate} | reason={row.selection_reason}"
            )
    else:
        print("No integrated rows found.")

    print_section("Conflict candidate samples")
    if conflict_rows:
        for row in conflict_rows:
            print(
                f"company_key={row.company_key} | metric={row.raw_metric_name} | period_type={row.period_type} | "
                f"fy={row.key_fiscal_year} | fq={row.key_fiscal_quarter} | date_raw={row.key_date_raw} | "
                f"candidate_count={row.candidate_count} | selected_source_group={row.selected_source_group} | "
                f"selected_raw_observation_id={row.selected_raw_observation_id}"
            )
    else:
        print("No conflict candidates found.")

    print_section("Anomaly summary")
    print(f"null company_key rows: {int(anomaly_summary.null_company_key_rows or 0)}")
    print(f"empty raw_metric_name rows: {int(anomaly_summary.empty_raw_metric_name_rows or 0)}")
    print(f"null selected_raw_observation_id rows: {int(anomaly_summary.null_selected_raw_observation_rows or 0)}")
    print(f"null selected_source_group rows: {int(anomaly_summary.null_selected_source_group_rows or 0)}")
    print(f"duplicated integrated key rows: {int(anomaly_summary.duplicated_integrated_key_rows or 0)}")


if __name__ == "__main__":
    main()
