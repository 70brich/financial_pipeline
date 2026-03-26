from __future__ import annotations

import argparse

from sqlalchemy import text

from python.etl.db_runtime import create_sqlite_engine
from python.etl.inventory_sources import utc_now_iso
from python.etl.release_management import (
    build_archive_db_path,
    copy_database_file,
    ensure_release_management_schema,
    get_release_entry,
    resolve_db_path,
    upsert_release_registry,
    utc_timestamp_label,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Rollback the current database to an archived release."
    )
    parser.add_argument("release_label", help="Archived release label to restore.")
    parser.add_argument("--db-path", help="Current SQLite database path.")
    parser.add_argument(
        "--backup-label",
        help="Optional label for the backup taken before rollback.",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Execute the rollback. Without this flag the command is dry-run only.",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    current_db_path = resolve_db_path(args.db_path)
    engine = create_sqlite_engine(current_db_path)
    ensure_release_management_schema(engine)

    release_entry = get_release_entry(engine, args.release_label)
    if release_entry is None:
        raise SystemExit(f"Release label not found: {args.release_label}")
    if release_entry["release_type"] != "ARCHIVE":
        raise SystemExit(
            f"Release {args.release_label} is not an archive. "
            f"release_type={release_entry['release_type']}"
        )

    archive_db_path = resolve_db_path(release_entry["db_path"])
    backup_label = args.backup_label or f"pre_rollback_{utc_timestamp_label()}"
    backup_db_path = build_archive_db_path(backup_label)

    if not args.apply:
        print(
            "Dry run only. "
            f"current_db_path={current_db_path} "
            f"restore_from={archive_db_path} "
            f"backup_db_path={backup_db_path}"
        )
        return

    copy_database_file(current_db_path, backup_db_path, overwrite=False)
    copy_database_file(archive_db_path, current_db_path, overwrite=True)

    restored_engine = create_sqlite_engine(current_db_path)
    ensure_release_management_schema(restored_engine)
    with restored_engine.begin() as connection:
        connection.execute(
            text(
                """
                UPDATE release_registry
                SET status = 'SUPERSEDED'
                WHERE release_type = 'CURRENT'
                  AND status = 'ACTIVE'
                """
            )
        )

    upsert_release_registry(
        restored_engine,
        release_label=backup_label,
        db_path=backup_db_path,
        release_type="ARCHIVE",
        status="ARCHIVED",
        notes=f"Backup created before rollback to {args.release_label}.",
    )
    upsert_release_registry(
        restored_engine,
        release_label=args.release_label,
        db_path=current_db_path,
        release_type="CURRENT",
        status="ACTIVE",
        promoted_at=utc_now_iso(),
        notes="Restored from archive into the current DB slot.",
    )

    print(
        "Rollback complete. "
        f"release_label={args.release_label} current_db_path={current_db_path} backup_db_path={backup_db_path}"
    )


if __name__ == "__main__":
    main()
