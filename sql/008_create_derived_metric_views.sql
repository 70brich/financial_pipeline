DROP VIEW IF EXISTS company_metric_derived_v1;

CREATE VIEW company_metric_derived_v1 AS
WITH ranked_base AS (
    SELECT
        cmt.*,
        ROW_NUMBER() OVER (
            PARTITION BY
                cmt.company_key,
                cmt.standard_metric_name,
                cmt.period_type,
                COALESCE(cmt.fiscal_year, -1),
                COALESCE(cmt.fiscal_quarter, -1),
                COALESCE(cmt.date_raw, '')
            ORDER BY
                COALESCE(cmt.is_estimate, 0) ASC,
                CASE
                    WHEN cmt.period_type = 'YEAR' AND cmt.selected_source_group = 'QDATA' THEN 0
                    WHEN cmt.period_type = 'YEAR' AND cmt.selected_source_group = 'KDATA2' THEN 1
                    WHEN cmt.period_type = 'YEAR' AND cmt.selected_source_group = 'KDATA1' THEN 2
                    WHEN cmt.period_type = 'QUARTER' AND cmt.selected_source_group = 'QDATA' THEN 0
                    WHEN cmt.period_type = 'QUARTER' AND cmt.selected_source_group = 'KDATA1' THEN 1
                    WHEN cmt.period_type = 'QUARTER' AND cmt.selected_source_group = 'KDATA2' THEN 2
                    WHEN cmt.period_type = 'SNAPSHOT' AND cmt.selected_source_group = 'QDATA' THEN 0
                    WHEN cmt.period_type = 'SNAPSHOT' AND cmt.selected_source_group = 'KDATA2' THEN 1
                    WHEN cmt.period_type = 'SNAPSHOT' AND cmt.selected_source_group = 'KDATA1' THEN 2
                    ELSE 9
                END ASC,
                CASE WHEN cmt.value_numeric IS NULL THEN 1 ELSE 0 END ASC,
                cmt.integrated_observation_id DESC
        ) AS row_num
    FROM company_metric_timeseries AS cmt
    WHERE cmt.standard_metric_name IN ('REVENUE', 'OPERATING_INCOME', 'NET_INCOME', 'EPS')
),
base_metric_timeseries AS (
    SELECT
        integrated_observation_id,
        company_id,
        company_name,
        company_key,
        normalized_stock_code,
        raw_stock_code,
        standard_metric_id,
        standard_metric_name,
        raw_metric_name,
        normalized_metric_key,
        fiscal_year,
        fiscal_quarter,
        period_type,
        period_label_std,
        date_raw,
        value_numeric,
        value_text,
        is_estimate,
        selected_source_group,
        selection_reason
    FROM ranked_base
    WHERE row_num = 1
),
yoy_metrics AS (
    SELECT
        curr.integrated_observation_id AS anchor_integrated_observation_id,
        prev.integrated_observation_id AS compare_integrated_observation_id,
        curr.company_id,
        curr.company_name,
        curr.company_key,
        curr.normalized_stock_code,
        curr.raw_stock_code,
        CASE curr.standard_metric_name
            WHEN 'REVENUE' THEN 'REVENUE_YOY'
            WHEN 'OPERATING_INCOME' THEN 'OPERATING_INCOME_YOY'
            WHEN 'NET_INCOME' THEN 'NET_INCOME_YOY'
            WHEN 'EPS' THEN 'EPS_YOY'
        END AS standard_metric_name,
        curr.standard_metric_name AS base_standard_metric_name,
        prev.standard_metric_name AS compare_standard_metric_name,
        curr.period_type,
        curr.fiscal_year,
        curr.fiscal_quarter,
        curr.period_label_std,
        curr.date_raw,
        CASE
            WHEN curr.value_numeric IS NULL OR prev.value_numeric IS NULL OR prev.value_numeric = 0 THEN NULL
            ELSE ((1.0 * curr.value_numeric) - (1.0 * prev.value_numeric)) / (1.0 * prev.value_numeric)
        END AS value_numeric,
        curr.value_numeric AS current_value_numeric,
        prev.value_numeric AS compare_value_numeric,
        CASE
            WHEN COALESCE(curr.is_estimate, 0) = 1 OR COALESCE(prev.is_estimate, 0) = 1 THEN 1
            ELSE 0
        END AS is_estimate,
        CASE
            WHEN prev.selected_source_group IS NULL THEN curr.selected_source_group
            WHEN curr.selected_source_group = prev.selected_source_group THEN curr.selected_source_group
            ELSE curr.selected_source_group || '+' || prev.selected_source_group
        END AS selected_source_group,
        'YOY' AS calculation_method
    FROM base_metric_timeseries AS curr
    LEFT JOIN base_metric_timeseries AS prev
        ON prev.company_key = curr.company_key
       AND prev.standard_metric_name = curr.standard_metric_name
       AND (
            (curr.period_type = 'YEAR'
             AND prev.period_type = 'YEAR'
             AND curr.fiscal_year = prev.fiscal_year + 1)
         OR (curr.period_type = 'QUARTER'
             AND prev.period_type = 'QUARTER'
             AND curr.fiscal_year = prev.fiscal_year + 1
             AND curr.fiscal_quarter = prev.fiscal_quarter)
       )
    WHERE curr.standard_metric_name IN ('REVENUE', 'OPERATING_INCOME', 'NET_INCOME', 'EPS')
      AND curr.period_type IN ('YEAR', 'QUARTER')
),
qoq_metrics AS (
    SELECT
        curr.integrated_observation_id AS anchor_integrated_observation_id,
        prev.integrated_observation_id AS compare_integrated_observation_id,
        curr.company_id,
        curr.company_name,
        curr.company_key,
        curr.normalized_stock_code,
        curr.raw_stock_code,
        CASE curr.standard_metric_name
            WHEN 'REVENUE' THEN 'REVENUE_QOQ'
            WHEN 'OPERATING_INCOME' THEN 'OPERATING_INCOME_QOQ'
            WHEN 'NET_INCOME' THEN 'NET_INCOME_QOQ'
            WHEN 'EPS' THEN 'EPS_QOQ'
        END AS standard_metric_name,
        curr.standard_metric_name AS base_standard_metric_name,
        prev.standard_metric_name AS compare_standard_metric_name,
        curr.period_type,
        curr.fiscal_year,
        curr.fiscal_quarter,
        curr.period_label_std,
        curr.date_raw,
        CASE
            WHEN curr.value_numeric IS NULL OR prev.value_numeric IS NULL OR prev.value_numeric = 0 THEN NULL
            ELSE ((1.0 * curr.value_numeric) - (1.0 * prev.value_numeric)) / (1.0 * prev.value_numeric)
        END AS value_numeric,
        curr.value_numeric AS current_value_numeric,
        prev.value_numeric AS compare_value_numeric,
        CASE
            WHEN COALESCE(curr.is_estimate, 0) = 1 OR COALESCE(prev.is_estimate, 0) = 1 THEN 1
            ELSE 0
        END AS is_estimate,
        CASE
            WHEN prev.selected_source_group IS NULL THEN curr.selected_source_group
            WHEN curr.selected_source_group = prev.selected_source_group THEN curr.selected_source_group
            ELSE curr.selected_source_group || '+' || prev.selected_source_group
        END AS selected_source_group,
        'QOQ' AS calculation_method
    FROM base_metric_timeseries AS curr
    LEFT JOIN base_metric_timeseries AS prev
        ON prev.company_key = curr.company_key
       AND prev.standard_metric_name = curr.standard_metric_name
       AND prev.period_type = 'QUARTER'
       AND curr.period_type = 'QUARTER'
       AND (
            (curr.fiscal_quarter > 1
             AND prev.fiscal_year = curr.fiscal_year
             AND prev.fiscal_quarter = curr.fiscal_quarter - 1)
         OR (curr.fiscal_quarter = 1
             AND prev.fiscal_year = curr.fiscal_year - 1
             AND prev.fiscal_quarter = 4)
       )
    WHERE curr.standard_metric_name IN ('REVENUE', 'OPERATING_INCOME', 'NET_INCOME', 'EPS')
      AND curr.period_type = 'QUARTER'
),
operating_margin_metrics AS (
    SELECT
        revenue.integrated_observation_id AS anchor_integrated_observation_id,
        operating_income.integrated_observation_id AS compare_integrated_observation_id,
        revenue.company_id,
        revenue.company_name,
        revenue.company_key,
        revenue.normalized_stock_code,
        revenue.raw_stock_code,
        'OPERATING_MARGIN' AS standard_metric_name,
        'OPERATING_INCOME' AS base_standard_metric_name,
        'REVENUE' AS compare_standard_metric_name,
        revenue.period_type,
        revenue.fiscal_year,
        revenue.fiscal_quarter,
        revenue.period_label_std,
        revenue.date_raw,
        CASE
            WHEN operating_income.value_numeric IS NULL OR revenue.value_numeric IS NULL OR revenue.value_numeric = 0 THEN NULL
            ELSE (1.0 * operating_income.value_numeric) / (1.0 * revenue.value_numeric)
        END AS value_numeric,
        operating_income.value_numeric AS current_value_numeric,
        revenue.value_numeric AS compare_value_numeric,
        CASE
            WHEN COALESCE(revenue.is_estimate, 0) = 1 OR COALESCE(operating_income.is_estimate, 0) = 1 THEN 1
            ELSE 0
        END AS is_estimate,
        CASE
            WHEN operating_income.selected_source_group IS NULL THEN revenue.selected_source_group
            WHEN revenue.selected_source_group = operating_income.selected_source_group THEN revenue.selected_source_group
            ELSE revenue.selected_source_group || '+' || operating_income.selected_source_group
        END AS selected_source_group,
        'MARGIN' AS calculation_method
    FROM base_metric_timeseries AS revenue
    LEFT JOIN base_metric_timeseries AS operating_income
        ON operating_income.company_key = revenue.company_key
       AND operating_income.standard_metric_name = 'OPERATING_INCOME'
       AND (
            (revenue.period_type = 'YEAR'
             AND operating_income.period_type = 'YEAR'
             AND revenue.fiscal_year = operating_income.fiscal_year)
         OR (revenue.period_type = 'QUARTER'
             AND operating_income.period_type = 'QUARTER'
             AND revenue.fiscal_year = operating_income.fiscal_year
             AND revenue.fiscal_quarter = operating_income.fiscal_quarter)
         OR (revenue.period_type = 'SNAPSHOT'
             AND operating_income.period_type = 'SNAPSHOT'
             AND COALESCE(revenue.date_raw, '') = COALESCE(operating_income.date_raw, ''))
       )
    WHERE revenue.standard_metric_name = 'REVENUE'
      AND revenue.period_type IN ('YEAR', 'QUARTER', 'SNAPSHOT')
),
net_margin_metrics AS (
    SELECT
        revenue.integrated_observation_id AS anchor_integrated_observation_id,
        net_income.integrated_observation_id AS compare_integrated_observation_id,
        revenue.company_id,
        revenue.company_name,
        revenue.company_key,
        revenue.normalized_stock_code,
        revenue.raw_stock_code,
        'NET_MARGIN' AS standard_metric_name,
        'NET_INCOME' AS base_standard_metric_name,
        'REVENUE' AS compare_standard_metric_name,
        revenue.period_type,
        revenue.fiscal_year,
        revenue.fiscal_quarter,
        revenue.period_label_std,
        revenue.date_raw,
        CASE
            WHEN net_income.value_numeric IS NULL OR revenue.value_numeric IS NULL OR revenue.value_numeric = 0 THEN NULL
            ELSE (1.0 * net_income.value_numeric) / (1.0 * revenue.value_numeric)
        END AS value_numeric,
        net_income.value_numeric AS current_value_numeric,
        revenue.value_numeric AS compare_value_numeric,
        CASE
            WHEN COALESCE(revenue.is_estimate, 0) = 1 OR COALESCE(net_income.is_estimate, 0) = 1 THEN 1
            ELSE 0
        END AS is_estimate,
        CASE
            WHEN net_income.selected_source_group IS NULL THEN revenue.selected_source_group
            WHEN revenue.selected_source_group = net_income.selected_source_group THEN revenue.selected_source_group
            ELSE revenue.selected_source_group || '+' || net_income.selected_source_group
        END AS selected_source_group,
        'MARGIN' AS calculation_method
    FROM base_metric_timeseries AS revenue
    LEFT JOIN base_metric_timeseries AS net_income
        ON net_income.company_key = revenue.company_key
       AND net_income.standard_metric_name = 'NET_INCOME'
       AND (
            (revenue.period_type = 'YEAR'
             AND net_income.period_type = 'YEAR'
             AND revenue.fiscal_year = net_income.fiscal_year)
         OR (revenue.period_type = 'QUARTER'
             AND net_income.period_type = 'QUARTER'
             AND revenue.fiscal_year = net_income.fiscal_year
             AND revenue.fiscal_quarter = net_income.fiscal_quarter)
         OR (revenue.period_type = 'SNAPSHOT'
             AND net_income.period_type = 'SNAPSHOT'
             AND COALESCE(revenue.date_raw, '') = COALESCE(net_income.date_raw, ''))
       )
    WHERE revenue.standard_metric_name = 'REVENUE'
      AND revenue.period_type IN ('YEAR', 'QUARTER', 'SNAPSHOT')
)
SELECT * FROM yoy_metrics
UNION ALL
SELECT * FROM qoq_metrics
UNION ALL
SELECT * FROM operating_margin_metrics
UNION ALL
SELECT * FROM net_margin_metrics;
