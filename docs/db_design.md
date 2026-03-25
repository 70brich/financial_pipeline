# Database design draft

## Main tables
- company
- source_file
- company_identifier_map
- metric_dictionary
- raw_observation
- integrated_observation
- manual_override
- import_log

## Key principles
- company stores standardized company identity
- source_file stores import file metadata and source_group
- company_identifier_map stores raw-to-standard company mapping and code resolution history
- metric_dictionary stores raw-to-standard metric mapping
- raw_observation stores all imported observations in long format
- integrated_observation stores final selected analysis-ready values
- manual_override stores manual source/value preferences
- import_log stores run-level import history
