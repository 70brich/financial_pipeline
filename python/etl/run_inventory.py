from __future__ import annotations

from python.etl.db_runtime import DEFAULT_SQLITE_DB_PATH, create_sqlite_engine, execute_sql_script
from python.etl.inventory_sources import scan_source_files


def main() -> None:
    engine = create_sqlite_engine()
    execute_sql_script(engine)
    import_log_id = scan_source_files(engine, trigger_mode="sqlite_inventory")
    print(f"SQLite inventory complete. import_log_id={import_log_id}")
    print(f"Database path: {DEFAULT_SQLITE_DB_PATH}")


if __name__ == "__main__":
    main()
