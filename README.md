# Financial Pipeline

This project builds a local-first financial data pipeline on SQLite, with schema
and ETL code kept portable to PostgreSQL later.

## Project docs

- `docs/current_architecture.md`
  - current operational architecture and table layer summary
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

## Current status

The pipeline currently supports these layers:

- `source_file`
  - canonical file inventory for `KDATA1`, `KDATA2`, `QDATA`
- `raw_observation`
  - long-format raw observations parsed from each source group
- `integrated_observation`
  - exact `raw_metric_name` based selected layer
- `integrated_observation_enriched`
  - rule-based `standard_metric_name` enrichment layer

The current canonical inputs are:

- `data/input/KDATA1`
- `data/input/KDATA2`
- `data/input/QDATA`

Loose files directly under `data/input/` are ignored.

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
```

## SQL files

- `sql/003_create_base_financial_tables.sql`
  - base SQLite-first tables for company, file inventory, raw observations, import log
- `sql/004_create_integrated_tables.sql`
  - integrated selected layer
- `sql/005_create_metric_mapping_tables.sql`
  - metric alias map and enriched metric layer

## Current scope

Implemented:

- canonical source file inventory
- KDATA1 parser
- KDATA2 parser
- QDATA parser
- exact-name integrated selection
- rule-based standard metric enrichment
- documented conservative metric taxonomy v1
- documented data quality and validation checklist for the v1 baseline

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
