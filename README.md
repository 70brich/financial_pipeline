# Financial Pipeline

This project builds a local-first financial data pipeline on SQLite, with schema
and ETL code kept portable to PostgreSQL later.

## Project docs

- `docs/current_architecture.md`
  - current operational architecture and table layer summary
- `docs/standard_metric_master_v2.md`
  - v2 `standard_metric` master baseline, seed flow, and verified baseline snapshot
- `docs/analysis_layer_v1.md`
  - analysis-oriented `company_metric_timeseries` view and example SQL
- `docs/derived_metrics_v1.md`
  - first-pass YoY, QoQ, and margin derived metrics built on the analysis layer
- `docs/fnguide_ingestion.md`
  - FnGuide Samsung sample ingestion flow, outputs, and commands
- `docs/fnguide_data_dictionary.md`
  - FnGuide source table dictionary
- `docs/runbook.md`
  - rebuild order and validation commands
- `docs/table_reference.md`
  - current table-by-table reference
- `docs/script_reference.md`
  - current Python entrypoint reference
- `docs/current_limitations.md`
  - intentionally unimplemented scope and safe next areas
- `docs/data_quality_checklist.md`
  - operational data quality and validation checklist for the current pipeline
- `docs/metric_taxonomy_v1.md`
  - current conservative `standard_metric_name` taxonomy and deferred families
- `docs/db_design.md`
  - database design draft
- `docs/data_rules.md`
  - current data handling rules
- `docs/v1_release_notes.md`
  - v1 closeout plus v2 master extension handoff note

## Current status

Financial Pipeline is currently operating on the `v2 standard_metric master`
baseline.

Transition note:

- v1 established the validated raw, integrated, and enriched pipeline
- v2 keeps those validated layers intact and adds the master-keyed
  `standard_metric` and `metric_name_mapping` structure on top
- this project should now be treated as the frozen `Financial Pipeline v2
  baseline`

Baseline snapshot:

- `standard_metric`: `79`
- active `metric_name_mapping`: `141`
- `integrated_observation_enriched`: `2432`
- rows linked to `standard_metric_id`: `2077`
- distinct coverage: `66.88%`
- row-level coverage: `85.40%`
- tests: `28 passed`

See:

- `docs/standard_metric_master_v2.md`
- `docs/current_architecture.md`
- `PROJECT_STATUS.md`

The pipeline currently supports these layers:

- `source_file`
  - canonical file inventory for `KDATA1`, `KDATA2`, `QDATA`
- `raw_observation`
  - long-format raw observations parsed from each source group
- `integrated_observation`
  - exact `raw_metric_name` based selected layer
- `integrated_observation_enriched`
  - rule-based `standard_metric_name` enrichment layer with `standard_metric_id`
- `company_metric_timeseries`
  - analysis-oriented SQLite view for company / metric / period / value queries
- `company_metric_derived_v1`
  - derived analysis SQLite view for YoY, QoQ, and margin metrics

The current canonical inputs are:

- `data/input/KDATA1`
- `data/input/KDATA2`
- `data/input/QDATA`

Loose files directly under `data/input/` are ignored.

Additional web source:

- `FNGUIDE`
  - requests-first web ingestion for the Samsung sample implementation
  - stored in dedicated sidecar tables to avoid breaking current file-source
    constraints

## Source groups

- `KDATA1`
  - quarterly source
- `KDATA2`
  - yearly source
- `QDATA`
  - CSV source interpreted as `overview`, `yearly`, `quarterly`

## SQLite database

The local SQLite database file is:

- `data/financial_pipeline.sqlite3`

## Main scripts

Inventory:

```powershell
py -3 -m python.etl.run_inventory
```

KDATA1:

```powershell
py -3 -m python.etl.run_kdata1_parser
py -3 -m python.etl.inspect_kdata1_load
```

KDATA2:

```powershell
py -3 -m python.etl.debug_kdata2_layout
py -3 -m python.etl.run_kdata2_parser; py -3 -m python.etl.inspect_kdata2_load
```

QDATA:

```powershell
py -3 -m python.etl.debug_qdata_layout
py -3 -m python.etl.run_qdata_parser
```

Integrated selection:

```powershell
py -3 -m python.etl.run_integrated_selection
py -3 -m python.etl.inspect_integrated_load
```

Standard metric mapping:

```powershell
py -3 -m python.etl.run_standard_metric_mapping
py -3 -m python.etl.inspect_standard_metric_mapping
py -3 -m python.etl.inspect_standard_metric_master
py -3 -m python.etl.inspect_unmapped_metrics
```

Analysis layer:

```powershell
py -3 -m python.etl.run_analysis_views
py -3 -m python.etl.inspect_company_metric_timeseries
```

Derived metrics layer:

```powershell
py -3 -m python.etl.run_derived_views
py -3 -m python.etl.inspect_company_metric_derived
```

FnGuide source:

```powershell
py -3 -m python.etl.debug_fnguide_layout
py -3 -m python.etl.run_fnguide_parser
py -3 -m python.etl.inspect_fnguide_load
py -3 -m unittest tests.test_parse_fnguide
```

Release management scaffold:

```powershell
py -3 -m python.etl.run_incremental_update
py -3 -m python.etl.run_full_rebuild --release-label 2026Q2_candidate
py -3 -m python.etl.inspect_release
py -3 -m python.etl.compare_release_series --release-label 2026Q2_candidate
```

Current derived layer snapshot:

- `company_metric_derived_v1`: `440`
- top derived counts:
  - `EPS_YOY = 49`
  - `NET_INCOME_YOY = 49`
  - `NET_MARGIN = 49`
  - `OPERATING_MARGIN = 47`

Current analysis layer snapshot:

- `company_metric_timeseries`: `2432`
- `YEAR / QUARTER / SNAPSHOT`: `1247 / 1158 / 27`

## SQL files

- `sql/003_create_base_financial_tables.sql`
  - base SQLite-first tables for company, file inventory, raw observations, import log
- `sql/004_create_integrated_tables.sql`
  - integrated selected layer
- `sql/005_create_metric_mapping_tables.sql`
  - metric alias map and enriched metric layer
- `sql/006_create_standard_metric_master_tables.sql`
  - standard metric master and authoritative metric-name mapping layer
- `sql/007_create_analysis_views.sql`
  - non-destructive analysis views built on top of the validated baseline
- `sql/008_create_derived_metric_views.sql`
  - non-destructive derived metric views built on top of the analysis layer
- `sql/009_create_fnguide_tables.sql`
  - non-destructive FnGuide sidecar ingestion tables
- `sql/010_create_release_management_tables.sql`
  - non-destructive update / rebuild / release management metadata tables

## Current scope

Implemented:

- canonical source file inventory
- KDATA1 parser
- KDATA2 parser
- QDATA parser
- exact-name integrated selection
- rule-based standard metric enrichment
- master-keyed `standard_metric` and `metric_name_mapping` layer
- analysis-oriented `company_metric_timeseries` view
- derived metric `company_metric_derived_v1` view
- documented conservative metric taxonomy v1
- documented data quality and validation checklist for the v1 baseline
- metadata-first update / rebuild / release management scaffold

Not implemented yet:

- company matching beyond simple company key fallback
- metric semantic merge beyond exact alias mapping
- manual overrides
- UI / Streamlit
- fuzzy or LLM-based mapping

## Notes

- `raw_metric_name` is preserved as-is.
- `standard_metric_name` is added only in the enriched layer.
- ambiguous metrics remain unmapped by design.
