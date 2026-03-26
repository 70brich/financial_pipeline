CREATE TABLE IF NOT EXISTS ingest_run (
    ingest_run_id INTEGER PRIMARY KEY,
    run_mode TEXT NOT NULL,
    source_group TEXT,
    target_scope TEXT NOT NULL,
    started_at TEXT NOT NULL,
    finished_at TEXT,
    status TEXT NOT NULL,
    release_label TEXT,
    notes TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT ck_ingest_run_mode CHECK (
        run_mode IN ('INCREMENTAL', 'FULL_REBUILD', 'PROMOTE', 'ROLLBACK', 'INSPECT')
    ),
    CONSTRAINT ck_ingest_run_source_group CHECK (
        source_group IS NULL OR source_group IN ('KDATA1', 'KDATA2', 'QDATA', 'FNGUIDE')
    ),
    CONSTRAINT ck_ingest_run_status CHECK (
        status IN ('STARTED', 'SUCCESS', 'FAILED', 'PARTIAL', 'SKIPPED')
    )
);

CREATE TABLE IF NOT EXISTS source_snapshot (
    source_snapshot_id INTEGER PRIMARY KEY,
    ingest_run_id INTEGER NOT NULL,
    source_group TEXT NOT NULL,
    company_name TEXT,
    stock_code TEXT,
    source_locator TEXT NOT NULL,
    content_hash TEXT NOT NULL,
    snapshot_type TEXT NOT NULL,
    detected_change_type TEXT NOT NULL,
    is_identical_to_previous INTEGER NOT NULL DEFAULT 0,
    notes TEXT,
    captured_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_source_snapshot_ingest_run
        FOREIGN KEY (ingest_run_id) REFERENCES ingest_run (ingest_run_id),
    CONSTRAINT ck_source_snapshot_source_group CHECK (
        source_group IN ('KDATA1', 'KDATA2', 'QDATA', 'FNGUIDE')
    ),
    CONSTRAINT ck_source_snapshot_is_identical CHECK (
        is_identical_to_previous IN (0, 1)
    ),
    CONSTRAINT ck_source_snapshot_detected_change_type CHECK (
        detected_change_type IN (
            'NEW_SOURCE',
            'NO_CHANGE',
            'CONTENT_CHANGE',
            'MANUAL_REVIEW'
        )
    )
);

CREATE TABLE IF NOT EXISTS series_change_audit (
    series_change_audit_id INTEGER PRIMARY KEY,
    ingest_run_id INTEGER NOT NULL,
    company_name TEXT,
    stock_code TEXT,
    metric_name TEXT NOT NULL,
    ifrs_scope TEXT,
    period_scope TEXT,
    source_group TEXT,
    change_type TEXT NOT NULL,
    changed_period_count INTEGER NOT NULL DEFAULT 0,
    old_series_hash TEXT,
    new_series_hash TEXT,
    remarks TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_series_change_audit_ingest_run
        FOREIGN KEY (ingest_run_id) REFERENCES ingest_run (ingest_run_id),
    CONSTRAINT ck_series_change_audit_source_group CHECK (
        source_group IS NULL OR source_group IN ('KDATA1', 'KDATA2', 'QDATA', 'FNGUIDE')
    ),
    CONSTRAINT ck_series_change_audit_change_type CHECK (
        change_type IN (
            'SKIP_NO_CHANGE',
            'APPEND_RECENT',
            'PATCH_PERIOD',
            'REBASE_FULL_SERIES',
            'NEW_SERIES',
            'MANUAL_REVIEW'
        )
    )
);

CREATE TABLE IF NOT EXISTS release_registry (
    release_id INTEGER PRIMARY KEY,
    release_label TEXT NOT NULL UNIQUE,
    db_path TEXT NOT NULL,
    release_type TEXT NOT NULL,
    created_at TEXT NOT NULL,
    promoted_at TEXT,
    status TEXT NOT NULL,
    notes TEXT,
    CONSTRAINT ck_release_registry_release_type CHECK (
        release_type IN ('CURRENT', 'CANDIDATE', 'ARCHIVE')
    ),
    CONSTRAINT ck_release_registry_status CHECK (
        status IN (
            'ACTIVE',
            'READY_FOR_VALIDATION',
            'VALIDATED',
            'ARCHIVED',
            'SUPERSEDED',
            'FAILED'
        )
    )
);

CREATE INDEX IF NOT EXISTS idx_ingest_run_started_at
    ON ingest_run (started_at, run_mode);

CREATE INDEX IF NOT EXISTS idx_source_snapshot_locator
    ON source_snapshot (source_group, source_locator, source_snapshot_id);

CREATE INDEX IF NOT EXISTS idx_series_change_audit_lookup
    ON series_change_audit (stock_code, metric_name, change_type, created_at);

CREATE INDEX IF NOT EXISTS idx_release_registry_type_status
    ON release_registry (release_type, status, created_at);
