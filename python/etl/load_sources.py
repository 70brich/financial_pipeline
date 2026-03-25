from __future__ import annotations

import os
from pathlib import Path
from typing import Iterable

import pandas as pd
from sqlalchemy import create_engine, text


BASE_DIR = Path(__file__).resolve().parents[2]
INPUT_DIR = BASE_DIR / "data" / "input"


def get_engine():
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise RuntimeError("DATABASE_URL environment variable is not set.")
    return create_engine(database_url)


def iter_source_files() -> Iterable[Path]:
    if not INPUT_DIR.exists():
        return []
    patterns = ("*.xlsx", "*.xls", "*.csv")
    files = []
    for pattern in patterns:
        files.extend(INPUT_DIR.glob(pattern))
    return sorted(files)


def normalize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = [
        str(column).strip().lower().replace(" ", "_").replace("-", "_")
        for column in df.columns
    ]
    return df


def load_excel(file_path: Path) -> list[tuple[str, pd.DataFrame]]:
    sheets = pd.read_excel(file_path, sheet_name=None, dtype=str)
    return [
        (sheet_name, normalize_column_names(dataframe.fillna("")))
        for sheet_name, dataframe in sheets.items()
    ]


def load_csv(file_path: Path) -> list[tuple[str, pd.DataFrame]]:
    dataframe = pd.read_csv(file_path, dtype=str).fillna("")
    return [("csv", normalize_column_names(dataframe))]


def append_metadata(
    df: pd.DataFrame, file_name: str, sheet_name: str | None
) -> pd.DataFrame:
    enriched = df.copy()
    enriched.insert(0, "source_row_no", range(2, len(enriched) + 2))
    enriched.insert(0, "source_sheet_name", sheet_name or "")
    enriched.insert(0, "source_file_name", file_name)
    return enriched


def target_table_for(file_name: str) -> str:
    lowered = file_name.lower()
    if "customer" in lowered:
        return "customer_source"
    if "contract" in lowered:
        return "contract_source"
    if "sales" in lowered:
        return "sales_source"
    raise ValueError(
        f"Could not infer target raw table from file name: {file_name}. "
        "Rename the file or update target_table_for()."
    )


def record_audit(engine, file_name: str, source_type: str, target_table: str, rows: int):
    sql = text(
        """
        INSERT INTO raw.load_audit (
            source_file_name,
            source_type,
            target_table,
            loaded_rows,
            load_status
        ) VALUES (
            :source_file_name,
            :source_type,
            :target_table,
            :loaded_rows,
            'SUCCESS'
        )
        """
    )
    with engine.begin() as connection:
        connection.execute(
            sql,
            {
                "source_file_name": file_name,
                "source_type": source_type,
                "target_table": target_table,
                "loaded_rows": rows,
            },
        )


def load_file(engine, file_path: Path):
    loader = load_csv if file_path.suffix.lower() == ".csv" else load_excel
    loaded = loader(file_path)
    for sheet_name, dataframe in loaded:
        target_table = target_table_for(file_path.name)
        payload = append_metadata(dataframe, file_path.name, sheet_name)
        payload.to_sql(
            target_table,
            engine,
            schema="raw",
            if_exists="append",
            index=False,
        )
        record_audit(
            engine,
            file_name=file_path.name,
            source_type=file_path.suffix.lower().lstrip("."),
            target_table=f"raw.{target_table}",
            rows=len(payload),
        )
        print(f"Loaded {len(payload)} rows from {file_path.name} ({sheet_name})")


def main():
    source_files = list(iter_source_files())
    if not source_files:
        print(f"No source files found in {INPUT_DIR}")
        return

    engine = get_engine()
    for file_path in source_files:
        load_file(engine, file_path)


if __name__ == "__main__":
    main()
