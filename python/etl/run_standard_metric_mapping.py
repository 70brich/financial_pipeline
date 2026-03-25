from __future__ import annotations

from python.etl.build_integrated_observation import execute_integrated_schema
from python.etl.build_integrated_observation_enriched import rebuild_integrated_observation_enriched
from python.etl.db_runtime import create_sqlite_engine, ensure_runtime_schema


def main() -> None:
    engine = create_sqlite_engine()
    ensure_runtime_schema(engine)
    execute_integrated_schema(engine)
    enriched_rows = rebuild_integrated_observation_enriched(engine)
    print(f"Standard metric mapping complete. integrated_observation_enriched_rows={enriched_rows}")


if __name__ == "__main__":
    main()
