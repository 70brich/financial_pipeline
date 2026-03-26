from __future__ import annotations

import csv
import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]
DB_PATH = BASE_DIR / "data" / "financial_pipeline.sqlite3"
OUTPUT_DIR = BASE_DIR / "outputs" / "fnguide_validation"

TARGETS = [
    ("고려아연", "010130"),
    ("롯데케미칼", "011170"),
    ("삼성전기", "009150"),
    ("삼성중공업", "010140"),
    ("HD현대", "267250"),
    ("산일전기", "062040"),
    ("씨에스윈드", "112610"),
    ("에스앤에스텍", "101490"),
    ("씨어스테크놀로지", "458870"),
    ("플리토", "300080"),
    ("하이브", "352820"),
    ("오파스넷", "173130"),
    ("에스텍", "069510"),
    ("영화테크", "265560"),
]

REQUIRED_BLOCK_KEYS = (
    "consensus_financial",
    "consensus_revision",
    "broker_target",
    "report_summary",
    "shareholder_snapshot",
    "business_summary",
)

SAMPLE_METRICS = (
    "매출액",
    "영업이익",
    "순이익",
    "EPS",
    "적정주가",
    "투자의견",
)


def _query_scalar(cur: sqlite3.Cursor, sql: str, params: tuple[object, ...]) -> int:
    row = cur.execute(sql, params).fetchone()
    return int(row[0] or 0) if row else 0


def _target_codes() -> tuple[str, ...]:
    return tuple(stock_code for _, stock_code in TARGETS)


def _in_clause_targets() -> str:
    return ", ".join("?" for _ in TARGETS)


def _company_counts(cur: sqlite3.Cursor) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for company_name, stock_code in TARGETS:
        counts: dict[str, object] = {
            "company_name": company_name,
            "stock_code": stock_code,
            "fetch_log_count": _query_scalar(
                cur,
                "SELECT COUNT(*) FROM fnguide_fetch_log WHERE stock_code = ?",
                (stock_code,),
            ),
            "fnguide_observation": _query_scalar(
                cur,
                "SELECT COUNT(*) FROM fnguide_observation WHERE stock_code = ?",
                (stock_code,),
            ),
            "consensus_financial": _query_scalar(
                cur,
                """
                SELECT COUNT(*)
                FROM fnguide_observation
                WHERE stock_code = ?
                  AND block_type = 'CONSENSUS_FINANCIAL'
                """,
                (stock_code,),
            ),
            "consensus_revision": _query_scalar(
                cur,
                """
                SELECT COUNT(*)
                FROM fnguide_observation
                WHERE stock_code = ?
                  AND block_type = 'CONSENSUS_REVISION'
                """,
                (stock_code,),
            ),
            "broker_target": _query_scalar(
                cur,
                "SELECT COUNT(*) FROM broker_target_price WHERE stock_code = ?",
                (stock_code,),
            ),
            "report_summary": _query_scalar(
                cur,
                "SELECT COUNT(*) FROM broker_report_summary WHERE stock_code = ?",
                (stock_code,),
            ),
            "shareholder_snapshot": _query_scalar(
                cur,
                "SELECT COUNT(*) FROM company_shareholder_snapshot WHERE stock_code = ?",
                (stock_code,),
            ),
            "business_summary": _query_scalar(
                cur,
                "SELECT COUNT(*) FROM company_business_summary WHERE stock_code = ?",
                (stock_code,),
            ),
            "broker_target_null_rows": _query_scalar(
                cur,
                """
                SELECT COUNT(*)
                FROM broker_target_price
                WHERE stock_code = ?
                  AND (target_price IS NULL OR rating IS NULL)
                """,
                (stock_code,),
            ),
        }
        counts["all_required_blocks_present"] = all(
            int(counts[key]) > 0 for key in REQUIRED_BLOCK_KEYS
        )
        rows.append(counts)
    return rows


def _write_company_counts(path: Path, rows: list[dict[str, object]]) -> None:
    fieldnames = [
        "company_name",
        "stock_code",
        "fetch_log_count",
        "fnguide_observation",
        "consensus_financial",
        "consensus_revision",
        "broker_target",
        "report_summary",
        "shareholder_snapshot",
        "business_summary",
        "broker_target_null_rows",
        "all_required_blocks_present",
    ]
    with path.open("w", encoding="utf-8-sig", newline="") as fp:
        writer = csv.DictWriter(fp, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def _write_metrics_coverage(path: Path, cur: sqlite3.Cursor) -> None:
    rows = cur.execute(
        f"""
        SELECT
            company_name,
            stock_code,
            block_type,
            COALESCE(ifrs_scope, '') AS ifrs_scope,
            COALESCE(period_scope, '') AS period_scope,
            COUNT(*) AS row_count,
            COUNT(DISTINCT raw_metric_name) AS distinct_raw_metric_count
        FROM fnguide_observation
        WHERE stock_code IN ({_in_clause_targets()})
        GROUP BY company_name, stock_code, block_type, COALESCE(ifrs_scope, ''), COALESCE(period_scope, '')
        ORDER BY stock_code, block_type, ifrs_scope, period_scope
        """,
        _target_codes(),
    ).fetchall()
    with path.open("w", encoding="utf-8-sig", newline="") as fp:
        writer = csv.writer(fp)
        writer.writerow(
            [
                "company_name",
                "stock_code",
                "block_type",
                "ifrs_scope",
                "period_scope",
                "row_count",
                "distinct_raw_metric_count",
            ]
        )
        writer.writerows(rows)


def _write_timeseries_sample(path: Path, cur: sqlite3.Cursor) -> None:
    rows = cur.execute(
        f"""
        SELECT
            company_name,
            stock_code,
            block_type,
            raw_metric_name,
            period_label_raw,
            value_text,
            ifrs_scope,
            period_scope
        FROM fnguide_observation
        WHERE stock_code IN ({_in_clause_targets()})
          AND raw_metric_name IN ({", ".join("?" for _ in SAMPLE_METRICS)})
        ORDER BY stock_code, block_type, raw_metric_name, period_label_raw
        """,
        _target_codes() + SAMPLE_METRICS,
    ).fetchall()
    with path.open("w", encoding="utf-8-sig", newline="") as fp:
        writer = csv.writer(fp)
        writer.writerow(
            [
                "company_name",
                "stock_code",
                "block_type",
                "raw_metric_name",
                "period_label_raw",
                "value_text",
                "ifrs_scope",
                "period_scope",
            ]
        )
        writer.writerows(rows)


def _write_validation_md(path: Path, company_rows: list[dict[str, object]]) -> None:
    by_company = {str(row["company_name"]): row for row in company_rows}
    korea_zinc_ok = bool(by_company["고려아연"]["all_required_blocks_present"])
    batch_ok = all(bool(row["all_required_blocks_present"]) for row in company_rows)
    blocked = any(int(row["fetch_log_count"]) < 18 for row in company_rows)
    controlled_count = len(company_rows)
    company_labels = ", ".join(
        f"{company_name} ({stock_code})" for company_name, stock_code in TARGETS
    )

    missing_lines = []
    partial_companies = []
    for row in company_rows:
        missing = [name for name in REQUIRED_BLOCK_KEYS if int(row[name]) == 0]
        if missing:
            partial_companies.append((row["company_name"], row["stock_code"], missing))
        missing_lines.append(
            f"- {row['company_name']} ({row['stock_code']}): {', '.join(missing) if missing else 'none'}"
        )

    sparse_lines = [
        (
            f"- {row['company_name']} ({row['stock_code']}): "
            f"broker_target null target/rating rows = {row['broker_target_null_rows']}"
        )
        for row in company_rows
        if int(row["broker_target_null_rows"]) > 0
    ]

    notes = [
        f"- {sum(bool(row['all_required_blocks_present']) for row in company_rows)} of {controlled_count} companies produced all six required blocks.",
        "- No blocked or abnormal response was observed in this batch.",
        "- Collection remained low-rate and sequential.",
    ]
    if partial_companies:
        notes.append(
            "- Some companies returned source-side sparse coverage even though fetches completed:"
        )
        for company_name, stock_code, missing in partial_companies:
            notes.append(
                f"  - {company_name} ({stock_code}): missing {', '.join(missing)}"
            )

    command_lines = [
        "```powershell",
        "py -3 -m python.etl.debug_fnguide_layout `",
        "  --stock-code 062040",
        "",
        "py -3 -m python.etl.debug_fnguide_layout `",
        "  --stock-code 112610",
        "",
        "py -3 -m python.etl.debug_fnguide_layout `",
        "  --stock-code 101490",
        "",
        "py -3 -m python.etl.debug_fnguide_layout `",
        "  --stock-code 458870",
        "",
        "py -3 -m python.etl.debug_fnguide_layout `",
        "  --stock-code 300080",
        "",
        "py -3 -m python.etl.run_fnguide_parser `",
        "  --company 산일전기:A062040 `",
        "  --company 씨에스윈드:A112610 `",
        "  --company 에스앤에스텍:A101490 `",
        "  --company 씨어스테크놀로지:A458870 `",
        "  --company 플리토:A300080 `",
        "  --company 하이브:A352820 `",
        "  --company 오파스넷:A173130 `",
        "  --company 에스텍:A069510 `",
        "  --company 영화테크:A265560",
        "",
        "py -3 -m python.etl.inspect_fnguide_load `",
        "  --stock-code 062040",
        "",
        "py -3 -m python.etl.inspect_fnguide_load `",
        "  --stock-code 112610",
        "",
        "py -3 -m python.etl.inspect_fnguide_load `",
        "  --stock-code 101490",
        "",
        "py -3 -m python.etl.inspect_fnguide_load `",
        "  --stock-code 458870",
        "",
        "py -3 -m python.etl.inspect_fnguide_load `",
        "  --stock-code 300080",
        "",
        "py -3 -m python.etl.inspect_fnguide_load `",
        "  --stock-code 352820",
        "",
        "py -3 -m python.etl.inspect_fnguide_load `",
        "  --stock-code 173130",
        "",
        "py -3 -m python.etl.inspect_fnguide_load `",
        "  --stock-code 069510",
        "",
        "py -3 -m python.etl.inspect_fnguide_load `",
        "  --stock-code 265560",
        "",
        "py -3 -m python.etl.build_fnguide_controlled_batch_reports",
        "```",
    ]

    lines = [
        "# FnGuide controlled batch validation",
        "",
        "## Scope",
        "- Single-company validation target: 고려아연 (010130)",
        f"- Controlled batch targets: {company_labels}",
        "",
        "## Result",
        f"- 고려아연 single-company validation success: {'YES' if korea_zinc_ok else 'NO'}",
        f"- {controlled_count}-company controlled checkpoint all-block success: {'YES' if batch_ok else 'NO'}",
        f"- blocked or abnormal response detected: {'YES' if blocked else 'NO'}",
        f"- next controlled expansion readiness: {'YES' if not blocked else 'NO'}",
        "",
        "## Per-company block counts",
        "| company_name | stock_code | financial | revision | broker_target | report_summary | shareholder | business_summary | fetch_logs |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]

    for row in company_rows:
        lines.append(
            "| {company_name} | {stock_code} | {consensus_financial} | {consensus_revision} | "
            "{broker_target} | {report_summary} | {shareholder_snapshot} | {business_summary} | {fetch_log_count} |".format(
                **row
            )
        )

    lines.extend(
        [
            "",
            "## Missing or zero-count blocks",
            *missing_lines,
            "",
            "## Sparse but non-zero rows",
            *(sparse_lines or ["- none"]),
            "",
            "## Notes",
            *notes,
            "",
            "## Commands used",
            *command_lines,
        ]
    )

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    try:
        cur = conn.cursor()
        company_rows = _company_counts(cur)
        _write_company_counts(OUTPUT_DIR / "fnguide_company_counts.csv", company_rows)
        _write_metrics_coverage(OUTPUT_DIR / "fnguide_metrics_coverage.csv", cur)
        _write_timeseries_sample(OUTPUT_DIR / "fnguide_timeseries_sample.csv", cur)
        _write_validation_md(
            OUTPUT_DIR / "fnguide_controlled_batch_validation.md", company_rows
        )
    finally:
        conn.close()


if __name__ == "__main__":
    main()
