# FnGuide data dictionary

## `fnguide_fetch_log`

Purpose:

- records live FnGuide URL/mode requests used during a run

Key fields:

- `fetch_log_id`
- `company_id`
- `company_name`
- `stock_code`
- `page_type`
- `ifrs_scope`
- `period_scope`
- `consensus_year_label`
- `source_group`
- `source_url`
- `fetch_status`
- `notes`
- `fetched_at`
- `raw_payload_json`

## `fnguide_observation`

Purpose:

- stores FnGuide numeric blocks in long format
- used for consensus financial main tables and revision timeseries

Key fields:

- `fnguide_observation_id`
- `company_id`
- `company_name`
- `stock_code`
- `source_group`
- `source_url`
- `page_type`
- `block_type`
- `ifrs_scope`
- `period_scope`
- `consensus_year_label`
- `source_row_order`
- `line_group`
- `raw_metric_name`
- `period_label_raw`
- `period_type`
- `fiscal_year`
- `fiscal_quarter`
- `date_raw`
- `value_text`
- `value_numeric`
- `value_unit`
- `is_estimate`
- `note_text`
- `raw_payload_json`
- `scraped_at`

## `broker_target_price`

Purpose:

- stores broker-level target prices and investment opinions
- also stores one synthetic `Consensus` aggregate row

Key fields:

- `broker_target_price_id`
- `company_id`
- `company_name`
- `stock_code`
- `broker_name`
- `estimate_date`
- `target_price`
- `previous_target_price`
- `change_pct`
- `rating`
- `previous_rating`
- `is_consensus_aggregate`
- `source_group`
- `source_url`
- `scraped_at`
- `raw_payload_json`

## `broker_report_summary`

Purpose:

- stores FnGuide report-summary rows

Key fields:

- `broker_report_summary_id`
- `company_id`
- `company_name`
- `stock_code`
- `report_date`
- `report_title`
- `report_body`
- `rating_text`
- `target_price_text`
- `prev_close_price_text`
- `provider_name`
- `analyst_name`
- `source_group`
- `source_url`
- `scraped_at`
- `raw_payload_json`

## `company_shareholder_snapshot`

Purpose:

- stores shareholder-detail rows and shareholder-group summary rows from
  FnGuide Main

Key fields:

- `shareholder_snapshot_id`
- `company_id`
- `company_name`
- `stock_code`
- `holder_name`
- `holder_type`
- `snapshot_kind`
- `shares`
- `ownership_pct`
- `as_of_date`
- `source_group`
- `source_url`
- `scraped_at`
- `raw_payload_json`

## `company_business_summary`

Purpose:

- stores the Business Summary title/text block from FnGuide Main

Key fields:

- `business_summary_id`
- `company_id`
- `company_name`
- `stock_code`
- `summary_title`
- `summary_text`
- `as_of_date`
- `source_group`
- `source_url`
- `scraped_at`
