# FnGuide ingestion

## Purpose

This document describes the non-destructive FnGuide source extension added on
top of the frozen `Financial Pipeline v2 baseline`.

Current scope:

- Samsung Electronics (`A005930`) sample implementation
- `Consensus` page
- `Main` page
- requests-first collection
- JSON endpoint + HTML table/text parsing

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
- `outputs/fnguide_validation/samsung_consensus_financial_long.csv`
- `outputs/fnguide_validation/samsung_consensus_revision_long.csv`
- `outputs/fnguide_validation/samsung_broker_target_prices.csv`
- `outputs/fnguide_validation/samsung_report_summary.csv`
- `outputs/fnguide_validation/samsung_shareholder_snapshot.csv`
- `outputs/fnguide_validation/samsung_business_summary.txt`
- `outputs/fnguide_validation/fnguide_validation_report.md`
- `outputs/fnguide_validation/fnguide_db_check.md`

## Current verified snapshot

- `fnguide_observation`: `566`
- `broker_target_price`: `26`
- `broker_report_summary`: `23`
- `company_shareholder_snapshot`: `10`
- `company_business_summary`: `1`

## Execution commands

```powershell
py -3 -m python.etl.debug_fnguide_layout
py -3 -m python.etl.run_fnguide_parser
py -3 -m python.etl.inspect_fnguide_load
py -3 -m unittest tests.test_parse_fnguide
```

One-line form:

```powershell
py -3 -m python.etl.debug_fnguide_layout; py -3 -m python.etl.run_fnguide_parser; py -3 -m python.etl.inspect_fnguide_load; py -3 -m unittest tests.test_parse_fnguide
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
- multi-company batch runner
- DART cross-checking

## Next extension candidates

- extend from Samsung sample to multi-company list input
- merge FnGuide numeric blocks into future analysis-ready views
- cross-validate with DART API in a later phase
