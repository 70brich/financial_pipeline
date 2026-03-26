from __future__ import annotations

from pathlib import Path

from python.etl.parse_fnguide import (
    DEFAULT_STOCK_CODE,
    ensure_fnguide_output_dir,
    fetch_consensus_page,
    fetch_main_page,
    detect_consensus_modes,
)


def _escape(text: str) -> str:
    return text.replace("|", "\\|").replace("\n", " ").strip()


def _table_summary_lines(page_name: str, tables) -> list[str]:
    lines = [f"## {page_name} pandas.read_html tables", ""]
    if not tables:
        return lines + ["- no tables detected", ""]

    for index, table in enumerate(tables):
        columns = [_escape(str(column)) for column in table.columns[:8]]
        lines.append(f"### Table {index}")
        lines.append(f"- shape: {table.shape}")
        lines.append(f"- columns: {', '.join(columns)}")
        preview = table.head(5).fillna("").astype(str).to_dict(orient="records")
        if preview:
            headers = [str(header) for header in list(preview[0].keys())[: min(6, len(preview[0]))]]
            lines.append("")
            lines.append("| " + " | ".join(headers) + " |")
            lines.append("| " + " | ".join(["---"] * len(headers)) + " |")
            for row in preview:
                lines.append("| " + " | ".join(_escape(row.get(header, "")) for header in headers) + " |")
        lines.append("")
    return lines


def main() -> None:
    consensus = fetch_consensus_page(DEFAULT_STOCK_CODE)
    main_page = fetch_main_page(DEFAULT_STOCK_CODE)
    modes = detect_consensus_modes(consensus)
    output_dir = ensure_fnguide_output_dir()
    report_path = output_dir / "fnguide_layout_debug.md"

    lines = [
        "# FnGuide layout debug",
        "",
        f"- stock_code: {DEFAULT_STOCK_CODE}",
        f"- consensus_url: {consensus.url}",
        f"- main_url: {main_page.url}",
        "",
        "## Detected consensus modes",
        f"- financial_ifrs_modes: {modes['financial_ifrs_modes']}",
        f"- financial_period_modes: {modes['financial_period_modes']}",
        f"- revision_period_options: {modes['revision_period_options']}",
        f"- detected_select_ids: {modes['detected_select_ids']}",
        "",
    ]
    lines.extend(_table_summary_lines("Consensus", consensus.tables))
    lines.extend(_table_summary_lines("Main", main_page.tables))

    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print("FnGuide layout debug complete")
    print(f"Output: {report_path}")
    print(f"Consensus tables: {len(consensus.tables)}")
    print(f"Main tables: {len(main_page.tables)}")


if __name__ == "__main__":
    main()
