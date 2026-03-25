from __future__ import annotations

import hashlib
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

from sqlalchemy import create_engine, text


BASE_DIR = Path(__file__).resolve().parents[2]
INPUT_DIR = BASE_DIR / "data" / "input"
CANONICAL_SOURCE_GROUPS = ("KDATA1", "KDATA2", "QDATA")
SUPPORTED_EXTENSIONS = {".xlsx", ".xls", ".csv"}


@dataclass(frozen=True)
class SourceFileRecord:
    source_group: str
    relative_path: str
    file_name: str
    file_extension: str
    file_size_bytes: int
    file_modified_at: str
    file_hash: str
    canonical_input: int
    discovered_at: str


def get_engine():
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise RuntimeError("DATABASE_URL environment variable is not set.")
    return create_engine(database_url)


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def derive_source_group(file_path: Path, input_dir: Path = INPUT_DIR) -> str:
    relative_parts = file_path.relative_to(input_dir).parts
    if not relative_parts:
        raise ValueError(f"Could not derive source_group from path: {file_path}")

    source_group = relative_parts[0]
    if source_group not in CANONICAL_SOURCE_GROUPS:
        raise ValueError(f"Non-canonical source_group for path: {file_path}")
    return source_group


def build_relative_path(file_path: Path, input_dir: Path = INPUT_DIR) -> str:
    return file_path.relative_to(input_dir).as_posix()


def iter_canonical_source_files(input_dir: Path = INPUT_DIR) -> Iterable[Path]:
    if not input_dir.exists():
        return []

    files: list[Path] = []
    for source_group in CANONICAL_SOURCE_GROUPS:
        source_dir = input_dir / source_group
        if not source_dir.exists():
            continue
        for path in source_dir.rglob("*"):
            if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS:
                files.append(path)
    return sorted(files)


def compute_file_hash(file_path: Path) -> str:
    digest = hashlib.sha256()
    with file_path.open("rb") as file_handle:
        for chunk in iter(lambda: file_handle.read(8192), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build_source_file_record(
    file_path: Path,
    input_dir: Path = INPUT_DIR,
    discovered_at: str | None = None,
) -> SourceFileRecord:
    stat = file_path.stat()
    return SourceFileRecord(
        source_group=derive_source_group(file_path, input_dir=input_dir),
        relative_path=build_relative_path(file_path, input_dir=input_dir),
        file_name=file_path.name,
        file_extension=file_path.suffix.lower(),
        file_size_bytes=stat.st_size,
        file_modified_at=datetime.fromtimestamp(
            stat.st_mtime, tz=timezone.utc
        ).replace(microsecond=0).isoformat(),
        file_hash=compute_file_hash(file_path),
        canonical_input=1,
        discovered_at=discovered_at or utc_now_iso(),
    )


def start_scan_run(engine, source_group: str | None = None, trigger_mode: str = "manual") -> int:
    sql = text(
        """
        INSERT INTO import_log (
            source_group,
            run_started_at,
            status,
            trigger_mode
        ) VALUES (
            :source_group,
            :run_started_at,
            'STARTED',
            :trigger_mode
        )
        """
    )
    run_started_at = utc_now_iso()
    with engine.begin() as connection:
        result = connection.execute(
            sql,
            {
                "source_group": source_group,
                "run_started_at": run_started_at,
                "trigger_mode": trigger_mode,
            },
        )
        return int(result.lastrowid)


def upsert_source_file(connection, record: SourceFileRecord) -> None:
    existing_id = connection.execute(
        text(
            """
            SELECT source_file_id
            FROM source_file
            WHERE source_group = :source_group
              AND relative_path = :relative_path
            """
        ),
        {
            "source_group": record.source_group,
            "relative_path": record.relative_path,
        },
    ).scalar()

    payload = {
        "source_group": record.source_group,
        "relative_path": record.relative_path,
        "file_name": record.file_name,
        "file_extension": record.file_extension,
        "file_size_bytes": record.file_size_bytes,
        "file_modified_at": record.file_modified_at,
        "file_hash": record.file_hash,
        "canonical_input": record.canonical_input,
        "discovered_at": record.discovered_at,
    }

    if existing_id is None:
        connection.execute(
            text(
                """
                INSERT INTO source_file (
                    source_group,
                    relative_path,
                    file_name,
                    file_extension,
                    file_size_bytes,
                    file_modified_at,
                    file_hash,
                    canonical_input,
                    discovered_at
                ) VALUES (
                    :source_group,
                    :relative_path,
                    :file_name,
                    :file_extension,
                    :file_size_bytes,
                    :file_modified_at,
                    :file_hash,
                    :canonical_input,
                    :discovered_at
                )
                """
            ),
            payload,
        )
        return

    payload["source_file_id"] = existing_id
    connection.execute(
        text(
            """
            UPDATE source_file
            SET file_name = :file_name,
                file_extension = :file_extension,
                file_size_bytes = :file_size_bytes,
                file_modified_at = :file_modified_at,
                file_hash = :file_hash,
                canonical_input = :canonical_input,
                discovered_at = :discovered_at
            WHERE source_file_id = :source_file_id
            """
        ),
        payload,
    )


def finish_scan_run(
    engine,
    import_log_id: int,
    status: str,
    files_scanned: int,
    files_loaded: int,
    rows_loaded: int = 0,
    error_message: str | None = None,
) -> None:
    sql = text(
        """
        UPDATE import_log
        SET run_finished_at = :run_finished_at,
            status = :status,
            files_scanned = :files_scanned,
            files_loaded = :files_loaded,
            rows_loaded = :rows_loaded,
            error_message = :error_message
        WHERE import_log_id = :import_log_id
        """
    )
    with engine.begin() as connection:
        connection.execute(
            sql,
            {
                "run_finished_at": utc_now_iso(),
                "status": status,
                "files_scanned": files_scanned,
                "files_loaded": files_loaded,
                "rows_loaded": rows_loaded,
                "error_message": error_message,
                "import_log_id": import_log_id,
            },
        )


def scan_source_files(engine, input_dir: Path = INPUT_DIR, trigger_mode: str = "manual") -> int:
    import_log_id = start_scan_run(engine, source_group=None, trigger_mode=trigger_mode)
    files = list(iter_canonical_source_files(input_dir=input_dir))

    if not files:
        finish_scan_run(
            engine,
            import_log_id=import_log_id,
            status="SKIPPED",
            files_scanned=0,
            files_loaded=0,
        )
        return import_log_id

    try:
        with engine.begin() as connection:
            for file_path in files:
                record = build_source_file_record(file_path, input_dir=input_dir)
                upsert_source_file(connection, record)
        finish_scan_run(
            engine,
            import_log_id=import_log_id,
            status="SUCCESS",
            files_scanned=len(files),
            files_loaded=len(files),
        )
    except Exception as exc:
        finish_scan_run(
            engine,
            import_log_id=import_log_id,
            status="FAILED",
            files_scanned=len(files),
            files_loaded=0,
            error_message=str(exc),
        )
        raise

    return import_log_id


def summarize_inventory(engine) -> dict[str, int]:
    with engine.begin() as connection:
        source_file_count = connection.execute(
            text("SELECT COUNT(*) FROM source_file")
        ).scalar_one()
        import_log_count = connection.execute(
            text("SELECT COUNT(*) FROM import_log")
        ).scalar_one()
    return {
        "source_file_count": int(source_file_count),
        "import_log_count": int(import_log_count),
    }


def main() -> None:
    engine = get_engine()
    import_log_id = scan_source_files(engine)
    print(f"Completed source file inventory run {import_log_id}")


if __name__ == "__main__":
    main()
