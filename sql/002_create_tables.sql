CREATE TABLE IF NOT EXISTS raw.load_audit (
    load_id bigserial PRIMARY KEY,
    source_file_name text NOT NULL,
    source_type text NOT NULL,
    target_table text NOT NULL,
    loaded_rows integer NOT NULL DEFAULT 0,
    load_status text NOT NULL DEFAULT 'SUCCESS',
    error_message text,
    loaded_at timestamp NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS raw.customer_source (
    raw_id bigserial PRIMARY KEY,
    source_file_name text NOT NULL,
    source_sheet_name text,
    source_row_no integer,
    customer_id text,
    customer_name text,
    status_text text,
    join_date_text text,
    phone_text text,
    email_text text,
    loaded_at timestamp NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS raw.contract_source (
    raw_id bigserial PRIMARY KEY,
    source_file_name text NOT NULL,
    source_sheet_name text,
    source_row_no integer,
    contract_id text,
    customer_id text,
    contract_start_date_text text,
    contract_end_date_text text,
    contract_status_text text,
    loaded_at timestamp NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS raw.sales_source (
    raw_id bigserial PRIMARY KEY,
    source_file_name text NOT NULL,
    source_row_no integer,
    sales_id text,
    customer_id text,
    contract_id text,
    sales_date_text text,
    amount_text text,
    loaded_at timestamp NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS config.code_mapping (
    mapping_id bigserial PRIMARY KEY,
    source_table text NOT NULL,
    source_column text NOT NULL,
    source_value text NOT NULL,
    target_value text NOT NULL,
    is_active boolean NOT NULL DEFAULT true,
    created_at timestamp NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS config.business_rule (
    rule_id text PRIMARY KEY,
    target_table text NOT NULL,
    target_column text NOT NULL,
    condition_description text NOT NULL,
    result_expression text NOT NULL,
    priority integer NOT NULL DEFAULT 100,
    is_active boolean NOT NULL DEFAULT true,
    created_at timestamp NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS stg.customer (
    customer_id text PRIMARY KEY,
    customer_name text,
    status_code text,
    join_date date,
    phone_number text,
    email text,
    source_file_name text,
    updated_at timestamp NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS stg.contract (
    contract_id text PRIMARY KEY,
    customer_id text NOT NULL,
    contract_start_date date,
    contract_end_date date,
    contract_status text,
    source_file_name text,
    updated_at timestamp NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS stg.sales (
    sales_id text PRIMARY KEY,
    customer_id text NOT NULL,
    contract_id text,
    sales_date date,
    amount numeric(18, 2),
    source_file_name text,
    updated_at timestamp NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS mart.customer_status (
    customer_id text PRIMARY KEY,
    active_yn char(1),
    customer_grade text,
    latest_contract_status text,
    total_sales numeric(18, 2),
    rule_applied text,
    calculated_at timestamp NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_raw_customer_source_customer_id
    ON raw.customer_source (customer_id);

CREATE INDEX IF NOT EXISTS idx_raw_contract_source_customer_id
    ON raw.contract_source (customer_id);

CREATE INDEX IF NOT EXISTS idx_raw_sales_source_customer_id
    ON raw.sales_source (customer_id);
