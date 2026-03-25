INSERT INTO stg.customer (
    customer_id,
    customer_name,
    status_code,
    join_date,
    phone_number,
    email,
    source_file_name,
    updated_at
)
SELECT
    customer_id,
    customer_name,
    COALESCE(cm.target_value, NULLIF(status_text, '')) AS status_code,
    NULLIF(join_date_text, '')::date AS join_date,
    NULLIF(phone_text, '') AS phone_number,
    NULLIF(email_text, '') AS email,
    source_file_name,
    now()
FROM raw.customer_source r
LEFT JOIN config.code_mapping cm
    ON cm.source_table = 'raw.customer_source'
   AND cm.source_column = 'status_text'
   AND cm.source_value = r.status_text
   AND cm.is_active = true
ON CONFLICT (customer_id) DO UPDATE
SET customer_name = EXCLUDED.customer_name,
    status_code = EXCLUDED.status_code,
    join_date = EXCLUDED.join_date,
    phone_number = EXCLUDED.phone_number,
    email = EXCLUDED.email,
    source_file_name = EXCLUDED.source_file_name,
    updated_at = now();

INSERT INTO stg.contract (
    contract_id,
    customer_id,
    contract_start_date,
    contract_end_date,
    contract_status,
    source_file_name,
    updated_at
)
SELECT
    contract_id,
    customer_id,
    NULLIF(contract_start_date_text, '')::date AS contract_start_date,
    NULLIF(contract_end_date_text, '')::date AS contract_end_date,
    NULLIF(contract_status_text, '') AS contract_status,
    source_file_name,
    now()
FROM raw.contract_source
ON CONFLICT (contract_id) DO UPDATE
SET customer_id = EXCLUDED.customer_id,
    contract_start_date = EXCLUDED.contract_start_date,
    contract_end_date = EXCLUDED.contract_end_date,
    contract_status = EXCLUDED.contract_status,
    source_file_name = EXCLUDED.source_file_name,
    updated_at = now();

INSERT INTO stg.sales (
    sales_id,
    customer_id,
    contract_id,
    sales_date,
    amount,
    source_file_name,
    updated_at
)
SELECT
    sales_id,
    customer_id,
    NULLIF(contract_id, '') AS contract_id,
    NULLIF(sales_date_text, '')::date AS sales_date,
    NULLIF(REPLACE(amount_text, ',', ''), '')::numeric(18, 2) AS amount,
    source_file_name,
    now()
FROM raw.sales_source
ON CONFLICT (sales_id) DO UPDATE
SET customer_id = EXCLUDED.customer_id,
    contract_id = EXCLUDED.contract_id,
    sales_date = EXCLUDED.sales_date,
    amount = EXCLUDED.amount,
    source_file_name = EXCLUDED.source_file_name,
    updated_at = now();

INSERT INTO mart.customer_status (
    customer_id,
    active_yn,
    customer_grade,
    latest_contract_status,
    total_sales,
    rule_applied,
    calculated_at
)
SELECT
    c.customer_id,
    CASE
        WHEN MAX(ct.contract_end_date) < current_date THEN 'N'
        ELSE 'Y'
    END AS active_yn,
    CASE
        WHEN COALESCE(SUM(s.amount), 0) >= 1000000 THEN 'VIP'
        WHEN COALESCE(SUM(s.amount), 0) >= 300000 THEN 'GOLD'
        ELSE 'NORMAL'
    END AS customer_grade,
    MAX(ct.contract_status) AS latest_contract_status,
    COALESCE(SUM(s.amount), 0) AS total_sales,
    'base_rules_v1' AS rule_applied,
    now()
FROM stg.customer c
LEFT JOIN stg.contract ct
    ON ct.customer_id = c.customer_id
LEFT JOIN stg.sales s
    ON s.customer_id = c.customer_id
GROUP BY c.customer_id
ON CONFLICT (customer_id) DO UPDATE
SET active_yn = EXCLUDED.active_yn,
    customer_grade = EXCLUDED.customer_grade,
    latest_contract_status = EXCLUDED.latest_contract_status,
    total_sales = EXCLUDED.total_sales,
    rule_applied = EXCLUDED.rule_applied,
    calculated_at = now();
