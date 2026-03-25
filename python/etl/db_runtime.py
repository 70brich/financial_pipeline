from __future__ import annotations

from pathlib import Path

from sqlalchemy import create_engine, text


BASE_DIR = Path(__file__).resolve().parents[2]
DEFAULT_SQLITE_DB_PATH = BASE_DIR / "data" / "financial_pipeline.sqlite3"
BASE_SCHEMA_SQL_PATH = BASE_DIR / "sql" / "003_create_base_financial_tables.sql"


def get_sqlite_database_url(db_path: Path = DEFAULT_SQLITE_DB_PATH) -> str:
    return f"sqlite:///{db_path.as_posix()}"


def create_sqlite_engine(db_path: Path = DEFAULT_SQLITE_DB_PATH):
    db_path.parent.mkdir(parents=True, exist_ok=True)
    engine = create_engine(get_sqlite_database_url(db_path), future=True)
    with engine.begin() as connection:
        connection.execute(text("PRAGMA foreign_keys = ON"))
    return engine


def execute_sql_script(engine, sql_path: Path = BASE_SCHEMA_SQL_PATH) -> None:
    script = sql_path.read_text(encoding="utf-8")
    statements = [statement.strip() for statement in script.split(";") if statement.strip()]

    with engine.begin() as connection:
        for statement in statements:
            connection.exec_driver_sql(statement)


def ensure_raw_observation_columns(engine) -> None:
    required_columns = {
        "date_raw": "ALTER TABLE raw_observation ADD COLUMN date_raw TEXT",
        "period_label_raw": "ALTER TABLE raw_observation ADD COLUMN period_label_raw TEXT",
        "period_label_std": "ALTER TABLE raw_observation ADD COLUMN period_label_std TEXT",
    }

    with engine.begin() as connection:
        existing_columns = {
            row[1] for row in connection.exec_driver_sql("PRAGMA table_info(raw_observation)")
        }
        for column_name, ddl in required_columns.items():
            if column_name not in existing_columns:
                connection.exec_driver_sql(ddl)


def ensure_runtime_schema(engine) -> None:
    execute_sql_script(engine)
    ensure_raw_observation_columns(engine)
