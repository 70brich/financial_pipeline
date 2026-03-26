from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
import re

from sqlalchemy import text

from python.etl.inventory_sources import INPUT_DIR, utc_now_iso


ESTIMATE_HINT_PATTERN = re.compile(r"\(e\)|\ucd94\uc815|\uc608\uc0c1|estimate", re.IGNORECASE)
YEAR_LABEL_PATTERN = re.compile(r"^(?P<year>\d{2,4})\ub144(?:\dQ\uc5f0\ud658\uc0b0)?$")
QUARTER_LABEL_PATTERN = re.compile(r"^(?P<year>\d{2,4})\.(?P<quarter>[1-4])Q$")
SNAPSHOT_DATE_PATTERN = re.compile(r"_(?P<yyyymmdd>\d{8})_")
ANNUAL_SUMMARY_TITLE = "\uc5f0\uac04 \uc190\uc775 \uc694\uc57d"
QUARTERLY_SUMMARY_TITLE = "\ubd84\uae30 \uc190\uc775 \uc694\uc57d"
YEARLY_SECTION_TITLE = "\ud22c\uc790\uc9c0\ud45c"


@dataclass(frozen=True)
class QdataFileContext:
    source_file_id: int
    source_group: str
    relative_path: str
    file_name: str


def read_qdata_rows(file_path: Path) -> list[list[str]]:
    for encoding in ("utf-8-sig", "cp949", "utf-8"):
        try:
            with file_path.open("r", encoding=encoding, newline="") as handle:
                return [row for row in csv.reader(handle)]
        except UnicodeDecodeError:
            continue
    raise UnicodeDecodeError("qdata", b"", 0, 1, f"Could not decode file: {file_path}")


def is_blank_row(row: list[str]) -> bool:
    return all(not cell.strip() for cell in row)


def split_blocks(rows: list[list[str]]) -> list[tuple[int, list[list[str]]]]:
    blocks: list[tuple[int, list[list[str]]]] = []
    current_block: list[list[str]] = []
    block_start = 1

    for row_number, row in enumerate(rows, start=1):
        if is_blank_row(row):
            if current_block:
                blocks.append((block_start, current_block))
                current_block = []
            block_start = row_number + 1
            continue

        if not current_block:
            block_start = row_number
        current_block.append(row)

    if current_block:
        blocks.append((block_start, current_block))

    return blocks


def normalize_two_digit_year(year_text: str) -> int:
    year = int(year_text)
    return 2000 + year if year < 100 else year


def derive_snapshot_date_from_filename(file_name: str) -> tuple[str, int]:
    match = SNAPSHOT_DATE_PATTERN.search(file_name)
    if not match:
        raise ValueError(f"Could not derive snapshot date from QDATA file name: {file_name}")

    yyyymmdd = match.group("yyyymmdd")
    date_raw = f"{yyyymmdd[:4]}/{yyyymmdd[4:6]}/{yyyymmdd[6:8]}"
    return date_raw, int(yyyymmdd[:4])


def normalize_year_period(period_label_raw: str) -> tuple[str, int, str]:
    match = YEAR_LABEL_PATTERN.match(period_label_raw.strip())
    if not match:
        raise ValueError(f"Unsupported QDATA yearly period label: {period_label_raw}")

    fiscal_year = normalize_two_digit_year(match.group("year"))
    return f"{fiscal_year}/01/01", fiscal_year, str(fiscal_year)


def normalize_quarter_period(period_label_raw: str) -> tuple[str, int, int, str]:
    match = QUARTER_LABEL_PATTERN.match(period_label_raw.strip())
    if not match:
        raise ValueError(f"Unsupported QDATA quarterly period label: {period_label_raw}")

    fiscal_year = normalize_two_digit_year(match.group("year"))
    fiscal_quarter = int(match.group("quarter"))
    month = {1: "01", 2: "04", 3: "07", 4: "10"}[fiscal_quarter]
    date_raw = f"{fiscal_year}/{month}/01"
    period_label_std = f"{str(fiscal_year)[-2:]}.{fiscal_quarter}Q"
    return date_raw, fiscal_year, fiscal_quarter, period_label_std


def contains_estimate_hint(*values: object) -> bool:
    for value in values:
        if value is None:
            continue
        text_value = str(value).strip()
        if text_value and ESTIMATE_HINT_PATTERN.search(text_value):
            return True
    return False


def coerce_value_numeric(value: str) -> float | None:
    stripped = value.strip().replace(",", "")
    if not stripped or stripped in {"-", "N/A", "na", "NA"}:
        return None
    try:
        return float(stripped)
    except ValueError:
        return None


def company_name_from_file_name(file_name: str) -> str:
    return Path(file_name).stem.split("_")[0]


def build_record(
    context: QdataFileContext,
    source_row_number: int,
    sector_name: str,
    raw_metric_name: str,
    value_text: str,
    date_raw: str,
    fiscal_year: int | None,
    fiscal_quarter: int | None,
    period_type: str,
    period_label_raw: str,
    period_label_std: str,
    is_estimate: int,
) -> dict:
    return {
        "source_file_id": context.source_file_id,
        "source_group": context.source_group,
        "sheet_name": "csv",
        "source_row_number": source_row_number,
        "sector_name": sector_name,
        "raw_company_name": company_name_from_file_name(context.file_name),
        "raw_stock_code": None,
        "normalized_stock_code": None,
        "company_id": None,
        "raw_metric_name": raw_metric_name,
        "standard_metric_name": None,
        "value_text": value_text,
        "value_numeric": coerce_value_numeric(value_text),
        "value_unit": None,
        "value_nature": None,
        "is_estimate": is_estimate,
        "date_raw": date_raw,
        "raw_period_label": period_label_raw,
        "period_label_raw": period_label_raw,
        "period_type": period_type,
        "fiscal_year": fiscal_year,
        "fiscal_quarter": fiscal_quarter,
        "normalized_quarter_label": period_label_std if period_type == "QUARTER" else None,
        "period_label_std": period_label_std,
        "ingested_at": utc_now_iso(),
    }


def parse_overview_block(
    block_start_row: int,
    block: list[list[str]],
    context: QdataFileContext,
) -> list[dict]:
    snapshot_date_raw, snapshot_year = derive_snapshot_date_from_filename(context.file_name)
    records: list[dict] = []

    for pair_index in range(0, len(block) - 1, 2):
        header_row = block[pair_index]
        value_row = block[pair_index + 1]
        source_row_number = block_start_row + pair_index + 1

        for column_index in range(1, min(len(header_row), len(value_row))):
            raw_metric_name = header_row[column_index].strip()
            value_text = value_row[column_index].strip()
            if not raw_metric_name or not value_text:
                continue
            if re.fullmatch(r"[-+]?\d+(\.\d+)?", raw_metric_name):
                continue

            records.append(
                build_record(
                    context=context,
                    source_row_number=source_row_number,
                    sector_name="overview",
                    raw_metric_name=raw_metric_name,
                    value_text=value_text,
                    date_raw=snapshot_date_raw,
                    fiscal_year=snapshot_year,
                    fiscal_quarter=None,
                    period_type="SNAPSHOT",
                    period_label_raw=snapshot_date_raw,
                    period_label_std=snapshot_date_raw,
                    is_estimate=1 if contains_estimate_hint(raw_metric_name, value_text) else 0,
                )
            )

    return records


def extract_yearly_and_quarterly_columns(header_row: list[str]) -> tuple[list[tuple[int, str]], list[tuple[int, str]]]:
    yearly_columns: list[tuple[int, str]] = []
    quarterly_columns: list[tuple[int, str]] = []

    for column_index, cell in enumerate(header_row):
        label = cell.strip()
        if not label:
            continue
        if YEAR_LABEL_PATTERN.match(label):
            yearly_columns.append((column_index, label))
        elif QUARTER_LABEL_PATTERN.match(label):
            quarterly_columns.append((column_index, label))

    return yearly_columns, quarterly_columns


def parse_mixed_summary_block(
    block_start_row: int,
    block: list[list[str]],
    context: QdataFileContext,
) -> list[dict]:
    header_row = block[0]
    yearly_columns, quarterly_columns = extract_yearly_and_quarterly_columns(header_row)
    yearly_metric_column = (min(index for index, _ in yearly_columns) - 1) if yearly_columns else 1
    quarterly_metric_column = (min(index for index, _ in quarterly_columns) - 1) if quarterly_columns else None
    records: list[dict] = []

    for data_offset, row in enumerate(block[1:], start=1):
        source_row_number = block_start_row + data_offset
        yearly_metric = row[yearly_metric_column].strip() if len(row) > yearly_metric_column else ""
        quarterly_metric = (
            row[quarterly_metric_column].strip()
            if quarterly_metric_column is not None and len(row) > quarterly_metric_column
            else ""
        )

        if yearly_metric and not yearly_metric.startswith("*"):
            for column_index, period_label_raw in yearly_columns:
                if column_index >= len(row):
                    continue
                value_text = row[column_index].strip()
                if not value_text:
                    continue
                date_raw, fiscal_year, period_label_std = normalize_year_period(period_label_raw)
                records.append(
                    build_record(
                        context=context,
                        source_row_number=source_row_number,
                        sector_name="yearly",
                        raw_metric_name=yearly_metric,
                        value_text=value_text,
                        date_raw=date_raw,
                        fiscal_year=fiscal_year,
                        fiscal_quarter=None,
                        period_type="YEAR",
                        period_label_raw=period_label_raw,
                        period_label_std=period_label_std,
                        is_estimate=1 if contains_estimate_hint(yearly_metric, period_label_raw, value_text) else 0,
                    )
                )

        if quarterly_metric and not quarterly_metric.startswith("*"):
            for column_index, period_label_raw in quarterly_columns:
                if column_index >= len(row):
                    continue
                value_text = row[column_index].strip()
                if not value_text:
                    continue
                date_raw, fiscal_year, fiscal_quarter, period_label_std = normalize_quarter_period(period_label_raw)
                records.append(
                    build_record(
                        context=context,
                        source_row_number=source_row_number,
                        sector_name="quarterly",
                        raw_metric_name=quarterly_metric,
                        value_text=value_text,
                        date_raw=date_raw,
                        fiscal_year=fiscal_year,
                        fiscal_quarter=fiscal_quarter,
                        period_type="QUARTER",
                        period_label_raw=period_label_raw,
                        period_label_std=period_label_std,
                        is_estimate=1 if contains_estimate_hint(quarterly_metric, period_label_raw, value_text) else 0,
                    )
                )

    return records


def parse_yearly_block(
    block_start_row: int,
    block: list[list[str]],
    context: QdataFileContext,
) -> list[dict]:
    header_row = block[0]
    yearly_columns, _ = extract_yearly_and_quarterly_columns(header_row)
    metric_column = (min(index for index, _ in yearly_columns) - 1) if yearly_columns else 1
    records: list[dict] = []

    for data_offset, row in enumerate(block[1:], start=1):
        source_row_number = block_start_row + data_offset
        raw_metric_name = row[metric_column].strip() if len(row) > metric_column else ""
        if not raw_metric_name or raw_metric_name.startswith("*"):
            continue

        for column_index, period_label_raw in yearly_columns:
            if column_index >= len(row):
                continue
            value_text = row[column_index].strip()
            if not value_text:
                continue
            date_raw, fiscal_year, period_label_std = normalize_year_period(period_label_raw)
            records.append(
                build_record(
                    context=context,
                    source_row_number=source_row_number,
                    sector_name="yearly",
                    raw_metric_name=raw_metric_name,
                    value_text=value_text,
                    date_raw=date_raw,
                    fiscal_year=fiscal_year,
                    fiscal_quarter=None,
                    period_type="YEAR",
                    period_label_raw=period_label_raw,
                    period_label_std=period_label_std,
                    is_estimate=1 if contains_estimate_hint(raw_metric_name, period_label_raw, value_text) else 0,
                )
            )

    return records


def parse_qdata_rows(rows: list[list[str]], context: QdataFileContext) -> list[dict]:
    blocks = split_blocks(rows)
    records: list[dict] = []

    for block_start_row, block in blocks:
        block_text = " | ".join(cell.strip() for row in block[:2] for cell in row if cell.strip())
        if ANNUAL_SUMMARY_TITLE in block_text and QUARTERLY_SUMMARY_TITLE in block_text:
            records.extend(parse_mixed_summary_block(block_start_row, block, context))
        elif YEARLY_SECTION_TITLE in block_text or any(YEAR_LABEL_PATTERN.match(cell.strip()) for cell in block[0] if cell.strip()):
            records.extend(parse_yearly_block(block_start_row, block, context))
        else:
            records.extend(parse_overview_block(block_start_row, block, context))

    return records


def fetch_qdata_source_files(engine) -> list[QdataFileContext]:
    with engine.begin() as connection:
        rows = connection.execute(
            text(
                """
                SELECT source_file_id, source_group, relative_path, file_name
                FROM source_file
                WHERE source_group = 'QDATA'
                ORDER BY source_file_id
                """
            )
        ).fetchall()

    return [
        QdataFileContext(
            source_file_id=int(row.source_file_id),
            source_group=str(row.source_group),
            relative_path=str(row.relative_path),
            file_name=str(row.file_name),
        )
        for row in rows
    ]


def clear_qdata_downstream_rows(connection, source_file_id: int) -> None:
    params = {"source_file_id": source_file_id}
    selected_raw_subquery = """
        SELECT raw_observation_id
        FROM raw_observation
        WHERE source_file_id = :source_file_id
          AND source_group = 'QDATA'
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


def replace_qdata_raw_observations(connection, source_file_id: int, records: list[dict]) -> None:
    clear_qdata_downstream_rows(connection, source_file_id)
    connection.execute(
        text(
            """
            DELETE FROM raw_observation
            WHERE source_file_id = :source_file_id
              AND source_group = 'QDATA'
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
                sector_name,
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
                :sector_name,
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


def parse_qdata_source_files(engine, input_dir: Path = INPUT_DIR) -> int:
    source_files = fetch_qdata_source_files(engine)
    inserted_rows = 0

    with engine.begin() as connection:
        for context in source_files:
            csv_path = input_dir / context.relative_path
            rows = read_qdata_rows(csv_path)
            records = parse_qdata_rows(rows, context)
            replace_qdata_raw_observations(
                connection,
                source_file_id=context.source_file_id,
                records=records,
            )
            inserted_rows += len(records)

            if not records:
                raise ValueError(f"No QDATA rows parsed from file: {csv_path}")

    return inserted_rows
