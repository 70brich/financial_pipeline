from __future__ import annotations

from sqlalchemy import text

from python.etl.analysis_views import ensure_analysis_layer
from python.etl.db_runtime import DEFAULT_SQLITE_DB_PATH, create_sqlite_engine


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
    ensure_analysis_layer(engine)

    with engine.begin() as connection:
        total_rows = connection.execute(
            text("SELECT COUNT(*) FROM company_metric_timeseries")
        ).scalar_one()

        period_distribution = connection.execute(
            text(
                """
                SELECT period_type, COUNT(*) AS row_count
                FROM company_metric_timeseries
                GROUP BY period_type
                ORDER BY row_count DESC, period_type
                """
            )
        ).mappings().all()

        company_counts = connection.execute(
            text(
                """
                SELECT
                    COALESCE(company_name, company_key, 'UNKNOWN') AS company_label,
                    COUNT(*) AS row_count
                FROM company_metric_timeseries
                GROUP BY company_label
                ORDER BY row_count DESC, company_label
                LIMIT 10
                """
            )
        ).mappings().all()

        standard_metric_counts = connection.execute(
            text(
                """
                SELECT
                    COALESCE(standard_metric_name, 'UNMAPPED') AS metric_label,
                    COUNT(*) AS row_count
                FROM company_metric_timeseries
                GROUP BY metric_label
                ORDER BY row_count DESC, metric_label
                LIMIT 20
                """
            )
        ).mappings().all()

        top_company_row = connection.execute(
            text(
                """
                SELECT COALESCE(company_name, company_key, 'UNKNOWN') AS company_label
                FROM company_metric_timeseries
                GROUP BY company_label
                ORDER BY COUNT(*) DESC, company_label
                LIMIT 1
                """
            )
        ).mappings().first()

        recent_timeseries = []
        if top_company_row:
            recent_timeseries = connection.execute(
                text(
                    """
                    SELECT
                        company_name,
                        company_key,
                        standard_metric_name,
                        raw_metric_name,
                        period_type,
                        fiscal_year,
                        fiscal_quarter,
                        date_raw,
                        value_numeric,
                        value_text,
                        is_estimate,
                        selected_source_group
                    FROM company_metric_timeseries
                    WHERE COALESCE(company_name, company_key, 'UNKNOWN') = :company_label
                    ORDER BY
                        COALESCE(date_raw, '') DESC,
                        COALESCE(fiscal_year, 0) DESC,
                        COALESCE(fiscal_quarter, 0) DESC,
                        integrated_observation_id DESC
                    LIMIT 20
                    """
                ),
                {"company_label": top_company_row["company_label"]},
            ).mappings().all()

    print("Company metric timeseries inspection")
    print(f"Database: {DEFAULT_SQLITE_DB_PATH}")
    print()
    print("=== Total row count ===")
    print(total_rows)

    _print_rows(
        "=== Period distribution ===",
        period_distribution,
        lambda row: f"{row['period_type']}: {row['row_count']}",
    )
    _print_rows(
        "=== Company row count sample ===",
        company_counts,
        lambda row: f"{row['company_label']}: {row['row_count']}",
    )
    _print_rows(
        "=== Standard metric row count sample ===",
        standard_metric_counts,
        lambda row: f"{row['metric_label']}: {row['row_count']}",
    )
    _print_rows(
        "=== Recent timeseries sample for top company ===",
        recent_timeseries,
        lambda row: (
            f"{row['company_name'] or row['company_key']} | "
            f"{row['standard_metric_name'] or 'UNMAPPED'} | "
            f"raw={row['raw_metric_name']} | "
            f"{row['period_type']} fy={row['fiscal_year']} fq={row['fiscal_quarter']} "
            f"date={row['date_raw']} | "
            f"value_numeric={row['value_numeric']} value_text={row['value_text']} | "
            f"estimate={row['is_estimate']} source={row['selected_source_group']}"
        ),
    )


if __name__ == "__main__":
    main()
