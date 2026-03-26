from __future__ import annotations

import json
import re
import time
from dataclasses import dataclass
from io import StringIO
from pathlib import Path
from typing import Any

import pandas as pd
import requests
from bs4 import BeautifulSoup
from sqlalchemy import text

from python.etl.db_runtime import BASE_DIR, execute_sql_script
from python.etl.inventory_sources import utc_now_iso


FNGUIDE_SQL_PATH = BASE_DIR / "sql" / "009_create_fnguide_tables.sql"
FNGUIDE_OUTPUT_DIR = BASE_DIR / "outputs" / "fnguide_validation"
FNGUIDE_SOURCE_GROUP = "FNGUIDE"
DEFAULT_COMPANY_NAME = "삼성전자"
DEFAULT_STOCK_CODE = "005930"

CONSENSUS_URL_TEMPLATE = (
    "https://comp.fnguide.com/SVO2/ASP/SVD_Consensus.asp"
    "?pGB=1&gicode={gicode}&cID=&MenuYn=Y&ReportGB=&NewMenuID=108&stkGb=701"
)
MAIN_URL_TEMPLATE = (
    "https://comp.fnguide.com/SVO2/ASP/SVD_Main.asp"
    "?pGB=1&gicode={gicode}&cID=&MenuYn=Y&ReportGB=&NewMenuID=101&stkGb=701"
)
JSON_URL_TEMPLATE = "https://comp.fnguide.com/SVO2/json/data/01_06/{path}"

REQUEST_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/135.0 Safari/537.36"
    ),
    "Referer": "https://comp.fnguide.com/",
}
REQUEST_MIN_INTERVAL_SECONDS = 1.2
REQUEST_SESSION = requests.Session()
REQUEST_SESSION.headers.update(REQUEST_HEADERS)
_LAST_REQUEST_AT = 0.0

DATE_PATTERN = re.compile(r"^(?P<year>\d{4})/(?P<month>\d{2})(?:/(?P<day>\d{2}))?(?P<estimate>\(E\))?$")
RELATIVE_PERIOD_PATTERN = re.compile(r"^\d+(개월전|년전)$")
UNIT_PATTERN = re.compile(r"\(([^)]+)\)")
REPORT_GB_LABELS = {"D": "CONNECTED", "B": "SEPARATE"}


@dataclass(frozen=True)
class FnGuideCompanyContext:
    company_name: str
    stock_code: str
    gicode: str
    company_id: int | None = None


@dataclass(frozen=True)
class FnGuidePageBundle:
    url: str
    html: str
    soup: BeautifulSoup
    tables: list[pd.DataFrame]


def ensure_fnguide_output_dir() -> Path:
    FNGUIDE_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    return FNGUIDE_OUTPUT_DIR


def execute_fnguide_schema(engine) -> None:
    execute_sql_script(engine, FNGUIDE_SQL_PATH)


def clean_text(value: Any) -> str:
    if value is None:
        return ""
    return str(value).replace("\xa0", " ").strip()


def normalize_stock_code(stock_code: str | None) -> str:
    cleaned = clean_text(stock_code)
    if cleaned.startswith("A"):
        cleaned = cleaned[1:]
    return cleaned


def normalize_gicode(stock_code: str) -> str:
    normalized_stock_code = normalize_stock_code(stock_code)
    if not normalized_stock_code:
        raise ValueError("A six-digit stock_code is required to build a FnGuide gicode.")
    return f"A{normalized_stock_code}"


def _throttle_request() -> None:
    global _LAST_REQUEST_AT
    now = time.monotonic()
    wait_seconds = REQUEST_MIN_INTERVAL_SECONDS - (now - _LAST_REQUEST_AT)
    if wait_seconds > 0:
        time.sleep(wait_seconds)
    _LAST_REQUEST_AT = time.monotonic()


def _http_get(url: str) -> requests.Response:
    _throttle_request()
    response = REQUEST_SESSION.get(url, timeout=30)
    response.raise_for_status()
    return response


def _fetch_text(url: str) -> str:
    response = _http_get(url)
    return response.text


def _fetch_json(path: str) -> dict[str, Any]:
    response = _http_get(JSON_URL_TEMPLATE.format(path=path))
    return json.loads(response.content.decode("utf-8-sig"))


def fetch_consensus_page(stock_code: str = DEFAULT_STOCK_CODE) -> FnGuidePageBundle:
    gicode = normalize_gicode(stock_code)
    url = CONSENSUS_URL_TEMPLATE.format(gicode=gicode)
    html = _fetch_text(url)
    return FnGuidePageBundle(
        url=url,
        html=html,
        soup=BeautifulSoup(html, "html.parser"),
        tables=pd.read_html(StringIO(html)),
    )


def fetch_main_page(stock_code: str = DEFAULT_STOCK_CODE) -> FnGuidePageBundle:
    gicode = normalize_gicode(stock_code)
    url = MAIN_URL_TEMPLATE.format(gicode=gicode)
    html = _fetch_text(url)
    return FnGuidePageBundle(
        url=url,
        html=html,
        soup=BeautifulSoup(html, "html.parser"),
        tables=pd.read_html(StringIO(html)),
    )


def resolve_company_context(
    engine,
    company_name: str | None = DEFAULT_COMPANY_NAME,
    stock_code: str | None = DEFAULT_STOCK_CODE,
) -> FnGuideCompanyContext:
    requested_company_name = clean_text(company_name)
    requested_stock_code = normalize_stock_code(stock_code)

    with engine.begin() as connection:
        row = connection.execute(
            text(
                """
                SELECT company_id, company_name, normalized_stock_code
                FROM company
                WHERE normalized_stock_code = :stock_code
                   OR company_name = :company_name
                ORDER BY CASE WHEN normalized_stock_code = :stock_code THEN 0 ELSE 1 END
                LIMIT 1
                """
            ),
            {"stock_code": requested_stock_code, "company_name": requested_company_name},
        ).mappings().first()

    if row:
        resolved_stock_code = normalize_stock_code(row["normalized_stock_code"] or requested_stock_code)
        return FnGuideCompanyContext(
            company_name=row["company_name"] or requested_company_name or requested_stock_code,
            stock_code=resolved_stock_code,
            gicode=normalize_gicode(resolved_stock_code),
            company_id=row["company_id"],
        )

    if requested_stock_code:
        fallback_company_name = requested_company_name or requested_stock_code
        return FnGuideCompanyContext(
            company_name=fallback_company_name,
            stock_code=requested_stock_code,
            gicode=normalize_gicode(requested_stock_code),
            company_id=None,
        )

    if requested_company_name:
        raise ValueError(
            f"Could not resolve FnGuide company '{requested_company_name}' to a normalized stock code."
        )

    raise ValueError("Either company_name or stock_code is required for FnGuide ingestion.")


def build_company_output_stem(company: FnGuideCompanyContext) -> str:
    return normalize_stock_code(company.stock_code)


def output_stem_for_company(company: FnGuideCompanyContext) -> str | None:
    if normalize_stock_code(company.stock_code) == normalize_stock_code(DEFAULT_STOCK_CODE):
        return None
    return build_company_output_stem(company)


def default_company_request() -> tuple[str, str]:
    return DEFAULT_COMPANY_NAME, normalize_stock_code(DEFAULT_STOCK_CODE)


def requested_company_or_default(company_name: str | None, stock_code: str | None) -> tuple[str | None, str | None]:
    requested_company_name = clean_text(company_name) or None
    requested_stock_code = normalize_stock_code(stock_code) or None
    if requested_company_name or requested_stock_code:
        return requested_company_name, requested_stock_code
    return default_company_request()


def validation_output_paths(
    company: FnGuideCompanyContext,
    output_stem: str | None = None,
) -> dict[str, Path]:
    output_dir = ensure_fnguide_output_dir()
    if output_stem:
        stem = output_stem
        return {
            "consensus_financial_csv": output_dir / f"{stem}_consensus_financial_long.csv",
            "consensus_revision_csv": output_dir / f"{stem}_consensus_revision_long.csv",
            "broker_target_csv": output_dir / f"{stem}_broker_target_prices.csv",
            "report_summary_csv": output_dir / f"{stem}_report_summary.csv",
            "shareholder_csv": output_dir / f"{stem}_shareholder_snapshot.csv",
            "business_summary_txt": output_dir / f"{stem}_business_summary.txt",
            "validation_report_md": output_dir / f"{stem}_validation_report.md",
            "db_check_md": output_dir / f"{stem}_db_check.md",
            "layout_debug_md": output_dir / f"{stem}_layout_debug.md",
        }

    return {
        "consensus_financial_csv": output_dir / "samsung_consensus_financial_long.csv",
        "consensus_revision_csv": output_dir / "samsung_consensus_revision_long.csv",
        "broker_target_csv": output_dir / "samsung_broker_target_prices.csv",
        "report_summary_csv": output_dir / "samsung_report_summary.csv",
        "shareholder_csv": output_dir / "samsung_shareholder_snapshot.csv",
        "business_summary_txt": output_dir / "samsung_business_summary.txt",
        "validation_report_md": output_dir / "fnguide_validation_report.md",
        "db_check_md": output_dir / "fnguide_db_check.md",
        "layout_debug_md": output_dir / "fnguide_layout_debug.md",
    }


def detect_consensus_modes(bundle: FnGuidePageBundle) -> dict[str, Any]:
    quarterly_pairs = re.findall(r'FQ(\d).*?(\d{6})', bundle.html)
    quarterly_options: list[dict[str, str]] = []
    seen_values: set[str] = set()
    for index, label in quarterly_pairs:
        value = f"FQ{index}"
        if value in seen_values:
            continue
        quarterly_options.append({"value": value, "label": label})
        seen_values.add(value)
    return {
        "financial_ifrs_modes": [
            {"value": "D", "label": "CONNECTED"},
            {"value": "B", "label": "SEPARATE"},
        ],
        "financial_period_modes": [
            {"value": "A", "label": "YEAR"},
            {"value": "Q", "label": "QUARTER"},
        ],
        "revision_period_options": {
            "YEAR": [
                {"value": option.get("value", ""), "label": option.get_text(strip=True)}
                for option in bundle.soup.select("#selGsym option")
            ],
            "QUARTER": quarterly_options,
        },
        "detected_select_ids": [select.get("id") for select in bundle.soup.find_all("select")],
    }


def normalize_fnguide_numeric(value: Any) -> float | None:
    if value is None:
        return None
    text_value = clean_text(value)
    if not text_value or text_value in {"-", "--", "N/A", "nan"}:
        return None

    cleaned = (
        text_value.replace(",", "")
        .replace("%", "")
        .replace("배", "")
        .replace("원", "")
        .replace("억원", "")
        .strip()
    )
    if not cleaned:
        return None

    try:
        return float(cleaned)
    except ValueError:
        return None


def normalize_period_label(period_label_raw: str, period_scope: str | None = None) -> dict[str, Any]:
    label = period_label_raw.strip()
    match = DATE_PATTERN.match(label)
    if match:
        year = int(match.group("year"))
        month = int(match.group("month"))
        day = int(match.group("day")) if match.group("day") else 1
        is_estimate = 1 if match.group("estimate") else 0

        if period_scope == "QUARTER":
            fiscal_quarter = ((month - 1) // 3) + 1
            return {
                "period_type": "QUARTER",
                "fiscal_year": year,
                "fiscal_quarter": fiscal_quarter,
                "date_raw": f"{year:04d}/{month:02d}/{day:02d}",
                "period_label_std": f"{str(year)[-2:]}.{fiscal_quarter}Q",
                "is_estimate": is_estimate,
            }

        if day != 1:
            return {
                "period_type": "SNAPSHOT",
                "fiscal_year": None,
                "fiscal_quarter": None,
                "date_raw": f"{year:04d}/{month:02d}/{day:02d}",
                "period_label_std": f"{year:04d}/{month:02d}/{day:02d}",
                "is_estimate": is_estimate,
            }

        return {
            "period_type": "YEAR",
            "fiscal_year": year,
            "fiscal_quarter": None,
            "date_raw": f"{year:04d}/{month:02d}/{day:02d}",
            "period_label_std": f"{year:04d}",
            "is_estimate": is_estimate,
        }

    if RELATIVE_PERIOD_PATTERN.match(label):
        return {
            "period_type": "SNAPSHOT",
            "fiscal_year": None,
            "fiscal_quarter": None,
            "date_raw": None,
            "period_label_std": label,
            "is_estimate": 0,
        }

    return {
        "period_type": "SNAPSHOT",
        "fiscal_year": None,
        "fiscal_quarter": None,
        "date_raw": None,
        "period_label_std": label,
        "is_estimate": 0,
    }


def extract_unit(raw_metric_name: str) -> tuple[str, str | None]:
    raw_metric_name = clean_text(raw_metric_name)
    match = UNIT_PATTERN.search(raw_metric_name)
    unit = match.group(1) if match else None
    metric_name = UNIT_PATTERN.sub("", raw_metric_name).strip()
    return metric_name, unit


def _json_metric_row_payload(row: dict[str, Any]) -> str:
    return json.dumps(row, ensure_ascii=False)


def to_long_records(
    payload_rows: list[dict[str, Any]],
    *,
    company: FnGuideCompanyContext,
    source_url: str,
    block_type: str,
    ifrs_scope: str | None,
    period_scope: str | None,
    consensus_year_label: str | None,
    row_metric_key: str,
    period_columns: list[tuple[str, str]],
    line_group_key: str,
) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for row_index, row in enumerate(payload_rows, start=1):
        metric_raw = clean_text(row.get(row_metric_key, ""))
        if not metric_raw or metric_raw == "항목":
            continue

        metric_name, unit = extract_unit(metric_raw)
        note_text = f"GB={row.get('GB', '')};PARENT_YN={row.get('PARENT_YN', '')}"
        for column_key, period_label_raw in period_columns:
            value_text = clean_text(row.get(column_key, ""))
            if not value_text or value_text == "-":
                continue

            period_info = normalize_period_label(period_label_raw, period_scope)
            records.append(
                {
                    "company_id": company.company_id,
                    "company_name": company.company_name,
                    "stock_code": company.stock_code,
                    "source_group": FNGUIDE_SOURCE_GROUP,
                    "source_url": source_url,
                    "page_type": "CONSENSUS",
                    "block_type": block_type,
                    "ifrs_scope": ifrs_scope,
                    "period_scope": period_scope,
                    "consensus_year_label": consensus_year_label,
                    "source_row_order": row_index,
                    "line_group": str(row.get(line_group_key, "")) or None,
                    "raw_metric_name": metric_name,
                    "period_label_raw": period_label_raw,
                    "period_type": period_info["period_type"],
                    "fiscal_year": period_info["fiscal_year"],
                    "fiscal_quarter": period_info["fiscal_quarter"],
                    "date_raw": period_info["date_raw"],
                    "value_text": value_text,
                    "value_numeric": normalize_fnguide_numeric(value_text),
                    "value_unit": unit,
                    "is_estimate": 1 if period_info["is_estimate"] or "(E)" in value_text else 0,
                    "note_text": note_text,
                    "raw_payload_json": _json_metric_row_payload(row),
                    "scraped_at": utc_now_iso(),
                }
            )
    return records


def parse_consensus_financial_table(
    payload: dict[str, Any],
    *,
    company: FnGuideCompanyContext,
    source_url: str,
    ifrs_scope: str,
    period_scope: str,
) -> list[dict[str, Any]]:
    rows = payload.get("comp", [])
    if not rows:
        return []
    header = rows[0]
    period_columns = [
        (column_key, str(header[column_key]).strip())
        for column_key in sorted(header.keys())
        if column_key.startswith("D_") and column_key != "D_0" and str(header[column_key]).strip()
    ]
    return to_long_records(
        rows[1:],
        company=company,
        source_url=source_url,
        block_type="CONSENSUS_FINANCIAL",
        ifrs_scope=ifrs_scope,
        period_scope=period_scope,
        consensus_year_label=None,
        row_metric_key="ACCOUNT_NM",
        period_columns=period_columns,
        line_group_key="SORT_ORDER",
    )


def parse_consensus_revision_table(
    payload: dict[str, Any],
    *,
    company: FnGuideCompanyContext,
    source_url: str,
    ifrs_scope: str,
    period_scope: str,
    consensus_year_label: str,
) -> list[dict[str, Any]]:
    rows = payload.get("comp", [])
    if not rows:
        return []
    header = rows[0]
    period_columns = [
        (column_key, str(header[column_key]).strip())
        for column_key in sorted(header.keys())
        if column_key.startswith("D_") and column_key != "D_0" and str(header[column_key]).strip()
    ]
    return to_long_records(
        rows[1:],
        company=company,
        source_url=source_url,
        block_type="CONSENSUS_REVISION",
        ifrs_scope=ifrs_scope,
        period_scope=period_scope,
        consensus_year_label=consensus_year_label,
        row_metric_key="D_0",
        period_columns=period_columns,
        line_group_key="D_0",
    )


def parse_broker_target_table(
    payload: dict[str, Any],
    *,
    company: FnGuideCompanyContext,
    source_url: str,
) -> list[dict[str, Any]]:
    rows = payload.get("comp", [])
    if not rows:
        return []

    first_row = rows[0]
    records: list[dict[str, Any]] = [
        {
            "company_id": company.company_id,
            "company_name": company.company_name,
            "stock_code": company.stock_code,
            "broker_name": "Consensus",
            "estimate_date": None,
            "target_price": normalize_fnguide_numeric(first_row.get("AVG_PRC")),
            "previous_target_price": normalize_fnguide_numeric(first_row.get("AVG_PRC_BF")),
            "change_pct": normalize_fnguide_numeric(first_row.get("YOY")),
            "rating": clean_text(first_row.get("AVG_RECOM_CD")) or None,
            "previous_rating": clean_text(first_row.get("AVG_RECOM_CD_BF")) or None,
            "is_consensus_aggregate": 1,
            "source_group": FNGUIDE_SOURCE_GROUP,
            "source_url": source_url,
            "scraped_at": utc_now_iso(),
            "raw_payload_json": _json_metric_row_payload(first_row),
        }
    ]

    for row in rows:
        records.append(
            {
                "company_id": company.company_id,
                "company_name": company.company_name,
                "stock_code": company.stock_code,
                "broker_name": clean_text(row.get("INST_NM")),
                "estimate_date": clean_text(row.get("EST_DT")) or None,
                "target_price": normalize_fnguide_numeric(row.get("TARGET_PRC")),
                "previous_target_price": normalize_fnguide_numeric(row.get("TARGET_PRC_BF")),
                "change_pct": normalize_fnguide_numeric(row.get("YOY")),
                "rating": clean_text(row.get("RECOM_CD")) or None,
                "previous_rating": clean_text(row.get("RECOM_CD_BF")) or None,
                "is_consensus_aggregate": 0,
                "source_group": FNGUIDE_SOURCE_GROUP,
                "source_url": source_url,
                "scraped_at": utc_now_iso(),
                "raw_payload_json": _json_metric_row_payload(row),
            }
        )
    return records


def parse_report_summary(
    payload: dict[str, Any],
    *,
    company: FnGuideCompanyContext,
    source_url: str,
) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for row in payload.get("comp", []):
        bullet_date = clean_text(row.get("BULLET_DT"))
        report_date = None
        if len(bullet_date) == 8:
            report_date = f"{bullet_date[:4]}/{bullet_date[4:6]}/{bullet_date[6:8]}"

        records.append(
            {
                "company_id": company.company_id,
                "company_name": company.company_name,
                "stock_code": company.stock_code,
                "report_date": report_date,
                "report_title": clean_text(row.get("TITLE")) or None,
                "report_body": clean_text(row.get("SYNOPSIS")) or None,
                "rating_text": clean_text(row.get("RECOMMEND")) or None,
                "target_price_text": clean_text(row.get("TARGET_PRC")) or None,
                "prev_close_price_text": clean_text(row.get("CLS_PRC")) or None,
                "provider_name": clean_text(row.get("OFFER_INST_NM")) or None,
                "analyst_name": clean_text(row.get("BEST_ANAL_NM") or row.get("NICK_NM")) or None,
                "source_group": FNGUIDE_SOURCE_GROUP,
                "source_url": source_url,
                "scraped_at": utc_now_iso(),
                "raw_payload_json": _json_metric_row_payload(row),
            }
        )
    return records


def _find_shareholder_tables(main_bundle: FnGuidePageBundle) -> tuple[pd.DataFrame | None, pd.DataFrame | None]:
    detailed_table = None
    summary_table = None
    for table in main_bundle.tables:
        normalized_columns = [str(column).strip() for column in table.columns]
        if normalized_columns[:4] == ["항목", "보통주", "지분율", "최종변동일"]:
            detailed_table = table.copy()
        if normalized_columns[:5] == ["주주구분", "대표주주수", "보통주", "지분율", "최종변동일"]:
            summary_table = table.copy()
    return detailed_table, summary_table


def parse_shareholder_table(
    main_bundle: FnGuidePageBundle,
    *,
    company: FnGuideCompanyContext,
    source_url: str,
) -> list[dict[str, Any]]:
    detailed_table, summary_table = _find_shareholder_tables(main_bundle)
    records: list[dict[str, Any]] = []

    if detailed_table is not None:
        for _, row in detailed_table.fillna("").iterrows():
            holder_name = clean_text(row.get("항목"))
            if not holder_name:
                continue
            records.append(
                {
                    "company_id": company.company_id,
                    "company_name": company.company_name,
                    "stock_code": company.stock_code,
                    "holder_name": holder_name,
                    "holder_type": "holder_detail",
                    "snapshot_kind": "DETAIL",
                    "shares": normalize_fnguide_numeric(row.get("보통주")),
                    "ownership_pct": normalize_fnguide_numeric(row.get("지분율")),
                    "as_of_date": clean_text(row.get("최종변동일")) or None,
                    "source_group": FNGUIDE_SOURCE_GROUP,
                    "source_url": source_url,
                    "scraped_at": utc_now_iso(),
                    "raw_payload_json": row.to_json(force_ascii=False),
                }
            )

    if summary_table is not None:
        for _, row in summary_table.fillna("").iterrows():
            holder_name = clean_text(row.get("주주구분"))
            if not holder_name:
                continue
            records.append(
                {
                    "company_id": company.company_id,
                    "company_name": company.company_name,
                    "stock_code": company.stock_code,
                    "holder_name": holder_name,
                    "holder_type": "shareholder_group",
                    "snapshot_kind": "SUMMARY",
                    "shares": normalize_fnguide_numeric(row.get("보통주")),
                    "ownership_pct": normalize_fnguide_numeric(row.get("지분율")),
                    "as_of_date": clean_text(row.get("최종변동일")) or None,
                    "source_group": FNGUIDE_SOURCE_GROUP,
                    "source_url": source_url,
                    "scraped_at": utc_now_iso(),
                    "raw_payload_json": row.to_json(force_ascii=False),
                }
            )
    return records


def parse_business_summary(
    main_bundle: FnGuidePageBundle,
    *,
    company: FnGuideCompanyContext,
    source_url: str,
) -> dict[str, Any] | None:
    title_node = main_bundle.soup.select_one("#bizSummaryHeader")
    date_node = main_bundle.soup.select_one("#bizSummaryDate")
    content_nodes = main_bundle.soup.select("#bizSummaryContent li")
    if not title_node and not content_nodes:
        return None

    summary_lines = [clean_text(node.get_text(" ", strip=True)) for node in content_nodes if clean_text(node.get_text(" ", strip=True))]
    return {
        "company_id": company.company_id,
        "company_name": company.company_name,
        "stock_code": company.stock_code,
        "summary_title": clean_text(title_node.get_text(" ", strip=True)) if title_node else None,
        "summary_text": "\n".join(summary_lines),
        "as_of_date": clean_text(date_node.get_text(" ", strip=True)).strip("[]") if date_node else None,
        "source_group": FNGUIDE_SOURCE_GROUP,
        "source_url": source_url,
        "scraped_at": utc_now_iso(),
    }


def build_consensus_json_plan(stock_code: str = DEFAULT_STOCK_CODE) -> list[dict[str, str]]:
    gicode = normalize_gicode(stock_code)
    plans: list[dict[str, str]] = []

    financial_modes = [
        ("CONNECTED", "YEAR", f"01_{gicode}_A_D.json"),
        ("CONNECTED", "QUARTER", f"01_{gicode}_Q_D.json"),
        ("SEPARATE", "YEAR", f"01_{gicode}_A_B.json"),
        ("SEPARATE", "QUARTER", f"01_{gicode}_Q_B.json"),
    ]
    for ifrs_scope, period_scope, suffix in financial_modes:
        plans.append(
            {
                "kind": "CONSENSUS_FINANCIAL",
                "ifrs_scope": ifrs_scope,
                "period_scope": period_scope,
                "consensus_year_label": "",
                "path": suffix,
                "url": JSON_URL_TEMPLATE.format(path=suffix),
            }
        )

    for ifrs_scope_code, ifrs_scope_label in REPORT_GB_LABELS.items():
        for label in ["FY1", "FY2", "FY3"]:
            suffix = f"02_{gicode}_A_{ifrs_scope_code}_{label}.json"
            plans.append(
                {
                    "kind": "CONSENSUS_REVISION",
                    "ifrs_scope": ifrs_scope_label,
                    "period_scope": "YEAR",
                    "consensus_year_label": label,
                    "path": suffix,
                    "url": JSON_URL_TEMPLATE.format(path=suffix),
                }
            )
        for label in ["FQ1", "FQ2", "FQ3"]:
            suffix = f"02_{gicode}_Q_{ifrs_scope_code}_{label}.json"
            plans.append(
                {
                    "kind": "CONSENSUS_REVISION",
                    "ifrs_scope": ifrs_scope_label,
                    "period_scope": "QUARTER",
                    "consensus_year_label": label,
                    "path": suffix,
                    "url": JSON_URL_TEMPLATE.format(path=suffix),
                }
            )

    for kind, suffix in [
        ("BROKER_TARGET", f"03_{gicode}.json"),
        ("REPORT_SUMMARY", f"04_{gicode}.json"),
    ]:
        plans.append(
            {
                "kind": kind,
                "ifrs_scope": "",
                "period_scope": "",
                "consensus_year_label": "",
                "path": suffix,
                "url": JSON_URL_TEMPLATE.format(path=suffix),
            }
        )

    return plans


def delete_existing_fnguide_rows(connection, stock_code: str) -> None:
    connection.execute(text("DELETE FROM fnguide_fetch_log WHERE stock_code = :stock_code"), {"stock_code": stock_code})
    connection.execute(text("DELETE FROM fnguide_observation WHERE stock_code = :stock_code"), {"stock_code": stock_code})
    connection.execute(text("DELETE FROM company_shareholder_snapshot WHERE stock_code = :stock_code"), {"stock_code": stock_code})
    connection.execute(text("DELETE FROM company_business_summary WHERE stock_code = :stock_code"), {"stock_code": stock_code})
    connection.execute(text("DELETE FROM broker_target_price WHERE stock_code = :stock_code"), {"stock_code": stock_code})
    connection.execute(text("DELETE FROM broker_report_summary WHERE stock_code = :stock_code"), {"stock_code": stock_code})


def insert_rows(connection, table_name: str, rows: list[dict[str, Any]]) -> None:
    if not rows:
        return
    columns = list(rows[0].keys())
    column_sql = ", ".join(columns)
    placeholder_sql = ", ".join(f":{column}" for column in columns)
    connection.execute(text(f"INSERT INTO {table_name} ({column_sql}) VALUES ({placeholder_sql})"), rows)


def load_fnguide_data(engine, company_name: str = DEFAULT_COMPANY_NAME, stock_code: str = DEFAULT_STOCK_CODE) -> dict[str, Any]:
    company = resolve_company_context(engine, company_name=company_name, stock_code=stock_code)
    consensus_bundle = fetch_consensus_page(company.stock_code)
    main_bundle = fetch_main_page(company.stock_code)

    result: dict[str, Any] = {
        "company": company,
        "consensus_url": consensus_bundle.url,
        "main_url": main_bundle.url,
        "consensus_modes": detect_consensus_modes(consensus_bundle),
        "consensus_bundle": consensus_bundle,
        "main_bundle": main_bundle,
        "fetch_logs": [],
        "consensus_financial_records": [],
        "consensus_revision_records": [],
        "broker_target_records": [],
        "report_summary_records": [],
        "shareholder_records": [],
        "business_summary_record": None,
        "execution_started_at": utc_now_iso(),
    }

    for plan in build_consensus_json_plan(company.stock_code):
        payload = _fetch_json(plan["path"])
        result["fetch_logs"].append(
            {
                "company_id": company.company_id,
                "company_name": company.company_name,
                "stock_code": company.stock_code,
                "page_type": plan["kind"],
                "ifrs_scope": plan["ifrs_scope"] or None,
                "period_scope": plan["period_scope"] or None,
                "consensus_year_label": plan["consensus_year_label"] or None,
                "source_group": FNGUIDE_SOURCE_GROUP,
                "source_url": plan["url"],
                "fetch_status": "SUCCESS",
                "notes": None,
                "fetched_at": utc_now_iso(),
                "raw_payload_json": json.dumps(payload, ensure_ascii=False),
            }
        )

        if plan["kind"] == "CONSENSUS_FINANCIAL":
            result["consensus_financial_records"].extend(
                parse_consensus_financial_table(
                    payload,
                    company=company,
                    source_url=plan["url"],
                    ifrs_scope=plan["ifrs_scope"],
                    period_scope=plan["period_scope"],
                )
            )
        elif plan["kind"] == "CONSENSUS_REVISION":
            result["consensus_revision_records"].extend(
                parse_consensus_revision_table(
                    payload,
                    company=company,
                    source_url=plan["url"],
                    ifrs_scope=plan["ifrs_scope"],
                    period_scope=plan["period_scope"],
                    consensus_year_label=plan["consensus_year_label"],
                )
            )
        elif plan["kind"] == "BROKER_TARGET":
            result["broker_target_records"] = parse_broker_target_table(
                payload,
                company=company,
                source_url=plan["url"],
            )
        elif plan["kind"] == "REPORT_SUMMARY":
            result["report_summary_records"] = parse_report_summary(
                payload,
                company=company,
                source_url=plan["url"],
            )

    result["shareholder_records"] = parse_shareholder_table(
        main_bundle,
        company=company,
        source_url=main_bundle.url,
    )
    result["business_summary_record"] = parse_business_summary(
        main_bundle,
        company=company,
        source_url=main_bundle.url,
    )
    return result


def persist_fnguide_data(engine, parsed: dict[str, Any]) -> dict[str, int]:
    company: FnGuideCompanyContext = parsed["company"]
    counts = {
        "fetch_logs": len(parsed["fetch_logs"]),
        "fnguide_observation": len(parsed["consensus_financial_records"]) + len(parsed["consensus_revision_records"]),
        "broker_target_price": len(parsed["broker_target_records"]),
        "broker_report_summary": len(parsed["report_summary_records"]),
        "company_shareholder_snapshot": len(parsed["shareholder_records"]),
        "company_business_summary": 1 if parsed["business_summary_record"] else 0,
    }

    with engine.begin() as connection:
        delete_existing_fnguide_rows(connection, company.stock_code)
        insert_rows(connection, "fnguide_fetch_log", parsed["fetch_logs"])
        insert_rows(connection, "fnguide_observation", parsed["consensus_financial_records"] + parsed["consensus_revision_records"])
        insert_rows(connection, "broker_target_price", parsed["broker_target_records"])
        insert_rows(connection, "broker_report_summary", parsed["report_summary_records"])
        insert_rows(connection, "company_shareholder_snapshot", parsed["shareholder_records"])
        if parsed["business_summary_record"]:
            insert_rows(connection, "company_business_summary", [parsed["business_summary_record"]])
    return counts


def dataframe_from_records(records: list[dict[str, Any]]) -> pd.DataFrame:
    return pd.DataFrame(records) if records else pd.DataFrame()


def markdown_table_from_mappings(rows: list[dict[str, Any]], columns: list[str]) -> str:
    if not rows:
        return "_No rows_\n"
    header = "| " + " | ".join(columns) + " |"
    divider = "| " + " | ".join(["---"] * len(columns)) + " |"
    body = [
        "| " + " | ".join(str(row.get(column, "")) for column in columns) + " |"
        for row in rows
    ]
    return "\n".join([header, divider, *body]) + "\n"


def write_validation_outputs(
    parsed: dict[str, Any],
    db_counts: dict[str, int],
    output_stem: str | None = None,
) -> dict[str, Path]:
    paths = validation_output_paths(parsed["company"], output_stem=output_stem)

    dataframe_from_records(parsed["consensus_financial_records"]).to_csv(paths["consensus_financial_csv"], index=False, encoding="utf-8-sig")
    dataframe_from_records(parsed["consensus_revision_records"]).to_csv(paths["consensus_revision_csv"], index=False, encoding="utf-8-sig")
    dataframe_from_records(parsed["broker_target_records"]).to_csv(paths["broker_target_csv"], index=False, encoding="utf-8-sig")
    dataframe_from_records(parsed["report_summary_records"]).to_csv(paths["report_summary_csv"], index=False, encoding="utf-8-sig")
    dataframe_from_records(parsed["shareholder_records"]).to_csv(paths["shareholder_csv"], index=False, encoding="utf-8-sig")
    business_summary = parsed["business_summary_record"]
    paths["business_summary_txt"].write_text((business_summary or {}).get("summary_text", ""), encoding="utf-8")

    financial_sample = dataframe_from_records(parsed["consensus_financial_records"]).head(12).to_dict(orient="records")
    revision_sample = dataframe_from_records(parsed["consensus_revision_records"]).head(12).to_dict(orient="records")
    broker_sample = dataframe_from_records(parsed["broker_target_records"]).head(8).to_dict(orient="records")
    shareholder_sample = dataframe_from_records(parsed["shareholder_records"]).head(8).to_dict(orient="records")
    report_sample = dataframe_from_records(parsed["report_summary_records"]).head(6).to_dict(orient="records")

    report_lines = [
        "# FnGuide validation report",
        "",
        "## Company",
        f"- company_name: {parsed['company'].company_name}",
        f"- stock_code: {parsed['company'].stock_code}",
        "",
        "## Source URLs",
        f"- consensus: {parsed['consensus_url']}",
        f"- main: {parsed['main_url']}",
        "",
        "## Extracted blocks",
        f"- consensus financial long rows: {len(parsed['consensus_financial_records'])}",
        f"- consensus revision long rows: {len(parsed['consensus_revision_records'])}",
        f"- broker target rows: {len(parsed['broker_target_records'])}",
        f"- report summary rows: {len(parsed['report_summary_records'])}",
        f"- shareholder snapshot rows: {len(parsed['shareholder_records'])}",
        f"- business summary present: {'yes' if business_summary else 'no'}",
        "",
        "## 확보 범위",
        f"- consensus modes: {parsed['consensus_modes']}",
        "- 확보됨: 연결/별도, 연간/분기, 증권사별 적정주가, 리포트 요약, 주주현황, Business Summary",
        "- 보류: 차트 이미지 자체 저장, Selenium 전용 렌더링 영역",
        "",
        "## Requests-only viability",
        "- consensus and broker/report blocks are available through requests-accessible JSON endpoints",
        "- shareholder and Business Summary are available through requests-accessible HTML",
        "- Selenium fallback is not required for the current company implementation",
        "",
        "## DB row counts",
        *(f"- {name}: {count}" for name, count in db_counts.items()),
        "",
        "## 삼성전자 대표 샘플 - consensus financial",
        markdown_table_from_mappings(
            financial_sample,
            ["raw_metric_name", "period_label_raw", "value_text", "value_unit", "ifrs_scope", "period_scope"],
        ),
        "## 삼성전자 대표 샘플 - consensus revision",
        markdown_table_from_mappings(
            revision_sample,
            ["raw_metric_name", "period_label_raw", "value_text", "consensus_year_label", "ifrs_scope", "period_scope"],
        ),
        "## 삼성전자 대표 샘플 - broker target",
        markdown_table_from_mappings(
            broker_sample,
            ["broker_name", "estimate_date", "target_price", "previous_target_price", "rating", "is_consensus_aggregate"],
        ),
        "## 삼성전자 대표 샘플 - report summary",
        markdown_table_from_mappings(
            report_sample,
            ["report_date", "report_title", "provider_name", "analyst_name", "rating_text"],
        ),
        "## 삼성전자 대표 샘플 - shareholder",
        markdown_table_from_mappings(
            shareholder_sample,
            ["holder_name", "holder_type", "shares", "ownership_pct", "as_of_date"],
        ),
        "## 삼성전자 대표 샘플 - Business Summary",
        business_summary["summary_text"][:800] if business_summary else "_No business summary_",
        "## 다음 작업 제안",
        "- 다종목 확장 시 gicode 리스트 입력과 batch runner를 추가",
        "- DART API를 다음 단계에서 연결해 FnGuide 데이터와 교차 검증",
        "- 필요 시 차트 데이터 XML endpoint까지 확장",
    ]
    paths["validation_report_md"].write_text("\n".join(report_lines) + "\n", encoding="utf-8")
    return paths


def write_db_check_report(
    engine,
    company: FnGuideCompanyContext,
    output_stem: str | None = None,
) -> Path:
    report_path = validation_output_paths(company, output_stem=output_stem)["db_check_md"]
    with engine.begin() as connection:
        raw_sample = connection.execute(
            text(
                """
                SELECT raw_metric_name, period_label_raw, value_text, value_numeric, block_type, ifrs_scope, period_scope
                FROM fnguide_observation
                WHERE stock_code = :stock_code
                ORDER BY fnguide_observation_id
                LIMIT 30
                """
            ),
            {"stock_code": company.stock_code},
        ).mappings().all()
        broker_sample = connection.execute(
            text(
                """
                SELECT broker_name, estimate_date, target_price, previous_target_price, rating
                FROM broker_target_price
                WHERE stock_code = :stock_code
                ORDER BY broker_target_price_id
                LIMIT 20
                """
            ),
            {"stock_code": company.stock_code},
        ).mappings().all()
        report_sample = connection.execute(
            text(
                """
                SELECT report_date, report_title, provider_name, analyst_name, rating_text
                FROM broker_report_summary
                WHERE stock_code = :stock_code
                ORDER BY broker_report_summary_id
                LIMIT 20
                """
            ),
            {"stock_code": company.stock_code},
        ).mappings().all()
        shareholder_sample = connection.execute(
            text(
                """
                SELECT holder_name, holder_type, shares, ownership_pct, as_of_date
                FROM company_shareholder_snapshot
                WHERE stock_code = :stock_code
                ORDER BY shareholder_snapshot_id
                LIMIT 20
                """
            ),
            {"stock_code": company.stock_code},
        ).mappings().all()
        counts = connection.execute(
            text(
                """
                SELECT 'fnguide_observation' AS table_name, COUNT(*) AS row_count
                FROM fnguide_observation WHERE stock_code = :stock_code
                UNION ALL
                SELECT 'broker_target_price', COUNT(*) FROM broker_target_price WHERE stock_code = :stock_code
                UNION ALL
                SELECT 'broker_report_summary', COUNT(*) FROM broker_report_summary WHERE stock_code = :stock_code
                UNION ALL
                SELECT 'company_shareholder_snapshot', COUNT(*) FROM company_shareholder_snapshot WHERE stock_code = :stock_code
                UNION ALL
                SELECT 'company_business_summary', COUNT(*) FROM company_business_summary WHERE stock_code = :stock_code
                UNION ALL
                SELECT 'fnguide_fetch_log', COUNT(*) FROM fnguide_fetch_log WHERE stock_code = :stock_code
                """
            ),
            {"stock_code": company.stock_code},
        ).mappings().all()

    lines = [
        "# FnGuide DB check",
        "",
        "## Row counts",
        markdown_table_from_mappings(counts, ["table_name", "row_count"]),
        "## fnguide_observation sample",
        markdown_table_from_mappings(raw_sample, ["raw_metric_name", "period_label_raw", "value_text", "value_numeric", "block_type", "ifrs_scope", "period_scope"]),
        "## broker_target_price sample",
        markdown_table_from_mappings(broker_sample, ["broker_name", "estimate_date", "target_price", "previous_target_price", "rating"]),
        "## broker_report_summary sample",
        markdown_table_from_mappings(report_sample, ["report_date", "report_title", "provider_name", "analyst_name", "rating_text"]),
        "## company_shareholder_snapshot sample",
        markdown_table_from_mappings(shareholder_sample, ["holder_name", "holder_type", "shares", "ownership_pct", "as_of_date"]),
    ]
    report_path.write_text("\n".join(lines), encoding="utf-8")
    return report_path
