from __future__ import annotations

import csv
from pathlib import Path

from python.etl.inventory_sources import INPUT_DIR


ANNUAL_SUMMARY_TITLE = "\uc5f0\uac04 \uc190\uc775 \uc694\uc57d"
QUARTERLY_SUMMARY_TITLE = "\ubd84\uae30 \uc190\uc775 \uc694\uc57d"
YEARLY_SECTION_TITLE = "\ud22c\uc790\uc9c0\ud45c"
OVERVIEW_TITLE = "\ud68c\uc0ac\uba85"
CODE_TITLE = "\ucf54\ub4dc\ubc88\ud638"
NOTE_TEXT = "\uc5f0\uac04\uae30\uc900=\ub2ec\ub825\uae30\uc900"


def read_qdata_rows(file_path: Path) -> list[list[str]]:
    for encoding in ("utf-8-sig", "cp949", "utf-8"):
        try:
            with file_path.open("r", encoding=encoding, newline="") as handle:
                return [row for row in csv.reader(handle)]
        except UnicodeDecodeError:
            continue
    raise UnicodeDecodeError("qdata", b"", 0, 1, f"Could not decode file: {file_path}")


def classify_row(row: list[str]) -> str:
    text = " | ".join(cell.strip() for cell in row if cell.strip())
    if not text:
        return "BLANK"
    if "* " in text or text.startswith("*") or NOTE_TEXT in text:
        return "NOTE"
    if ANNUAL_SUMMARY_TITLE in text and QUARTERLY_SUMMARY_TITLE in text:
        return "MIXED_HEADER"
    if YEARLY_SECTION_TITLE in text:
        return "YEARLY_HEADER"
    if OVERVIEW_TITLE in text or CODE_TITLE in text:
        return "OVERVIEW_HEADER"
    return "DATA"


def main() -> None:
    candidates = sorted((INPUT_DIR / "QDATA").glob("*.csv"))
    if not candidates:
        raise FileNotFoundError("No QDATA csv found under data/input/QDATA")

    file_path = candidates[0]
    rows = read_qdata_rows(file_path)
    print(f"FILE={file_path}")
    print(f"ROW_COUNT={len(rows)}")
    print()

    for row_number, row in enumerate(rows[:60], start=1):
        visible = [cell.strip() for cell in row[:20]]
        while visible and visible[-1] == "":
            visible.pop()
        print(f"{row_number:>3}: [{classify_row(row)}] {visible}")


if __name__ == "__main__":
    main()
