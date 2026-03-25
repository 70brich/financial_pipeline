# Financial Pipeline v1 Baseline

## Snapshot
- Date: 2026-03-25
- Status: stable documentation baseline
- Canonical source groups: `KDATA1`, `KDATA2`, `QDATA`
- SQLite-first pipeline layers are in place:
  - `source_file`
  - `raw_observation`
  - `integrated_observation`
  - `integrated_observation_enriched`

## Verified v1 baseline
- Raw load status:
  - KDATA1: 1086 rows
  - KDATA2: 247 rows
  - QDATA: 1264 rows
- Integrated status:
  - `integrated_observation`: 2432 rows
- Recent standard metric coverage from user-verified local run:
  - distinct coverage: `103 / 154 = 66.88%`
  - row-level coverage: `2077 / 2432 = 85.40%`
- Latest local verification:
  - tests: `23` passed

## Most recent completed work
- Approved exact-alias batches now implemented and user-verified:
  - accounting / cash flow / balance sheet core metrics
  - pre-tax / non-operating / affiliate / tax metrics
  - accounting / investment metrics
  - conservative ratio metrics
  - conservative growth-rate metrics tied to already-approved base metrics
- Existing safe normalization remains in place:
  - lookup-only stripping for leading `-`, `+`, `=`
  - `raw_metric_name` preserved exactly
- Inspection/reporting improvements now include:
  - top unmapped `normalized_metric_key`
  - unicode-escaped unmapped samples
  - symbol-prefixed unmapped samples
  - policy bucket summary
  - row counts for approved metric batches

## Latest verified row gains
- Ratio batch:
  - `DEPRECIATION_RATIO`: `10`
  - `SGA_RATIO`: `10`
  - `RND_RATIO`: `10`
  - `BORROWING_RATIO`: `10`
  - `OPERATING_INCOME_TO_BORROWINGS_RATIO`: `10`
- Growth-rate batch:
  - `REVENUE_GROWTH_RATE`: `44`
  - `SGA_GROWTH_RATE`: `28`
  - `OPERATING_INCOME_GROWTH_RATE`: `40`
  - `BPS_GROWTH_RATE`: `10`
  - `EPS_GROWTH_RATE`: `10`
  - `FCF_GROWTH_RATE`: `10`
  - `NPM_GROWTH_RATE`: `10`
  - `OPM_GROWTH_RATE`: `10`
  - `ROA_GROWTH_RATE`: `10`
  - `ROE_GROWTH_RATE`: `10`
  - `CAPEX_GROWTH_RATE`: `10`
  - `OPERATING_CASHFLOW_GROWTH_RATE`: `10`
  - `EQUITY_GROWTH_RATE`: `10`
  - `ASSET_GROWTH_RATE`: `10`

## Current top unmapped candidate classes
- Turnover-day families
- Dividend families
- Supplementary per-share families such as `CPS`, `DPS`, `OPS`, `SPS`
- Valuation and market families such as `EV/EBITDA`, `PCR`, `PEG`, `POR`, `PRR`, `PSR`, `ROIC`, `주가`
- Score/meta families such as `벨류점수`, `성장점수`, `수익점수`, `안정점수`
- 5-year-average families
- Still-deferred growth-like items not safely covered by the approved batch, such as:
  - `지배주주EPS증가율`
  - `지배순익 증가율(%)`
  - `주식수증가율(%)`

## Next recommended safe task
- The approved growth-rate batch is fully verified.
- Coverage targets have already been exceeded:
  - distinct metric coverage target `~60%`: achieved
  - row-level coverage target `~80%`: achieved
- Taxonomy expansion is intentionally stopped for the current version.
- The next safe focus is pipeline stabilization and taxonomy documentation.
- Primary reference documents for the v1 baseline:
  - [docs/metric_taxonomy_v1.md](C:\Users\slpar\OneDrive\문서\CODEX\docs\metric_taxonomy_v1.md)
  - [docs/data_quality_checklist.md](C:\Users\slpar\OneDrive\문서\CODEX\docs\data_quality_checklist.md)
- See [docs/metric_taxonomy_v1.md](C:\Users\slpar\OneDrive\문서\CODEX\docs\metric_taxonomy_v1.md).

## Known risks / blockers
- This Codex environment does not currently expose `py` or `python` on `PATH`, so automated local test execution from here is blocked.
- The next blocker is policy-driven:
  - turnover-day families
  - dividend families
  - supplementary per-share metrics
  - valuation / price / score families
  - 5-year-average metrics
  - growth-like items that are not obviously tied 1:1 to an already-approved base metric
