from __future__ import annotations

from pathlib import Path
import re

from sqlalchemy import text

from python.etl.metric_mapping import DEFAULT_ALIAS_MAP, normalize_metric_key


STANDARD_METRIC_MASTER_SCHEMA_SQL_PATH = (
    Path(__file__).resolve().parents[2] / "sql" / "006_create_standard_metric_master_tables.sql"
)


STANDARD_METRIC_SEED_ROWS = [
    {"standard_metric_name": "REVENUE", "metric_family": "INCOME_STATEMENT", "description": "Revenue or sales"},
    {"standard_metric_name": "COST_OF_SALES", "metric_family": "INCOME_STATEMENT", "description": "Cost of sales"},
    {"standard_metric_name": "GROSS_PROFIT", "metric_family": "INCOME_STATEMENT", "description": "Gross profit"},
    {"standard_metric_name": "OPERATING_INCOME", "metric_family": "INCOME_STATEMENT", "description": "Operating income"},
    {"standard_metric_name": "SGA_EXPENSE", "metric_family": "INCOME_STATEMENT", "description": "Selling, general and administrative expense"},
    {"standard_metric_name": "NET_INCOME", "metric_family": "INCOME_STATEMENT", "description": "Net income"},
    {"standard_metric_name": "CONTROLLING_NET_INCOME", "metric_family": "INCOME_STATEMENT", "description": "Controlling shareholder net income"},
    {"standard_metric_name": "NON_CONTROLLING_PROFIT", "metric_family": "INCOME_STATEMENT", "description": "Non-controlling interest profit"},
    {"standard_metric_name": "PRE_TAX_CONTINUING_INCOME", "metric_family": "INCOME_STATEMENT", "description": "Pre-tax continuing income"},
    {"standard_metric_name": "PRE_TAX_CONTINUING_MARGIN", "metric_family": "MARGIN_RATIO", "description": "Pre-tax continuing margin"},
    {"standard_metric_name": "PRE_TAX_INCOME", "metric_family": "INCOME_STATEMENT", "description": "Pre-tax income"},
    {"standard_metric_name": "CORPORATE_TAX", "metric_family": "INCOME_STATEMENT", "description": "Corporate tax"},
    {"standard_metric_name": "AFFILIATE_INCOME", "metric_family": "INCOME_STATEMENT", "description": "Affiliate income"},
    {"standard_metric_name": "FINANCIAL_INCOME", "metric_family": "INCOME_STATEMENT", "description": "Financial income"},
    {"standard_metric_name": "NON_OPERATING_INCOME", "metric_family": "INCOME_STATEMENT", "description": "Non-operating income"},
    {"standard_metric_name": "OPERATING_CASH_FLOW", "metric_family": "CASH_FLOW", "description": "Operating cash flow"},
    {"standard_metric_name": "INVESTING_CASH_FLOW", "metric_family": "CASH_FLOW", "description": "Investing cash flow"},
    {"standard_metric_name": "FINANCING_CASH_FLOW", "metric_family": "CASH_FLOW", "description": "Financing cash flow"},
    {"standard_metric_name": "FREE_CASH_FLOW", "metric_family": "CASH_FLOW", "description": "Free cash flow"},
    {"standard_metric_name": "TOTAL_ASSETS", "metric_family": "BALANCE_SHEET", "description": "Total assets"},
    {"standard_metric_name": "TOTAL_LIABILITIES", "metric_family": "BALANCE_SHEET", "description": "Total liabilities"},
    {"standard_metric_name": "TOTAL_EQUITY", "metric_family": "BALANCE_SHEET", "description": "Total equity"},
    {"standard_metric_name": "CURRENT_ASSETS", "metric_family": "BALANCE_SHEET", "description": "Current assets"},
    {"standard_metric_name": "CURRENT_LIABILITIES", "metric_family": "BALANCE_SHEET", "description": "Current liabilities"},
    {"standard_metric_name": "NON_CURRENT_ASSETS", "metric_family": "BALANCE_SHEET", "description": "Non-current assets"},
    {"standard_metric_name": "NON_CURRENT_LIABILITIES", "metric_family": "BALANCE_SHEET", "description": "Non-current liabilities"},
    {"standard_metric_name": "CASH_EQUIVALENTS", "metric_family": "BALANCE_SHEET", "description": "Cash equivalents"},
    {"standard_metric_name": "INVENTORIES", "metric_family": "BALANCE_SHEET", "description": "Inventories"},
    {"standard_metric_name": "INTANGIBLE_ASSETS", "metric_family": "BALANCE_SHEET", "description": "Intangible assets"},
    {"standard_metric_name": "PROPERTY_PLANT_EQUIPMENT", "metric_family": "BALANCE_SHEET", "description": "Property, plant and equipment"},
    {"standard_metric_name": "RETAINED_EARNINGS", "metric_family": "BALANCE_SHEET", "description": "Retained earnings"},
    {"standard_metric_name": "ACCOUNTS_RECEIVABLE", "metric_family": "BALANCE_SHEET", "description": "Accounts receivable"},
    {"standard_metric_name": "ACCOUNTS_PAYABLE", "metric_family": "BALANCE_SHEET", "description": "Accounts payable"},
    {"standard_metric_name": "WORKING_CAPITAL", "metric_family": "BALANCE_SHEET", "description": "Working capital"},
    {"standard_metric_name": "BORROWINGS", "metric_family": "BALANCE_SHEET", "description": "Borrowings"},
    {"standard_metric_name": "NET_DEBT", "metric_family": "BALANCE_SHEET", "description": "Net debt"},
    {"standard_metric_name": "CONTROLLING_EQUITY", "metric_family": "BALANCE_SHEET", "description": "Controlling equity"},
    {"standard_metric_name": "INVESTMENT_ASSETS", "metric_family": "BALANCE_SHEET", "description": "Investment assets"},
    {"standard_metric_name": "INVESTED_CAPITAL", "metric_family": "BALANCE_SHEET", "description": "Invested capital"},
    {"standard_metric_name": "CAPEX", "metric_family": "CASH_FLOW", "description": "Capital expenditure"},
    {"standard_metric_name": "DEPRECIATION_EXPENSE", "metric_family": "CASH_FLOW", "description": "Depreciation expense"},
    {"standard_metric_name": "OPERATING_MARGIN", "metric_family": "MARGIN_RATIO", "description": "Operating margin"},
    {"standard_metric_name": "GROSS_MARGIN", "metric_family": "MARGIN_RATIO", "description": "Gross margin"},
    {"standard_metric_name": "NET_MARGIN", "metric_family": "MARGIN_RATIO", "description": "Net margin"},
    {"standard_metric_name": "DEBT_RATIO", "metric_family": "BALANCE_RATIO", "description": "Debt ratio"},
    {"standard_metric_name": "CURRENT_RATIO", "metric_family": "BALANCE_RATIO", "description": "Current ratio"},
    {"standard_metric_name": "QUICK_RATIO", "metric_family": "BALANCE_RATIO", "description": "Quick ratio"},
    {"standard_metric_name": "DEPRECIATION_RATIO", "metric_family": "BALANCE_RATIO", "description": "Depreciation ratio"},
    {"standard_metric_name": "SGA_RATIO", "metric_family": "BALANCE_RATIO", "description": "SGA ratio"},
    {"standard_metric_name": "RND_RATIO", "metric_family": "BALANCE_RATIO", "description": "R&D ratio"},
    {"standard_metric_name": "BORROWING_RATIO", "metric_family": "BALANCE_RATIO", "description": "Borrowing ratio"},
    {"standard_metric_name": "OPERATING_INCOME_TO_BORROWINGS_RATIO", "metric_family": "BALANCE_RATIO", "description": "Operating income to borrowings ratio"},
    {"standard_metric_name": "EPS", "metric_family": "PER_SHARE", "description": "Earnings per share"},
    {"standard_metric_name": "BPS", "metric_family": "PER_SHARE", "description": "Book value per share"},
    {"standard_metric_name": "PER", "metric_family": "MARKET_RATIO", "description": "Price earnings ratio"},
    {"standard_metric_name": "PBR", "metric_family": "MARKET_RATIO", "description": "Price book ratio"},
    {"standard_metric_name": "ROE", "metric_family": "RETURN_RATIO", "description": "Return on equity"},
    {"standard_metric_name": "ROA", "metric_family": "RETURN_RATIO", "description": "Return on assets"},
    {"standard_metric_name": "SHAREHOLDER_ROE", "metric_family": "RETURN_RATIO", "description": "Shareholder ROE"},
    {"standard_metric_name": "MARKET_CAP", "metric_family": "MARKET_PRICE", "description": "Market capitalization"},
    {"standard_metric_name": "OPEN_PRICE", "metric_family": "MARKET_PRICE", "description": "Open price"},
    {"standard_metric_name": "HIGH_PRICE", "metric_family": "MARKET_PRICE", "description": "High price"},
    {"standard_metric_name": "LOW_PRICE", "metric_family": "MARKET_PRICE", "description": "Low price"},
    {"standard_metric_name": "CLOSE_PRICE", "metric_family": "MARKET_PRICE", "description": "Close price"},
    {"standard_metric_name": "REVENUE_GROWTH_RATE", "metric_family": "GROWTH_RATE", "description": "Revenue growth rate"},
    {"standard_metric_name": "SGA_GROWTH_RATE", "metric_family": "GROWTH_RATE", "description": "SGA growth rate"},
    {"standard_metric_name": "OPERATING_INCOME_GROWTH_RATE", "metric_family": "GROWTH_RATE", "description": "Operating income growth rate"},
    {"standard_metric_name": "NET_INCOME_GROWTH_RATE", "metric_family": "GROWTH_RATE", "description": "Net income growth rate"},
    {"standard_metric_name": "BPS_GROWTH_RATE", "metric_family": "GROWTH_RATE", "description": "BPS growth rate"},
    {"standard_metric_name": "EPS_GROWTH_RATE", "metric_family": "GROWTH_RATE", "description": "EPS growth rate"},
    {"standard_metric_name": "FCF_GROWTH_RATE", "metric_family": "GROWTH_RATE", "description": "FCF growth rate"},
    {"standard_metric_name": "NPM_GROWTH_RATE", "metric_family": "GROWTH_RATE", "description": "Net margin growth rate"},
    {"standard_metric_name": "OPM_GROWTH_RATE", "metric_family": "GROWTH_RATE", "description": "Operating margin growth rate"},
    {"standard_metric_name": "ROA_GROWTH_RATE", "metric_family": "GROWTH_RATE", "description": "ROA growth rate"},
    {"standard_metric_name": "ROE_GROWTH_RATE", "metric_family": "GROWTH_RATE", "description": "ROE growth rate"},
    {"standard_metric_name": "CAPEX_GROWTH_RATE", "metric_family": "GROWTH_RATE", "description": "CAPEX growth rate"},
    {"standard_metric_name": "OPERATING_CASHFLOW_GROWTH_RATE", "metric_family": "GROWTH_RATE", "description": "Operating cash flow growth rate"},
    {"standard_metric_name": "EQUITY_GROWTH_RATE", "metric_family": "GROWTH_RATE", "description": "Equity growth rate"},
    {"standard_metric_name": "ASSET_GROWTH_RATE", "metric_family": "GROWTH_RATE", "description": "Asset growth rate"},
]


HIGH_CONFIDENCE_ALIAS_GROUPS = {
    "REVENUE": ["매출", "revenue", "sales"],
    "OPERATING_INCOME": ["operating income", "operatingincome", "operating profit", "operatingprofit"],
    "NET_INCOME": ["net income", "netincome", "net profit", "netprofit"],
    "TOTAL_ASSETS": ["total assets", "totalassets"],
    "TOTAL_LIABILITIES": ["total liabilities", "totalliabilities"],
    "TOTAL_EQUITY": ["total equity", "totalequity"],
    "EPS": ["earnings per share", "earningspershare"],
    "BPS": ["book value per share", "bookvaluepershare"],
    "ROE": ["return on equity", "returnonequity"],
    "ROA": ["return on assets", "returnonassets"],
    "MARKET_CAP": ["market cap", "marketcap", "market capitalization", "marketcapitalization"],
    "OPEN_PRICE": ["open price", "openprice"],
    "HIGH_PRICE": ["high price", "highprice"],
    "LOW_PRICE": ["low price", "lowprice"],
    "CLOSE_PRICE": ["close price", "closeprice"],
    "REVENUE_GROWTH_RATE": ["revenue growth", "revenuegrowth", "sales growth", "salesgrowth"],
    "OPERATING_INCOME_GROWTH_RATE": ["operating income growth", "operatingincomegrowth"],
    "NET_INCOME_GROWTH_RATE": ["net income growth", "netincomegrowth"],
}


DEFERRED_FAMILY_PATTERNS = [
    ("turnover_days_family", ["회전일수"]),
    ("dividend_family", ["배당", "dps"]),
    ("five_year_average_family", ["5년평균"]),
    ("valuation_price_family", ["ev/ebitda", "pcr", "peg", "por", "prr", "psr", "roic", "주가"]),
    ("supplementary_per_share_family", ["cps", "ops", "sps"]),
    ("score_meta_family", ["점수", "업종", "코드번호", "회사명", "yoy"]),
]


def execute_standard_metric_master_schema(engine) -> None:
    script = STANDARD_METRIC_MASTER_SCHEMA_SQL_PATH.read_text(encoding="utf-8")
    statements = [statement.strip() for statement in script.split(";") if statement.strip()]
    with engine.begin() as connection:
        for statement in statements:
            connection.exec_driver_sql(statement)


def ensure_standard_metric_runtime_columns(engine) -> None:
    required_columns = {
        "metric_alias_map": {
            "standard_metric_id": "ALTER TABLE metric_alias_map ADD COLUMN standard_metric_id INTEGER",
        },
        "integrated_observation_enriched": {
            "standard_metric_id": "ALTER TABLE integrated_observation_enriched ADD COLUMN standard_metric_id INTEGER",
        },
    }

    with engine.begin() as connection:
        for table_name, column_ddls in required_columns.items():
            table_exists = connection.execute(
                text(
                    """
                    SELECT COUNT(*)
                    FROM sqlite_master
                    WHERE type = 'table'
                      AND name = :table_name
                    """
                ),
                {"table_name": table_name},
            ).scalar_one()
            if not table_exists:
                continue

            existing_columns = {
                row[1] for row in connection.exec_driver_sql(f"PRAGMA table_info({table_name})")
            }
            for column_name, ddl in column_ddls.items():
                if column_name not in existing_columns:
                    connection.exec_driver_sql(ddl)

        metric_alias_map_exists = connection.execute(
            text(
                """
                SELECT COUNT(*)
                FROM sqlite_master
                WHERE type = 'table'
                  AND name = 'metric_alias_map'
                """
            )
        ).scalar_one()
        if metric_alias_map_exists:
            connection.exec_driver_sql(
                "CREATE INDEX IF NOT EXISTS idx_metric_alias_map_standard_metric_id ON metric_alias_map (standard_metric_id)"
            )

        enriched_exists = connection.execute(
            text(
                """
                SELECT COUNT(*)
                FROM sqlite_master
                WHERE type = 'table'
                  AND name = 'integrated_observation_enriched'
                """
            )
        ).scalar_one()
        if enriched_exists:
            connection.exec_driver_sql(
                "CREATE INDEX IF NOT EXISTS idx_integrated_enriched_standard_metric_id ON integrated_observation_enriched (standard_metric_id)"
            )


def upsert_standard_metric_seed_rows(connection) -> dict[str, int]:
    for row in STANDARD_METRIC_SEED_ROWS:
        connection.execute(
            text(
                """
                INSERT INTO standard_metric (
                    standard_metric_name,
                    metric_family,
                    description,
                    active_flag
                ) VALUES (
                    :standard_metric_name,
                    :metric_family,
                    :description,
                    1
                )
                ON CONFLICT(standard_metric_name) DO UPDATE SET
                    metric_family = excluded.metric_family,
                    description = excluded.description,
                    active_flag = 1,
                    updated_at = CURRENT_TIMESTAMP
                """
            ),
            row,
        )

    rows = connection.execute(
        text(
            """
            SELECT standard_metric_id, standard_metric_name
            FROM standard_metric
            """
        )
    ).fetchall()
    return {row.standard_metric_name: row.standard_metric_id for row in rows}


def _build_seed_alias_entries() -> list[tuple[str, str, str, float]]:
    seed_entries: list[tuple[str, str, str, float]] = []

    for alias_text, standard_metric_name in DEFAULT_ALIAS_MAP.items():
        seed_entries.append((alias_text, standard_metric_name, "curated_exact_alias", 1.0))

    for standard_metric_name, aliases in HIGH_CONFIDENCE_ALIAS_GROUPS.items():
        for alias_text in aliases:
            seed_entries.append((alias_text, standard_metric_name, "seed_high_confidence_alias", 0.95))

    return seed_entries


def build_metric_name_mapping_seed_rows(standard_metric_lookup: dict[str, int]) -> list[dict]:
    deduped_rows: dict[str, dict] = {}

    for alias_text, standard_metric_name, mapping_rule, mapping_confidence in _build_seed_alias_entries():
        normalized_metric_key, _ = normalize_metric_key(alias_text)
        if not normalized_metric_key:
            continue

        existing = deduped_rows.get(normalized_metric_key)
        candidate_row = {
            "normalized_metric_key": normalized_metric_key,
            "raw_metric_name_example": alias_text,
            "standard_metric_id": standard_metric_lookup[standard_metric_name],
            "standard_metric_name": standard_metric_name,
            "mapping_rule": mapping_rule,
            "mapping_confidence": mapping_confidence,
            "is_active": 1,
        }

        if existing is None:
            deduped_rows[normalized_metric_key] = candidate_row
            continue

        if existing["mapping_confidence"] < candidate_row["mapping_confidence"]:
            deduped_rows[normalized_metric_key] = candidate_row
            continue

        if (
            existing["mapping_confidence"] == candidate_row["mapping_confidence"]
            and existing["mapping_rule"] != "curated_exact_alias"
            and candidate_row["mapping_rule"] == "curated_exact_alias"
        ):
            deduped_rows[normalized_metric_key] = candidate_row

    return sorted(deduped_rows.values(), key=lambda row: row["normalized_metric_key"])


def reseed_metric_name_mapping(connection, standard_metric_lookup: dict[str, int]) -> list[dict]:
    seed_rows = build_metric_name_mapping_seed_rows(standard_metric_lookup)
    connection.execute(text("DELETE FROM metric_name_mapping"))
    if seed_rows:
        connection.execute(
            text(
                """
                INSERT INTO metric_name_mapping (
                    normalized_metric_key,
                    raw_metric_name_example,
                    standard_metric_id,
                    standard_metric_name,
                    mapping_rule,
                    mapping_confidence,
                    is_active
                ) VALUES (
                    :normalized_metric_key,
                    :raw_metric_name_example,
                    :standard_metric_id,
                    :standard_metric_name,
                    :mapping_rule,
                    :mapping_confidence,
                    :is_active
                )
                """
            ),
            seed_rows,
        )
    return seed_rows


def sync_metric_alias_map(connection) -> int:
    mapping_rows = connection.execute(
        text(
            """
            SELECT
                normalized_metric_key,
                standard_metric_id,
                standard_metric_name,
                is_active
            FROM metric_name_mapping
            WHERE is_active = 1
            """
        )
    ).mappings().all()

    connection.execute(text("DELETE FROM metric_alias_map"))
    if mapping_rows:
        connection.execute(
            text(
                """
                INSERT INTO metric_alias_map (
                    normalized_metric_key,
                    standard_metric_id,
                    standard_metric_name,
                    is_active
                ) VALUES (
                    :normalized_metric_key,
                    :standard_metric_id,
                    :standard_metric_name,
                    :is_active
                )
                """
            ),
            [dict(row) for row in mapping_rows],
        )
    return len(mapping_rows)


def fetch_metric_name_mapping_lookup(connection) -> dict[str, dict]:
    rows = connection.execute(
        text(
            """
            SELECT
                normalized_metric_key,
                standard_metric_id,
                standard_metric_name,
                mapping_rule,
                mapping_confidence
            FROM metric_name_mapping
            WHERE is_active = 1
            """
        )
    ).mappings().all()
    return {row["normalized_metric_key"]: dict(row) for row in rows}


def canonical_metric_candidate_text(raw_metric_name: str) -> str:
    normalized_metric_key, _ = normalize_metric_key(raw_metric_name)
    text = normalized_metric_key.casefold()
    text = re.sub(r"[\s\(\)\[\]\{\}\-_=+%/.,]", "", text)
    return text


def suggest_standard_metric_candidates(raw_metric_name: str) -> list[str]:
    candidate_text = canonical_metric_candidate_text(raw_metric_name)
    if not candidate_text:
        return []

    suggestions: list[str] = []
    for standard_metric_name, aliases in HIGH_CONFIDENCE_ALIAS_GROUPS.items():
        alias_candidates = {canonical_metric_candidate_text(alias_text) for alias_text in aliases}
        if candidate_text in alias_candidates:
            suggestions.append(standard_metric_name)
    return sorted(set(suggestions))


def classify_deferred_metric_family(raw_metric_name: str) -> str | None:
    normalized_metric_key, _ = normalize_metric_key(raw_metric_name)
    text = normalized_metric_key.casefold()
    for family_name, patterns in DEFERRED_FAMILY_PATTERNS:
        if any(pattern.casefold() in text for pattern in patterns):
            return family_name
    return None
