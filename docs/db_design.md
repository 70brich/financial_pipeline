# Database design draft

## Main tables
- company
- source_file
- company_identifier_map
- metric_dictionary
- standard_metric
- metric_name_mapping
- raw_observation
- fnguide_observation
- integrated_observation
- integrated_observation_enriched
- manual_override
- import_log

## Key principles
- company stores standardized company identity
- source_file stores import file metadata and source_group
- company_identifier_map stores raw-to-standard company mapping and code resolution history
- metric_dictionary stores raw-to-standard metric mapping
- standard_metric stores the approved master metric taxonomy
- metric_name_mapping stores normalized raw-name to standard-metric mappings
- raw_observation stores all imported observations in long format
- fnguide_observation stores long-format numeric observations from the FnGuide web source
- integrated_observation stores final selected analysis-ready values
- integrated_observation_enriched stores normalized metric output while preserving raw names
- manual_override stores manual source/value preferences
- import_log stores run-level import history

## FnGuide sidecar tables

- fnguide_fetch_log
- broker_target_price
- broker_report_summary
- company_shareholder_snapshot
- company_business_summary

## Current implementation note

The current project now uses a non-destructive hybrid structure:

- `metric_name_mapping` is the authoritative v2 mapping table
- `metric_alias_map` is retained for compatibility with the v1 enrichment flow
- `integrated_observation_enriched` keeps `standard_metric_name` and now also
  stores `standard_metric_id`
