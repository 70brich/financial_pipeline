DROP VIEW IF EXISTS company_metric_timeseries;

CREATE VIEW company_metric_timeseries AS
SELECT
    io.integrated_observation_id,
    io.company_key,
    io.raw_metric_name,
    ioe.standard_metric_name,
    ioe.standard_metric_id,
    io.period_type,
    io.fiscal_year,
    io.fiscal_quarter,
    io.period_label_std,
    io.date_raw,

    io.selected_value_numeric AS value_numeric,

    io.selected_is_estimate AS is_estimate,
    io.selected_source_group AS source_group,
    io.selection_reason

FROM integrated_observation io
LEFT JOIN integrated_observation_enriched ioe
    ON io.integrated_observation_id = ioe.integrated_observation_id

WHERE io.selected_value_numeric IS NOT NULL;