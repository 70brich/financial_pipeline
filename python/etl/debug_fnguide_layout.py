from __future__ import annotations

import argparse

from python.etl.db_runtime import create_sqlite_engine, ensure_runtime_schema
from python.etl.parse_fnguide import (
    build_company_output_stem,
    execute_fnguide_schema,
    fetch_consensus_page,
    fetch_main_page,
    requested_company_or_default,
    resolve_company_context,
    validation_output_paths,
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


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Debug the HTML table layout for a FnGuide company page.")
    parser.add_argument("--company-name", help="Company name to resolve through the company table.")
    parser.add_argument("--stock-code", help="Six-digit stock code to debug directly.")
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    engine = create_sqlite_engine()
    ensure_runtime_schema(engine)
    execute_fnguide_schema(engine)
    requested_company_name, requested_stock_code = requested_company_or_default(args.company_name, args.stock_code)
    company = resolve_company_context(
        engine,
        company_name=requested_company_name,
        stock_code=requested_stock_code,
    )

    consensus = fetch_consensus_page(company.stock_code)
    main_page = fetch_main_page(company.stock_code)
    modes = detect_consensus_modes(consensus)
    use_legacy_names = company.stock_code == requested_company_or_default(None, None)[1] and not args.company_name and not args.stock_code
    output_stem = None if use_legacy_names else build_company_output_stem(company)
    report_path = validation_output_paths(company, output_stem=output_stem)["layout_debug_md"]

    lines = [
        "# FnGuide layout debug",
        "",
        f"- company_name: {company.company_name}",
        f"- stock_code: {company.stock_code}",
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
    print(f"company_name={company.company_name}")
    print(f"stock_code={company.stock_code}")
    print(f"Consensus tables: {len(consensus.tables)}")
    print(f"Main tables: {len(main_page.tables)}")


if __name__ == "__main__":
    main()
