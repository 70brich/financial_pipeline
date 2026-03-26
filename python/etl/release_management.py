from __future__ import annotations

import re
import shutil
from datetime import datetime, timezone
from pathlib import Path

from sqlalchemy import text

from python.etl.db_runtime import (
    BASE_DIR,
    DEFAULT_SQLITE_DB_PATH,
    create_sqlite_engine,
    ensure_runtime_schema,
    execute_sql_script,
)
from python.etl.inventory_sources import utc_now_iso


RELEASE_SCHEMA_SQL_PATH = BASE_DIR / "sql" / "010_create_release_management_tables.sql"
DEFAULT_RELEASES_DIR = BASE_DIR / "data" / "releases"
DEFAULT_ARCHIVE_DIR = BASE_DIR / "data" / "archive"
MANAGED_TABLE_NAMES = (
    "source_file",
    "raw_observation",
    "integrated_observation",
    "integrated_observation_enriched",
    "standard_metric",
    "metric_name_mapping",
    "fnguide_observation",
)


def resolve_db_path(db_path: str | None = None) -> Path:
    if not db_path:
        return DEFAULT_SQLITE_DB_PATH
    return Path(db_path).expanduser().resolve()


def sanitize_release_label(release_label: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9._-]+", "_", release_label.strip())
    if not cleaned:
        raise ValueError("release_label must contain at least one filename-safe character.")
    return cleaned


def utc_timestamp_label() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def ensure_release_management_schema(engine) -> None:
    ensure_runtime_schema(engine)
    execute_sql_script(engine, RELEASE_SCHEMA_SQL_PATH)


def start_ingest_run(
    engine,
    run_mode: str,
    *,
    source_group: str | None = None,
    target_scope: str = "current",
    release_label: str | None = None,
    notes: str | None = None,
) -> int:
    with engine.begin() as connection:
        result = connection.execute(
            text(
                """
                INSERT INTO ingest_run (
                    run_mode,
                    source_group,
                    target_scope,
                    started_at,
                    status,
                    release_label,
                    notes
                ) VALUES (
                    :run_mode,
                    :source_group,
                    :target_scope,
                    :started_at,
                    'STARTED',
                    :release_label,
                    :notes
                )
                """
            ),
            {
                "run_mode": run_mode,
                "source_group": source_group,
                "target_scope": target_scope,
                "started_at": utc_now_iso(),
                "release_label": release_label,
                "notes": notes,
            },
        )
        return int(result.lastrowid)


def finish_ingest_run(
    engine,
    ingest_run_id: int,
    *,
    status: str,
    notes: str | None = None,
) -> None:
    with engine.begin() as connection:
        connection.execute(
            text(
                """
                UPDATE ingest_run
                SET finished_at = :finished_at,
                    status = :status,
                    notes = COALESCE(:notes, notes)
                WHERE ingest_run_id = :ingest_run_id
                """
            ),
            {
                "finished_at": utc_now_iso(),
                "status": status,
                "notes": notes,
                "ingest_run_id": ingest_run_id,
            },
        )


def register_source_snapshots_from_inventory(
    engine,
    ingest_run_id: int,
    *,
    source_group: str | None = None,
    snapshot_type: str = "CANONICAL_FILE",
) -> int:
    where_clause = "WHERE canonical_input = 1"
    params: dict[str, object] = {}
    if source_group:
        where_clause += " AND source_group = :source_group"
        params["source_group"] = source_group

    with engine.begin() as connection:
        source_rows = connection.execute(
            text(
                f"""
                SELECT
                    source_group,
                    relative_path,
                    file_name,
                    file_hash
                FROM source_file
                {where_clause}
                ORDER BY source_group, relative_path
                """
            ),
            params,
        ).mappings().all()

        inserted = 0
        for row in source_rows:
            previous_hash = connection.execute(
                text(
                    """
                    SELECT content_hash
                    FROM source_snapshot
                    WHERE source_group = :source_group
                      AND source_locator = :source_locator
                    ORDER BY source_snapshot_id DESC
                    LIMIT 1
                    """
                ),
                {
                    "source_group": row["source_group"],
                    "source_locator": row["relative_path"],
                },
            ).scalar()

            if previous_hash is None:
                detected_change_type = "NEW_SOURCE"
                identical = 0
            elif previous_hash == row["file_hash"]:
                detected_change_type = "NO_CHANGE"
                identical = 1
            else:
                detected_change_type = "CONTENT_CHANGE"
                identical = 0

            connection.execute(
                text(
                    """
                    INSERT INTO source_snapshot (
                        ingest_run_id,
                        source_group,
                        company_name,
                        stock_code,
                        source_locator,
                        content_hash,
                        snapshot_type,
                        detected_change_type,
                        is_identical_to_previous,
                        notes
                    ) VALUES (
                        :ingest_run_id,
                        :source_group,
                        NULL,
                        NULL,
                        :source_locator,
                        :content_hash,
                        :snapshot_type,
                        :detected_change_type,
                        :is_identical_to_previous,
                        :notes
                    )
                    """
                ),
                {
                    "ingest_run_id": ingest_run_id,
                    "source_group": row["source_group"],
                    "source_locator": row["relative_path"],
                    "content_hash": row["file_hash"],
                    "snapshot_type": snapshot_type,
                    "detected_change_type": detected_change_type,
                    "is_identical_to_previous": identical,
                    "notes": f"file_name={row['file_name']}",
                },
            )
            inserted += 1

    return inserted


def record_series_change_audit(
    engine,
    *,
    ingest_run_id: int,
    metric_name: str,
    change_type: str,
    company_name: str | None = None,
    stock_code: str | None = None,
    ifrs_scope: str | None = None,
    period_scope: str | None = None,
    source_group: str | None = None,
    changed_period_count: int = 0,
    old_series_hash: str | None = None,
    new_series_hash: str | None = None,
    remarks: str | None = None,
) -> None:
    with engine.begin() as connection:
        connection.execute(
            text(
                """
                INSERT INTO series_change_audit (
                    ingest_run_id,
                    company_name,
                    stock_code,
                    metric_name,
                    ifrs_scope,
                    period_scope,
                    source_group,
                    change_type,
                    changed_period_count,
                    old_series_hash,
                    new_series_hash,
                    remarks
                ) VALUES (
                    :ingest_run_id,
                    :company_name,
                    :stock_code,
                    :metric_name,
                    :ifrs_scope,
                    :period_scope,
                    :source_group,
                    :change_type,
                    :changed_period_count,
                    :old_series_hash,
                    :new_series_hash,
                    :remarks
                )
                """
            ),
            {
                "ingest_run_id": ingest_run_id,
                "company_name": company_name,
                "stock_code": stock_code,
                "metric_name": metric_name,
                "ifrs_scope": ifrs_scope,
                "period_scope": period_scope,
                "source_group": source_group,
                "change_type": change_type,
                "changed_period_count": changed_period_count,
                "old_series_hash": old_series_hash,
                "new_series_hash": new_series_hash,
                "remarks": remarks,
            },
        )


def upsert_release_registry(
    engine,
    *,
    release_label: str,
    db_path: Path,
    release_type: str,
    status: str,
    notes: str | None = None,
    promoted_at: str | None = None,
) -> int:
    created_at = utc_now_iso()
    normalized_db_path = str(db_path.resolve())

    with engine.begin() as connection:
        existing_id = connection.execute(
            text(
                """
                SELECT release_id
                FROM release_registry
                WHERE release_label = :release_label
                """
            ),
            {"release_label": release_label},
        ).scalar()

        payload = {
            "release_label": release_label,
            "db_path": normalized_db_path,
            "release_type": release_type,
            "created_at": created_at,
            "promoted_at": promoted_at,
            "status": status,
            "notes": notes,
        }

        if existing_id is None:
            result = connection.execute(
                text(
                    """
                    INSERT INTO release_registry (
                        release_label,
                        db_path,
                        release_type,
                        created_at,
                        promoted_at,
                        status,
                        notes
                    ) VALUES (
                        :release_label,
                        :db_path,
                        :release_type,
                        :created_at,
                        :promoted_at,
                        :status,
                        :notes
                    )
                    """
                ),
                payload,
            )
            return int(result.lastrowid)

        payload["release_id"] = int(existing_id)
        connection.execute(
            text(
                """
                UPDATE release_registry
                SET db_path = :db_path,
                    release_type = :release_type,
                    promoted_at = :promoted_at,
                    status = :status,
                    notes = :notes
                WHERE release_id = :release_id
                """
            ),
            payload,
        )
        return int(existing_id)


def get_release_entry(engine, release_label: str) -> dict | None:
    with engine.begin() as connection:
        row = connection.execute(
            text(
                """
                SELECT
                    release_id,
                    release_label,
                    db_path,
                    release_type,
                    created_at,
                    promoted_at,
                    status,
                    notes
                FROM release_registry
                WHERE release_label = :release_label
                """
            ),
            {"release_label": release_label},
        ).mappings().first()
    return dict(row) if row else None


def iter_release_registry(engine) -> list[dict]:
    with engine.begin() as connection:
        rows = connection.execute(
            text(
                """
                SELECT
                    release_label,
                    db_path,
                    release_type,
                    created_at,
                    promoted_at,
                    status,
                    notes
                FROM release_registry
                ORDER BY created_at DESC, release_label DESC
                """
            )
        ).mappings().all()
    return [dict(row) for row in rows]


def summarize_release_tables(engine) -> dict[str, int]:
    table_names = (
        "ingest_run",
        "source_snapshot",
        "series_change_audit",
        "release_registry",
    )
    summary: dict[str, int] = {}
    with engine.begin() as connection:
        for table_name in table_names:
            count = connection.execute(
                text(f"SELECT COUNT(*) FROM {table_name}")
            ).scalar_one()
            summary[table_name] = int(count)
    return summary


def build_candidate_db_path(release_label: str) -> Path:
    safe_label = sanitize_release_label(release_label)
    return DEFAULT_RELEASES_DIR / f"financial_pipeline_{safe_label}_candidate.sqlite3"


def build_archive_db_path(release_label: str) -> Path:
    safe_label = sanitize_release_label(release_label)
    return DEFAULT_ARCHIVE_DIR / f"financial_pipeline_{safe_label}.sqlite3"


def copy_database_file(source_db_path: Path, target_db_path: Path, *, overwrite: bool = False) -> Path:
    if not source_db_path.exists():
        raise FileNotFoundError(f"Source database not found: {source_db_path}")
    if target_db_path.exists() and not overwrite:
        raise FileExistsError(f"Target database already exists: {target_db_path}")

    target_db_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source_db_path, target_db_path)
    return target_db_path


def fetch_table_count(engine, table_name: str) -> int | None:
    with engine.begin() as connection:
        exists = connection.execute(
            text(
                """
                SELECT COUNT(*)
                FROM sqlite_master
                WHERE type = 'table'
                  AND name = :table_name
                """
            ),
            {"table_name": table_name},
        ).scalar_one()
        if int(exists) == 0:
            return None

        count = connection.execute(
            text(f"SELECT COUNT(*) FROM {table_name}")
        ).scalar_one()
        return int(count)


def compare_managed_table_counts(
    current_db_path: Path,
    other_db_path: Path,
    *,
    table_names: tuple[str, ...] = MANAGED_TABLE_NAMES,
) -> list[dict]:
    current_engine = create_sqlite_engine(current_db_path)
    other_engine = create_sqlite_engine(other_db_path)

    comparison_rows: list[dict] = []
    for table_name in table_names:
        current_count = fetch_table_count(current_engine, table_name)
        other_count = fetch_table_count(other_engine, table_name)
        comparison_rows.append(
            {
                "table_name": table_name,
                "current_count": current_count,
                "other_count": other_count,
                "count_delta": (
                    None
                    if current_count is None or other_count is None
                    else other_count - current_count
                ),
            }
        )
    return comparison_rows
