# Next Thread Handoff

## Scope
This handoff is based on actual local file existence and current Git state in:

- `C:\Users\slpar\OneDrive\문서\CODEX`

Git status basis:

- `HEAD = origin/main`
- latest pushed commit verified as:
  - `c0d88c1 Implement FnGuide ingestion, analysis views, derived metrics, and docs`

Local-only classification below is based on current `git status --short`, not session memory.

## 1. Actually completed in this thread

The following work is already implemented locally and included in the latest pushed baseline unless noted otherwise.

### A. FnGuide Samsung sample ingestion
- Added FnGuide debug/parser/run/inspect flow:
  - `python/etl/debug_fnguide_layout.py`
  - `python/etl/parse_fnguide.py`
  - `python/etl/run_fnguide_parser.py`
  - `python/etl/inspect_fnguide_load.py`
- Added FnGuide sidecar schema:
  - `sql/009_create_fnguide_tables.sql`
- Added FnGuide tests:
  - `tests/test_parse_fnguide.py`
- Implemented non-destructive sidecar storage for FnGuide data instead of forcing it into existing source-group constraints.

### B. Analysis layer
- Added analysis view:
  - `company_metric_timeseries`
- Added runner and inspect helper:
  - `python/etl/run_analysis_views.py`
  - `python/etl/inspect_company_metric_timeseries.py`
- Added tests:
  - `tests/test_analysis_views.py`

### C. Derived metrics v1
- Added derived view:
  - `company_metric_derived_v1`
- Added runner and inspect helper:
  - `python/etl/run_derived_views.py`
  - `python/etl/inspect_company_metric_derived.py`
- Added tests:
  - `tests/test_derived_views.py`

### D. Standard metric master v2 baseline
- Added master structure around `standard_metric`
- Preserved compatibility with existing `integrated_observation_enriched.standard_metric_name`
- Added master seed / inspect / validation helpers
- Verified baseline metrics:
  - `standard_metric = 79`
  - `metric_name_mapping = 141`
  - `metric_alias_map = 141`
  - `integrated_observation_enriched = 2432`
  - rows linked to `standard_metric_id = 2077`
  - distinct coverage `66.88%`
  - row-level coverage `85.40%`
  - tests `28 passed`

### E. Validation outputs already generated
FnGuide validation outputs exist under:

- `C:\Users\slpar\OneDrive\문서\CODEX\outputs\fnguide_validation`

Confirmed files include:
- `fnguide_layout_debug.md`
- `fnguide_validation_report.md`
- `fnguide_db_check.md`
- `samsung_consensus_financial_long.csv`
- `samsung_consensus_revision_long.csv`
- `samsung_broker_target_prices.csv`
- `samsung_report_summary.csv`
- `samsung_shareholder_snapshot.csv`
- `samsung_business_summary.txt`

## 2. Core files already included in commit/push

These are the main files confirmed to be in pushed commit `c0d88c1`.

### Core code
- `python/etl/debug_fnguide_layout.py`
- `python/etl/parse_fnguide.py`
- `python/etl/run_fnguide_parser.py`
- `python/etl/inspect_fnguide_load.py`
- `python/etl/analysis_views.py`
- `python/etl/run_analysis_views.py`
- `python/etl/inspect_company_metric_timeseries.py`
- `python/etl/derived_views.py`
- `python/etl/run_derived_views.py`
- `python/etl/inspect_company_metric_derived.py`
- `python/etl/standard_metric_master.py`
- `python/etl/seed_standard_metric_master.py`
- `python/etl/run_standard_metric_mapping.py`
- `python/etl/inspect_standard_metric_mapping.py`
- `python/etl/inspect_standard_metric_master.py`
- `python/etl/inspect_unmapped_metrics.py`

### Core SQL
- `sql/005_create_metric_mapping_tables.sql`
- `sql/006_create_standard_metric_master_tables.sql`
- `sql/007_create_analysis_views.sql`
- `sql/008_create_derived_metric_views.sql`
- `sql/009_create_fnguide_tables.sql`

### Core docs
- `README.md`
- `PROJECT_STATUS.md`
- `RUN_LOG.md`
- `docs/current_architecture.md`
- `docs/db_design.md`
- `docs/runbook.md`
- `docs/analysis_layer_v1.md`
- `docs/derived_metrics_v1.md`
- `docs/standard_metric_master_v2.md`
- `docs/fnguide_ingestion.md`
- `docs/fnguide_data_dictionary.md`

### Core tests
- `tests/test_parse_fnguide.py`
- `tests/test_analysis_views.py`
- `tests/test_derived_views.py`
- `tests/test_standard_metric_master.py`

## 3. Files still only local, classified

This section is based on current `git status --short`.

### A. Next commit candidates

These are the most reasonable candidates for the next commit if the user wants newly added local content versioned.

- `docs/next_thread_handoff.md`
- `data/input/KDATA1/*` newly added company files
- `data/input/KDATA2/*` newly added company files
- `data/input/QDATA/*` newly added company files

Why:
- new input files appear to be intentional project inputs
- this handoff document is useful to preserve

### B. Keep local-only

These should usually remain local artifacts unless the repo policy changes.

- `data/financial_pipeline.sqlite3`
- `outputs/fnguide_validation/*`
- `실행피드백.txt`

Why:
- SQLite DB is an environment/runtime artifact
- validation outputs are generated artifacts
- execution feedback file looks like local operator evidence/logging

### C. .gitignore targets

These are good candidates to ignore if they are not meant to become maintained project utilities.

- `outputs/`
- `data/financial_pipeline.sqlite3`
- `analysis_sample_metrics.py`
- `analysis_sample_revenue.py`
- `check_tables.py`
- `check_view.py`
- `check_view_rows.py`
- `inspect_columns.py`
- `inspect_table_columns.py`
- `run_create_view.py`
- `run_full_load.py`

Why:
- generated outputs and DB file should typically not be versioned
- root-level scratch/debug scripts look like local exploration helpers, not stable ETL entrypoints

### D. Delete-review candidates

These should be reviewed before deletion or cleanup because they look duplicated, obsolete, or scratch-like.

Tracked deleted files:
- `my_markdown/financial_pipeline_handoff_2026-03-24_ 2.md`
- `my_markdown/financial_pipeline_handoff_2026-03-25 _ 3.md`
- `my_markdown/financial_pipeline_project_context 03-25_  4.md`
- `my_markdown/financial_pipeline_project_summary (챗지피티 3.24 첫기획 마크다운) 1.md`
- `my_markdown/대화창 자체 기록 2 - 복사본.txt`

Untracked my_markdown files to review:
- `my_markdown/1 financial_pipeline_project_summary (챗지피티 3.24 첫기획 마크다운) 1.md`
- `my_markdown/2 financial_pipeline_handoff_2026-03-24_ 2.md`
- `my_markdown/3 financial_pipeline_handoff_2026-03-25 _ 3.md`
- `my_markdown/4 financial_pipeline_project_context 03-25_  4.md`
- `my_markdown/5 FINANCIAL_PIPELINE_MASTER_CONTEXT 03-25 5.md`
- `my_markdown/6 financial_pipeline_master_context 6.md`
- `my_markdown/7 financial_pipeline_fnguide_phase_handoff 7 FN가이드 작업중 260326.md`
- `my_markdown/8 financial_pipeline_full_worker_handoff 8 깃허브 푸시전 체크.md`
- `my_markdown/FN가이드 자료 추출 기존방식 전달 및 다른제안요청.txt`
- `my_markdown/PROJECT_CONTEXT 5.md`
- `my_markdown/대화창 자체 기록 3.txt`
- `my_markdown/작업플랜 기획.txt`
- `my_markdown/주요사항 기록...txt`
- `my_markdown/챗GPT DB화 기획 첫단계대화 - 바로 가기.lnk`
- `my_markdown/코덱스명령문_Fn가이드 첫시도 260326.txt`
- `my_markdown/*.docx`

Why:
- many appear to be duplicated handoff/context files, local notes, or shortcuts
- cleanup should be done intentionally, not automatically

## 4. Key artifact paths requiring actual existence confirmation

The next worker should confirm these first before assuming the baseline is intact.

### Database and docs
- `C:\Users\slpar\OneDrive\문서\CODEX\data\financial_pipeline.sqlite3`
- `C:\Users\slpar\OneDrive\문서\CODEX\README.md`
- `C:\Users\slpar\OneDrive\문서\CODEX\PROJECT_STATUS.md`
- `C:\Users\slpar\OneDrive\문서\CODEX\RUN_LOG.md`
- `C:\Users\slpar\OneDrive\문서\CODEX\docs\current_architecture.md`
- `C:\Users\slpar\OneDrive\문서\CODEX\docs\standard_metric_master_v2.md`
- `C:\Users\slpar\OneDrive\문서\CODEX\docs\fnguide_ingestion.md`
- `C:\Users\slpar\OneDrive\문서\CODEX\docs\fnguide_data_dictionary.md`

### Core FnGuide code
- `C:\Users\slpar\OneDrive\문서\CODEX\python\etl\debug_fnguide_layout.py`
- `C:\Users\slpar\OneDrive\문서\CODEX\python\etl\parse_fnguide.py`
- `C:\Users\slpar\OneDrive\문서\CODEX\python\etl\run_fnguide_parser.py`
- `C:\Users\slpar\OneDrive\문서\CODEX\python\etl\inspect_fnguide_load.py`

### Validation outputs
- `C:\Users\slpar\OneDrive\문서\CODEX\outputs\fnguide_validation\fnguide_layout_debug.md`
- `C:\Users\slpar\OneDrive\문서\CODEX\outputs\fnguide_validation\fnguide_validation_report.md`
- `C:\Users\slpar\OneDrive\문서\CODEX\outputs\fnguide_validation\fnguide_db_check.md`
- `C:\Users\slpar\OneDrive\문서\CODEX\outputs\fnguide_validation\samsung_consensus_financial_long.csv`
- `C:\Users\slpar\OneDrive\문서\CODEX\outputs\fnguide_validation\samsung_consensus_revision_long.csv`
- `C:\Users\slpar\OneDrive\문서\CODEX\outputs\fnguide_validation\samsung_broker_target_prices.csv`
- `C:\Users\slpar\OneDrive\문서\CODEX\outputs\fnguide_validation\samsung_report_summary.csv`
- `C:\Users\slpar\OneDrive\문서\CODEX\outputs\fnguide_validation\samsung_shareholder_snapshot.csv`
- `C:\Users\slpar\OneDrive\문서\CODEX\outputs\fnguide_validation\samsung_business_summary.txt`

## 5. Read order for the next thread

Recommended reading order:

1. `C:\Users\slpar\OneDrive\문서\CODEX\README.md`
2. `C:\Users\slpar\OneDrive\문서\CODEX\PROJECT_STATUS.md`
3. `C:\Users\slpar\OneDrive\문서\CODEX\RUN_LOG.md`
4. `C:\Users\slpar\OneDrive\문서\CODEX\docs\current_architecture.md`
5. `C:\Users\slpar\OneDrive\문서\CODEX\docs\standard_metric_master_v2.md`
6. `C:\Users\slpar\OneDrive\문서\CODEX\docs\analysis_layer_v1.md`
7. `C:\Users\slpar\OneDrive\문서\CODEX\docs\derived_metrics_v1.md`
8. `C:\Users\slpar\OneDrive\문서\CODEX\docs\fnguide_ingestion.md`
9. `C:\Users\slpar\OneDrive\문서\CODEX\docs\fnguide_data_dictionary.md`
10. `C:\Users\slpar\OneDrive\문서\CODEX\docs\data_quality_checklist.md`

## 6. Next priority task

### First priority
Expand FnGuide ingestion from the Samsung sample to a controlled multi-company batch, while keeping the current non-destructive sidecar-table design.

Why this is the best next step:
- the Samsung sample flow is already built and validated
- the project now has stable raw/integrated/enriched/analysis/derived layers
- FnGuide is the newest ingestion path and still sample-scoped
- multi-company validation will expose the next real parsing/generalization issues faster than more taxonomy work

Suggested scope:
- start with a small allowlist of additional stock codes
- rerun FnGuide debug/parser/inspect
- compare which blocks stay stable across issuers
- only after that consider DART or deeper integration into raw/integrated layers

## 7. Re-run PowerShell command

Use this one-line command to re-run the current FnGuide Samsung validation path:

```powershell
py -3 -m python.etl.debug_fnguide_layout; py -3 -m python.etl.run_fnguide_parser; py -3 -m python.etl.inspect_fnguide_load; py -3 -m unittest tests.test_parse_fnguide
```

## 8. Verification order for the next thread

Use this exact order so the next worker can continue safely without re-discovering baseline assumptions.

1. Confirm local repo state:
   - verify current branch
   - verify `HEAD` vs `origin/main`
   - inspect `git status --short`
2. Confirm DB and output existence:
   - `data/financial_pipeline.sqlite3`
   - `outputs/fnguide_validation/*`
3. Read baseline docs in the order listed above.
4. Re-run FnGuide Samsung validation:
   - debug
   - parser
   - inspect
   - tests
5. Confirm DB-side results:
   - FnGuide sidecar row counts
   - Samsung sample record counts by block
6. Compare file outputs against DB outputs:
   - validation report
   - CSVs
   - DB check markdown
7. Only after the above:
   - begin multi-company FnGuide expansion
   - or explicitly choose a different next milestone

## Quick baseline snapshot

Current working baseline to carry into the next thread:

- Financial Pipeline v2 baseline freeze is established
- analysis layer `company_metric_timeseries` is validated
- derived metrics v1 is validated
- FnGuide Samsung sample ingestion is implemented and validated
- pushed baseline commit:
  - `c0d88c1 Implement FnGuide ingestion, analysis views, derived metrics, and docs`

