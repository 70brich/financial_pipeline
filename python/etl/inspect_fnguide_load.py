from __future__ import annotations

import argparse

from sqlalchemy import text

from python.etl.db_runtime import DEFAULT_SQLITE_DB_PATH, create_sqlite_engine, ensure_runtime_schema
from python.etl.parse_fnguide import (
    execute_fnguide_schema,
    requested_company_or_default,
    resolve_company_context,
)


def _safe_text(value) -> str:
    return str(value).replace("\xa0", " ")


def _print_section(title: str, rows, formatter) -> None:
    print()
    print(title)
    if not rows:
        print("No rows found.")
        return
    for row in rows:
        print(_safe_text(formatter(row)))


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Inspect the persisted FnGuide sidecar tables for one company.")
    parser.add_argument("--company-name", help="Company name to resolve through the company table.")
    parser.add_argument("--stock-code", help="Six-digit stock code to inspect directly.")
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    engine = create_sqlite_engine()
    ensure_runtime_schema(engine)
    execute_fnguide_schema(engine)
    requested_company_name, requested_stock_code = requested_company_or_default(args.company_name, args.stock_code)
    company = resolve_company_context(
        engine,
        company_name=requested_company_name,
        stock_code=requested_stock_code,
    )

    with engine.begin() as connection:
        fetch_logs = connection.execute(
            text(
                """
                SELECT page_type, ifrs_scope, period_scope, consensus_year_label, source_url
                FROM fnguide_fetch_log
                WHERE stock_code = :stock_code
                ORDER BY fetch_log_id
                """
            ),
            {"stock_code": company.stock_code},
        ).mappings().all()

        block_counts = connection.execute(
            text(
                """
                SELECT block_type, COUNT(*) AS row_count
                FROM fnguide_observation
                WHERE stock_code = :stock_code
                GROUP BY block_type
                ORDER BY row_count DESC, block_type
                """
            ),
            {"stock_code": company.stock_code},
        ).mappings().all()

        table_counts = connection.execute(
            text(
                """
                SELECT 'fnguide_observation' AS table_name, COUNT(*) AS row_count
                FROM fnguide_observation WHERE stock_code = :stock_code
                UNION ALL
                SELECT 'broker_target_price', COUNT(*) FROM broker_target_price WHERE stock_code = :stock_code
                UNION ALL
                SELECT 'broker_report_summary', COUNT(*) FROM broker_report_summary WHERE stock_code = :stock_code
                UNION ALL
                SELECT 'company_shareholder_snapshot', COUNT(*) FROM company_shareholder_snapshot WHERE stock_code = :stock_code
                UNION ALL
                SELECT 'company_business_summary', COUNT(*) FROM company_business_summary WHERE stock_code = :stock_code
                """
            ),
            {"stock_code": company.stock_code},
        ).mappings().all()

        raw_sample = connection.execute(
            text(
                """
                SELECT raw_metric_name, period_label_raw, value_text, block_type, ifrs_scope, period_scope
                FROM fnguide_observation
                WHERE stock_code = :stock_code
                ORDER BY fnguide_observation_id DESC
                LIMIT 20
                """
            ),
            {"stock_code": company.stock_code},
        ).mappings().all()

        broker_sample = connection.execute(
            text(
                """
                SELECT broker_name, estimate_date, target_price, previous_target_price, rating, is_consensus_aggregate
                FROM broker_target_price
                WHERE stock_code = :stock_code
                ORDER BY broker_target_price_id
                LIMIT 10
                """
            ),
            {"stock_code": company.stock_code},
        ).mappings().all()

        report_sample = connection.execute(
            text(
                """
                SELECT report_date, report_title, provider_name, analyst_name
                FROM broker_report_summary
                WHERE stock_code = :stock_code
                ORDER BY broker_report_summary_id
                LIMIT 10
                """
            ),
            {"stock_code": company.stock_code},
        ).mappings().all()

        shareholder_sample = connection.execute(
            text(
                """
                SELECT holder_name, holder_type, shares, ownership_pct, as_of_date
                FROM company_shareholder_snapshot
                WHERE stock_code = :stock_code
                ORDER BY shareholder_snapshot_id
                LIMIT 10
                """
            ),
            {"stock_code": company.stock_code},
        ).mappings().all()

        business_summary = connection.execute(
            text(
                """
                SELECT summary_title, as_of_date, summary_text
                FROM company_business_summary
                WHERE stock_code = :stock_code
                ORDER BY business_summary_id DESC
                LIMIT 1
                """
            ),
            {"stock_code": company.stock_code},
        ).mappings().first()

    print("FnGuide load inspection")
    print(f"Database: {DEFAULT_SQLITE_DB_PATH}")
    print(f"company_name: {company.company_name}")
    print(f"stock_code: {company.stock_code}")

    _print_section(
        "=== URL / mode combinations ===",
        fetch_logs,
        lambda row: (
            f"{row['page_type']} | ifrs={row['ifrs_scope']} | period={row['period_scope']} | "
            f"label={row['consensus_year_label']} | {row['source_url']}"
        ),
    )
    _print_section(
        "=== Extracted block row counts ===",
        block_counts,
        lambda row: f"{row['block_type']}: {row['row_count']}",
    )
    _print_section(
        "=== DB table row counts ===",
        table_counts,
        lambda row: f"{row['table_name']}: {row['row_count']}",
    )
    _print_section(
        "=== raw-like FnGuide observation sample ===",
        raw_sample,
        lambda row: (
            f"{row['block_type']} | {row['raw_metric_name']} | {row['period_label_raw']} | "
            f"value={row['value_text']} | ifrs={row['ifrs_scope']} | period={row['period_scope']}"
        ),
    )
    _print_section(
        "=== broker target sample ===",
        broker_sample,
        lambda row: (
            f"{row['broker_name']} | {row['estimate_date']} | target={row['target_price']} | "
            f"prev={row['previous_target_price']} | rating={row['rating']} | "
            f"aggregate={row['is_consensus_aggregate']}"
        ),
    )
    _print_section(
        "=== report summary sample ===",
        report_sample,
        lambda row: f"{row['report_date']} | {row['report_title']} | {row['provider_name']} | {row['analyst_name']}",
    )
    _print_section(
        "=== shareholder snapshot sample ===",
        shareholder_sample,
        lambda row: (
            f"{row['holder_name']} | {row['holder_type']} | shares={row['shares']} | "
            f"pct={row['ownership_pct']} | as_of={row['as_of_date']}"
        ),
    )

    print()
    print("=== business summary ===")
    if not business_summary:
        print("No business summary found.")
    else:
        summary_text = _safe_text((business_summary["summary_text"] or "")[:500])
        print(_safe_text(f"title={business_summary['summary_title']} | as_of={business_summary['as_of_date']}"))
        print(summary_text)

    print()
    print("=== deferred / missing blocks ===")
    print("- No Selenium-only blocks are loaded in v1.")
    print("- Consensus rendering charts are not persisted as image outputs in v1.")
    print("- FNGUIDE source is stored in dedicated tables, not in raw_observation, to preserve current source-group constraints.")
    print("- Next extension point: multi-company expansion or DART cross-checking.")


if __name__ == "__main__":
    main()
