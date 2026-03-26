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
        description="Promote a validated candidate release into the current database slot."
    )
    parser.add_argument("release_label", help="Candidate release label to promote.")
    parser.add_argument("--db-path", help="Current SQLite database path.")
    parser.add_argument(
        "--archive-label",
        help="Optional label for the pre-promotion archive copy.",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Execute file promotion. Without this flag the command is dry-run only.",
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
    if release_entry["release_type"] != "CANDIDATE":
        raise SystemExit(
            f"Release {args.release_label} is not a candidate. "
            f"release_type={release_entry['release_type']}"
        )

    candidate_db_path = resolve_db_path(release_entry["db_path"])
    archive_label = args.archive_label or f"pre_promote_{utc_timestamp_label()}"
    archive_db_path = build_archive_db_path(archive_label)

    if not args.apply:
        print(
            "Dry run only. "
            f"current_db_path={current_db_path} "
            f"candidate_db_path={candidate_db_path} "
            f"archive_db_path={archive_db_path}"
        )
        return

    copy_database_file(current_db_path, archive_db_path, overwrite=False)
    copy_database_file(candidate_db_path, current_db_path, overwrite=True)

    promoted_engine = create_sqlite_engine(current_db_path)
    ensure_release_management_schema(promoted_engine)
    with promoted_engine.begin() as connection:
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
        promoted_engine,
        release_label=archive_label,
        db_path=archive_db_path,
        release_type="ARCHIVE",
        status="ARCHIVED",
        notes=f"Archive copy created before promoting {args.release_label}.",
    )
    upsert_release_registry(
        promoted_engine,
        release_label=args.release_label,
        db_path=current_db_path,
        release_type="CURRENT",
        status="ACTIVE",
        promoted_at=utc_now_iso(),
        notes="Promoted from candidate into the current DB slot.",
    )

    print(
        "Release promotion complete. "
        f"release_label={args.release_label} current_db_path={current_db_path} archive_db_path={archive_db_path}"
    )


if __name__ == "__main__":
    main()
