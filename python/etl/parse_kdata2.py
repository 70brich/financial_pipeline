from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re

import pandas as pd
from sqlalchemy import text

from python.etl.inventory_sources import INPUT_DIR, utc_now_iso


KDATA2_INPUT_DIR = INPUT_DIR / "KDATA2"
ESTIMATE_HINT_PATTERN = re.compile(r"\(e\)|추정|예상|estimate", re.IGNORECASE)


@dataclass(frozen=True)
class Kdata2FileContext:
    source_file_id: int
    source_group: str
    relative_path: str
    file_name: str


def choose_excel_engine(file_path: Path) -> str:
    suffix = Path(file_path).suffix.lower()
    if suffix == ".xls":
        return "xlrd"
    if suffix in {".xlsx", ".xlsm"}:
        return "openpyxl"
    raise ValueError(f"Unsupported KDATA2 workbook extension: {suffix}")


def load_xls_workbook_with_xlrd(file_path: Path) -> dict[str, pd.DataFrame]:
    try:
        import xlrd
    except ImportError as exc:
        raise ImportError("For .xls files, install xlrd.") from exc

    workbook = xlrd.open_workbook(file_path.as_posix(), encoding_override="cp949")
    sheets: dict[str, pd.DataFrame] = {}

    for sheet in workbook.sheets():
        rows: list[list[object]] = []
        for row_index in range(sheet.nrows):
            row_values: list[object] = []
            for col_index in range(sheet.ncols):
                cell = sheet.cell(row_index, col_index)
                value: object = cell.value

                if cell.ctype == xlrd.XL_CELL_DATE:
                    value = xlrd.xldate_as_datetime(cell.value, workbook.datemode).strftime(
                        "%Y/%m/%d"
                    )
                elif cell.ctype in {xlrd.XL_CELL_EMPTY, xlrd.XL_CELL_BLANK}:
                    value = ""

                row_values.append(value)
            rows.append(row_values)

        sheets[str(sheet.name)] = pd.DataFrame(rows).fillna("")

    return sheets


def load_kdata2_workbook(file_path: Path) -> dict[str, pd.DataFrame]:
    engine = choose_excel_engine(file_path)
    if engine == "xlrd":
        return load_xls_workbook_with_xlrd(file_path)

    sheets = pd.read_excel(
        file_path,
        sheet_name=None,
        header=None,
        dtype=object,
        engine=engine,
    )
    return {
        str(sheet_name): dataframe.fillna("")
        for sheet_name, dataframe in sheets.items()
    }


def derive_year_fields(date_value: object) -> tuple[str, int, str]:
    if isinstance(date_value, (int, float)):
        raise ValueError(f"Numeric values are not accepted as KDATA2 date headers: {date_value}")

    parsed = pd.to_datetime(date_value)
    if pd.isna(parsed):
        raise ValueError(f"Could not parse KDATA2 date value: {date_value}")

    fiscal_year = int(parsed.year)
    date_raw = parsed.strftime("%Y/%m/%d")
    period_label_std = str(fiscal_year)
    return date_raw, fiscal_year, period_label_std


def is_date_like(value: object) -> bool:
    if value is None:
        return False
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            return False
        if not re.fullmatch(r"\d{4}[-/]\d{1,2}[-/]\d{1,2}", stripped):
            return False
        try:
            pd.to_datetime(stripped)
        except (TypeError, ValueError):
            return False
        return True
    if isinstance(value, (int, float)):
        return False
    return isinstance(value, pd.Timestamp)


def is_empty_cell(value: object) -> bool:
    if value is None:
        return True
    if isinstance(value, str):
        return value.strip() == ""
    return pd.isna(value)


def get_metric_columns(header_row: list[object]) -> list[tuple[int, str]]:
    metric_columns: list[tuple[int, str]] = []
    for column_index, header_value in enumerate(header_row[1:], start=1):
        metric_name = "" if header_value is None else str(header_value).strip()
        if not metric_name:
            continue
        if is_date_like(metric_name):
            continue
        metric_columns.append((column_index, metric_name))
    return metric_columns


def coerce_value_numeric(value: object) -> float | None:
    if value is None:
        return None
    if isinstance(value, str):
        stripped = value.strip().replace(",", "")
        if not stripped or stripped in {"-", "N/A", "na", "NA"}:
            return None
        try:
            return float(stripped)
        except ValueError:
            return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def company_name_from_file_name(file_name: str) -> str:
    return Path(file_name).stem


def contains_estimate_hint(*values: object) -> bool:
    for value in values:
        if value is None:
            continue
        text_value = str(value).strip()
        if text_value and ESTIMATE_HINT_PATTERN.search(text_value):
            return True
    return False


def melt_kdata2_sheet(
    dataframe: pd.DataFrame,
    context: Kdata2FileContext,
    sheet_name: str,
) -> list[dict]:
    if dataframe.empty or dataframe.shape[1] < 2:
        return []

    header_row = dataframe.iloc[0].tolist()
    metric_columns = get_metric_columns(header_row)
    if not metric_columns:
        return []

    records: list[dict] = []

    for row_index in range(1, len(dataframe)):
        date_value = dataframe.iat[row_index, 0]
        if is_empty_cell(date_value) or not is_date_like(date_value):
            continue

        try:
            date_raw, fiscal_year, period_label_std = derive_year_fields(date_value)
        except ValueError:
            continue

        for column_index, metric_name in metric_columns:
            cell_value = dataframe.iat[row_index, column_index]
            if is_empty_cell(cell_value):
                continue

            value_text = str(cell_value).strip()
            value_numeric = coerce_value_numeric(cell_value)
            is_estimate = 1 if contains_estimate_hint(sheet_name, metric_name, date_raw, value_text) else 0

            records.append(
                {
                    "source_file_id": context.source_file_id,
                    "source_group": context.source_group,
                    "sheet_name": sheet_name,
                    "source_row_number": row_index + 1,
                    "raw_company_name": company_name_from_file_name(context.file_name),
                    "raw_stock_code": None,
                    "normalized_stock_code": None,
                    "company_id": None,
                    "raw_metric_name": metric_name,
                    "standard_metric_name": None,
                    "value_text": value_text,
                    "value_numeric": value_numeric,
                    "value_unit": None,
                    "value_nature": None,
                    "is_estimate": is_estimate,
                    "date_raw": date_raw,
                    "raw_period_label": date_raw,
                    "period_label_raw": date_raw,
                    "period_type": "YEAR",
                    "fiscal_year": fiscal_year,
                    "fiscal_quarter": None,
                    "normalized_quarter_label": None,
                    "period_label_std": period_label_std,
                    "ingested_at": utc_now_iso(),
                }
            )

    return records


def fetch_kdata2_source_files(engine) -> list[Kdata2FileContext]:
    with engine.begin() as connection:
        rows = connection.execute(
            text(
                """
                SELECT source_file_id, source_group, relative_path, file_name
                FROM source_file
                WHERE source_group = 'KDATA2'
                ORDER BY source_file_id
                """
            )
        ).fetchall()

    return [
        Kdata2FileContext(
            source_file_id=int(row.source_file_id),
            source_group=str(row.source_group),
            relative_path=str(row.relative_path),
            file_name=str(row.file_name),
        )
        for row in rows
    ]


def clear_kdata2_downstream_rows(connection, source_file_id: int) -> None:
    params = {"source_file_id": source_file_id}
    selected_raw_subquery = """
        SELECT raw_observation_id
        FROM raw_observation
        WHERE source_file_id = :source_file_id
          AND source_group = 'KDATA2'
    """

    connection.execute(
        text(
            f"""
            DELETE FROM integrated_observation_enriched
            WHERE integrated_observation_id IN (
                SELECT integrated_observation_id
                FROM integrated_observation
                WHERE selected_raw_observation_id IN ({selected_raw_subquery})
            )
            """
        ),
        params,
    )
    connection.execute(
        text(
            f"""
            DELETE FROM integrated_observation
            WHERE selected_raw_observation_id IN ({selected_raw_subquery})
            """
        ),
        params,
    )


def replace_kdata2_raw_observations(connection, source_file_id: int, records: list[dict]) -> None:
    clear_kdata2_downstream_rows(connection, source_file_id)
    connection.execute(
        text(
            """
            DELETE FROM raw_observation
            WHERE source_file_id = :source_file_id
              AND source_group = 'KDATA2'
            """
        ),
        {"source_file_id": source_file_id},
    )

    if not records:
        return

    connection.execute(
        text(
            """
            INSERT INTO raw_observation (
                source_file_id,
                source_group,
                sheet_name,
                source_row_number,
                raw_company_name,
                raw_stock_code,
                normalized_stock_code,
                company_id,
                raw_metric_name,
                standard_metric_name,
                value_text,
                value_numeric,
                value_unit,
                value_nature,
                is_estimate,
                date_raw,
                raw_period_label,
                period_label_raw,
                period_type,
                fiscal_year,
                fiscal_quarter,
                normalized_quarter_label,
                period_label_std,
                ingested_at
            ) VALUES (
                :source_file_id,
                :source_group,
                :sheet_name,
                :source_row_number,
                :raw_company_name,
                :raw_stock_code,
                :normalized_stock_code,
                :company_id,
                :raw_metric_name,
                :standard_metric_name,
                :value_text,
                :value_numeric,
                :value_unit,
                :value_nature,
                :is_estimate,
                :date_raw,
                :raw_period_label,
                :period_label_raw,
                :period_type,
                :fiscal_year,
                :fiscal_quarter,
                :normalized_quarter_label,
                :period_label_std,
                :ingested_at
            )
            """
        ),
        records,
    )


def parse_kdata2_source_files(engine, input_dir: Path = INPUT_DIR) -> int:
    source_files = fetch_kdata2_source_files(engine)
    inserted_rows = 0

    with engine.begin() as connection:
        for context in source_files:
            workbook_path = input_dir / context.relative_path
            sheet_frames = load_kdata2_workbook(workbook_path)
            records: list[dict] = []
            for sheet_name, dataframe in sheet_frames.items():
                records.extend(melt_kdata2_sheet(dataframe, context=context, sheet_name=sheet_name))

            replace_kdata2_raw_observations(
                connection,
                source_file_id=context.source_file_id,
                records=records,
            )
            inserted_rows += len(records)

            if not records:
                raise ValueError(f"No KDATA2 rows parsed from workbook: {workbook_path}")

    return inserted_rows
