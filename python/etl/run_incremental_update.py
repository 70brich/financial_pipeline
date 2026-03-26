from __future__ import annotations

import argparse

from python.etl.db_runtime import create_sqlite_engine
from python.etl.release_management import (
    ensure_release_management_schema,
    finish_ingest_run,
    register_source_snapshots_from_inventory,
    resolve_db_path,
    start_ingest_run,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Record incremental-update metadata without mutating validated source layers."
    )
    parser.add_argument("--db-path", help="Target SQLite database path.")
    parser.add_argument(
        "--source-group",
        choices=["KDATA1", "KDATA2", "QDATA", "FNGUIDE"],
        help="Optional source group scope for this incremental run.",
    )
    parser.add_argument(
        "--target-scope",
        default="current",
        help="Human-readable target scope label. Default: current",
    )
    parser.add_argument("--release-label", help="Optional release label to associate.")
    parser.add_argument("--notes", help="Optional run note.")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    db_path = resolve_db_path(args.db_path)
    engine = create_sqlite_engine(db_path)
    ensure_release_management_schema(engine)

    run_id = start_ingest_run(
        engine,
        "INCREMENTAL",
        source_group=args.source_group,
        target_scope=args.target_scope,
        release_label=args.release_label,
        notes=args.notes,
    )

    try:
        snapshot_count = register_source_snapshots_from_inventory(
            engine,
            run_id,
            source_group=args.source_group,
        )
        note = (
            "Policy scaffold only. "
            f"source_snapshots={snapshot_count}. "
            "No raw, integrated, or enriched rows were mutated."
        )
        if args.notes:
            note = f"{note} user_note={args.notes}"
        finish_ingest_run(engine, run_id, status="SKIPPED", notes=note)
        print(
            "Incremental update scaffold complete. "
            f"db_path={db_path} ingest_run_id={run_id} source_snapshots={snapshot_count}"
        )
    except Exception as exc:
        finish_ingest_run(engine, run_id, status="FAILED", notes=str(exc))
        raise


if __name__ == "__main__":
    main()
