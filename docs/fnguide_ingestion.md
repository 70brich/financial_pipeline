# FnGuide ingestion

## Purpose

This document describes the non-destructive FnGuide source extension added on
top of the frozen `Financial Pipeline v2 baseline`.

Current scope:

- Samsung Electronics (`A005930`) sample implementation
- controlled next-company verification for `고려아연 (A010130)`
- controlled 5-company batch verification for:
  - `고려아연 (A010130)`
  - `롯데케미칼 (A011170)`
  - `삼성전기 (A009150)`
  - `삼성중공업 (A010140)`
  - `HD현대 (A267250)`
- additional sequential 5-company verification for:
  - `산일전기 (A062040)`
  - `씨에스윈드 (A112610)`
  - `에스앤에스텍 (A101490)`
  - `씨어스테크놀로지 (A458870)`
  - `플리토 (A300080)`
- `Consensus` page
- `Main` page
- requests-first collection
- JSON endpoint + HTML table/text parsing

## Collection policy

- Do not optimize for bypassing blocks.
- Follow site policy and keep the collection rate low.
- Use sequential controlled batches only.
- Stop immediately and record the event if abnormal responses or block signs appear.
- Leave validation outputs and document updates at each checkpoint.

## Why this source uses dedicated tables

The current validated `raw_observation` pipeline is constrained to the canonical
file-based source groups:

- `KDATA1`
- `KDATA2`
- `QDATA`

FnGuide is a web source with:

- URL-based provenance
- mixed JSON, HTML-table, and text blocks
- block types that do not map cleanly to the existing file-ingest constraints

For that reason, FnGuide is implemented as a non-destructive sidecar ingestion
layer instead of forcing `source_group='FNGUIDE'` into the existing
file-constrained raw tables.

## Implemented data blocks

### Consensus page

- financial consensus main table
  - 연결 / 별도
  - 연간 / 분기
- consensus revision timeseries
  - FY1 / FY2 / FY3
  - FQ1 / FQ2 / FQ3
- broker target price / investment opinion
- report summary

### Main page

- shareholder snapshot tables
- Business Summary text

## Current storage

Tables:

- `fnguide_fetch_log`
- `fnguide_observation`
- `broker_target_price`
- `broker_report_summary`
- `company_shareholder_snapshot`
- `company_business_summary`

Validation artifacts:

- `outputs/fnguide_validation/fnguide_layout_debug.md`
- `outputs/fnguide_validation/010130_layout_debug.md`
- `outputs/fnguide_validation/samsung_consensus_financial_long.csv`
- `outputs/fnguide_validation/samsung_consensus_revision_long.csv`
- `outputs/fnguide_validation/samsung_broker_target_prices.csv`
- `outputs/fnguide_validation/samsung_report_summary.csv`
- `outputs/fnguide_validation/samsung_shareholder_snapshot.csv`
- `outputs/fnguide_validation/samsung_business_summary.txt`
- `outputs/fnguide_validation/fnguide_validation_report.md`
- `outputs/fnguide_validation/fnguide_db_check.md`
- `outputs/fnguide_validation/010130_validation_report.md`
- `outputs/fnguide_validation/010130_db_check.md`
- `outputs/fnguide_validation/011170_validation_report.md`
- `outputs/fnguide_validation/011170_db_check.md`
- `outputs/fnguide_validation/009150_validation_report.md`
- `outputs/fnguide_validation/009150_db_check.md`
- `outputs/fnguide_validation/010140_validation_report.md`
- `outputs/fnguide_validation/010140_db_check.md`
- `outputs/fnguide_validation/267250_validation_report.md`
- `outputs/fnguide_validation/267250_db_check.md`
- `outputs/fnguide_validation/fnguide_controlled_batch_validation.md`
- `outputs/fnguide_validation/fnguide_company_counts.csv`
- `outputs/fnguide_validation/fnguide_metrics_coverage.csv`
- `outputs/fnguide_validation/fnguide_timeseries_sample.csv`

## Current verified snapshot

- `fnguide_observation`: `566`
- `broker_target_price`: `26`
- `broker_report_summary`: `23`
- `company_shareholder_snapshot`: `10`
- `company_business_summary`: `1`

## Current controlled batch snapshot

- `고려아연 (010130)`
  - `fnguide_observation`: `667`
  - `consensus_financial`: `326`
  - `consensus_revision`: `341`
  - `broker_target_price`: `6`
  - `broker_report_summary`: `2`
  - `company_shareholder_snapshot`: `12`
  - `company_business_summary`: `1`
- `롯데케미칼 (011170)`
  - `fnguide_observation`: `527`
  - `consensus_financial`: `292`
  - `consensus_revision`: `235`
  - `broker_target_price`: `17`
  - `broker_report_summary`: `4`
  - `company_shareholder_snapshot`: `9`
  - `company_business_summary`: `1`
- `삼성전기 (009150)`
  - `fnguide_observation`: `566`
  - `consensus_financial`: `290`
  - `consensus_revision`: `276`
  - `broker_target_price`: `23`
  - `broker_report_summary`: `17`
  - `company_shareholder_snapshot`: `10`
  - `company_business_summary`: `1`
- `삼성중공업 (010140)`
  - `fnguide_observation`: `576`
  - `consensus_financial`: `281`
  - `consensus_revision`: `295`
  - `broker_target_price`: `23`
  - `broker_report_summary`: `1`
  - `company_shareholder_snapshot`: `9`
  - `company_business_summary`: `1`
- `HD현대 (267250)`
  - `fnguide_observation`: `611`
  - `consensus_financial`: `303`
  - `consensus_revision`: `308`
  - `broker_target_price`: `5`
  - `broker_report_summary`: `3`
  - `company_shareholder_snapshot`: `9`
  - `company_business_summary`: `1`
- controlled batch result:
  - previous 5-company checkpoint: all required blocks present
  - no blocked or abnormal response detected
  - `고려아연` broker target block contains `3` sparse null target/rating rows

## Current 10-company checkpoint summary

- all fetches completed without abnormal response or block signs
- `8 / 10` companies currently have all six required blocks
- partial source-side sparse companies:
  - `에스앤에스텍 (101490)`
    - missing `broker_target`
  - `플리토 (300080)`
    - missing `consensus_revision`
    - missing `broker_target`
    - missing `report_summary`

## Execution commands

```powershell
py -3 -m python.etl.debug_fnguide_layout

py -3 -m python.etl.run_fnguide_parser

py -3 -m python.etl.inspect_fnguide_load

py -3 -m unittest tests.test_parse_fnguide
```

### Controlled next-company verification

```powershell
py -3 -m python.etl.debug_fnguide_layout `
  --stock-code 010130

py -3 -m python.etl.run_fnguide_parser `
  --company 고려아연:A010130

py -3 -m python.etl.inspect_fnguide_load `
  --stock-code 010130
```

### Controlled 3-company batch

```powershell
py -3 -m python.etl.run_fnguide_parser `
  --company 고려아연:A010130 `
  --company 롯데케미칼:A011170 `
  --company 삼성전기:A009150

py -3 -m python.etl.inspect_fnguide_load `
  --stock-code 010130

py -3 -m python.etl.inspect_fnguide_load `
  --stock-code 011170

py -3 -m python.etl.inspect_fnguide_load `
  --stock-code 009150

py -3 -m python.etl.build_fnguide_controlled_batch_reports
```

### Sequential 5-company checkpoint

```powershell
py -3 -m python.etl.debug_fnguide_layout `
  --stock-code 010140

py -3 -m python.etl.debug_fnguide_layout `
  --stock-code 267250

py -3 -m python.etl.run_fnguide_parser `
  --company 삼성중공업:A010140 `
  --company HD현대:A267250

py -3 -m python.etl.inspect_fnguide_load `
  --stock-code 010140

py -3 -m python.etl.inspect_fnguide_load `
  --stock-code 267250

py -3 -m python.etl.build_fnguide_controlled_batch_reports
```

### Additional sequential 5-company batch

```powershell
py -3 -m python.etl.debug_fnguide_layout `
  --stock-code 062040

py -3 -m python.etl.debug_fnguide_layout `
  --stock-code 112610

py -3 -m python.etl.debug_fnguide_layout `
  --stock-code 101490

py -3 -m python.etl.debug_fnguide_layout `
  --stock-code 458870

py -3 -m python.etl.debug_fnguide_layout `
  --stock-code 300080

py -3 -m python.etl.run_fnguide_parser `
  --company 산일전기:A062040 `
  --company 씨에스윈드:A112610 `
  --company 에스앤에스텍:A101490 `
  --company 씨어스테크놀로지:A458870 `
  --company 플리토:A300080

py -3 -m python.etl.inspect_fnguide_load `
  --stock-code 062040

py -3 -m python.etl.inspect_fnguide_load `
  --stock-code 112610

py -3 -m python.etl.inspect_fnguide_load `
  --stock-code 101490

py -3 -m python.etl.inspect_fnguide_load `
  --stock-code 458870

py -3 -m python.etl.inspect_fnguide_load `
  --stock-code 300080

py -3 -m python.etl.build_fnguide_controlled_batch_reports
```

## Collection strategy

### Requests-only blocks

FnGuide Samsung sample collection currently works with `requests` only:

- `01_06/01_*` JSON
  - consensus financial main table
- `01_06/02_*` JSON
  - consensus revision timeseries
- `01_06/03_*` JSON
  - broker target price / opinion
- `01_06/04_*` JSON
  - report summary
- `SVD_Main.asp` HTML
  - shareholder tables
  - Business Summary

### Deferred

- chart image capture
- Selenium-only fallback logic
- DART cross-checking
- name-only company resolution without explicit stock code

## Next extension candidates

- extend from the current 10-company checkpoint to the remaining low-rate sequential batch
- keep explicit `company_name:stock_code` inputs for controlled execution
- merge FnGuide numeric blocks into future analysis-ready views
- cross-validate with DART API in a later phase

## Latest 12-company addendum

- follow-up mini-batch completed for:
  - `?섏씠釉?(A352820)`
  - `?ㅽ뙆?ㅻ꽬 (A173130)`
- current all-block status:
  - `9 / 12` companies
- newly confirmed stable all-block company:
  - `?섏씠釉?(352820)`
- current source-side sparse companies:
  - `?먯뒪?ㅼ뿉?ㅽ뀓 (101490)`: missing `broker_target`
  - `?뚮━??(300080)`: missing `consensus_revision`, `broker_target`,
    `report_summary`
  - `?ㅽ뙆?ㅻ꽬 (173130)`: missing `consensus_revision`, `broker_target`,
    `report_summary`
- latest abnormal-response status:
  - no blocked or abnormal response observed

## FnGuide operating policy addendum

Current verified interpretation after the first 14-company pass:

- `9 / 14` companies are `full` all-block success
- `5 / 14` companies are source-side sparse success, not technical failure
- no blocked or abnormal response was observed in the controlled universe pass

Stable all-block cohort:

- `고려아연 (010130)`
- `롯데케미칼 (011170)`
- `삼성전기 (009150)`
- `삼성중공업 (010140)`
- `HD현대 (267250)`
- `산일전기 (062040)`
- `씨에스윈드 (112610)`
- `씨어스테크놀로지 (458870)`
- `하이브 (352820)`

Partial or sparse cohort:

- `에스앤에스텍 (101490)`: currently `partial`
- `플리토 (300080)`: currently `sparse`
- `오파스넷 (173130)`: currently `sparse`
- `에스텍 (069510)`: currently `sparse`
- `영화테크 (265560)`: currently `sparse`

Interpretation rule:

- if fetch logs complete normally, the parser layout remains stable, and no
  blocked or abnormal response is detected, missing blocks are classified as
  `source-side sparse success` rather than `technical failure`

Operating usage rule:

- recurring refresh allowlist should default to the stable all-block cohort
- partial or sparse companies may still be refreshed and stored, but should be
  separated in downstream usage and reporting
- downstream logic that requires all six blocks should exclude non-`full`
  companies by default
- remaining local universe:
  - `?먯뒪??(069510)`
  - `?곹솕?뚰겕 (265560)`

## Final 14-company local-universe addendum

- final mini-batch completed for:
  - `에스텍 (A069510)`
  - `영화테크 (A265560)`
- full local operating-company universe is now checked once
- current all-block status:
  - `9 / 14` companies
- newly confirmed additional source-side sparse companies:
  - `에스텍 (069510)`: missing `consensus_revision`, `broker_target`,
    `report_summary`
  - `영화테크 (265560)`: missing `consensus_revision`, `broker_target`,
    `report_summary`
- latest abnormal-response status:
  - no blocked or abnormal response observed
