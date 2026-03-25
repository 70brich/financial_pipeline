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

- `metric_alias_map`
- `integrated_observation_enriched`

Role:

- keeps `integrated_observation` unchanged
- adds rule-based `standard_metric_name`
- preserves original `raw_metric_name`
- uses `normalized_metric_key` only for lookup
- leaves ambiguous metrics unmapped

## Current database file

- `data/financial_pipeline.sqlite3`

## Main SQL files

- `sql/003_create_base_financial_tables.sql`
- `sql/004_create_integrated_tables.sql`
- `sql/005_create_metric_mapping_tables.sql`

See also:

- `docs/table_reference.md`
  - table-by-table reference for current layers
- `docs/metric_taxonomy_v1.md`
  - current conservative `standard_metric_name` taxonomy
- `docs/runbook.md`
  - execution and validation order
- `docs/script_reference.md`
  - Python entrypoint and helper summary
- `docs/current_limitations.md`
  - intentionally unimplemented scope and safe next areas

## Main run order

1. Inventory canonical files
2. Parse `KDATA1`
3. Parse `KDATA2`
4. Parse `QDATA`
5. Rebuild `integrated_observation`
6. Rebuild `integrated_observation_enriched`

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

## Current non-goals

Not implemented yet:

- advanced company matching
- metric semantic merge beyond exact alias mapping
- manual override workflow
- UI or Streamlit layer
- fuzzy or LLM-based mapping
- further taxonomy expansion into deferred metric families for the current version
