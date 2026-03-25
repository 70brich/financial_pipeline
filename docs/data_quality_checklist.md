# Data quality checklist

## Purpose

This document summarizes practical data quality and validation checks for the
current SQLite-first financial pipeline.

It is intended for operational validation of the Financial Pipeline v1
baseline, not taxonomy expansion.

See also:

- `docs/metric_taxonomy_v1.md`
  - current conservative taxonomy baseline
- `docs/current_architecture.md`
  - current pipeline layers and run order

## Pipeline layers and validation points

### `source_file`

Purpose:

- tracks canonical input files under `data/input/KDATA1`
- tracks canonical input files under `data/input/KDATA2`
- tracks canonical input files under `data/input/QDATA`

Validation points:

- only canonical folders are inventoried
- `source_group` is derived from folder path, not filename
- `source_group + relative_path` is stable and unique
- `file_hash`, size, extension, and modified time are populated

Typical questions:

- were all canonical input files discovered?
- were loose files under `data/input/` ignored?
- did a rerun update existing file metadata rather than create duplicates?

### `raw_observation`

Purpose:

- stores long-format parsed observations from each source group
- preserves raw metric labels, raw period values, and source trace fields

Validation points:

- expected rows were loaded for each `source_group`
- required source trace fields are populated
- period fields are populated according to source-specific rules
- stale rows are replaced on rerun for the same `source_file_id + source_group`

Typical questions:

- did the parser load rows at all?
- are `raw_metric_name`, `date_raw`, and period fields populated sensibly?
- are `is_estimate` values present where explicit estimate hints exist?

### `integrated_observation`

Purpose:

- stores one selected row per exact-name integrated key
- preserves which raw row won selection

Validation points:

- selection produced one row per integrated key
- `selected_raw_observation_id` points to a real raw row
- source priority and estimate preference behaved as expected
- duplicate raw candidates collapse to one selected row

Typical questions:

- did integrated rebuild complete without leaving duplicates?
- do selected rows reference valid raw rows?
- do known collisions resolve to the expected source group?

### `integrated_observation_enriched`

Purpose:

- preserves integrated rows
- adds `normalized_metric_key`, `metric_variant`, and optional
  `standard_metric_name`

Validation points:

- `raw_metric_name` remains unchanged
- `normalized_metric_key` is generated consistently
- `standard_metric_name` is populated only when an approved exact alias exists
- deferred families remain unmapped

Typical questions:

- do mapped metrics resolve to the intended standard names?
- are ambiguous or deferred metrics still unmapped?
- does coverage remain stable across rebuilds?

## Data validation rules

### Row count consistency between layers

Recommended checks:

- `source_file`
  - canonical file count should match the number of files under the three
    canonical input folders
- `raw_observation`
  - each parser run should produce a non-zero row count for its intended source
    group when canonical inputs exist
- `integrated_observation`
  - row count should be less than or equal to `raw_observation`
  - row count should remain stable across repeated rebuilds when inputs are
    unchanged
- `integrated_observation_enriched`
  - row count should match `integrated_observation`
  - enrichment should not create or drop integrated rows

Operational expectation:

- `integrated_observation_enriched_rows == integrated_observation_rows`

### Required field checks

Recommended minimum checks by layer:

`source_file`

- `source_group` is not null
- `relative_path` is not null
- `file_name` is not null
- `canonical_input` is populated

`raw_observation`

- `source_file_id` is not null
- `source_group` is not null
- `raw_metric_name` should be present for valid loaded rows
- `period_type` is not null
- `date_raw` should be present when the source provides a date-based period
- `fiscal_year` should be present for `YEAR` and `QUARTER` rows
- `fiscal_quarter` should be present for `QUARTER` rows

`integrated_observation`

- `company_key` is not null for valid selected rows
- `raw_metric_name` is not empty
- `selected_raw_observation_id` is not null
- `selected_source_group` is not null

`integrated_observation_enriched`

- `integrated_observation_id` is not null
- `company_key` is not null
- `raw_metric_name` is preserved
- `normalized_metric_key` is not null
- `standard_metric_name` may be null by design

### `normalized_metric_key` generation checks

Current rules:

- preserve `raw_metric_name` exactly
- use `normalized_metric_key` only for lookup
- strip lookup-only cosmetic prefixes `-`, `+`, `=`
- extract and preserve metric variants like `개별`, `연결`, `분기`, `연간`
- collapse repeated spaces
- casefold for stable alias lookup

Validation questions:

- does `raw_metric_name` remain unchanged after enrichment?
- do `- 매출액`, `+ 매출액`, `=매출액` normalize to the same lookup key?
- do `(개별)자본총계` and `자본총계` preserve different `metric_variant` values
  while sharing the same normalized lookup key?
- do deferred suffix-heavy metrics such as `PER(5년평균)` remain distinct and
  unmapped?

### Alias mapping coverage checks

Coverage should be checked at two levels:

- distinct coverage
  - how many distinct `raw_metric_name` values are mapped
- row-level coverage
  - how many total enriched rows receive a `standard_metric_name`

Recommended checks:

- coverage should not unexpectedly drop after a rebuild
- newly added aliases should increase or preserve coverage
- deferred families should remain unmapped unless policy changes

## Standard metric mapping validation

### How to verify alias mappings

Use these checks:

- confirm the intended alias appears in `metric_alias_map`
- confirm the expected `normalized_metric_key` is present
- rebuild the enriched layer
- inspect recent enriched rows and row counts by `standard_metric_name`

Examples of what to verify:

- `raw_metric_name` still shows the original source label
- `standard_metric_name` is added only when an exact approved alias exists
- `metric_variant` is preserved for prefixed names such as `(개별)매출액`

### How to detect unmapped metrics

Look for:

- top unmapped `raw_metric_name`
- top unmapped `normalized_metric_key`
- symbol-prefixed unmapped rows
- policy-bucket summaries for deferred families

These checks help distinguish:

- safe exact-alias misses
- intentionally deferred metrics
- possible normalization bugs

### Inspection workflow using `inspect_standard_metric_mapping`

Recommended command:

```powershell
py -3 -m python.etl.inspect_standard_metric_mapping
```

Review these sections in order:

1. `Distinct coverage summary`
2. `Row-level coverage summary`
3. approved batch row-count sections
4. `Top unmapped raw_metric_name`
5. `Top unmapped normalized_metric_key`
6. escaped unmapped samples
7. `Unmapped rows with active alias present`
8. `Recent enriched rows`

What to watch for:

- coverage unexpectedly dropping
- mapped metrics disappearing from approved row-count sections
- unmapped rows that already have an active alias
- raw labels changing when they should remain preserved

## Recommended validation workflow for new datasets

### 1. Inventory validation

Run:

```powershell
py -3 -m python.etl.run_inventory; py -3 -m python.etl.inspect_inventory
```

Check:

- canonical files were discovered
- `source_group` counts are sensible
- loose files were ignored

### 2. Source-specific raw load validation

Run parsers and inspectors for the relevant sources.

Examples:

```powershell
py -3 -m python.etl.run_kdata1_parser; py -3 -m python.etl.inspect_kdata1_load
```

```powershell
py -3 -m python.etl.run_kdata2_parser; py -3 -m python.etl.inspect_kdata2_load
```

```powershell
py -3 -m python.etl.run_qdata_parser
```

Check:

- raw row counts are non-zero
- `raw_metric_name` looks correct
- `date_raw`, `fiscal_year`, `fiscal_quarter`, and `period_label_std` are
  populated where expected

### 3. Integrated layer validation

Run:

```powershell
py -3 -m python.etl.run_integrated_selection; py -3 -m python.etl.inspect_integrated_load
```

Check:

- one selected row exists per integrated key
- selected source groups look reasonable
- estimate preference and source priority appear correct

### 4. Enriched layer validation

Run:

```powershell
py -3 -m python.etl.run_standard_metric_mapping; py -3 -m python.etl.inspect_standard_metric_mapping
```

Check:

- enriched row count matches integrated row count
- approved `standard_metric_name` values appear in expected row-count sections
- deferred families remain unmapped

### 5. Regression test validation

Run:

```powershell
py -3 -m unittest tests.test_metric_mapping
```

Check:

- exact alias rules still pass
- deferred families still remain unmapped
- prefix normalization and variant handling still behave correctly

## Current stabilization guidance

For the current version:

- do not expand taxonomy without a new explicit policy decision
- prefer validation, documentation, and targeted regression checks
- treat unexpected coverage drops as a pipeline issue
- treat newly discovered unmapped metrics as review items, not automatic mapping
