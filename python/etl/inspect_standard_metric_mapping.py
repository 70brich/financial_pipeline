from __future__ import annotations

from sqlalchemy import text

from python.etl.build_integrated_observation import execute_integrated_schema
from python.etl.build_integrated_observation_enriched import execute_metric_mapping_schema
from python.etl.db_runtime import DEFAULT_SQLITE_DB_PATH, create_sqlite_engine, ensure_runtime_schema

NEW_STANDARD_METRICS_V12 = [
    "RETAINED_EARNINGS",
    "QUICK_RATIO",
    "ACCOUNTS_PAYABLE",
    "ACCOUNTS_RECEIVABLE",
    "CURRENT_ASSETS",
    "CURRENT_LIABILITIES",
    "NON_CURRENT_ASSETS",
    "NON_CURRENT_LIABILITIES",
    "INTANGIBLE_ASSETS",
    "PROPERTY_PLANT_EQUIPMENT",
    "INVENTORIES",
    "CASH_EQUIVALENTS",
    "WORKING_CAPITAL",
    "BORROWINGS",
    "NET_DEBT",
    "CONTROLLING_EQUITY",
]

NEW_STANDARD_METRICS_V13 = [
    "PRE_TAX_CONTINUING_INCOME",
    "PRE_TAX_CONTINUING_MARGIN",
    "SHAREHOLDER_ROE",
    "NET_MARGIN",
]

NEW_STANDARD_METRICS_V14 = [
    "PRE_TAX_INCOME",
    "CORPORATE_TAX",
    "AFFILIATE_INCOME",
    "FINANCIAL_INCOME",
    "NON_OPERATING_INCOME",
]

NEW_STANDARD_METRICS_V15 = [
    "NON_CONTROLLING_PROFIT",
    "DEPRECIATION_EXPENSE",
    "CAPEX",
    "INVESTMENT_ASSETS",
    "INVESTED_CAPITAL",
]

NEW_STANDARD_METRICS_V16 = [
    "DEPRECIATION_RATIO",
    "SGA_RATIO",
    "RND_RATIO",
    "BORROWING_RATIO",
    "OPERATING_INCOME_TO_BORROWINGS_RATIO",
]

NEW_STANDARD_METRICS_V17 = [
    "REVENUE_GROWTH_RATE",
    "SGA_GROWTH_RATE",
    "OPERATING_INCOME_GROWTH_RATE",
    "NET_INCOME_GROWTH_RATE",
    "BPS_GROWTH_RATE",
    "EPS_GROWTH_RATE",
    "FCF_GROWTH_RATE",
    "NPM_GROWTH_RATE",
    "OPM_GROWTH_RATE",
    "ROA_GROWTH_RATE",
    "ROE_GROWTH_RATE",
    "CAPEX_GROWTH_RATE",
    "OPERATING_CASHFLOW_GROWTH_RATE",
    "EQUITY_GROWTH_RATE",
    "ASSET_GROWTH_RATE",
]

UNMAPPED_POLICY_BUCKET_PATTERNS = [
    ("growth_rate_family", ["증가율"]),
    ("turnover_days_family", ["회전일수"]),
    ("five_year_average_family", ["5년평균"]),
    ("pre_tax_continuing_family", ["세전계속사업"]),
    ("shareholder_return_family", ["지배주주roe"]),
    ("net_margin_family", ["npm"]),
    ("estimate_period_label_family", ["q(e)", "(e)"]),
    ("score_meta_family", ["점수", "yoy", "코드번호", "회사명", "업종"]),
    ("dividend_family", ["배당"]),
]


def print_section(title: str) -> None:
    print()
    print(f"=== {title} ===")


def escape_text(value) -> str:
    if value is None:
        return "None"
    return str(value).encode("unicode_escape").decode("ascii")


def summarize_unmapped_policy_buckets(unmapped_rows) -> list[tuple[str, int, int]]:
    summaries: list[tuple[str, int, int]] = []
    remaining_rows = []

    for bucket_name, patterns in UNMAPPED_POLICY_BUCKET_PATTERNS:
        matched_rows = []
        for row in unmapped_rows:
            normalized_metric_key = str(row.normalized_metric_key or "")
            if any(pattern in normalized_metric_key for pattern in patterns):
                matched_rows.append(row)

        if matched_rows:
            summaries.append(
                (
                    bucket_name,
                    sum(int(row.row_count or 0) for row in matched_rows),
                    len(matched_rows),
                )
            )

    return summaries


def main() -> None:
    engine = create_sqlite_engine()
    ensure_runtime_schema(engine)
    execute_integrated_schema(engine)
    execute_metric_mapping_schema(engine)

    with engine.begin() as connection:
        coverage = connection.execute(
            text(
                """
                SELECT
                    (SELECT COUNT(*) FROM standard_metric) AS total_standard_metric_rows,
                    (SELECT COUNT(*) FROM metric_name_mapping WHERE is_active = 1) AS active_metric_name_mapping_rows,
                    COUNT(DISTINCT raw_metric_name) AS total_distinct_raw_metric_name,
                    COUNT(DISTINCT CASE WHEN standard_metric_name IS NOT NULL THEN raw_metric_name END) AS mapped_distinct_raw_metric_name,
                    COUNT(DISTINCT CASE WHEN standard_metric_name IS NULL THEN raw_metric_name END) AS unmapped_distinct_raw_metric_name,
                    COUNT(*) AS total_enriched_rows,
                    SUM(CASE WHEN standard_metric_name IS NOT NULL THEN 1 ELSE 0 END) AS mapped_enriched_rows,
                    SUM(CASE WHEN standard_metric_name IS NULL THEN 1 ELSE 0 END) AS unmapped_enriched_rows,
                    SUM(CASE WHEN standard_metric_id IS NOT NULL THEN 1 ELSE 0 END) AS linked_standard_metric_rows
                FROM integrated_observation_enriched
                """
            )
        ).one()

        standard_counts = connection.execute(
            text(
                """
                SELECT standard_metric_name, COUNT(*) AS row_count
                FROM integrated_observation_enriched
                WHERE standard_metric_name IS NOT NULL
                GROUP BY standard_metric_name
                ORDER BY row_count DESC, standard_metric_name
                LIMIT 30
                """
            )
        ).fetchall()

        new_standard_counts = connection.execute(
            text(
                """
                SELECT standard_metric_name, COUNT(*) AS row_count
                FROM integrated_observation_enriched
                WHERE standard_metric_name IN (
                    'RETAINED_EARNINGS',
                    'QUICK_RATIO',
                    'ACCOUNTS_PAYABLE',
                    'ACCOUNTS_RECEIVABLE',
                    'CURRENT_ASSETS',
                    'CURRENT_LIABILITIES',
                    'NON_CURRENT_ASSETS',
                    'NON_CURRENT_LIABILITIES',
                    'INTANGIBLE_ASSETS',
                    'PROPERTY_PLANT_EQUIPMENT',
                    'INVENTORIES',
                    'CASH_EQUIVALENTS',
                    'WORKING_CAPITAL',
                    'BORROWINGS',
                    'NET_DEBT',
                    'CONTROLLING_EQUITY'
                )
                GROUP BY standard_metric_name
                ORDER BY row_count DESC, standard_metric_name
                """
            )
        ).fetchall()

        choice2_standard_counts = connection.execute(
            text(
                """
                SELECT standard_metric_name, COUNT(*) AS row_count
                FROM integrated_observation_enriched
                WHERE standard_metric_name IN (
                    'PRE_TAX_CONTINUING_INCOME',
                    'PRE_TAX_CONTINUING_MARGIN',
                    'SHAREHOLDER_ROE',
                    'NET_MARGIN'
                )
                GROUP BY standard_metric_name
                ORDER BY row_count DESC, standard_metric_name
                """
            )
        ).fetchall()

        choice2_income_component_counts = connection.execute(
            text(
                """
                SELECT standard_metric_name, COUNT(*) AS row_count
                FROM integrated_observation_enriched
                WHERE standard_metric_name IN (
                    'PRE_TAX_INCOME',
                    'CORPORATE_TAX',
                    'AFFILIATE_INCOME',
                    'FINANCIAL_INCOME',
                    'NON_OPERATING_INCOME'
                )
                GROUP BY standard_metric_name
                ORDER BY row_count DESC, standard_metric_name
                """
            )
        ).fetchall()

        choice2_income_component_alias_map_rows = connection.execute(
            text(
                """
                SELECT normalized_metric_key, standard_metric_name
                FROM metric_alias_map
                WHERE is_active = 1
                  AND standard_metric_name IN (
                    'PRE_TAX_INCOME',
                    'CORPORATE_TAX',
                    'AFFILIATE_INCOME',
                    'FINANCIAL_INCOME',
                    'NON_OPERATING_INCOME'
                  )
                ORDER BY standard_metric_name, normalized_metric_key
                """
            )
        ).fetchall()

        choice2_accounting_investment_counts = connection.execute(
            text(
                """
                SELECT standard_metric_name, COUNT(*) AS row_count
                FROM integrated_observation_enriched
                WHERE standard_metric_name IN (
                    'NON_CONTROLLING_PROFIT',
                    'DEPRECIATION_EXPENSE',
                    'CAPEX',
                    'INVESTMENT_ASSETS',
                    'INVESTED_CAPITAL'
                )
                GROUP BY standard_metric_name
                ORDER BY row_count DESC, standard_metric_name
                """
            )
        ).fetchall()

        choice2_ratio_counts = connection.execute(
            text(
                """
                SELECT standard_metric_name, COUNT(*) AS row_count
                FROM integrated_observation_enriched
                WHERE standard_metric_name IN (
                    'DEPRECIATION_RATIO',
                    'SGA_RATIO',
                    'RND_RATIO',
                    'BORROWING_RATIO',
                    'OPERATING_INCOME_TO_BORROWINGS_RATIO'
                )
                GROUP BY standard_metric_name
                ORDER BY row_count DESC, standard_metric_name
                """
            )
        ).fetchall()

        choice2_growth_rate_counts = connection.execute(
            text(
                """
                SELECT standard_metric_name, COUNT(*) AS row_count
                FROM integrated_observation_enriched
                WHERE standard_metric_name IN (
                    'REVENUE_GROWTH_RATE',
                    'SGA_GROWTH_RATE',
                    'OPERATING_INCOME_GROWTH_RATE',
                    'NET_INCOME_GROWTH_RATE',
                    'BPS_GROWTH_RATE',
                    'EPS_GROWTH_RATE',
                    'FCF_GROWTH_RATE',
                    'NPM_GROWTH_RATE',
                    'OPM_GROWTH_RATE',
                    'ROA_GROWTH_RATE',
                    'ROE_GROWTH_RATE',
                    'CAPEX_GROWTH_RATE',
                    'OPERATING_CASHFLOW_GROWTH_RATE',
                    'EQUITY_GROWTH_RATE',
                    'ASSET_GROWTH_RATE'
                )
                GROUP BY standard_metric_name
                ORDER BY row_count DESC, standard_metric_name
                """
            )
        ).fetchall()

        unmapped_rows_with_active_alias = connection.execute(
            text(
                """
                SELECT
                    e.raw_metric_name,
                    e.normalized_metric_key,
                    m.standard_metric_name,
                    COUNT(*) AS row_count
                FROM integrated_observation_enriched e
                JOIN metric_alias_map m
                  ON m.normalized_metric_key = e.normalized_metric_key
                 AND m.is_active = 1
                WHERE e.standard_metric_name IS NULL
                GROUP BY e.raw_metric_name, e.normalized_metric_key, m.standard_metric_name
                ORDER BY row_count DESC, e.raw_metric_name
                LIMIT 50
                """
            )
        ).fetchall()

        unmapped_counts = connection.execute(
            text(
                """
                SELECT raw_metric_name, COUNT(*) AS row_count
                FROM integrated_observation_enriched
                WHERE standard_metric_name IS NULL
                GROUP BY raw_metric_name
                ORDER BY row_count DESC, raw_metric_name
                LIMIT 100
                """
            )
        ).fetchall()

        unmapped_normalized_counts = connection.execute(
            text(
                """
                SELECT
                    normalized_metric_key,
                    COUNT(*) AS row_count,
                    COUNT(DISTINCT raw_metric_name) AS raw_metric_name_count
                FROM integrated_observation_enriched
                WHERE standard_metric_name IS NULL
                GROUP BY normalized_metric_key
                ORDER BY row_count DESC, raw_metric_name_count DESC, normalized_metric_key
                """
            )
        ).fetchall()

        symbol_prefixed_unmapped = connection.execute(
            text(
                """
                SELECT raw_metric_name, normalized_metric_key, COUNT(*) AS row_count
                FROM integrated_observation_enriched
                WHERE standard_metric_name IS NULL
                  AND raw_metric_name GLOB '[-+=]*'
                GROUP BY raw_metric_name, normalized_metric_key
                ORDER BY row_count DESC, raw_metric_name
                LIMIT 50
                """
            )
        ).fetchall()

        alias_samples = connection.execute(
            text(
                """
                SELECT normalized_metric_key, standard_metric_name
                FROM metric_alias_map
                WHERE is_active = 1
                ORDER BY standard_metric_name, normalized_metric_key
                LIMIT 50
                """
            )
        ).fetchall()

        recent_rows = connection.execute(
            text(
                """
                SELECT
                    integrated_observation_enriched_id,
                    integrated_observation_id,
                    company_key,
                    raw_metric_name,
                    normalized_metric_key,
                    standard_metric_id,
                    standard_metric_name,
                    metric_variant,
                    period_type,
                    fiscal_year,
                    fiscal_quarter,
                    date_raw,
                    selected_source_group,
                    selected_raw_observation_id,
                    selected_value_numeric,
                    selected_is_estimate
                FROM integrated_observation_enriched
                ORDER BY integrated_observation_enriched_id DESC
                LIMIT 30
                """
            )
        ).fetchall()

    total_distinct = int(coverage.total_distinct_raw_metric_name or 0)
    mapped_distinct = int(coverage.mapped_distinct_raw_metric_name or 0)
    unmapped_distinct = int(coverage.unmapped_distinct_raw_metric_name or 0)
    coverage_ratio = (mapped_distinct / total_distinct * 100.0) if total_distinct else 0.0
    total_rows = int(coverage.total_enriched_rows or 0)
    mapped_rows = int(coverage.mapped_enriched_rows or 0)
    unmapped_rows = int(coverage.unmapped_enriched_rows or 0)
    row_coverage_ratio = (mapped_rows / total_rows * 100.0) if total_rows else 0.0

    print("Standard metric mapping inspection")
    print(f"Database: {DEFAULT_SQLITE_DB_PATH}")

    print_section("Distinct coverage summary")
    print(f"standard_metric rows: {coverage.total_standard_metric_rows}")
    print(f"active metric_name_mapping rows: {coverage.active_metric_name_mapping_rows}")
    print(f"total distinct raw_metric_name: {total_distinct}")
    print(f"mapped distinct raw_metric_name: {mapped_distinct}")
    print(f"unmapped distinct raw_metric_name: {unmapped_distinct}")
    print(f"coverage ratio: {coverage_ratio:.2f}%")

    print_section("Row-level coverage summary")
    print(f"total enriched rows: {total_rows}")
    print(f"mapped enriched rows: {mapped_rows}")
    print(f"unmapped enriched rows: {unmapped_rows}")
    print(f"rows linked to standard_metric_id: {coverage.linked_standard_metric_rows}")
    print(f"row coverage ratio: {row_coverage_ratio:.2f}%")

    print_section("Top standard_metric_name row counts")
    for row in standard_counts:
        print(f"{row.standard_metric_name}: {row.row_count}")

    print_section("New v1.2 standard_metric_name row counts")
    if new_standard_counts:
        for row in new_standard_counts:
            print(f"{row.standard_metric_name}: {row.row_count}")
    else:
        for standard_metric_name in NEW_STANDARD_METRICS_V12:
            print(f"{standard_metric_name}: 0")

    print_section("Choice 2 standard_metric_name row counts")
    if choice2_standard_counts:
        for row in choice2_standard_counts:
            print(f"{row.standard_metric_name}: {row.row_count}")
    else:
        for standard_metric_name in NEW_STANDARD_METRICS_V13:
            print(f"{standard_metric_name}: 0")

    print_section("Choice 2 income-component row counts")
    choice2_income_component_count_map = {
        row.standard_metric_name: row.row_count for row in choice2_income_component_counts
    }
    for standard_metric_name in NEW_STANDARD_METRICS_V14:
        print(f"{standard_metric_name}: {choice2_income_component_count_map.get(standard_metric_name, 0)}")

    print_section("Choice 2 income-component alias map rows")
    if choice2_income_component_alias_map_rows:
        for row in choice2_income_component_alias_map_rows:
            print(f"{escape_text(row.normalized_metric_key)} -> {row.standard_metric_name}")
    else:
        print("No Choice 2 income-component aliases found in metric_alias_map.")

    print_section("Choice 2 accounting-investment row counts")
    choice2_accounting_investment_count_map = {
        row.standard_metric_name: row.row_count for row in choice2_accounting_investment_counts
    }
    for standard_metric_name in NEW_STANDARD_METRICS_V15:
        print(f"{standard_metric_name}: {choice2_accounting_investment_count_map.get(standard_metric_name, 0)}")

    print_section("Choice 2 ratio row counts")
    choice2_ratio_count_map = {row.standard_metric_name: row.row_count for row in choice2_ratio_counts}
    for standard_metric_name in NEW_STANDARD_METRICS_V16:
        print(f"{standard_metric_name}: {choice2_ratio_count_map.get(standard_metric_name, 0)}")

    print_section("Choice 2 growth-rate row counts")
    choice2_growth_rate_count_map = {
        row.standard_metric_name: row.row_count for row in choice2_growth_rate_counts
    }
    for standard_metric_name in NEW_STANDARD_METRICS_V17:
        print(f"{standard_metric_name}: {choice2_growth_rate_count_map.get(standard_metric_name, 0)}")

    print_section("Top unmapped raw_metric_name")
    for row in unmapped_counts:
        print(f"{row.raw_metric_name}: {row.row_count}")

    print_section("Top unmapped normalized_metric_key")
    for row in unmapped_normalized_counts[:100]:
        print(
            f"{row.normalized_metric_key}: {row.row_count} "
            f"(distinct raw names: {row.raw_metric_name_count})"
        )

    print_section("Symbol-prefixed unmapped samples")
    if symbol_prefixed_unmapped:
        for row in symbol_prefixed_unmapped:
            print(
                f"{row.raw_metric_name} -> normalized={row.normalized_metric_key}: {row.row_count}"
            )
    else:
        print("No symbol-prefixed unmapped rows found.")

    print_section("Escaped unmapped normalized_metric_key samples")
    for row in unmapped_normalized_counts[:30]:
        print(
            f"{escape_text(row.normalized_metric_key)}: {row.row_count} "
            f"(distinct raw names: {row.raw_metric_name_count})"
        )

    print_section("Escaped unmapped raw_metric_name samples")
    for row in unmapped_counts[:30]:
        print(f"{escape_text(row.raw_metric_name)}: {row.row_count}")

    print_section("Escaped symbol-prefixed unmapped samples")
    if symbol_prefixed_unmapped:
        for row in symbol_prefixed_unmapped:
            print(
                f"{escape_text(row.raw_metric_name)} -> "
                f"normalized={escape_text(row.normalized_metric_key)}: {row.row_count}"
            )
    else:
        print("No symbol-prefixed unmapped rows found.")

    print_section("Unmapped rows with active alias present")
    if unmapped_rows_with_active_alias:
        for row in unmapped_rows_with_active_alias:
            print(
                f"{escape_text(row.raw_metric_name)} -> "
                f"normalized={escape_text(row.normalized_metric_key)} -> "
                f"alias={row.standard_metric_name}: {row.row_count}"
            )
    else:
        print("No unmapped rows were found with an active alias in metric_alias_map.")

    print_section("Unmapped policy bucket summary")
    policy_bucket_summaries = summarize_unmapped_policy_buckets(unmapped_normalized_counts)
    if policy_bucket_summaries:
        for bucket_name, row_count, distinct_metric_count in policy_bucket_summaries:
            print(
                f"{bucket_name}: rows={row_count}, distinct normalized metrics={distinct_metric_count}"
            )
    else:
        print("No policy-style unmapped buckets detected.")

    print_section("Alias mapping samples")
    for row in alias_samples:
        print(f"{row.normalized_metric_key} -> {row.standard_metric_name}")

    print_section("Recent enriched rows")
    for row in recent_rows:
        print(
            f"[{row.integrated_observation_enriched_id}] integrated_id={row.integrated_observation_id} | "
            f"company_key={row.company_key} | raw_metric_name={row.raw_metric_name} | "
            f"normalized_metric_key={row.normalized_metric_key} | standard_metric_id={row.standard_metric_id} | "
            f"standard_metric_name={row.standard_metric_name} | "
            f"metric_variant={row.metric_variant} | period_type={row.period_type} | fy={row.fiscal_year} | "
            f"fq={row.fiscal_quarter} | date_raw={row.date_raw} | selected_source_group={row.selected_source_group} | "
            f"selected_raw_observation_id={row.selected_raw_observation_id} | selected_value_numeric={row.selected_value_numeric} | "
            f"selected_is_estimate={row.selected_is_estimate}"
        )


if __name__ == "__main__":
    main()
