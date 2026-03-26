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
