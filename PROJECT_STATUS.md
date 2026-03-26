# Financial Pipeline status

## Snapshot
- Date: 2026-03-25
- Canonical source groups: `KDATA1`, `KDATA2`, `QDATA`
- SQLite database file: `data/financial_pipeline.sqlite3`
- Current implementation status:
  - validated v1 raw / integrated pipeline preserved
  - v2 `standard_metric` master extension implemented non-destructively
  - current baseline is frozen as `Financial Pipeline v2 baseline`

## Verified baseline data
- Raw load status:
  - KDATA1: 1086 rows
  - KDATA2: 247 rows
  - QDATA: 1264 rows
- Integrated status:
  - `integrated_observation`: 2432 rows
- Latest user-verified v2 master coverage:
  - distinct coverage: `103 / 154 = 66.88%`
  - row-level coverage: `2077 / 2432 = 85.40%`
  - rows linked to `standard_metric_id`: `2077`
- Latest user-verified tests:
  - `28` passed for `tests.test_metric_mapping` and
    `tests.test_standard_metric_master`
- Latest user-verified v2 master counts:
  - `standard_metric`: `79` rows
  - active `metric_name_mapping`: `141` rows
  - mirrored `metric_alias_map`: `141` rows

## Current layer structure
- `source_file`
- `raw_observation`
- `fnguide_observation`
- `integrated_observation`
- `standard_metric`
- `metric_name_mapping`
- `metric_alias_map`
- `integrated_observation_enriched`
- `company_metric_timeseries`

## FnGuide Samsung sample baseline

Implemented:

- live `Consensus` page collection
- live `Main` page collection
- requests-first JSON/HTML ingestion
- dedicated sidecar tables for FnGuide data
- validation artifacts under `outputs/fnguide_validation`

Latest verified result:

- `fnguide_observation`: `566`
- `broker_target_price`: `26`
- `broker_report_summary`: `23`
- `company_shareholder_snapshot`: `10`
- `company_business_summary`: `1`
- tests:
  - `3` passed for `tests.test_parse_fnguide`

## Analysis layer baseline

Implemented:

- non-destructive SQLite view `company_metric_timeseries`
- analysis-oriented company / metric / period / value projection
- left-join company fallback so the view remains usable even when company
  matching is incomplete
- dedicated inspection helper:
  - `python.etl.inspect_company_metric_timeseries`

Latest user-verified analysis layer result:

- `company_metric_timeseries`: `2432` rows
- period distribution:
  - `YEAR`: `1247`
  - `QUARTER`: `1158`
  - `SNAPSHOT`: `27`
- tests:
  - `2` passed for `tests.test_analysis_views`

## Derived metrics v1 baseline

Implemented:

- non-destructive SQLite view `company_metric_derived_v1`
- first-pass YoY metrics:
  - `REVENUE_YOY`
  - `OPERATING_INCOME_YOY`
  - `NET_INCOME_YOY`
  - `EPS_YOY`
- first-pass QoQ metrics:
  - `REVENUE_QOQ`
  - `OPERATING_INCOME_QOQ`
  - `NET_INCOME_QOQ`
  - `EPS_QOQ`
- first-pass margin metrics:
  - `OPERATING_MARGIN`
  - `NET_MARGIN`

Latest user-verified derived layer result:

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
- tests:
  - `2` passed for `tests.test_derived_views`

## v2 standard metric master extension

Implemented:

- `standard_metric` master table
- `metric_name_mapping` authoritative mapping table
- `metric_alias_map.standard_metric_id` compatibility link
- `integrated_observation_enriched.standard_metric_id` master link
- idempotent seed flow for taxonomy and mappings
- compatibility-preserving rebuild through `run_standard_metric_mapping`
- dedicated inspection helpers for:
  - standard metric master state
  - unmapped metric review
- backward-compatible enriched rebuild:
  - legacy string-only alias mappings still work in tests
  - v2 structured mapping rows populate both `standard_metric_id` and
    `standard_metric_name`

Design choice:

- `integrated_observation` stays unchanged
- `integrated_observation_enriched` remains the main normalized output
- `standard_metric_id` is now the stable grouping key
- `standard_metric_name` string column is retained for compatibility

## Current documentation anchors
- [docs/standard_metric_master_v2.md](C:\Users\slpar\OneDrive\문서\CODEX\docs\standard_metric_master_v2.md)
- [docs/metric_taxonomy_v1.md](C:\Users\slpar\OneDrive\문서\CODEX\docs\metric_taxonomy_v1.md)
- [docs/data_quality_checklist.md](C:\Users\slpar\OneDrive\문서\CODEX\docs\data_quality_checklist.md)
- [docs/runbook.md](C:\Users\slpar\OneDrive\문서\CODEX\docs\runbook.md)

## Current guardrails
- existing raw and integrated data are preserved
- rebuilds replace target normalized layers instead of mutating raw history
- mapping remains deterministic and seed-driven
- ambiguous or deferred metric families remain unmapped unless policy changes

## Recommended next checks
- keep v2 master rebuild as the standard path
- inspect unmapped metrics only for future deferred-family policy work
- preserve current exact-alias taxonomy as the stable baseline

## Baseline freeze

`Financial Pipeline v2 baseline` is now the active frozen baseline for this
project.

This means:

- the current raw / integrated / enriched / master structure is the reference
  state
- current coverage and validation numbers are the baseline verification point
- further taxonomy expansion is deferred unless a new policy decision is made
- future work should focus on validation, governance, and controlled extension
  from this frozen state
