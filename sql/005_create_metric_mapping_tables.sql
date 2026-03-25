CREATE TABLE IF NOT EXISTS metric_alias_map (
    metric_alias_map_id INTEGER PRIMARY KEY,
    normalized_metric_key TEXT NOT NULL UNIQUE,
    standard_metric_name TEXT NOT NULL,
    is_active INTEGER NOT NULL DEFAULT 1,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT ck_metric_alias_map_is_active CHECK (is_active IN (0, 1))
);

CREATE TABLE IF NOT EXISTS integrated_observation_enriched (
    integrated_observation_enriched_id INTEGER PRIMARY KEY,
    integrated_observation_id INTEGER NOT NULL,
    company_key TEXT,
    raw_metric_name TEXT NOT NULL,
    normalized_metric_key TEXT NOT NULL,
    standard_metric_name TEXT,
    metric_variant TEXT,
    period_type TEXT NOT NULL,
    fiscal_year INTEGER,
    fiscal_quarter INTEGER,
    date_raw TEXT,
    selected_source_group TEXT,
    selected_raw_observation_id INTEGER,
    selected_value_numeric NUMERIC,
    selected_is_estimate INTEGER NOT NULL DEFAULT 0,
    enriched_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_enriched_integrated_observation
        FOREIGN KEY (integrated_observation_id) REFERENCES integrated_observation (integrated_observation_id),
    CONSTRAINT fk_enriched_selected_raw_observation
        FOREIGN KEY (selected_raw_observation_id) REFERENCES raw_observation (raw_observation_id),
    CONSTRAINT ck_enriched_period_type CHECK (
        period_type IN ('SNAPSHOT', 'YEAR', 'QUARTER')
    ),
    CONSTRAINT ck_enriched_selected_is_estimate CHECK (
        selected_is_estimate IN (0, 1)
    )
);

CREATE INDEX IF NOT EXISTS idx_metric_alias_map_standard_metric_name
    ON metric_alias_map (standard_metric_name);

CREATE INDEX IF NOT EXISTS idx_integrated_enriched_lookup
    ON integrated_observation_enriched (
        standard_metric_name,
        normalized_metric_key,
        period_type,
        fiscal_year,
        fiscal_quarter,
        date_raw
    );

CREATE INDEX IF NOT EXISTS idx_integrated_enriched_integrated_observation_id
    ON integrated_observation_enriched (integrated_observation_id);
