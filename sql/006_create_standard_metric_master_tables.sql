CREATE TABLE IF NOT EXISTS standard_metric (
    standard_metric_id INTEGER PRIMARY KEY,
    standard_metric_name TEXT NOT NULL UNIQUE,
    metric_family TEXT NOT NULL,
    description TEXT,
    active_flag INTEGER NOT NULL DEFAULT 1,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT ck_standard_metric_active_flag CHECK (active_flag IN (0, 1))
);

CREATE TABLE IF NOT EXISTS metric_name_mapping (
    metric_name_mapping_id INTEGER PRIMARY KEY,
    normalized_metric_key TEXT NOT NULL UNIQUE,
    raw_metric_name_example TEXT,
    standard_metric_id INTEGER,
    standard_metric_name TEXT NOT NULL,
    mapping_rule TEXT NOT NULL,
    mapping_confidence REAL NOT NULL DEFAULT 1.0,
    is_active INTEGER NOT NULL DEFAULT 1,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_metric_name_mapping_standard_metric
        FOREIGN KEY (standard_metric_id) REFERENCES standard_metric (standard_metric_id),
    CONSTRAINT ck_metric_name_mapping_is_active CHECK (is_active IN (0, 1)),
    CONSTRAINT ck_metric_name_mapping_confidence CHECK (
        mapping_confidence >= 0.0 AND mapping_confidence <= 1.0
    )
);

CREATE INDEX IF NOT EXISTS idx_standard_metric_metric_family
    ON standard_metric (metric_family);

CREATE INDEX IF NOT EXISTS idx_standard_metric_active_flag
    ON standard_metric (active_flag);

CREATE INDEX IF NOT EXISTS idx_metric_name_mapping_standard_metric_id
    ON metric_name_mapping (standard_metric_id);

CREATE INDEX IF NOT EXISTS idx_metric_name_mapping_standard_metric_name
    ON metric_name_mapping (standard_metric_name);

CREATE INDEX IF NOT EXISTS idx_metric_name_mapping_mapping_rule
    ON metric_name_mapping (mapping_rule);
