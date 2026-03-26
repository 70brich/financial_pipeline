# Run Log

## 2026-03-26

### FnGuide Samsung sample ingestion
- Reviewed current baseline docs and ETL structure before extending the project:
  - `README.md`
  - `PROJECT_STATUS.md`
  - `RUN_LOG.md`
  - `docs/current_architecture.md`
  - `docs/standard_metric_master_v2.md`
  - `docs/db_design.md`
  - `docs/data_rules.md`
- Added non-destructive FnGuide sidecar schema:
  - `sql/009_create_fnguide_tables.sql`
- Added requests-first FnGuide implementation:
  - `python/etl/debug_fnguide_layout.py`
  - `python/etl/parse_fnguide.py`
  - `python/etl/run_fnguide_parser.py`
  - `python/etl/inspect_fnguide_load.py`
- Added validation outputs:
  - `outputs/fnguide_validation/fnguide_layout_debug.md`
  - `outputs/fnguide_validation/samsung_consensus_financial_long.csv`
  - `outputs/fnguide_validation/samsung_consensus_revision_long.csv`
  - `outputs/fnguide_validation/samsung_broker_target_prices.csv`
  - `outputs/fnguide_validation/samsung_report_summary.csv`
  - `outputs/fnguide_validation/samsung_shareholder_snapshot.csv`
  - `outputs/fnguide_validation/samsung_business_summary.txt`
  - `outputs/fnguide_validation/fnguide_validation_report.md`
  - `outputs/fnguide_validation/fnguide_db_check.md`
- Verified live execution:
  - `py -3 -m python.etl.debug_fnguide_layout`
  - `py -3 -m python.etl.run_fnguide_parser`
  - `py -3 -m python.etl.inspect_fnguide_load`
  - `py -3 -m unittest tests.test_parse_fnguide`
- Verified outcomes:
  - `fnguide_observation`: `566`
  - `broker_target_price`: `26`
  - `broker_report_summary`: `23`
  - `company_shareholder_snapshot`: `10`
  - `company_business_summary`: `1`
  - tests: `3` passed
- Important design note:
  - FnGuide numeric data was kept out of `raw_observation`
  - current `source_group` constraints in the validated file-ingest schema were left unchanged
  - FnGuide therefore uses dedicated sidecar tables for a conservative, non-destructive v1 implementation

## 2026-03-25

### Documentation stabilization for v2 baseline freeze
- Updated [PROJECT_STATUS.md](C:\Users\slpar\OneDrive\문서\CODEX\PROJECT_STATUS.md)
  - marked the current project state as the frozen `Financial Pipeline v2 baseline`
- Updated [RUN_LOG.md](C:\Users\slpar\OneDrive\문서\CODEX\RUN_LOG.md)
  - recorded the documentation-only freeze step
- Updated [docs/standard_metric_master_v2.md](C:\Users\slpar\OneDrive\문서\CODEX\docs\standard_metric_master_v2.md)
  - added an explicit baseline snapshot section for the frozen v2 baseline
- Updated [README.md](C:\Users\slpar\OneDrive\문서\CODEX\README.md)
  - added a short v1 to v2 transition note
- Scope guard:
  - no code changes
  - no schema changes
  - no mapping changes

### Analysis layer verification
- Added non-destructive analysis view support:
  - `company_metric_timeseries`
- User-side local verification succeeded:
  - `py -3 -m python.etl.run_analysis_views`
  - `py -3 -m python.etl.inspect_company_metric_timeseries`
  - `py -3 -m unittest tests.test_analysis_views`
- Verified outcomes:
  - `company_metric_timeseries`: `2432` rows
  - period distribution:
    - `YEAR`: `1247`
    - `QUARTER`: `1158`
    - `SNAPSHOT`: `27`
  - tests: `2` passed
- Important note:
  - terminal output still shows Korean text mojibake in this environment
  - the analysis layer itself is functioning; this is a console rendering issue,
    not a schema or mapping failure

### Derived metrics v1 verification
- Added non-destructive derived analysis view support:
  - `company_metric_derived_v1`
- Initial issue fixed:
  - SQLite integer division caused `QOQ` and margin calculations like
    `200 / 150` and `33 / 417` to collapse to `0`
  - derived SQL was updated to force `REAL` arithmetic with `1.0 * value`
- User-side local verification succeeded:
  - `py -3 -m python.etl.run_derived_views`
  - `py -3 -m python.etl.inspect_company_metric_derived`
  - `py -3 -m unittest tests.test_derived_views`
- Verified outcomes:
  - `company_metric_derived_v1`: `440` rows
  - metric row counts:
    - `EPS_YOY`: `49`
    - `NET_INCOME_YOY`: `49`
    - `NET_MARGIN`: `49`
    - `OPERATING_MARGIN`: `47`
    - `OPERATING_INCOME_YOY`: `46`
    - `REVENUE_YOY`: `46`
    - `EPS_QOQ`: `41`
    - `NET_INCOME_QOQ`: `41`
    - `OPERATING_INCOME_QOQ`: `36`
    - `REVENUE_QOQ`: `36`
  - period distribution:
    - `QUARTER`: `378`
    - `YEAR`: `60`
    - `SNAPSHOT`: `2`
  - tests: `2` passed

### Latest verified result
- User-side local verification after the v2 standard metric master extension
  succeeded:
  - `py -3 -m python.etl.seed_standard_metric_master`
  - `py -3 -m python.etl.run_standard_metric_mapping`
  - `py -3 -m python.etl.inspect_standard_metric_mapping`
  - `py -3 -m python.etl.inspect_standard_metric_master`
  - `py -3 -m python.etl.inspect_unmapped_metrics`
  - `py -3 -m unittest tests.test_metric_mapping tests.test_standard_metric_master`
- Verified outcomes:
  - `standard_metric`: `79` rows
  - active `metric_name_mapping`: `141` rows
  - mirrored `metric_alias_map`: `141` rows
  - `integrated_observation_enriched`: `2432` rows
  - rows linked to `standard_metric_id`: `2077`
  - tests: `28` passed
  - distinct coverage: `103 / 154 = 66.88%`
  - row-level coverage: `2077 / 2432 = 85.40%`

### Compatibility fix that enabled final verification
- Updated [python/etl/build_integrated_observation_enriched.py](C:\Users\slpar\OneDrive\문서\CODEX\python\etl\build_integrated_observation_enriched.py)
  - `build_enriched_records()` now accepts both:
    - legacy `dict[str, str]` alias mappings used by older tests
    - v2 `dict[str, dict]` mapping rows carrying `standard_metric_id`
- This resolved the user-side failure:
  - `TypeError: string indices must be integers, not 'str'`

### Current deferred-family state
- Remaining unmapped metrics are concentrated in intentionally deferred groups:
  - valuation / price family: `111` rows
  - supplementary per-share family: `60` rows
  - dividend family: `45` rows
  - turnover-day family: `40` rows
  - score / meta family: `8` rows
  - 5-year-average family: `4` rows

### Prior verified result
- User-side local verification after the conservative growth-rate batch succeeded:
  - tests: `23` passed
  - distinct coverage: `103 / 154 = 66.88%`
  - row-level coverage: `2077 / 2432 = 85.40%`
  - `REVENUE_GROWTH_RATE`: `44` rows
  - `SGA_GROWTH_RATE`: `28` rows
  - `OPERATING_INCOME_GROWTH_RATE`: `40` rows
  - `BPS_GROWTH_RATE`: `10` rows
  - `EPS_GROWTH_RATE`: `10` rows
  - `FCF_GROWTH_RATE`: `10` rows
  - `NPM_GROWTH_RATE`: `10` rows
  - `OPM_GROWTH_RATE`: `10` rows
  - `ROA_GROWTH_RATE`: `10` rows
  - `ROE_GROWTH_RATE`: `10` rows
  - `CAPEX_GROWTH_RATE`: `10` rows
  - `OPERATING_CASHFLOW_GROWTH_RATE`: `10` rows
  - `EQUITY_GROWTH_RATE`: `10` rows
  - `ASSET_GROWTH_RATE`: `10` rows

### Recent changes
- Updated [python/etl/metric_mapping.py](C:\Users\slpar\OneDrive\문서\CODEX\python\etl\metric_mapping.py)
  - added exact aliases for the approved conservative growth-rate family
  - preserved exact-alias-only policy
  - preserved lookup-only stripping for leading cosmetic prefixes `-`, `+`, `=`
  - intentionally left growth-like but policy-risk metrics unmapped:
    - `지배주주EPS증가율`
    - `지배순익 증가율(%)`
    - `주식수증가율(%)`
- Updated [tests/test_metric_mapping.py](C:\Users\slpar\OneDrive\문서\CODEX\tests\test_metric_mapping.py)
  - added coverage for the approved growth-rate mappings
  - kept still-deferred families unmapped in tests
- Updated [python/etl/inspect_standard_metric_mapping.py](C:\Users\slpar\OneDrive\문서\CODEX\python\etl\inspect_standard_metric_mapping.py)
  - added `Choice 2 growth-rate row counts`

### Commands attempted in Codex environment
- `py -3 -m unittest tests.test_metric_mapping`
- `py -3 -m python.etl.run_standard_metric_mapping`
- `py -3 -m python.etl.inspect_standard_metric_mapping`
- `Get-Command python -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Source`
- `Get-Command py -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Source`

### Important environment note
- This Codex environment does not expose `py` or `python` on `PATH`.
- Verification therefore depends on user-side local runs.

### Next action
- Coverage targets have now been exceeded.
- Remaining high-volume unmapped metrics sit in explicitly deferred policy families.
- The next move should be another narrow policy decision, not autonomous taxonomy expansion.
