from __future__ import annotations

from pathlib import Path

from python.etl.build_integrated_observation import execute_integrated_schema
from python.etl.build_integrated_observation_enriched import execute_metric_mapping_schema
from python.etl.db_runtime import BASE_DIR, ensure_runtime_schema, execute_sql_script


ANALYSIS_VIEW_SQL_PATH = BASE_DIR / "sql" / "007_create_analysis_views.sql"


def execute_analysis_views(engine) -> None:
    execute_sql_script(engine, ANALYSIS_VIEW_SQL_PATH)


def ensure_analysis_layer(engine) -> None:
    ensure_runtime_schema(engine)
    execute_integrated_schema(engine)
    execute_metric_mapping_schema(engine)
    execute_analysis_views(engine)
