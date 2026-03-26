from __future__ import annotations

from sqlalchemy import text

from python.etl.analysis_views import ensure_analysis_layer
from python.etl.db_runtime import create_sqlite_engine


def main() -> None:
    engine = create_sqlite_engine()
    ensure_analysis_layer(engine)

    with engine.begin() as connection:
        row_count = connection.execute(
            text("SELECT COUNT(*) FROM company_metric_timeseries")
        ).scalar_one()

    print(f"Analysis views complete. company_metric_timeseries_rows={row_count}")


if __name__ == "__main__":
    main()
