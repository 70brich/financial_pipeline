# Update policy

## Purpose

This document defines the conservative default policy for updating the
financial pipeline without changing the meaning of the validated raw,
integrated, or enriched layers.

## Default operating mode

The default mode is incremental update against the current database.

Principles:

- compare the full known series for a source before changing current outputs
- skip unchanged inputs
- append only genuinely new periods
- patch only the changed periods when the metric meaning is unchanged
- escalate to a full-rebuild candidate when the source layout or selection
  meaning changes broadly

## Change detection units

### 1. Source snapshot

Tracked in `source_snapshot`.

This is the file or page level comparison unit used to answer:

- is this source new
- is this source unchanged
- did the source content hash change

### 2. Series change audit

Tracked in `series_change_audit`.

This is the company + metric family audit unit used to answer:

- no change
- append recent periods only
- patch one or more periods
- rebase a full series
- require manual review

## Current / history / archive split

### Current

- active SQLite file used for normal analysis
- path today: `data/financial_pipeline.sqlite3`
- should contain only the latest accepted state

### History / audit

- keeps change evidence, not full database copies for every run
- stored through `ingest_run`, `source_snapshot`, and `series_change_audit`

### Archive / release

- stores full SQLite copies only at meaningful release boundaries
- managed through `release_registry`

## Source-specific policy

### KDATA1

- default: `APPEND_RECENT`
- period corrections: `PATCH_PERIOD`
- broad meaning/layout changes: `REBASE_FULL_SERIES` through a candidate rebuild

### KDATA2

- default: `APPEND_RECENT`
- period corrections: `PATCH_PERIOD`
- broad yearly restatements: `REBASE_FULL_SERIES` through a candidate rebuild

### QDATA

- snapshot rows: keep current latest state and audit the source hash
- yearly / quarterly rows: `APPEND_RECENT` or `PATCH_PERIOD`
- no-change inputs: `SKIP_NO_CHANGE`

### FnGuide

- consensus financial blocks may use `APPEND_RECENT` or `PATCH_PERIOD`
- broker and report blocks behave like event history
- shareholder and business summary blocks are current-state first with optional
  history capture

## Guardrails

- do not overwrite `raw_metric_name`
- do not mutate `integrated_observation` semantics
- do not use fuzzy or semantic merging to classify changes
- do not update the active current DB directly when a rebuild candidate is
  required

## Current implementation note

`python.etl.run_incremental_update` is intentionally a safe metadata scaffold
for now.

What it does today:

- creates release-management tables if needed
- records an `ingest_run`
- snapshots canonical `source_file` hashes into `source_snapshot`

What it does not do yet:

- mutate raw rows
- mutate integrated rows
- mutate enriched rows
- emit detailed `series_change_audit` rows from period-level diffs

## FnGuide operating policy addendum

This addendum defines the current operating policy after the first controlled
collection pass across the full local operating-company universe.

### Current universe classification

Stable all-block companies for recurring refresh allowlist:

- `고려아연 (010130)`
- `롯데케미칼 (011170)`
- `삼성전기 (009150)`
- `삼성중공업 (010140)`
- `HD현대 (267250)`
- `산일전기 (062040)`
- `씨에스윈드 (112610)`
- `씨어스테크놀로지 (458870)`
- `하이브 (352820)`

Source-side sparse companies for partial-coverage handling:

- `에스앤에스텍 (101490)`
- `플리토 (300080)`
- `오파스넷 (173130)`
- `에스텍 (069510)`
- `영화테크 (265560)`

Interpretation rule:

- when fetch logs complete normally, no blocked or abnormal response is
  observed, and the parser layout remains stable, a company with missing
  FnGuide blocks is treated as `source-side sparse success`, not
  `technical failure`

### FnGuide success states

- `full`
  - all required blocks are present
  - eligible for recurring refresh allowlist
- `partial`
  - fetches are clean and parsing is stable
  - one limited block may be missing
  - downstream use is allowed only for block-tolerant logic
- `sparse`
  - fetches are clean and parsing is stable
  - multiple blocks are absent in a repeatable source-side pattern
  - keep the company in monitored collection history, but do not treat it as
    all-block complete
- `technical_failure`
  - blocked or abnormal response
  - incomplete fetch log set
  - parser or layout failure
  - rerun and manual review required before downstream use

Current operating interpretation:

- `에스앤에스텍 (101490)` is currently best treated as `partial`
- `플리토 (300080)`, `오파스넷 (173130)`, `에스텍 (069510)`,
  `영화테크 (265560)` are currently best treated as `sparse`

### Downstream policy

- all-block dependent downstream outputs should use the `full` cohort by
  default
- `partial` and `sparse` companies may remain in raw FnGuide sidecar storage
  and validation reports
- missing blocks must remain `NULL` or absent; do not backfill by inference
- downstream consumers must explicitly opt in if they want to use
  `partial` or `sparse` companies
- company-level status should travel with downstream extracts so coverage is
  visible during analysis

### Update and release linkage

- default update mode remains full-period comparison followed by
  `skip / append / patch`
- large layout shifts, widespread source meaning changes, or rule changes
  should produce a `full rebuild candidate`
- only validated candidates should be promoted to `current`
- audit and history should remain the primary record of change evidence rather
  than ad hoc DB replacement
