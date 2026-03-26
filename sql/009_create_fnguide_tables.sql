CREATE TABLE IF NOT EXISTS fnguide_fetch_log (
    fetch_log_id INTEGER PRIMARY KEY,
    company_id INTEGER,
    company_name TEXT NOT NULL,
    stock_code TEXT NOT NULL,
    page_type TEXT NOT NULL,
    ifrs_scope TEXT,
    period_scope TEXT,
    consensus_year_label TEXT,
    source_group TEXT NOT NULL DEFAULT 'FNGUIDE',
    source_url TEXT NOT NULL,
    fetch_status TEXT NOT NULL,
    notes TEXT,
    fetched_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    raw_payload_json TEXT,
    FOREIGN KEY (company_id) REFERENCES company (company_id)
);

CREATE TABLE IF NOT EXISTS fnguide_observation (
    fnguide_observation_id INTEGER PRIMARY KEY,
    company_id INTEGER,
    company_name TEXT NOT NULL,
    stock_code TEXT NOT NULL,
    source_group TEXT NOT NULL DEFAULT 'FNGUIDE',
    source_url TEXT NOT NULL,
    page_type TEXT NOT NULL,
    block_type TEXT NOT NULL,
    ifrs_scope TEXT,
    period_scope TEXT,
    consensus_year_label TEXT,
    source_row_order INTEGER,
    line_group TEXT,
    raw_metric_name TEXT NOT NULL,
    period_label_raw TEXT,
    period_type TEXT NOT NULL,
    fiscal_year INTEGER,
    fiscal_quarter INTEGER,
    date_raw TEXT,
    value_text TEXT,
    value_numeric NUMERIC,
    value_unit TEXT,
    is_estimate INTEGER NOT NULL DEFAULT 0,
    note_text TEXT,
    raw_payload_json TEXT,
    scraped_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (company_id) REFERENCES company (company_id)
);

CREATE TABLE IF NOT EXISTS company_shareholder_snapshot (
    shareholder_snapshot_id INTEGER PRIMARY KEY,
    company_id INTEGER,
    company_name TEXT NOT NULL,
    stock_code TEXT NOT NULL,
    holder_name TEXT NOT NULL,
    holder_type TEXT,
    snapshot_kind TEXT,
    shares NUMERIC,
    ownership_pct NUMERIC,
    as_of_date TEXT,
    source_group TEXT NOT NULL DEFAULT 'FNGUIDE',
    source_url TEXT NOT NULL,
    scraped_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    raw_payload_json TEXT,
    FOREIGN KEY (company_id) REFERENCES company (company_id)
);

CREATE TABLE IF NOT EXISTS company_business_summary (
    business_summary_id INTEGER PRIMARY KEY,
    company_id INTEGER,
    company_name TEXT NOT NULL,
    stock_code TEXT NOT NULL,
    summary_title TEXT,
    summary_text TEXT NOT NULL,
    as_of_date TEXT,
    source_group TEXT NOT NULL DEFAULT 'FNGUIDE',
    source_url TEXT NOT NULL,
    scraped_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (company_id) REFERENCES company (company_id)
);

CREATE TABLE IF NOT EXISTS broker_target_price (
    broker_target_price_id INTEGER PRIMARY KEY,
    company_id INTEGER,
    company_name TEXT NOT NULL,
    stock_code TEXT NOT NULL,
    broker_name TEXT NOT NULL,
    estimate_date TEXT,
    target_price NUMERIC,
    previous_target_price NUMERIC,
    change_pct NUMERIC,
    rating TEXT,
    previous_rating TEXT,
    is_consensus_aggregate INTEGER NOT NULL DEFAULT 0,
    source_group TEXT NOT NULL DEFAULT 'FNGUIDE',
    source_url TEXT NOT NULL,
    scraped_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    raw_payload_json TEXT,
    FOREIGN KEY (company_id) REFERENCES company (company_id)
);

CREATE TABLE IF NOT EXISTS broker_report_summary (
    broker_report_summary_id INTEGER PRIMARY KEY,
    company_id INTEGER,
    company_name TEXT NOT NULL,
    stock_code TEXT NOT NULL,
    report_date TEXT,
    report_title TEXT,
    report_body TEXT,
    rating_text TEXT,
    target_price_text TEXT,
    prev_close_price_text TEXT,
    provider_name TEXT,
    analyst_name TEXT,
    source_group TEXT NOT NULL DEFAULT 'FNGUIDE',
    source_url TEXT NOT NULL,
    scraped_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    raw_payload_json TEXT,
    FOREIGN KEY (company_id) REFERENCES company (company_id)
);

CREATE INDEX IF NOT EXISTS idx_fnguide_fetch_log_stock_code
    ON fnguide_fetch_log (stock_code, page_type, fetched_at);

CREATE INDEX IF NOT EXISTS idx_fnguide_observation_company_period
    ON fnguide_observation (stock_code, raw_metric_name, period_type, fiscal_year, fiscal_quarter);

CREATE INDEX IF NOT EXISTS idx_shareholder_snapshot_stock_code
    ON company_shareholder_snapshot (stock_code, snapshot_kind, as_of_date);

CREATE INDEX IF NOT EXISTS idx_business_summary_stock_code
    ON company_business_summary (stock_code, as_of_date);

CREATE INDEX IF NOT EXISTS idx_broker_target_price_stock_code
    ON broker_target_price (stock_code, estimate_date, broker_name);

CREATE INDEX IF NOT EXISTS idx_broker_report_summary_stock_code
    ON broker_report_summary (stock_code, report_date, provider_name);
