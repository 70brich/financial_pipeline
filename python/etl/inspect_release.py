from __future__ import annotations

import argparse

from python.etl.db_runtime import create_sqlite_engine
from python.etl.release_management import (
    ensure_release_management_schema,
    iter_release_registry,
    resolve_db_path,
    summarize_release_tables,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Inspect release-management metadata in a SQLite database."
    )
    parser.add_argument("--db-path", help="SQLite database path.")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    db_path = resolve_db_path(args.db_path)
    engine = create_sqlite_engine(db_path)
    ensure_release_management_schema(engine)

    summary = summarize_release_tables(engine)
    releases = iter_release_registry(engine)[:5]

    print(
        "Release metadata summary. "
        f"db_path={db_path} "
        f"ingest_run_rows={summary['ingest_run']} "
        f"source_snapshot_rows={summary['source_snapshot']} "
        f"series_change_audit_rows={summary['series_change_audit']} "
        f"release_registry_rows={summary['release_registry']}"
    )
    for release in releases:
        print(
            "release "
            f"label={release['release_label']} "
            f"type={release['release_type']} "
            f"status={release['status']} "
            f"db_path={release['db_path']}"
        )


if __name__ == "__main__":
    main()
