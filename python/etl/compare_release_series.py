from __future__ import annotations

import argparse

from python.etl.db_runtime import create_sqlite_engine
from python.etl.release_management import (
    compare_managed_table_counts,
    ensure_release_management_schema,
    get_release_entry,
    resolve_db_path,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Compare high-level managed-table row counts between current and another release DB."
    )
    parser.add_argument("--db-path", help="Current SQLite database path.")
    parser.add_argument(
        "--release-label",
        help="Candidate or archive release label registered in release_registry.",
    )
    parser.add_argument("--other-db-path", help="Explicit path to the comparison database.")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    if not args.release_label and not args.other_db_path:
        raise SystemExit("Provide either --release-label or --other-db-path.")

    current_db_path = resolve_db_path(args.db_path)
    engine = create_sqlite_engine(current_db_path)
    ensure_release_management_schema(engine)

    if args.other_db_path:
        other_db_path = resolve_db_path(args.other_db_path)
    else:
        release_entry = get_release_entry(engine, args.release_label)
        if release_entry is None:
            raise SystemExit(f"Release label not found: {args.release_label}")
        other_db_path = resolve_db_path(release_entry["db_path"])

    comparison_rows = compare_managed_table_counts(current_db_path, other_db_path)
    print(
        "Release table-count comparison. "
        f"current_db_path={current_db_path} other_db_path={other_db_path}"
    )
    for row in comparison_rows:
        print(
            f"{row['table_name']}: "
            f"current={row['current_count']} "
            f"other={row['other_count']} "
            f"delta={row['count_delta']}"
        )


if __name__ == "__main__":
    main()
