CREATE TABLE IF NOT EXISTS integrated_observation (
    integrated_observation_id INTEGER PRIMARY KEY,
    company_key TEXT,
    raw_metric_name TEXT NOT NULL,
    period_type TEXT NOT NULL,
    fiscal_year INTEGER,
    fiscal_quarter INTEGER,
    date_raw TEXT,
    period_label_std TEXT,
    selected_raw_observation_id INTEGER NOT NULL,
    selected_source_file_id INTEGER,
    selected_source_group TEXT NOT NULL,
    selected_value_text TEXT,
    selected_value_numeric NUMERIC,
    selected_is_estimate INTEGER NOT NULL DEFAULT 0,
    selection_reason TEXT NOT NULL,
    integrated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_integrated_selected_raw_observation
        FOREIGN KEY (selected_raw_observation_id) REFERENCES raw_observation (raw_observation_id),
    CONSTRAINT fk_integrated_selected_source_file
        FOREIGN KEY (selected_source_file_id) REFERENCES source_file (source_file_id),
    CONSTRAINT ck_integrated_period_type CHECK (
        period_type IN ('SNAPSHOT', 'YEAR', 'QUARTER')
    ),
    CONSTRAINT ck_integrated_selected_is_estimate CHECK (
        selected_is_estimate IN (0, 1)
    )
);

CREATE INDEX IF NOT EXISTS idx_integrated_lookup
    ON integrated_observation (
        company_key,
        raw_metric_name,
        period_type,
        fiscal_year,
        fiscal_quarter,
        date_raw
    );

CREATE INDEX IF NOT EXISTS idx_integrated_selected_source_group
    ON integrated_observation (selected_source_group);
