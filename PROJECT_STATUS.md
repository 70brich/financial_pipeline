# Financial Pipeline status

## Snapshot
- Date: 2026-03-26
- Canonical source groups: `KDATA1`, `KDATA2`, `QDATA`
- SQLite database file: `data/financial_pipeline.sqlite3`
- Current implementation status:
  - validated v1 raw / integrated pipeline preserved
  - v2 `standard_metric` master extension implemented non-destructively
  - FnGuide sidecar ingestion verified beyond Samsung baseline
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

## FnGuide controlled expansion status

Implemented:

- company-scoped layout debug output for non-default stock codes
- `inspect_fnguide_load --stock-code`
- controlled-batch reporting helper:
  - `python.etl.build_fnguide_controlled_batch_reports`
- per-company validation artifacts for:
  - `010130`
  - `011170`
  - `009150`
  - `010140`
  - `267250`
- policy-aligned sequential collection guard:
  - shared session-based fetch path
  - minimum inter-request spacing

Current collection policy:

- do not optimize for bypassing blocks
- follow site policy
- keep requests low-rate and sequential
- stop immediately and record if abnormal responses or block signs appear
- update validation artifacts and docs at each checkpoint

Latest verified result:

- single-company checkpoint:
  - `고려아연 (010130)`: `SUCCESS`
- controlled 10-company checkpoint:
  - `고려아연 (010130)`: `667 / 326 / 341 / 6 / 2 / 12 / 1`
  - `롯데케미칼 (011170)`: `527 / 292 / 235 / 17 / 4 / 9 / 1`
  - `삼성전기 (009150)`: `566 / 290 / 276 / 23 / 17 / 10 / 1`
  - `삼성중공업 (010140)`: `576 / 281 / 295 / 23 / 1 / 9 / 1`
  - `HD현대 (267250)`: `611 / 303 / 308 / 5 / 3 / 9 / 1`
  - `산일전기 (062040)`: `671 / 318 / 353 / 10 / 5 / 9 / 1`
  - `씨에스윈드 (112610)`: `516 / 271 / 245 / 9 / 3 / 9 / 1`
  - `에스앤에스텍 (101490)`: `281 / 202 / 79 / 0 / 1 / 11 / 1`
  - `씨어스테크놀로지 (458870)`: `561 / 267 / 294 / 8 / 2 / 8 / 1`
  - `플리토 (300080)`: `200 / 200 / 0 / 0 / 0 / 7 / 1`
- required block status:
  - `8 / 10` companies produced all six required blocks
  - `에스앤에스텍 (101490)` is missing `broker_target`
  - `플리토 (300080)` is missing `consensus_revision`, `broker_target`,
    `report_summary`
- abnormal response status:
  - no blocked or abnormal response observed
- sparse note:
  - `고려아연 (010130)` broker target rows include `3` null target/rating rows
  - `산일전기 (062040)` broker target rows include `1` null target/rating row
  - `씨어스테크놀로지 (458870)` broker target rows include `3` null target/rating rows
- controlled next step:
  - project is technically ready for the next low-rate sequential expansion,
    but the current partial-coverage companies should be kept flagged in reports

## FnGuide controlled batch baseline

Implemented:

- `python.etl.run_fnguide_parser` now supports repeated `--company` specs for
  a small controlled batch
- each `--company` value can be passed as `company_name:stock_code`
- `python.etl.debug_fnguide_layout` and `python.etl.inspect_fnguide_load`
  now support `--company-name` and `--stock-code`
- batch runs now write stock-code-scoped validation outputs so companies do not
  overwrite each other
- added parser-side tests:
  - `tests.test_run_fnguide_parser`

Latest verified batch:

- companies processed:
  - `삼성전자:005930`
  - `하이브:352820`
  - `오파스넷:173130`
- `삼성전자 (005930)`:
  - `fnguide_observation`: `566`
  - `broker_target_price`: `26`
  - `broker_report_summary`: `23`
  - `company_shareholder_snapshot`: `10`
  - `company_business_summary`: `1`
- `하이브 (352820)`:
  - `fnguide_observation`: `550`
  - `broker_target_price`: `23`
  - `broker_report_summary`: `16`
  - `company_shareholder_snapshot`: `9`
  - `company_business_summary`: `1`
- `오파스넷 (173130)`:
  - `fnguide_observation`: `207`
  - `broker_target_price`: `0`
  - `broker_report_summary`: `0`
  - `company_shareholder_snapshot`: `8`
  - `company_business_summary`: `1`
- tests:
  - `7` passed for `tests.test_parse_fnguide` and
    `tests.test_run_fnguide_parser`

Current operating note:

- name-only company resolution is not reliable yet for batch mode
- use explicit `company_name:stock_code` or `--stock-code` when running a
  controlled multi-company batch
- per-company outputs under `outputs/fnguide_validation/` are now the primary
  verification artifacts for FnGuide batch work

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

## Release-management scaffold addendum

Implemented:

- new operations metadata schema:
  - `ingest_run`
  - `source_snapshot`
  - `series_change_audit`
  - `release_registry`
- new SQL:
  - `sql/010_create_release_management_tables.sql`
- new operational helpers and entrypoints:
  - `python.etl.run_incremental_update`
  - `python.etl.run_full_rebuild`
  - `python.etl.inspect_release`
  - `python.etl.compare_release_series`
  - `python.etl.promote_release`
  - `python.etl.rollback_release`
- new policy docs:
  - `docs/update_policy.md`
  - `docs/rebuild_policy.md`
  - `docs/release_management.md`
- new verification artifact:
  - `outputs/release_checks/release_management_plan.md`

Verified in this round:

- `4` passed for `tests.test_release_management`
- active project DB inspection succeeded:
  - `ingest_run`: `0`
  - `source_snapshot`: `0`
  - `series_change_audit`: `0`
  - `release_registry`: `0`
- temporary smoke test on `data/release_test.sqlite3` succeeded:
  - `ingest_run`: `2`
  - `source_snapshot`: `18`
  - `series_change_audit`: `0`
  - `release_registry`: `1`
  - candidate comparison vs copied release: all key managed-table deltas were `0`

Guardrail:

- the active current DB data contents were not rebuilt or promoted in this round
- the new layer is metadata-first scaffolding on top of the frozen v2 baseline

## Current guardrails
- existing raw and integrated data are preserved
- rebuilds replace target normalized layers instead of mutating raw history
- mapping remains deterministic and seed-driven
- ambiguous or deferred metric families remain unmapped unless policy changes

## Recommended next checks
- keep v2 master rebuild as the standard path
- inspect unmapped metrics only for future deferred-family policy work
- preserve current exact-alias taxonomy as the stable baseline
- wire period-level diff logic into `series_change_audit` before any real
  incremental mutation workflow
- validate `promote_release --apply` and `rollback_release --apply` only on a
  disposable copy before using them on the active DB
- expand the FnGuide allowlist gradually with explicit stock codes from local
  source files
- next sequential FnGuide expansion candidates from the remaining local universe:
  - `하이브 (352820)`
  - `오파스넷 (173130)`
  - `에스텍 (069510)`
  - `영화테크 (265560)`
- compare broker/report availability between large-cap and small-cap issuers
  before deeper integration into shared layers

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

## Final FnGuide Universe Addendum

- final local-universe mini-batch completed for:
  - `에스텍 (069510)`
  - `영화테크 (265560)`
- full local operating-company universe has now been checked once
- latest controlled checkpoint now covers `14` companies
- current all-block status:
  - `9 / 14` companies produced all six required blocks
- current source-side sparse companies:
  - `에스앤에스텍 (101490)`: missing `broker_target`
  - `플리토 (300080)`: missing `consensus_revision`, `broker_target`,
    `report_summary`
  - `오파스넷 (173130)`: missing `consensus_revision`, `broker_target`,
    `report_summary`
  - `에스텍 (069510)`: missing `consensus_revision`, `broker_target`,
    `report_summary`
  - `영화테크 (265560)`: missing `consensus_revision`, `broker_target`,
    `report_summary`
- latest abnormal-response status:
  - no blocked or abnormal response observed
- remaining local universe to check:
  - none

## Latest FnGuide Addendum

- latest sequential mini-batch completed for:
  - `?섏씠釉?(352820)`
  - `?ㅽ뙆?ㅻ꽬 (173130)`
- latest controlled checkpoint now covers `12` companies
- current all-block status:
  - `9 / 12` companies produced all six required blocks
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
- remaining local universe to check:
  - `?먯뒪??(069510)`
  - `?곹솕?뚰겕 (265560)`
# FnGuide Policy Closeout Addendum

- current local FnGuide universe classification is now fixed for policy work:
  - stable all-block companies: `9`
  - source-side sparse companies: `5`
- stable all-block cohort:
  - `고려아연 (010130)`
  - `롯데케미칼 (011170)`
  - `삼성전기 (009150)`
  - `삼성중공업 (010140)`
  - `HD현대 (267250)`
  - `산일전기 (062040)`
  - `씨에스윈드 (112610)`
  - `씨어스테크놀로지 (458870)`
  - `하이브 (352820)`
- source-side sparse cohort:
  - `에스앤에스텍 (101490)` -> `partial`
  - `플리토 (300080)` -> `sparse`
  - `오파스넷 (173130)` -> `sparse`
  - `에스텍 (069510)` -> `sparse`
  - `영화테크 (265560)` -> `sparse`
- interpretation rule:
  - when fetch logs are complete and no blocked or abnormal response is seen,
    missing blocks are interpreted as source-side sparse success rather than
    technical failure
- recurring refresh draft:
  - default allowlist = stable all-block cohort
  - partial/sparse cohort remains stored and auditable, but excluded from
    all-block-dependent downstream logic by default
- update / release linkage:
  - normal path = compare full period history, then `skip / append / patch`
  - major rule or layout shifts = create a full rebuild candidate
  - only validated candidates should be promoted to current
  - audit/history remains the primary change record
- git working tree note:
  - commit is not clean as-is because unrelated local DB/input/output/scratch
    changes are present
  - policy docs can still be committed later as a curated subset
