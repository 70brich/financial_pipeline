from __future__ import annotations

from pathlib import Path
import re


MAPPING_SCHEMA_SQL_PATH = Path(__file__).resolve().parents[2] / "sql" / "005_create_metric_mapping_tables.sql"

PREFIX_PATTERNS = [
    (re.compile(r"^\((\uac1c\ubcc4|\uc5f0\uacb0)\)"), lambda match: match.group(1)),
    (re.compile(r"^(\uac1c\ubcc4|\uc5f0\uacb0)\s*"), lambda match: match.group(1)),
    (re.compile(r"^(\ubd84\uae30|\uc5f0\uac04)\s*"), lambda match: match.group(1)),
]

DEFAULT_ALIAS_MAP = {
    "\ub9e4\ucd9c\uc561": "REVENUE",
    "\ub9e4\ucd9c\uc6d0\uac00": "COST_OF_SALES",
    "\ub9e4\ucd9c\ucd1d\uc774\uc775": "GROSS_PROFIT",
    "\uc601\uc5c5\uc774\uc775": "OPERATING_INCOME",
    "\ud310\uad00\ube44": "SGA_EXPENSE",
    "\ub2f9\uae30\uc21c\uc774\uc775": "NET_INCOME",
    "\uc21c\uc774\uc775": "NET_INCOME",
    "\uc9c0\ubc30\uc8fc\uc8fc\uc21c\uc774\uc775": "CONTROLLING_NET_INCOME",
    "\uc9c0\ubc30\uc21c\uc775": "CONTROLLING_NET_INCOME",
    "\uc9c0\ubc30\uc21c\uc774\uc775": "CONTROLLING_NET_INCOME",
    "\uc21c\uc775(\uc9c0\ubc30)": "CONTROLLING_NET_INCOME",
    "\uc601\uc5c5\ud65c\ub3d9\ud604\uae08\ud750\ub984": "OPERATING_CASH_FLOW",
    "\ud22c\uc790\ud65c\ub3d9\ud604\uae08\ud750\ub984": "INVESTING_CASH_FLOW",
    "\uc7ac\ubb34\ud65c\ub3d9\ud604\uae08\ud750\ub984": "FINANCING_CASH_FLOW",
    "\uc789\uc5ec\ud604\uae08\ud750\ub984": "FREE_CASH_FLOW",
    "\uc774\uc775\uc789\uc5ec\uae08": "RETAINED_EARNINGS",
    "\ub2f9\uc88c\ube44\uc728": "QUICK_RATIO",
    "\ub2f9\uc88c\ube44\uc728(%)": "QUICK_RATIO",
    "\ub9e4\uc785\ucc44\ubb34": "ACCOUNTS_PAYABLE",
    "\ub9e4\ucd9c\ucc44\uad8c": "ACCOUNTS_RECEIVABLE",
    "\uc720\ub3d9\uc790\uc0b0": "CURRENT_ASSETS",
    "\uc720\ub3d9\ubd80\ucc44": "CURRENT_LIABILITIES",
    "\ube44\uc720\ub3d9\uc790\uc0b0": "NON_CURRENT_ASSETS",
    "\ube44\uc720\ub3d9\ubd80\ucc44": "NON_CURRENT_LIABILITIES",
    "\ubb34\ud615\uc790\uc0b0": "INTANGIBLE_ASSETS",
    "\uc720\ud615\uc790\uc0b0": "PROPERTY_PLANT_EQUIPMENT",
    "\uc7ac\uace0\uc790\uc0b0": "INVENTORIES",
    "\ud604\uae08\uc131\uc790\uc0b0": "CASH_EQUIVALENTS",
    "\uc6b4\uc804\uc790\ubcf8": "WORKING_CAPITAL",
    "\ucc28\uc785\uae08": "BORROWINGS",
    "\uc21c\ucc28\uc785\uae08": "NET_DEBT",
    "\uc9c0\ubc30\uc8fc\uc8fc\uc9c0\ubd84": "CONTROLLING_EQUITY",
    "\uc138\uc804\uacc4\uc18d\uc0ac\uc5c5\uc190\uc775": "PRE_TAX_CONTINUING_INCOME",
    "\uc138\uc804\uacc4\uc18d\uc0ac\uc5c5\uc774\uc775\ub960": "PRE_TAX_CONTINUING_MARGIN",
    "\uc138\uc804\uc21c\uc774\uc775": "PRE_TAX_INCOME",
    "\uc138\uc804\uc21c\uc775": "PRE_TAX_INCOME",
    "\ubc95\uc778\uc138": "CORPORATE_TAX",
    "\uad00\uacc4\uae30\uc5c5\uc190\uc775": "AFFILIATE_INCOME",
    "\uae08\uc735\uc190\uc775": "FINANCIAL_INCOME",
    "\uae30\ud0c0\uc601\uc5c5\uc678\uc190\uc775": "NON_OPERATING_INCOME",
    "\ube44\uc9c0\ubc30\uc21c\uc774\uc775": "NON_CONTROLLING_PROFIT",
    "\uac10\uac00\uc0c1\uac01\ube44": "DEPRECIATION_EXPENSE",
    "\uac10\uac00\uc0c1\uac01\ube44\uc728": "DEPRECIATION_RATIO",
    "\ub9e4\ucd9c\uc561\uc99d\uac00\uc728": "REVENUE_GROWTH_RATE",
    "\ub9e4\ucd9c\uc561 \uc99d\uac00\uc728(%)": "REVENUE_GROWTH_RATE",
    "\ud310\uad00\ube44\uc99d\uac00\uc728": "SGA_GROWTH_RATE",
    "\uc601\uc5c5\uc774\uc775\uc99d\uac00\uc728": "OPERATING_INCOME_GROWTH_RATE",
    "\uc601\uc5c5\uc774\uc775 \uc99d\uac00\uc728(%)": "OPERATING_INCOME_GROWTH_RATE",
    "\uc124\ube44\ud22c\uc790": "CAPEX",
    "\uc124\ube44\ud22c\uc790\uc99d\uac00\uc728(%)": "CAPEX_GROWTH_RATE",
    "\ud22c\uc790\uc790\uc0b0": "INVESTMENT_ASSETS",
    "\ud22c\ud558\uc790\ubcf8": "INVESTED_CAPITAL",
    "fcf": "FREE_CASH_FLOW",
    "fcf\uc99d\uac00\uc728(%)": "FCF_GROWTH_RATE",
    "\ucd1d\uc790\uc0b0": "TOTAL_ASSETS",
    "\uc790\uc0b0\uc99d\uac00\uc728(%)": "ASSET_GROWTH_RATE",
    "\uc790\ubcf8\ucd1d\uacc4": "TOTAL_EQUITY",
    "\uc790\ubcf8\uc99d\uac00\uc728(%)": "EQUITY_GROWTH_RATE",
    "\ubd80\ucc44\ucd1d\uacc4": "TOTAL_LIABILITIES",
    "eps": "EPS",
    "eps\uc99d\uac00\uc728(%)": "EPS_GROWTH_RATE",
    "bps": "BPS",
    "bps\uc99d\uac00\uc728(%)": "BPS_GROWTH_RATE",
    "per": "PER",
    "pbr": "PBR",
    "roe": "ROE",
    "roe\uc99d\uac00\uc728(%)": "ROE_GROWTH_RATE",
    "\uc9c0\ubc30\uc8fc\uc8fcroe": "SHAREHOLDER_ROE",
    "roa": "ROA",
    "roa\uc99d\uac00\uc728(%)": "ROA_GROWTH_RATE",
    "npm": "NET_MARGIN",
    "npm(%)": "NET_MARGIN",
    "npm\uc99d\uac00\uc728(%)": "NPM_GROWTH_RATE",
    "opm": "OPERATING_MARGIN",
    "opm(%)": "OPERATING_MARGIN",
    "opm\uc99d\uac00\uc728(%)": "OPM_GROWTH_RATE",
    "gpm": "GROSS_MARGIN",
    "\ud310\uad00\ube44\uc728": "SGA_RATIO",
    "\uc5f0\uad6c\ube44\uc728": "RND_RATIO",
    "\ucc28\uc785\ub960(%)": "BORROWING_RATIO",
    "\uc601\uc5c5\uc774\uc775/\ucc28\uc785\uae08(%)": "OPERATING_INCOME_TO_BORROWINGS_RATIO",
    "\uc601\uc5c5\ud604\uae08\uc99d\uac00\uc728(%)": "OPERATING_CASHFLOW_GROWTH_RATE",
    "\uc601\uc5c5\uc774\uc775\ub960": "OPERATING_MARGIN",
    "\uc601\uc5c5\uc774\uc775\ub960(%)": "OPERATING_MARGIN",
    "\ubd80\ucc44\ube44\uc728": "DEBT_RATIO",
    "\ubd80\ucc44\ube44\uc728(%)": "DEBT_RATIO",
    "\uc720\ub3d9\ube44\uc728": "CURRENT_RATIO",
    "\uc720\ub3d9\ube44\uc728(%)": "CURRENT_RATIO",
    "\ub9e4\ucd9c\ucd1d\uc774\uc775\ub960": "GROSS_MARGIN",
    "\ub9e4\ucd9c\ucd1d\uc774\uc775\ub960(%)": "GROSS_MARGIN",
    "\uc2dc\uac00\ucd1d\uc561": "MARKET_CAP",
    "\uc2dc\uac00\ucd1d\uc561(\uc5b5)": "MARKET_CAP",
    "\uc885\uac00": "CLOSE_PRICE",
    "\uc2dc\uac00": "OPEN_PRICE",
    "\uace0\uac00": "HIGH_PRICE",
    "\uc800\uac00": "LOW_PRICE",
}


def collapse_spaces(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def strip_cosmetic_symbol_prefixes(raw_metric_name: str) -> str:
    text = collapse_spaces(raw_metric_name)

    while text:
        if text[0] not in "-+=":
            break
        text = collapse_spaces(text[1:])

    return text


def extract_metric_variant(raw_metric_name: str) -> tuple[str | None, str]:
    text = strip_cosmetic_symbol_prefixes(raw_metric_name)
    variants: list[str] = []

    while text:
        matched = False
        for pattern, variant_fn in PREFIX_PATTERNS:
            match = pattern.match(text)
            if not match:
                continue
            variants.append(variant_fn(match))
            text = collapse_spaces(text[match.end():])
            matched = True
            break
        if not matched:
            break

    metric_variant = "|".join(variants) if variants else None
    return metric_variant, text


def normalize_metric_key(raw_metric_name: str) -> tuple[str, str | None]:
    metric_variant, stripped_name = extract_metric_variant(raw_metric_name)
    normalized_metric_key = collapse_spaces(stripped_name).casefold()
    return normalized_metric_key, metric_variant


def default_metric_alias_rows() -> list[dict]:
    return [
        {
            "normalized_metric_key": normalized_metric_key,
            "standard_metric_name": standard_metric_name,
            "is_active": 1,
        }
        for normalized_metric_key, standard_metric_name in DEFAULT_ALIAS_MAP.items()
    ]
