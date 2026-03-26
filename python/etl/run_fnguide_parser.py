from __future__ import annotations

import argparse
from pathlib import Path

from sqlalchemy import text

from python.etl.db_runtime import create_sqlite_engine, ensure_runtime_schema
from python.etl.parse_fnguide import (
    build_company_output_stem,
    clean_text,
    default_company_request,
    execute_fnguide_schema,
    load_fnguide_data,
    normalize_stock_code,
    persist_fnguide_data,
    resolve_company_context,
    write_db_check_report,
    write_validation_outputs,
)
from python.etl.inventory_sources import utc_now_iso


def _start_import_log(connection) -> int:
    result = connection.execute(
        text(
            """
            INSERT INTO import_log (
                source_group,
                run_started_at,
                status,
                files_scanned,
                files_loaded,
                rows_loaded,
                trigger_mode,
                created_at
            ) VALUES (
                NULL,
                :run_started_at,
                'STARTED',
                0,
                0,
                0,
                'fnguide_ingestion',
                :created_at
            )
            """
        ),
        {"run_started_at": utc_now_iso(), "created_at": utc_now_iso()},
    )
    return int(result.lastrowid)


def _finish_import_log(
    connection,
    import_log_id: int,
    status: str,
    rows_loaded: int,
    files_scanned: int,
    files_loaded: int,
    error_message: str | None = None,
) -> None:
    connection.execute(
        text(
            """
            UPDATE import_log
            SET run_finished_at = :run_finished_at,
                status = :status,
                files_scanned = :files_scanned,
                files_loaded = :files_loaded,
                rows_loaded = :rows_loaded,
                error_message = :error_message
            WHERE import_log_id = :import_log_id
            """
        ),
        {
            "run_finished_at": utc_now_iso(),
            "status": status,
            "files_scanned": files_scanned,
            "files_loaded": files_loaded,
            "rows_loaded": rows_loaded,
            "error_message": error_message,
            "import_log_id": import_log_id,
        },
    )


def _parse_company_spec(spec: str) -> tuple[str | None, str | None]:
    company_name, separator, stock_code = spec.partition(":")
    normalized_company_name = clean_text(company_name) or None
    normalized_stock_code = normalize_stock_code(stock_code) or None
    if separator and not normalized_stock_code:
        raise ValueError(f"Company spec '{spec}' must use company_name:stock_code when a colon is present.")
    if not normalized_company_name and not normalized_stock_code:
        raise ValueError("Company spec cannot be empty.")
    return normalized_company_name, normalized_stock_code


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the FnGuide ingestion flow for one or more companies.")
    parser.add_argument(
        "--company",
        action="append",
        default=[],
        help="Company name or company_name:stock_code. Repeat for a controlled batch.",
    )
    parser.add_argument(
        "--stock-code",
        action="append",
        default=[],
        help="Additional six-digit stock codes to fetch without an explicit company name.",
    )
    return parser.parse_args()


def _resolve_requested_targets(engine, args: argparse.Namespace):
    if not args.company and not args.stock_code:
        company_name, stock_code = default_company_request()
        return [resolve_company_context(engine, company_name=company_name, stock_code=stock_code)]

    requested_targets = []
    for spec in args.company:
        company_name, stock_code = _parse_company_spec(spec)
        requested_targets.append(
            resolve_company_context(
                engine,
                company_name=company_name,
                stock_code=stock_code,
            )
        )

    for stock_code in args.stock_code:
        requested_targets.append(
            resolve_company_context(
                engine,
                company_name=None,
                stock_code=normalize_stock_code(stock_code),
            )
        )

    deduped_targets = []
    seen_stock_codes: set[str] = set()
    for target in requested_targets:
        if target.stock_code in seen_stock_codes:
            continue
        deduped_targets.append(target)
        seen_stock_codes.add(target.stock_code)
    return deduped_targets


def _write_batch_summary(results: list[dict[str, object]]) -> Path | None:
    if not results:
        return None

    lines = [
        "# FnGuide batch summary",
        "",
        "| company_name | stock_code | fnguide_observation | broker_target_price | broker_report_summary | shareholder | business_summary | validation_report | db_check_report |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for result in results:
        counts = result["db_counts"]
        lines.append(
            "| {company_name} | {stock_code} | {fnguide_observation} | {broker_target_price} | "
            "{broker_report_summary} | {company_shareholder_snapshot} | {company_business_summary} | "
            "{validation_report} | {db_check_report} |".format(
                company_name=result["company_name"],
                stock_code=result["stock_code"],
                fnguide_observation=counts["fnguide_observation"],
                broker_target_price=counts["broker_target_price"],
                broker_report_summary=counts["broker_report_summary"],
                company_shareholder_snapshot=counts["company_shareholder_snapshot"],
                company_business_summary=counts["company_business_summary"],
                validation_report=result["validation_report"],
                db_check_report=result["db_check_report"],
            )
        )

    summary_path = Path(results[0]["validation_report"]).parent / "fnguide_batch_summary.md"
    summary_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return summary_path


def main() -> None:
    args = _parse_args()
    engine = create_sqlite_engine()
    ensure_runtime_schema(engine)
    execute_fnguide_schema(engine)
    targets = _resolve_requested_targets(engine, args)

    with engine.begin() as connection:
        import_log_id = _start_import_log(connection)

    try:
        results: list[dict[str, object]] = []
        total_rows_loaded = 0
        default_stock_code = default_company_request()[1]

        for target in targets:
            parsed = load_fnguide_data(engine, company_name=target.company_name, stock_code=target.stock_code)
            db_counts = persist_fnguide_data(engine, parsed)
            use_legacy_names = len(targets) == 1 and parsed["company"].stock_code == default_stock_code
            output_stem = None if use_legacy_names else build_company_output_stem(parsed["company"])
            output_paths = write_validation_outputs(parsed, db_counts, output_stem=output_stem)
            db_check_path = write_db_check_report(engine, parsed["company"], output_stem=output_stem)
            total_rows_loaded += sum(db_counts.values())
            results.append(
                {
                    "company_name": parsed["company"].company_name,
                    "stock_code": parsed["company"].stock_code,
                    "db_counts": db_counts,
                    "validation_report": output_paths["validation_report_md"],
                    "db_check_report": db_check_path,
                }
            )

        summary_path = _write_batch_summary(results)

        with engine.begin() as connection:
            _finish_import_log(
                connection,
                import_log_id,
                "SUCCESS",
                total_rows_loaded,
                files_scanned=2 * len(targets),
                files_loaded=2 * len(targets),
            )

        print("FnGuide parsing complete")
        print(f"companies_processed={len(results)}")
        if summary_path:
            print(f"batch_summary={summary_path}")
        for result in results:
            counts = result["db_counts"]
            print(f"company_name={result['company_name']}")
            print(f"stock_code={result['stock_code']}")
            print(f"fnguide_observation_rows={counts['fnguide_observation']}")
            print(f"broker_target_price_rows={counts['broker_target_price']}")
            print(f"broker_report_summary_rows={counts['broker_report_summary']}")
            print(f"company_shareholder_snapshot_rows={counts['company_shareholder_snapshot']}")
            print(f"company_business_summary_rows={counts['company_business_summary']}")
            print(f"validation_report={result['validation_report']}")
            print(f"db_check_report={result['db_check_report']}")
    except Exception as exc:
        with engine.begin() as connection:
            _finish_import_log(
                connection,
                import_log_id,
                "FAILED",
                0,
                files_scanned=2 * len(targets),
                files_loaded=0,
                error_message=str(exc),
            )
        raise


if __name__ == "__main__":
    main()
