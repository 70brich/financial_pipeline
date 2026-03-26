# Release management

## Purpose

This document describes the new operations metadata layer used to track update,
rebuild, promotion, and rollback workflows without changing the validated data
meaning of the current pipeline.

## Active database model

- current database path: `data/financial_pipeline.sqlite3`
- candidate databases: `data/releases/*.sqlite3`
- archive databases: `data/archive/*.sqlite3`

## Metadata tables

### `ingest_run`

- one row per operational run
- tracks run mode, scope, status, label, and notes

### `source_snapshot`

- stores source-level content hash capture
- distinguishes `NEW_SOURCE`, `NO_CHANGE`, and `CONTENT_CHANGE`

### `series_change_audit`

- reserved for company + metric series decisions such as `APPEND_RECENT` and
  `PATCH_PERIOD`

### `release_registry`

- tracks candidate, current, and archive database files
- stores lifecycle status such as `READY_FOR_VALIDATION` and `ACTIVE`

## Scripts

### Incremental scaffold

```powershell
py -3 -m python.etl.run_incremental_update
```

### Candidate rebuild scaffold

```powershell
py -3 -m python.etl.run_full_rebuild --release-label 2026Q2_candidate
```

### Release inspection

```powershell
py -3 -m python.etl.inspect_release
```

### Candidate comparison

```powershell
py -3 -m python.etl.compare_release_series --release-label 2026Q2_candidate
```

### Promotion

Dry-run by default:

```powershell
py -3 -m python.etl.promote_release 2026Q2_candidate
```

Apply explicitly:

```powershell
py -3 -m python.etl.promote_release 2026Q2_candidate --apply
```

### Rollback

Dry-run by default:

```powershell
py -3 -m python.etl.rollback_release 2026Q1_archive
```

Apply explicitly:

```powershell
py -3 -m python.etl.rollback_release 2026Q1_archive --apply
```

## Safety model

- `promote_release` and `rollback_release` are dry-run unless `--apply` is set
- promotion creates an archive copy before replacing current
- rollback creates a backup copy before restoring an archive
- row-level ETL logic remains separate from release-file operations

## Current implementation note

The release-management layer is implemented as an operational scaffold.

Verified today:

- metadata schema creation
- metadata inspection on the active project DB
- candidate copy creation on a temporary verification DB
- high-level table-count comparison between temporary current and candidate DBs

## Temporary verification artifacts

The following files were created only for smoke-test validation of the
scaffolding:

- `data/release_test.sqlite3`
  - temporary copy of the active DB used to test metadata capture safely
- `data/releases/financial_pipeline_test_release_candidate.sqlite3`
  - temporary candidate copy created from `data/release_test.sqlite3`

These are not release assets for normal operation.

Cleanup policy:

- safe to delete after the smoke-test results are recorded in
  `outputs/release_checks/release_management_plan.md`
- do not use these files as a promotion or rollback source

Cleanup status:

- deleted after documentation on `2026-03-27`
