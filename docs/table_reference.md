# Table reference

## Purpose

This document summarizes the current table layers used by the SQLite financial
pipeline.

## Inventory layer

### `source_file`

Purpose:

- stores canonical input file metadata
- preserves `source_group + relative_path`

Key fields:

- `source_file_id`
- `source_group`
- `relative_path`
- `file_name`
- `file_extension`
- `file_size_bytes`
- `file_modified_at`
- `file_hash`
- `canonical_input`
- `discovered_at`

### `import_log`

Purpose:

- stores run-level inventory/import history

Key fields:

- `import_log_id`
- `source_group`
- `run_started_at`
- `run_finished_at`
- `status`
- `files_scanned`
- `files_loaded`
- `rows_loaded`
- `error_message`
- `trigger_mode`

## Raw layer

### `raw_observation`

Purpose:

- stores parsed source data in long format
- preserves raw metric names and raw period labels

Key fields:

- `raw_observation_id`
- `source_file_id`
- `source_group`
- `sheet_name`
- `source_row_number`
- `sector_name`
- `raw_company_name`
- `raw_stock_code`
- `normalized_stock_code`
- `raw_metric_name`
- `value_text`
- `value_numeric`
- `is_estimate`
- `date_raw`
- `period_type`
- `fiscal_year`
- `fiscal_quarter`
- `period_label_raw`
- `period_label_std`
- `ingested_at`

## Selected layer

### `integrated_observation`

Purpose:

- stores one selected row per exact-name integrated key
- keeps raw source selection trace

Key fields:

- `integrated_observation_id`
- `company_key`
- `raw_metric_name`
- `period_type`
- `fiscal_year`
- `fiscal_quarter`
- `date_raw`
- `period_label_std`
- `selected_raw_observation_id`
- `selected_source_file_id`
- `selected_source_group`
- `selected_value_text`
- `selected_value_numeric`
- `selected_is_estimate`
- `selection_reason`
- `integrated_at`

Rebuild script:

- `python/etl/run_integrated_selection.py`

## Standardized layer

### `metric_alias_map`

Purpose:

- stores exact alias to `standard_metric_name` rules

Key fields:

- `metric_alias_map_id`
- `normalized_metric_key`
- `standard_metric_name`
- `is_active`
- `created_at`

### `integrated_observation_enriched`

Purpose:

- stores metric standardization results without changing integrated rows
- preserves `raw_metric_name`
- adds `normalized_metric_key`, `standard_metric_name`, `metric_variant`

Key fields:

- `integrated_observation_enriched_id`
- `integrated_observation_id`
- `company_key`
- `raw_metric_name`
- `normalized_metric_key`
- `standard_metric_name`
- `metric_variant`
- `period_type`
- `fiscal_year`
- `fiscal_quarter`
- `date_raw`
- `selected_source_group`
- `selected_raw_observation_id`
- `selected_value_numeric`
- `selected_is_estimate`
- `enriched_at`

Rebuild script:

- `python/etl/run_standard_metric_mapping.py`

## Supporting layer

### `company`

Purpose:

- reserved base company identity table
- currently not the main matching mechanism for integrated selection

Key fields:

- `company_id`
- `company_name`
- `normalized_stock_code`
- `country_code`
- `is_active`

## Notes

- `raw_metric_name` remains the source-of-truth metric label.
- `standard_metric_name` is optional and only exists in the enriched layer.
- ambiguous metrics are intentionally left unmapped.
