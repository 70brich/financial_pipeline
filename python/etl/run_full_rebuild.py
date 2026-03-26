from __future__ import annotations

import argparse

from python.etl.db_runtime import create_sqlite_engine
from python.etl.release_management import (
    build_candidate_db_path,
    copy_database_file,
    ensure_release_management_schema,
    finish_ingest_run,
    resolve_db_path,
    start_ingest_run,
    upsert_release_registry,
    utc_timestamp_label,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Create a non-destructive candidate database for a future full rebuild."
    )
    parser.add_argument("--db-path", help="Current SQLite database path.")
    parser.add_argument("--release-label", help="Release label for the candidate database.")
    parser.add_argument(
        "--candidate-db-path",
        help="Optional explicit path for the candidate SQLite database.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite an existing candidate database path.",
    )
    parser.add_argument("--notes", help="Optional run note.")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    db_path = resolve_db_path(args.db_path)
    engine = create_sqlite_engine(db_path)
    ensure_release_management_schema(engine)

    release_label = args.release_label or f"candidate_{utc_timestamp_label()}"
    candidate_db_path = (
        resolve_db_path(args.candidate_db_path)
        if args.candidate_db_path
        else build_candidate_db_path(release_label)
    )

    run_id = start_ingest_run(
        engine,
        "FULL_REBUILD",
        target_scope="candidate",
        release_label=release_label,
        notes=args.notes,
    )

    try:
        copy_database_file(db_path, candidate_db_path, overwrite=args.force)
        candidate_engine = create_sqlite_engine(candidate_db_path)
        ensure_release_management_schema(candidate_engine)
        upsert_release_registry(
            engine,
            release_label=release_label,
            db_path=candidate_db_path,
            release_type="CANDIDATE",
            status="READY_FOR_VALIDATION",
            notes=(
                "Candidate cloned from the current baseline. "
                "Source replay and reconciliation remain a future step."
            ),
        )
        finish_ingest_run(
            engine,
            run_id,
            status="SUCCESS",
            notes=(
                f"candidate_db_path={candidate_db_path} "
                "Current baseline copied without mutating the active DB."
            ),
        )
        print(
            "Full rebuild scaffold complete. "
            f"db_path={db_path} ingest_run_id={run_id} candidate_db_path={candidate_db_path}"
        )
    except Exception as exc:
        finish_ingest_run(engine, run_id, status="FAILED", notes=str(exc))
        raise


if __name__ == "__main__":
    main()
