from __future__ import annotations

from python.etl.analysis_views import ensure_analysis_layer
from python.etl.db_runtime import BASE_DIR, execute_sql_script


DERIVED_VIEW_SQL_PATH = BASE_DIR / "sql" / "008_create_derived_metric_views.sql"


def execute_derived_views(engine) -> None:
    execute_sql_script(engine, DERIVED_VIEW_SQL_PATH)


def ensure_derived_layer(engine) -> None:
    ensure_analysis_layer(engine)
    execute_derived_views(engine)
