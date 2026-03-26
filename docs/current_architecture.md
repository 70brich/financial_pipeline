# Current architecture

## Scope
This project is a local-first financial data pipeline built on SQLite first,
with schema and ETL code kept portable to PostgreSQL later.

Canonical source groups:

- `KDATA1`
- `KDATA2`
- `QDATA`

Only files under `data/input/KDATA1`, `data/input/KDATA2`, and
`data/input/QDATA` are treated as canonical inputs.

Additional web source extension:

- `FNGUIDE`
  - currently implemented as a non-destructive sidecar ingestion layer
  - does not mutate existing file-source constraints

## Current layers

### 1. File inventory
Table:

- `source_file`

Role:

- stores canonical file metadata
- preserves `source_group + relative_path`
- records file hash and discovery metadata

### 2. Raw observations
Table:

- `raw_observation`

Role:

- stores parsed source data in long format
- preserves raw metric names, raw company fields, raw period labels
- keeps source-specific rows separate from selected outputs

Current parsers:

- `KDATA1`
  - quarterly parser
- `KDATA2`
  - yearly parser
- `QDATA`
  - `overview`, `yearly`, `quarterly` sectors from CSV

### 2a. FnGuide web-ingestion layer
Tables:

- `fnguide_fetch_log`
- `fnguide_observation`
- `broker_target_price`
- `broker_report_summary`
- `company_shareholder_snapshot`
- `company_business_summary`

Role:

- stores requests-first web data from FnGuide
- preserves source URL, page type, mode combination, and raw payload JSON
- keeps numeric long-format observations separate from the file-ingest raw layer
- avoids destructive schema changes to the validated file-source pipeline

### 3. Integrated selected layer
Table:

- `integrated_observation`

Role:

- selects one winning raw row per exact `raw_metric_name` key
- uses company key fallback:
  - `normalized_stock_code`
  - `raw_stock_code`
  - `raw_company_name`
- applies period-aware source priority and estimate preference

Important limitation:

- this is exact-name selection only
- semantic metric merge is not implemented here

### 4. Enriched metric layer
Tables:

- `standard_metric`
- `metric_name_mapping`
- `metric_alias_map`
- `integrated_observation_enriched`

Role:

- keeps `integrated_observation` unchanged
- adds a master-keyed `standard_metric` structure
- keeps a compatibility `standard_metric_name` string
- preserves original `raw_metric_name`
- uses `normalized_metric_key` only for lookup
- leaves ambiguous metrics unmapped

Implementation note:

- `metric_name_mapping` is now the authoritative mapping table
- `metric_alias_map` is retained as a compatibility mirror
- `integrated_observation_enriched` now carries `standard_metric_id`

### 5. Analysis layer
View:

- `company_metric_timeseries`

Role:

- provides a company / metric / period / value shape for direct analysis
- joins enriched selections back to raw company identifier context
- keeps company matching optional through left-join fallback logic
- gives pandas-ready timeseries access without mutating validated source layers

### 6. Derived analysis layer
View:

- `company_metric_derived_v1`

Role:

- computes first-pass YoY and QoQ growth metrics
- computes first-pass margin metrics from base metrics
- keeps null handling explicit when prior periods or denominators are missing
- stays fully non-destructive by building only on `company_metric_timeseries`

### 7. Operations and release-management layer
Tables:

- `ingest_run`
- `source_snapshot`
- `series_change_audit`
- `release_registry`

Role:

- tracks update / rebuild / promote / rollback metadata
- keeps source-hash and release-file evidence separate from raw observations
- supports current / candidate / archive database management
- does not change validated raw, integrated, or enriched semantics by itself

## Current database file

- active current DB: `data/financial_pipeline.sqlite3`
- candidate DB directory: `data/releases/`
- archive DB directory: `data/archive/`

## Main SQL files

- `sql/003_create_base_financial_tables.sql`
- `sql/004_create_integrated_tables.sql`
- `sql/005_create_metric_mapping_tables.sql`
- `sql/006_create_standard_metric_master_tables.sql`
- `sql/007_create_analysis_views.sql`
- `sql/008_create_derived_metric_views.sql`
- `sql/009_create_fnguide_tables.sql`
- `sql/010_create_release_management_tables.sql`

See also:

- `docs/table_reference.md`
  - table-by-table reference for current layers
- `docs/metric_taxonomy_v1.md`
  - current conservative `standard_metric_name` taxonomy
- `docs/standard_metric_master_v2.md`
  - v2 master-keyed metric standardization design and verified baseline snapshot
- `docs/runbook.md`
  - execution and validation order
- `docs/script_reference.md`
  - Python entrypoint and helper summary
- `docs/analysis_layer_v1.md`
  - analysis view purpose, columns, and example SQL
- `docs/derived_metrics_v1.md`
  - derived metric view purpose, formulas, null handling, and example SQL
- `docs/fnguide_ingestion.md`
  - FnGuide ingestion flow, outputs, and execution commands
- `docs/fnguide_data_dictionary.md`
  - FnGuide table and field reference
- `docs/current_limitations.md`
  - intentionally unimplemented scope and safe next areas

## Main run order

1. Inventory canonical files
2. Parse `KDATA1`
3. Parse `KDATA2`
4. Parse `QDATA`
5. Rebuild `integrated_observation`
6. Seed `standard_metric` and `metric_name_mapping`
7. Rebuild `integrated_observation_enriched`
8. Create analysis views
9. Create derived metric views

FnGuide sample run:

1. Debug live page structure
2. Create FnGuide sidecar tables
3. Load Samsung sample data
4. Inspect DB/CSV/MD outputs

## Current baseline snapshot

The current operational baseline is `Financial Pipeline v2 standard_metric
master`.

- `standard_metric`: `79`
- active `metric_name_mapping`: `141`
- `integrated_observation_enriched`: `2432`
- rows linked to `standard_metric_id`: `2077`
- distinct coverage: `103 / 154 = 66.88%`
- row-level coverage: `2077 / 2432 = 85.40%`
- tests: `28 passed`

For the full baseline note, see:

- `docs/standard_metric_master_v2.md`
- `PROJECT_STATUS.md`

## Main operational scripts

Inventory:

- `py -3 -m python.etl.run_inventory`

Raw parsers:

- `py -3 -m python.etl.run_kdata1_parser`
- `py -3 -m python.etl.run_kdata2_parser`
- `py -3 -m python.etl.run_qdata_parser`

Selection layer:

- `py -3 -m python.etl.run_integrated_selection`

Metric enrichment:

- `py -3 -m python.etl.run_standard_metric_mapping`
- `py -3 -m python.etl.seed_standard_metric_master`
- `py -3 -m python.etl.inspect_standard_metric_master`
- `py -3 -m python.etl.inspect_unmapped_metrics`

Analysis layer:

- `py -3 -m python.etl.run_analysis_views`
- `py -3 -m python.etl.inspect_company_metric_timeseries`

Derived layer:

- `py -3 -m python.etl.run_derived_views`
- `py -3 -m python.etl.inspect_company_metric_derived`

FnGuide sidecar source:

- `py -3 -m python.etl.debug_fnguide_layout`
- `py -3 -m python.etl.run_fnguide_parser`
- `py -3 -m python.etl.inspect_fnguide_load`

Release-management source:

- `py -3 -m python.etl.run_incremental_update`
- `py -3 -m python.etl.run_full_rebuild`
- `py -3 -m python.etl.inspect_release`
- `py -3 -m python.etl.compare_release_series`
- `py -3 -m python.etl.promote_release`
- `py -3 -m python.etl.rollback_release`

## Current non-goals

Not implemented yet:

- advanced company matching
- metric semantic merge beyond exact alias mapping
- manual override workflow
- UI or Streamlit layer
- fuzzy or LLM-based mapping
- further taxonomy expansion into deferred metric families for the current version
