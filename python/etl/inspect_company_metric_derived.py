from __future__ import annotations

from sqlalchemy import text

from python.etl.db_runtime import DEFAULT_SQLITE_DB_PATH, create_sqlite_engine
from python.etl.derived_views import ensure_derived_layer


def _print_rows(title: str, rows, formatter) -> None:
    print()
    print(title)
    if not rows:
        print("No rows found.")
        return
    for row in rows:
        print(formatter(row))


def main() -> None:
    engine = create_sqlite_engine()
    ensure_derived_layer(engine)

    with engine.begin() as connection:
        total_rows = connection.execute(
            text("SELECT COUNT(*) FROM company_metric_derived_v1")
        ).scalar_one()

        metric_counts = connection.execute(
            text(
                """
                SELECT standard_metric_name, COUNT(*) AS row_count
                FROM company_metric_derived_v1
                GROUP BY standard_metric_name
                ORDER BY row_count DESC, standard_metric_name
                """
            )
        ).mappings().all()

        period_distribution = connection.execute(
            text(
                """
                SELECT period_type, COUNT(*) AS row_count
                FROM company_metric_derived_v1
                GROUP BY period_type
                ORDER BY row_count DESC, period_type
                """
            )
        ).mappings().all()

        top_company_row = connection.execute(
            text(
                """
                SELECT COALESCE(company_name, company_key, 'UNKNOWN') AS company_label
                FROM company_metric_derived_v1
                GROUP BY company_label
                ORDER BY COUNT(*) DESC, company_label
                LIMIT 1
                """
            )
        ).mappings().first()

        sample_rows = []
        if top_company_row:
            sample_rows = connection.execute(
                text(
                    """
                    SELECT
                        company_name,
                        company_key,
                        standard_metric_name,
                        period_type,
                        fiscal_year,
                        fiscal_quarter,
                        date_raw,
                        value_numeric,
                        current_value_numeric,
                        compare_value_numeric,
                        calculation_method
                    FROM company_metric_derived_v1
                    WHERE COALESCE(company_name, company_key, 'UNKNOWN') = :company_label
                      AND standard_metric_name IN ('REVENUE_YOY', 'EPS_YOY', 'OPERATING_MARGIN')
                    ORDER BY
                        COALESCE(date_raw, '') DESC,
                        COALESCE(fiscal_year, 0) DESC,
                        COALESCE(fiscal_quarter, 0) DESC,
                        anchor_integrated_observation_id DESC
                    LIMIT 20
                    """
                ),
                {"company_label": top_company_row["company_label"]},
            ).mappings().all()

        null_sample = connection.execute(
            text(
                """
                SELECT
                    company_name,
                    company_key,
                    standard_metric_name,
                    period_type,
                    fiscal_year,
                    fiscal_quarter,
                    date_raw,
                    current_value_numeric,
                    compare_value_numeric,
                    calculation_method
                FROM company_metric_derived_v1
                WHERE value_numeric IS NULL
                ORDER BY
                    COALESCE(date_raw, '') DESC,
                    COALESCE(fiscal_year, 0) DESC,
                    COALESCE(fiscal_quarter, 0) DESC,
                    anchor_integrated_observation_id DESC
                LIMIT 20
                """
            )
        ).mappings().all()

    print("Company derived metric inspection")
    print(f"Database: {DEFAULT_SQLITE_DB_PATH}")
    print()
    print("=== Total row count ===")
    print(total_rows)

    _print_rows(
        "=== Metric row counts ===",
        metric_counts,
        lambda row: f"{row['standard_metric_name']}: {row['row_count']}",
    )
    _print_rows(
        "=== Period distribution ===",
        period_distribution,
        lambda row: f"{row['period_type']}: {row['row_count']}",
    )
    _print_rows(
        "=== Sample company derived rows ===",
        sample_rows,
        lambda row: (
            f"{row['company_name'] or row['company_key']} | {row['standard_metric_name']} | "
            f"{row['period_type']} fy={row['fiscal_year']} fq={row['fiscal_quarter']} "
            f"date={row['date_raw']} | value={row['value_numeric']} | "
            f"current={row['current_value_numeric']} compare={row['compare_value_numeric']} | "
            f"method={row['calculation_method']}"
        ),
    )
    _print_rows(
        "=== Null handling sample ===",
        null_sample,
        lambda row: (
            f"{row['company_name'] or row['company_key']} | {row['standard_metric_name']} | "
            f"{row['period_type']} fy={row['fiscal_year']} fq={row['fiscal_quarter']} "
            f"date={row['date_raw']} | current={row['current_value_numeric']} "
            f"compare={row['compare_value_numeric']} | method={row['calculation_method']}"
        ),
    )


if __name__ == "__main__":
    main()
