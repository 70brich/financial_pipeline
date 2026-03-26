from __future__ import annotations

from sqlalchemy import text

from python.etl.build_integrated_observation import execute_integrated_schema
from python.etl.build_integrated_observation_enriched import rebuild_integrated_observation_enriched
from python.etl.db_runtime import create_sqlite_engine, ensure_runtime_schema


def main() -> None:
    engine = create_sqlite_engine()
    ensure_runtime_schema(engine)
    execute_integrated_schema(engine)
    enriched_rows = rebuild_integrated_observation_enriched(engine)
    with engine.begin() as connection:
        standard_metric_rows = connection.execute(
            text("SELECT COUNT(*) FROM standard_metric")
        ).scalar_one()
        metric_name_mapping_rows = connection.execute(
            text("SELECT COUNT(*) FROM metric_name_mapping WHERE is_active = 1")
        ).scalar_one()

    print(
        "Standard metric mapping complete. "
        f"integrated_observation_enriched_rows={enriched_rows} "
        f"standard_metric_rows={standard_metric_rows} "
        f"metric_name_mapping_rows={metric_name_mapping_rows}"
    )


if __name__ == "__main__":
    main()
