DROP VIEW IF EXISTS company_metric_timeseries;

CREATE VIEW company_metric_timeseries AS
SELECT
    ioe.integrated_observation_id,
    COALESCE(company_by_id.company_id, company_by_code.company_id, ro.company_id) AS company_id,
    COALESCE(
        company_by_id.company_name,
        company_by_code.company_name,
        ro.raw_company_name,
        io.company_key
    ) AS company_name,
    io.company_key,
    ro.normalized_stock_code,
    ro.raw_stock_code,
    ioe.standard_metric_id,
    ioe.standard_metric_name,
    ioe.raw_metric_name,
    ioe.normalized_metric_key,
    io.fiscal_year,
    io.fiscal_quarter,
    io.period_type,
    io.period_label_std,
    COALESCE(io.date_raw, ro.date_raw) AS date_raw,
    COALESCE(io.selected_value_numeric, ro.value_numeric) AS value_numeric,
    COALESCE(io.selected_value_text, ro.value_text) AS value_text,
    io.selected_is_estimate AS is_estimate,
    io.selected_source_group,
    io.selection_reason
FROM integrated_observation_enriched AS ioe
JOIN integrated_observation AS io
    ON io.integrated_observation_id = ioe.integrated_observation_id
LEFT JOIN raw_observation AS ro
    ON ro.raw_observation_id = io.selected_raw_observation_id
LEFT JOIN company AS company_by_id
    ON company_by_id.company_id = ro.company_id
LEFT JOIN company AS company_by_code
    ON ro.company_id IS NULL
   AND ro.normalized_stock_code IS NOT NULL
   AND company_by_code.normalized_stock_code = ro.normalized_stock_code;
