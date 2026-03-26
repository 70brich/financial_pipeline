# Release management plan

## Scope

Add a non-destructive operations layer for update, rebuild, promotion, and
rollback management without changing validated raw / integrated / enriched
semantics.

## Implemented in this round

- `sql/010_create_release_management_tables.sql`
- `python/etl/release_management.py`
- `python/etl/run_incremental_update.py`
- `python/etl/run_full_rebuild.py`
- `python/etl/promote_release.py`
- `python/etl/rollback_release.py`
- `python/etl/inspect_release.py`
- `python/etl/compare_release_series.py`
- `tests/test_release_management.py`

## Verified results

- active project DB inspection:
  - `ingest_run = 0`
  - `source_snapshot = 0`
  - `series_change_audit = 0`
  - `release_registry = 0`
- targeted tests:
  - `4` passed for `tests.test_release_management`
- temporary smoke test on `data/release_test.sqlite3`:
  - `ingest_run = 2`
  - `source_snapshot = 18`
  - `release_registry = 1`
  - candidate row-count deltas for key managed tables were all `0`

## Temporary verification files

- `data/release_test.sqlite3`
  - purpose: disposable smoke-test copy of the active DB
- `data/releases/financial_pipeline_test_release_candidate.sqlite3`
  - purpose: disposable candidate copy created from the smoke-test DB

Disposition:

- these files are not part of the intended steady-state release flow
- once their purpose is documented, they are safe to delete
- keep only named candidate or archive files that represent an actual release checkpoint
- cleanup completed on `2026-03-27`

## Known limitations

- incremental update currently records metadata only
- full rebuild currently copies the current DB into a candidate scaffold only
- `series_change_audit` is ready but not yet populated from automated diffs
- release promotion / rollback were implemented with dry-run defaults but were
  not executed against the active project DB
