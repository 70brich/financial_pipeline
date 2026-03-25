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

- rebuilds `metric_alias_map`
- rebuilds `integrated_observation_enriched`

### `python.etl.inspect_standard_metric_mapping`

Role:

- shows distinct and row-level mapping coverage
- shows mapped and unmapped metric summaries
- shows recent enriched rows

## Notes

- Rebuild scripts replace their target layer rather than append forever.
- Raw and integrated source layers remain unchanged by enrichment scripts.
