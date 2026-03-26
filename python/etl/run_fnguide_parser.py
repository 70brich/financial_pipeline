from __future__ import annotations

from sqlalchemy import text

from python.etl.db_runtime import create_sqlite_engine, ensure_runtime_schema
from python.etl.parse_fnguide import (
    DEFAULT_COMPANY_NAME,
    DEFAULT_STOCK_CODE,
    execute_fnguide_schema,
    load_fnguide_data,
    persist_fnguide_data,
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


def _finish_import_log(connection, import_log_id: int, status: str, rows_loaded: int, error_message: str | None = None) -> None:
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
            "files_scanned": 2,
            "files_loaded": 2 if status == "SUCCESS" else 0,
            "rows_loaded": rows_loaded,
            "error_message": error_message,
            "import_log_id": import_log_id,
        },
    )


def main() -> None:
    engine = create_sqlite_engine()
    ensure_runtime_schema(engine)
    execute_fnguide_schema(engine)

    with engine.begin() as connection:
        import_log_id = _start_import_log(connection)

    try:
        parsed = load_fnguide_data(engine, company_name=DEFAULT_COMPANY_NAME, stock_code=DEFAULT_STOCK_CODE)
        db_counts = persist_fnguide_data(engine, parsed)
        output_paths = write_validation_outputs(parsed, db_counts)
        db_check_path = write_db_check_report(engine, parsed["company"])
        output_paths["db_check_md"] = db_check_path
        total_rows_loaded = sum(db_counts.values())

        with engine.begin() as connection:
            _finish_import_log(connection, import_log_id, "SUCCESS", total_rows_loaded)

        print("FnGuide parsing complete")
        print(f"company_name={parsed['company'].company_name}")
        print(f"stock_code={parsed['company'].stock_code}")
        print(f"fnguide_observation_rows={db_counts['fnguide_observation']}")
        print(f"broker_target_price_rows={db_counts['broker_target_price']}")
        print(f"broker_report_summary_rows={db_counts['broker_report_summary']}")
        print(f"company_shareholder_snapshot_rows={db_counts['company_shareholder_snapshot']}")
        print(f"company_business_summary_rows={db_counts['company_business_summary']}")
        print(f"validation_report={output_paths['validation_report_md']}")
        print(f"db_check_report={db_check_path}")
    except Exception as exc:
        with engine.begin() as connection:
            _finish_import_log(connection, import_log_id, "FAILED", 0, str(exc))
        raise


if __name__ == "__main__":
    main()
