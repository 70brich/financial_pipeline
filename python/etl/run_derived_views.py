from __future__ import annotations

from sqlalchemy import text

from python.etl.db_runtime import create_sqlite_engine
from python.etl.derived_views import ensure_derived_layer


def main() -> None:
    engine = create_sqlite_engine()
    ensure_derived_layer(engine)

    with engine.begin() as connection:
        row_count = connection.execute(
            text("SELECT COUNT(*) FROM company_metric_derived_v1")
        ).scalar_one()

    print(f"Derived views complete. company_metric_derived_v1_rows={row_count}")


if __name__ == "__main__":
    main()
