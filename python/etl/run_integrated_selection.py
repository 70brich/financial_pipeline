from __future__ import annotations

from python.etl.build_integrated_observation import rebuild_integrated_observation
from python.etl.db_runtime import create_sqlite_engine, ensure_runtime_schema


def main() -> None:
    engine = create_sqlite_engine()
    ensure_runtime_schema(engine)
    integrated_rows = rebuild_integrated_observation(engine)
    print(f"Integrated selection complete. integrated_observation_rows={integrated_rows}")


if __name__ == "__main__":
    main()
