# Script reference

## Purpose

This document summarizes the current Python entrypoints and inspection helpers
used in the SQLite pipeline.

## Inventory

### `python.etl.run_inventory`

Role:

- scans canonical input folders
- refreshes `source_file`
- records scan status in `import_log`

### `python.etl.inspect_inventory`

Role:

- prints file inventory counts
- shows recent `source_file` and `import_log` rows

## Source parsers

### `python.etl.run_kdata1_parser`

Role:

- parses canonical `KDATA1` input
- rebuilds `raw_observation` rows for `source_group='KDATA1'`

### `python.etl.inspect_kdata1_load`

Role:

- shows current KDATA1 raw load status

### `python.etl.run_kdata2_parser`

Role:

- parses canonical `KDATA2` input
- rebuilds `raw_observation` rows for `source_group='KDATA2'`

### `python.etl.inspect_kdata2_load`

Role:

- shows current KDATA2 raw load status

### `python.etl.run_qdata_parser`

Role:

- parses canonical `QDATA` CSV input
- rebuilds `raw_observation` rows for `source_group='QDATA'`

### `python.etl.run_fnguide_parser`

Role:

- loads the Samsung FnGuide sample end-to-end
- rebuilds the FnGuide sidecar tables
- creates CSV / MD / TXT validation artifacts

## Debug helpers

### `python.etl.debug_kdata1_layout`

Role:

- prints top workbook cells for KDATA1 layout inspection

### `python.etl.debug_kdata2_layout`

Role:

- prints top workbook cells for KDATA2 layout inspection

### `python.etl.debug_qdata_layout`

Role:

- prints top CSV rows for QDATA block inspection

### `python.etl.debug_fnguide_layout`

Role:

- inspects live FnGuide Consensus/Main structure
- writes a markdown debug report under `outputs/fnguide_validation`

## Selected layer

### `python.etl.run_integrated_selection`

Role:

- rebuilds `integrated_observation`
- applies exact-name selection rules

### `python.etl.inspect_integrated_load`

Role:

- shows integrated row counts
- shows recent integrated rows and conflict candidate samples

## Standard metric layer

### `python.etl.run_standard_metric_mapping`

Role:

- seeds `standard_metric`
- seeds `metric_name_mapping`
- rebuilds `metric_alias_map`
- rebuilds `integrated_observation_enriched`

### `python.etl.seed_standard_metric_master`

Role:

- seeds `standard_metric`
- seeds `metric_name_mapping`
- syncs compatibility `metric_alias_map`

### `python.etl.inspect_standard_metric_mapping`

Role:

- shows distinct and row-level mapping coverage
- shows mapped and unmapped metric summaries
- shows recent enriched rows

### `python.etl.inspect_standard_metric_master`

Role:

- shows `standard_metric` master counts
- shows `metric_name_mapping` counts
- shows `standard_metric_id` linkage status in enriched rows

### `python.etl.inspect_unmapped_metrics`

Role:

- shows unmapped metrics
- shows deferred-family concentrations
- shows high-confidence and ambiguous suggestion candidates

## Analysis layer

### `python.etl.run_analysis_views`

Role:

- creates or refreshes analysis-oriented SQLite views
- currently builds `company_metric_timeseries`

### `python.etl.inspect_company_metric_timeseries`

Role:

- shows analysis-view row counts
- shows company and metric distribution samples
- shows recent timeseries samples for a top company

## Derived analysis layer

### `python.etl.run_derived_views`

Role:

- creates or refreshes derived analysis SQLite views
- currently builds `company_metric_derived_v1`

### `python.etl.inspect_company_metric_derived`

Role:

- shows derived-view row counts
- shows derived metric distribution samples
- shows sample company derived rows and null-handling samples

### `python.etl.inspect_fnguide_load`

Role:

- shows FnGuide URL/mode combinations
- shows loaded row counts and sample rows
- shows Samsung shareholder and Business Summary samples

## Notes

- Rebuild scripts replace their target layer rather than append forever.
- Raw and integrated source layers remain unchanged by enrichment scripts.
