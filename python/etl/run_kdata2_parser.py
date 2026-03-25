from __future__ import annotations

from python.etl.db_runtime import create_sqlite_engine, ensure_runtime_schema
from python.etl.inventory_sources import scan_source_files
from python.etl.parse_kdata2 import parse_kdata2_source_files


def main() -> None:
    engine = create_sqlite_engine()
    ensure_runtime_schema(engine)
    scan_source_files(engine, trigger_mode="sqlite_inventory")
    inserted_rows = parse_kdata2_source_files(engine)
    print(f"KDATA2 parsing complete. inserted_raw_observation_rows={inserted_rows}")


if __name__ == "__main__":
    main()
