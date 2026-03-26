from __future__ import annotations

from sqlalchemy import text

from python.etl.build_integrated_observation_enriched import execute_metric_mapping_schema
from python.etl.db_runtime import create_sqlite_engine, ensure_runtime_schema
from python.etl.standard_metric_master import (
    reseed_metric_name_mapping,
    sync_metric_alias_map,
    upsert_standard_metric_seed_rows,
)


def main() -> None:
    engine = create_sqlite_engine()
    ensure_runtime_schema(engine)
    execute_metric_mapping_schema(engine)

    with engine.begin() as connection:
        standard_metric_lookup = upsert_standard_metric_seed_rows(connection)
        mapping_rows = reseed_metric_name_mapping(connection, standard_metric_lookup)
        alias_rows = sync_metric_alias_map(connection)
        standard_metric_count = connection.execute(
            text("SELECT COUNT(*) FROM standard_metric")
        ).scalar_one()

    print(
        "Standard metric master seed complete. "
        f"standard_metric_rows={standard_metric_count} "
        f"metric_name_mapping_rows={len(mapping_rows)} "
        f"metric_alias_map_rows={alias_rows}"
    )


if __name__ == "__main__":
    main()
