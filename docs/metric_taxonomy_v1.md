# Metric taxonomy v1

## Purpose

This document summarizes the current conservative `standard_metric_name`
taxonomy used by `integrated_observation_enriched`.

It represents the Financial Pipeline v1 baseline taxonomy.

See also:

- `docs/data_quality_checklist.md`
  - operational validation checklist for this taxonomy and pipeline
- `docs/current_limitations.md`
  - intentionally deferred metric families

Design rules:

- `raw_metric_name` is always preserved as-is
- `normalized_metric_key` is used only for lookup
- mapping is exact-alias only
- fuzzy or semantic merge is not used
- ambiguous metrics remain unmapped

## Coverage status

Latest user-verified result:

- distinct coverage: `103 / 154 = 66.88%`
- row-level coverage: `2077 / 2432 = 85.40%`
- tests: `23` passed

## Base accounting and operating metrics

- `REVENUE`
- `COST_OF_SALES`
- `GROSS_PROFIT`
- `OPERATING_INCOME`
- `SGA_EXPENSE`
- `NET_INCOME`
- `CONTROLLING_NET_INCOME`
- `NON_CONTROLLING_PROFIT`
- `PRE_TAX_CONTINUING_INCOME`
- `PRE_TAX_CONTINUING_MARGIN`
- `PRE_TAX_INCOME`
- `CORPORATE_TAX`
- `AFFILIATE_INCOME`
- `FINANCIAL_INCOME`
- `NON_OPERATING_INCOME`

## Cash flow metrics

- `OPERATING_CASH_FLOW`
- `INVESTING_CASH_FLOW`
- `FINANCING_CASH_FLOW`
- `FREE_CASH_FLOW`

## Balance sheet and capital metrics

- `TOTAL_ASSETS`
- `TOTAL_LIABILITIES`
- `TOTAL_EQUITY`
- `CURRENT_ASSETS`
- `CURRENT_LIABILITIES`
- `NON_CURRENT_ASSETS`
- `NON_CURRENT_LIABILITIES`
- `CASH_EQUIVALENTS`
- `INVENTORIES`
- `INTANGIBLE_ASSETS`
- `PROPERTY_PLANT_EQUIPMENT`
- `RETAINED_EARNINGS`
- `ACCOUNTS_RECEIVABLE`
- `ACCOUNTS_PAYABLE`
- `WORKING_CAPITAL`
- `BORROWINGS`
- `NET_DEBT`
- `CONTROLLING_EQUITY`
- `INVESTMENT_ASSETS`
- `INVESTED_CAPITAL`
- `CAPEX`
- `DEPRECIATION_EXPENSE`

## Margin and ratio metrics

- `OPERATING_MARGIN`
- `GROSS_MARGIN`
- `NET_MARGIN`
- `DEBT_RATIO`
- `CURRENT_RATIO`
- `QUICK_RATIO`
- `DEPRECIATION_RATIO`
- `SGA_RATIO`
- `RND_RATIO`
- `BORROWING_RATIO`
- `OPERATING_INCOME_TO_BORROWINGS_RATIO`

## Per-share and market metrics currently included

- `EPS`
- `BPS`
- `PER`
- `PBR`
- `ROE`
- `ROA`
- `SHAREHOLDER_ROE`
- `MARKET_CAP`
- `OPEN_PRICE`
- `HIGH_PRICE`
- `LOW_PRICE`
- `CLOSE_PRICE`

## Conservative growth-rate family

These were added only for exact aliases tied to already-approved base metrics.

- `REVENUE_GROWTH_RATE`
- `SGA_GROWTH_RATE`
- `OPERATING_INCOME_GROWTH_RATE`
- `NET_INCOME_GROWTH_RATE`
- `BPS_GROWTH_RATE`
- `EPS_GROWTH_RATE`
- `FCF_GROWTH_RATE`
- `NPM_GROWTH_RATE`
- `OPM_GROWTH_RATE`
- `ROA_GROWTH_RATE`
- `ROE_GROWTH_RATE`
- `CAPEX_GROWTH_RATE`
- `OPERATING_CASHFLOW_GROWTH_RATE`
- `EQUITY_GROWTH_RATE`
- `ASSET_GROWTH_RATE`

Note:

- A name may exist in the taxonomy even if current data has `0` rows for it.
- Example: `NET_INCOME_GROWTH_RATE` is defined, but no current exact alias is
  mapped into it in the latest run.

## Explicitly deferred families

These remain intentionally unmapped in v1:

- turnover-day metrics
- dividend metrics
- supplementary per-share metrics such as `CPS`, `DPS`, `OPS`, `SPS`
- valuation / price expansion metrics such as `EV/EBITDA`, `PCR`, `PEG`,
  `POR`, `PRR`, `PSR`, `ROIC`, `주가`
- score / meta metrics
- 5-year-average metrics
- growth-like items not clearly tied 1:1 to an already-approved base metric
  such as `지배주주EPS증가율`, `지배순익 증가율(%)`, `주식수증가율(%)`

## Operational note

The current recommendation is to stabilize this taxonomy and avoid further
expansion until a new explicit policy decision is made.
