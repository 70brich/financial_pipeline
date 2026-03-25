CREATE TABLE IF NOT EXISTS company (
    company_id INTEGER PRIMARY KEY,
    company_name TEXT NOT NULL,
    normalized_stock_code TEXT,
    country_code TEXT,
    is_active INTEGER NOT NULL DEFAULT 1,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_company_normalized_stock_code UNIQUE (normalized_stock_code),
    CONSTRAINT ck_company_is_active CHECK (is_active IN (0, 1)),
    CONSTRAINT ck_company_normalized_stock_code_length CHECK (
        normalized_stock_code IS NULL OR length(normalized_stock_code) = 6
    )
);

CREATE TABLE IF NOT EXISTS source_file (
    source_file_id INTEGER PRIMARY KEY,
    source_group TEXT NOT NULL,
    relative_path TEXT NOT NULL,
    file_name TEXT NOT NULL,
    file_extension TEXT NOT NULL,
    file_size_bytes INTEGER,
    file_modified_at TEXT,
    file_hash TEXT,
    canonical_input INTEGER NOT NULL DEFAULT 1,
    discovered_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_source_file_source_group_relative_path UNIQUE (source_group, relative_path),
    CONSTRAINT ck_source_file_source_group CHECK (
        source_group IN ('KDATA1', 'KDATA2', 'QDATA')
    ),
    CONSTRAINT ck_source_file_canonical_input CHECK (canonical_input IN (0, 1))
);

CREATE TABLE IF NOT EXISTS import_log (
    import_log_id INTEGER PRIMARY KEY,
    source_group TEXT,
    run_started_at TEXT NOT NULL,
    run_finished_at TEXT,
    status TEXT NOT NULL,
    files_scanned INTEGER NOT NULL DEFAULT 0,
    files_loaded INTEGER NOT NULL DEFAULT 0,
    rows_loaded INTEGER NOT NULL DEFAULT 0,
    error_message TEXT,
    trigger_mode TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT ck_import_log_source_group CHECK (
        source_group IS NULL OR source_group IN ('KDATA1', 'KDATA2', 'QDATA')
    ),
    CONSTRAINT ck_import_log_status CHECK (
        status IN ('STARTED', 'SUCCESS', 'FAILED', 'PARTIAL', 'SKIPPED')
    )
);

CREATE TABLE IF NOT EXISTS raw_observation (
    raw_observation_id INTEGER PRIMARY KEY,
    source_file_id INTEGER NOT NULL,
    source_group TEXT NOT NULL,
    import_log_id INTEGER,
    sheet_name TEXT,
    source_row_number INTEGER,
    sector_name TEXT,
    raw_company_name TEXT,
    raw_stock_code TEXT,
    normalized_stock_code TEXT,
    company_id INTEGER,
    raw_metric_name TEXT NOT NULL,
    standard_metric_name TEXT,
    value_text TEXT,
    value_numeric NUMERIC,
    value_unit TEXT,
    value_nature TEXT,
    is_estimate INTEGER NOT NULL DEFAULT 0,
    date_raw TEXT,
    raw_period_label TEXT,
    period_label_raw TEXT,
    period_type TEXT NOT NULL,
    fiscal_year INTEGER,
    fiscal_quarter INTEGER,
    normalized_quarter_label TEXT,
    period_label_std TEXT,
    ingested_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_raw_observation_source_file
        FOREIGN KEY (source_file_id) REFERENCES source_file (source_file_id),
    CONSTRAINT fk_raw_observation_company
        FOREIGN KEY (company_id) REFERENCES company (company_id),
    CONSTRAINT fk_raw_observation_import_log
        FOREIGN KEY (import_log_id) REFERENCES import_log (import_log_id),
    CONSTRAINT ck_raw_observation_source_group CHECK (
        source_group IN ('KDATA1', 'KDATA2', 'QDATA')
    ),
    CONSTRAINT ck_raw_observation_is_estimate CHECK (is_estimate IN (0, 1)),
    CONSTRAINT ck_raw_observation_period_type CHECK (
        period_type IN ('SNAPSHOT', 'YEAR', 'QUARTER')
    ),
    CONSTRAINT ck_raw_observation_fiscal_quarter CHECK (
        fiscal_quarter IS NULL OR fiscal_quarter IN (1, 2, 3, 4)
    ),
    CONSTRAINT ck_raw_observation_normalized_stock_code_length CHECK (
        normalized_stock_code IS NULL OR length(normalized_stock_code) = 6
    )
);

CREATE INDEX IF NOT EXISTS idx_company_normalized_stock_code
    ON company (normalized_stock_code);

CREATE INDEX IF NOT EXISTS idx_source_file_source_group
    ON source_file (source_group);

CREATE INDEX IF NOT EXISTS idx_raw_observation_source_file_id
    ON raw_observation (source_file_id);

CREATE INDEX IF NOT EXISTS idx_raw_observation_company_id
    ON raw_observation (company_id);

CREATE INDEX IF NOT EXISTS idx_raw_observation_lookup
    ON raw_observation (
        source_group,
        normalized_stock_code,
        standard_metric_name,
        fiscal_year,
        fiscal_quarter
    );

CREATE INDEX IF NOT EXISTS idx_import_log_status
    ON import_log (status);
