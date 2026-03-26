# Run Log

## 2026-03-26

### FnGuide policy-aligned sequential expansion to 5 companies
- Updated the operating principle for FnGuide collection:
  - do not optimize for bypassing blocks
  - follow site policy
  - use low-rate sequential batches only
  - stop immediately and record if abnormal responses or block signs appear
  - leave validation artifacts and document updates at each step
- Added a small request-interval guard to `python/etl/parse_fnguide.py`:
  - shared session-based fetch path
  - minimum inter-request spacing for sequential collection
- Re-ran local parser verification:
  - `python -m unittest tests.test_parse_fnguide`
  - result: `3` passed
- Confirmed the next two companies from current local `QDATA` inputs:
  - `삼성중공업`: `010140`
  - `HD현대`: `267250`
- Ran low-rate pre-check layout debug:
  - `python -m python.etl.debug_fnguide_layout --stock-code 010140`
  - `python -m python.etl.debug_fnguide_layout --stock-code 267250`
  - both returned:
    - `Consensus tables: 2`
    - `Main tables: 17`
- Ran the next sequential ingestion batch:
  - `python -m python.etl.run_fnguide_parser --company 삼성중공업:A010140 --company HD현대:A267250`
  - verified results:
    - `삼성중공업 (010140)`: `576 / 23 / 1 / 9 / 1`
    - `HD현대 (267250)`: `611 / 5 / 3 / 9 / 1`
- Post-load inspection:
  - `python -m python.etl.inspect_fnguide_load --stock-code 010140`
  - `python -m python.etl.inspect_fnguide_load --stock-code 267250`
  - confirmed for both companies:
    - `18` expected fetch-log combinations
    - non-zero consensus financial
    - non-zero consensus revision
    - non-zero broker target
    - non-zero report summary
    - non-zero shareholder snapshot
    - non-zero business summary
  - abnormal-response status:
    - none observed
    - no Selenium-only fallback used
- Rebuilt the current 5-company validation artifacts:
  - `outputs/fnguide_validation/fnguide_controlled_batch_validation.md`
  - `outputs/fnguide_validation/fnguide_company_counts.csv`
  - `outputs/fnguide_validation/fnguide_metrics_coverage.csv`
  - `outputs/fnguide_validation/fnguide_timeseries_sample.csv`
- Current 5-company controlled checkpoint:
  - `고려아연 (010130)`: `667 / 326 / 341 / 6 / 2 / 12 / 1`
  - `롯데케미칼 (011170)`: `527 / 292 / 235 / 17 / 4 / 9 / 1`
  - `삼성전기 (009150)`: `566 / 290 / 276 / 23 / 17 / 10 / 1`
  - `삼성중공업 (010140)`: `576 / 281 / 295 / 23 / 1 / 9 / 1`
  - `HD현대 (267250)`: `611 / 303 / 308 / 5 / 3 / 9 / 1`
- Remaining current note:
  - `고려아연` still has `3` sparse broker-target rows with null target/rating
  - block-level success remains intact

### FnGuide additional sequential 5-company batch
- Selected five new companies not yet present in the FnGuide sidecar tables:
  - `산일전기 (062040)`
  - `씨에스윈드 (112610)`
  - `에스앤에스텍 (101490)`
  - `씨어스테크놀로지 (458870)`
  - `플리토 (300080)`
- Confirmed pre-run layout shape sequentially:
  - `python -m python.etl.debug_fnguide_layout --stock-code 062040`
  - `python -m python.etl.debug_fnguide_layout --stock-code 112610`
  - `python -m python.etl.debug_fnguide_layout --stock-code 101490`
  - `python -m python.etl.debug_fnguide_layout --stock-code 458870`
  - `python -m python.etl.debug_fnguide_layout --stock-code 300080`
  - all five returned:
    - `Consensus tables: 2`
    - `Main tables: 17`
- Ran the next low-rate sequential ingestion batch:
  - `python -m python.etl.run_fnguide_parser --company 산일전기:A062040 --company 씨에스윈드:A112610 --company 에스앤에스텍:A101490 --company 씨어스테크놀로지:A458870 --company 플리토:A300080`
- Parser-side persisted counts:
  - `산일전기 (062040)`: `671 / 10 / 5 / 9 / 1`
  - `씨에스윈드 (112610)`: `516 / 9 / 3 / 9 / 1`
  - `에스앤에스텍 (101490)`: `281 / 0 / 1 / 11 / 1`
  - `씨어스테크놀로지 (458870)`: `561 / 8 / 2 / 8 / 1`
  - `플리토 (300080)`: `200 / 0 / 0 / 7 / 1`
- Post-load inspection:
  - `python -m python.etl.inspect_fnguide_load --stock-code 062040`
  - `python -m python.etl.inspect_fnguide_load --stock-code 112610`
  - `python -m python.etl.inspect_fnguide_load --stock-code 101490`
  - `python -m python.etl.inspect_fnguide_load --stock-code 458870`
  - `python -m python.etl.inspect_fnguide_load --stock-code 300080`
- Inspection result summary:
  - all five companies recorded `18` fetch-log combinations
  - no blocked or abnormal response was observed
  - `산일전기`, `씨에스윈드`, `씨어스테크놀로지`:
    - all required blocks present
  - `에스앤에스텍`:
    - `broker_target` missing
    - other inspected blocks present
  - `플리토`:
    - `consensus_revision`, `broker_target`, `report_summary` missing
    - `consensus_financial`, `shareholder_snapshot`, `business_summary` present
- Interpretation:
  - the batch completed technically without response anomalies
  - the incomplete companies look like source-side sparse coverage rather than
    transport or layout failure
- Rebuilt controlled-batch artifacts to the current 10-company checkpoint:
  - `outputs/fnguide_validation/fnguide_controlled_batch_validation.md`
  - `outputs/fnguide_validation/fnguide_company_counts.csv`
  - `outputs/fnguide_validation/fnguide_metrics_coverage.csv`
  - `outputs/fnguide_validation/fnguide_timeseries_sample.csv`

### FnGuide sequential mini-batch for HYBE and OPASNET
- Confirmed current local state before rerun:
  - `하이브 (352820)` already had full block coverage
  - `오파스넷 (173130)` already had sparse coverage with missing
    `consensus_revision`, `broker_target`, `report_summary`
- Ran low-rate pre-check layout debug:
  - `python -m python.etl.debug_fnguide_layout --stock-code 352820`
  - `python -m python.etl.debug_fnguide_layout --stock-code 173130`
  - both returned:
    - `Consensus tables: 2`
    - `Main tables: 17`
- Ran low-rate sequential mini-batch:
  - `python -m python.etl.run_fnguide_parser --company 하이브:A352820 --company 오파스넷:A173130`
- Parser-side persisted counts:
  - `하이브 (352820)`: `550 / 23 / 16 / 9 / 1`
  - `오파스넷 (173130)`: `207 / 0 / 0 / 8 / 1`
- Post-load inspection:
  - `python -m python.etl.inspect_fnguide_load --stock-code 352820`
  - `python -m python.etl.inspect_fnguide_load --stock-code 173130`
- Inspection result summary:
  - both companies recorded `18` fetch-log combinations
  - no blocked or abnormal response was observed
  - `하이브`:
    - all required blocks present
  - `오파스넷`:
    - `consensus_revision`, `broker_target`, `report_summary` still missing
    - `consensus_financial`, `shareholder_snapshot`, `business_summary`
      present
- Interpretation:
  - `하이브` remains a stable all-block company
  - `오파스넷` remains source-side sparse rather than transport-failed
- Rebuilt controlled-batch artifacts to the current 12-company checkpoint:
  - `outputs/fnguide_validation/fnguide_controlled_batch_validation.md`
  - `outputs/fnguide_validation/fnguide_company_counts.csv`
  - `outputs/fnguide_validation/fnguide_metrics_coverage.csv`
  - `outputs/fnguide_validation/fnguide_timeseries_sample.csv`

### FnGuide controlled batch expansion from Samsung baseline
- Read only the active FnGuide handoff and validation artifacts before running:
  - `docs/next_thread_handoff.md`
  - `docs/fnguide_ingestion.md`
  - `outputs/fnguide_validation/fnguide_validation_report.md`
  - `outputs/fnguide_validation/fnguide_db_check.md`
  - `outputs/fnguide_validation/fnguide_layout_debug.md`
- Confirmed local operating-company stock codes from the current DB:
  - `고려아연`: `010130`
  - `롯데케미칼`: `011170`
  - `삼성전기`: `009150`
- Extended the FnGuide helpers for company-scoped verification:
  - `python/etl/debug_fnguide_layout.py`
    - supports `--stock-code`
    - writes non-default layout debug outputs as `{stock_code}_layout_debug.md`
  - `python/etl/inspect_fnguide_load.py`
    - supports `--stock-code`
  - `python/etl/parse_fnguide.py`
    - added reusable company output-stem helper
  - `python/etl/build_fnguide_controlled_batch_reports.py`
    - builds controlled-batch validation markdown and CSV artifacts
- Verified CLI and parser tests:
  - `python -m python.etl.run_fnguide_parser --help`
  - `python -m python.etl.debug_fnguide_layout --help`
  - `python -m python.etl.inspect_fnguide_load --help`
  - `python -m unittest tests.test_parse_fnguide`
  - result: `3` passed
- Ran single-company verification for `고려아연 (010130)`:
  - `python -m python.etl.debug_fnguide_layout --stock-code 010130`
  - `python -m python.etl.run_fnguide_parser --company 고려아연:A010130`
  - `python -m python.etl.inspect_fnguide_load --stock-code 010130`
  - verified results:
    - `fnguide_observation`: `667`
    - `consensus_financial`: `326`
    - `consensus_revision`: `341`
    - `broker_target_price`: `6`
    - `broker_report_summary`: `2`
    - `company_shareholder_snapshot`: `12`
    - `company_business_summary`: `1`
  - block result:
    - all required blocks present
    - no blocked or abnormal response observed
    - sparse note:
      - `broker_target_price` contains `3` null target/rating rows
- Expanded immediately to a controlled 3-company batch with concurrency kept at `1`:
  - `python -m python.etl.run_fnguide_parser --company 고려아연:A010130 --company 롯데케미칼:A011170 --company 삼성전기:A009150`
  - `python -m python.etl.inspect_fnguide_load --stock-code 010130`
  - `python -m python.etl.inspect_fnguide_load --stock-code 011170`
  - `python -m python.etl.inspect_fnguide_load --stock-code 009150`
  - per-company counts:
    - `고려아연 (010130)`: `667 / 326 / 341 / 6 / 2 / 12 / 1`
    - `롯데케미칼 (011170)`: `527 / 292 / 235 / 17 / 4 / 9 / 1`
    - `삼성전기 (009150)`: `566 / 290 / 276 / 23 / 17 / 10 / 1`
  - interpretation:
    - all three companies produced consensus financial, consensus revision,
      broker target, report summary, shareholder snapshot, and business summary
    - no blocked or abnormal response was observed in the 3-company run
- Generated controlled-batch artifacts:
  - `outputs/fnguide_validation/010130_layout_debug.md`
  - `outputs/fnguide_validation/010130_validation_report.md`
  - `outputs/fnguide_validation/010130_db_check.md`
  - `outputs/fnguide_validation/011170_validation_report.md`
  - `outputs/fnguide_validation/011170_db_check.md`
  - `outputs/fnguide_validation/009150_validation_report.md`
  - `outputs/fnguide_validation/009150_db_check.md`
  - `outputs/fnguide_validation/fnguide_batch_summary.md`
  - `outputs/fnguide_validation/fnguide_controlled_batch_validation.md`
  - `outputs/fnguide_validation/fnguide_company_counts.csv`
  - `outputs/fnguide_validation/fnguide_metrics_coverage.csv`
  - `outputs/fnguide_validation/fnguide_timeseries_sample.csv`
- Current recommendation after this round:
  - a 5-company controlled batch is now reasonable
  - preserve explicit `company_name:stock_code` inputs
  - keep verification per company under `outputs/fnguide_validation/`

### FnGuide controlled multi-company batch
- Continued from `docs/next_thread_handoff.md` without re-reading the large
  master context file.
- Verified the Samsung baseline still passes:
  - `python -m python.etl.debug_fnguide_layout`
  - `python -m python.etl.run_fnguide_parser`
  - `python -m python.etl.inspect_fnguide_load`
  - `python -m unittest tests.test_parse_fnguide`
- Added batch-safe FnGuide controls:
  - `python/etl/run_fnguide_parser.py`
    - repeated `--company company_name:stock_code`
    - repeated `--stock-code`
    - import-log counts now scale with batch size
    - per-company validation outputs use stock-code stems
  - `python/etl/debug_fnguide_layout.py`
    - supports `--company-name` and `--stock-code`
    - writes company-specific layout debug files for non-default runs
  - `python/etl/inspect_fnguide_load.py`
    - supports `--company-name` and `--stock-code`
  - `python/etl/parse_fnguide.py`
    - added stock-code normalization helpers
    - added reusable output-path helpers
    - made company resolution fail fast when only an unresolved name is given
- Added tests:
  - `tests/test_run_fnguide_parser.py`
- Verified targeted tests:
  - `python -m unittest tests.test_parse_fnguide tests.test_run_fnguide_parser`
  - result: `7` passed
- First batch attempt using names only failed safely:
  - `python -m python.etl.run_fnguide_parser --company 삼성전자 --company 하이브 --company 오파스넷`
  - failure:
    - `ValueError: Could not resolve FnGuide company '삼성전자' to a normalized stock code.`
  - fix:
    - read stock codes from local `QDATA` files and used explicit
      `company_name:stock_code`
- Verified controlled batch with explicit codes:
  - `python -m python.etl.run_fnguide_parser --company 삼성전자:005930 --company 하이브:352820 --company 오파스넷:173130`
  - outputs:
    - `삼성전자 (005930)`: `566 / 26 / 23 / 10 / 1`
    - `하이브 (352820)`: `550 / 23 / 16 / 9 / 1`
    - `오파스넷 (173130)`: `207 / 0 / 0 / 8 / 1`
  - generated per-company artifacts:
    - `outputs/fnguide_validation/005930_*`
    - `outputs/fnguide_validation/352820_*`
    - `outputs/fnguide_validation/173130_*`
- Post-run inspection evidence:
  - `python -m python.etl.inspect_fnguide_load --stock-code 352820`
  - confirmed persisted rows for `하이브`:
    - `fnguide_observation`: `550`
    - `broker_target_price`: `23`
    - `broker_report_summary`: `16`
    - `company_shareholder_snapshot`: `9`
    - `company_business_summary`: `1`
- Additional layout check:
  - `python -m python.etl.debug_fnguide_layout --stock-code 173130`
  - confirmed non-default layout output file:
    - `outputs/fnguide_validation/173130_layout_debug.md`
- Current safe usage note:
  - batch mode is currently reliable with explicit stock codes
  - name-only resolution should not be trusted yet
  - per-company output files are the trusted verification artifacts for this
    round

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

## 2026-03-26

### Release-management scaffold
- Reviewed:
  - `AGENTS.md`
  - `PROJECT_STATUS.md`
  - `RUN_LOG.md`
  - `README.md`
  - `docs/current_architecture.md`
  - handoff note:
    - `my_markdown/9 financial_pipeline_update_policy_newchat_handoff  9 향후 데이터 업데이트 중복처리 방안.md`
- Added new SQL schema:
  - `sql/010_create_release_management_tables.sql`
- Added new helper and entrypoints:
  - `python/etl/release_management.py`
  - `python/etl/run_incremental_update.py`
  - `python/etl/run_full_rebuild.py`
  - `python/etl/promote_release.py`
  - `python/etl/rollback_release.py`
  - `python/etl/inspect_release.py`
  - `python/etl/compare_release_series.py`
- Added targeted tests:
  - `tests/test_release_management.py`
- Added policy and release docs:
  - `docs/update_policy.md`
  - `docs/rebuild_policy.md`
  - `docs/release_management.md`
  - `outputs/release_checks/release_management_plan.md`
- Updated existing docs:
  - `docs/current_architecture.md`
  - `docs/table_reference.md`
  - `docs/script_reference.md`
  - `docs/runbook.md`
  - `PROJECT_STATUS.md`

### Commands run
- `& 'C:\Users\slpar\AppData\Local\Programs\Python\Python314\python.exe' -m unittest tests.test_release_management`
- `& 'C:\Users\slpar\AppData\Local\Programs\Python\Python314\python.exe' -m python.etl.inspect_release --db-path data\financial_pipeline.sqlite3`
- `Copy-Item data\financial_pipeline.sqlite3 data\release_test.sqlite3 -Force`
- `& 'C:\Users\slpar\AppData\Local\Programs\Python\Python314\python.exe' -m python.etl.run_incremental_update --db-path data\release_test.sqlite3 --source-group QDATA --notes smoke_test`
- `& 'C:\Users\slpar\AppData\Local\Programs\Python\Python314\python.exe' -m python.etl.run_full_rebuild --db-path data\release_test.sqlite3 --release-label test_release --candidate-db-path data\releases\financial_pipeline_test_release_candidate.sqlite3 --force --notes smoke_test`
- `& 'C:\Users\slpar\AppData\Local\Programs\Python\Python314\python.exe' -m python.etl.inspect_release --db-path data\release_test.sqlite3`
- `& 'C:\Users\slpar\AppData\Local\Programs\Python\Python314\python.exe' -m python.etl.compare_release_series --db-path data\release_test.sqlite3 --other-db-path data\releases\financial_pipeline_test_release_candidate.sqlite3`

### Important outputs
- new test result:
  - `4` passed for `tests.test_release_management`
- active project DB release metadata:
  - `ingest_run`: `0`
  - `source_snapshot`: `0`
  - `series_change_audit`: `0`
  - `release_registry`: `0`
- temporary smoke test DB:
  - `ingest_run`: `2`
  - `source_snapshot`: `18`
  - `release_registry`: `1`
  - registered release:
    - `test_release / CANDIDATE / READY_FOR_VALIDATION`
- current vs candidate temporary comparison:
  - `source_file`: delta `0`
  - `raw_observation`: delta `0`
  - `integrated_observation`: delta `0`
  - `integrated_observation_enriched`: delta `0`
  - `standard_metric`: delta `0`
  - `metric_name_mapping`: delta `0`
  - `fnguide_observation`: delta `0`

### Failure encountered
- direct local Python execution was initially blocked in the sandbox with
  `Access is denied`
- reran the verification commands with approval and completed successfully

### Safety note
- this round added metadata tables and scaffolding only
- no validated raw / integrated / enriched data logic was changed
- no candidate promotion or rollback was executed on the active project DB

### Cleanup follow-up
- reviewed the handoff markdown file:
  - it is not empty
  - current sandbox rendering shows mojibake, which appears to be a terminal
    encoding issue rather than an empty file
- documented the smoke-test DB files in:
  - `docs/release_management.md`
  - `outputs/release_checks/release_management_plan.md`
- README short release-management flow added
- deleted temporary smoke-test files:
  - `data/release_test.sqlite3`
  - `data/releases/financial_pipeline_test_release_candidate.sqlite3`
