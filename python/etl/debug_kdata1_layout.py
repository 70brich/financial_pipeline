from __future__ import annotations

from pathlib import Path

import xlrd

from python.etl.inventory_sources import INPUT_DIR


CELL_TYPE_NAMES = {
    xlrd.XL_CELL_EMPTY: "empty",
    xlrd.XL_CELL_TEXT: "text",
    xlrd.XL_CELL_NUMBER: "number",
    xlrd.XL_CELL_DATE: "date",
    xlrd.XL_CELL_BOOLEAN: "boolean",
    xlrd.XL_CELL_ERROR: "error",
    xlrd.XL_CELL_BLANK: "blank",
}


def format_cell(book: xlrd.book.Book, sheet: xlrd.sheet.Sheet, row_index: int, col_index: int) -> str:
    cell = sheet.cell(row_index, col_index)
    cell_type = CELL_TYPE_NAMES.get(cell.ctype, f"type_{cell.ctype}")
    value = cell.value

    if cell.ctype == xlrd.XL_CELL_DATE:
        try:
            value = xlrd.xldate_as_datetime(cell.value, book.datemode).strftime("%Y/%m/%d")
        except Exception:
            value = cell.value

    return f"c{col_index + 1}={value!r}({cell_type})"


def main() -> None:
    candidates = sorted((INPUT_DIR / "KDATA1").glob("*.xls")) + sorted((INPUT_DIR / "KDATA1").glob("*.xlsx")) + sorted((INPUT_DIR / "KDATA1").glob("*.xlsm"))
    if not candidates:
        raise FileNotFoundError("No KDATA1 workbook found under data/input/KDATA1")

    file_path = candidates[0]
    workbook = xlrd.open_workbook(file_path.as_posix())
    sheet = workbook.sheet_by_index(0)

    print(f"FILE={file_path}")
    print(f"SHEET={sheet.name}")

    for row_index in range(min(15, sheet.nrows)):
        rendered = [
            format_cell(workbook, sheet, row_index, col_index)
            for col_index in range(min(12, sheet.ncols))
        ]
        print(f"row={row_index + 1}: " + " | ".join(rendered))


if __name__ == "__main__":
    main()
