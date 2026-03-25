from __future__ import annotations

from sqlalchemy import text

from python.etl.db_runtime import DEFAULT_SQLITE_DB_PATH, create_sqlite_engine, execute_sql_script


def print_section(title: str) -> None:
    print()
    print(f"=== {title} ===")


def main() -> None:
    engine = create_sqlite_engine()
    execute_sql_script(engine)

    with engine.begin() as connection:
        total_source_files = connection.execute(
            text("SELECT COUNT(*) FROM source_file")
        ).scalar_one()

        counts_by_group = connection.execute(
            text(
                """
                SELECT source_group, COUNT(*) AS row_count
                FROM source_file
                GROUP BY source_group
                ORDER BY source_group
                """
            )
        ).fetchall()

        recent_source_files = connection.execute(
            text(
                """
                SELECT
                    source_file_id,
                    source_group,
                    relative_path,
                    file_size_bytes,
                    file_modified_at,
                    discovered_at
                FROM source_file
                ORDER BY discovered_at DESC, source_file_id DESC
                LIMIT 10
                """
            )
        ).fetchall()

        recent_import_logs = connection.execute(
            text(
                """
                SELECT
                    import_log_id,
                    status,
                    source_group,
                    files_scanned,
                    files_loaded,
                    rows_loaded,
                    trigger_mode,
                    run_started_at,
                    run_finished_at
                FROM import_log
                ORDER BY import_log_id DESC
                LIMIT 10
                """
            )
        ).fetchall()

    print("SQLite inventory inspection")
    print(f"Database: {DEFAULT_SQLITE_DB_PATH}")

    print_section("Total source_file rows")
    print(f"{total_source_files}")

    print_section("Count by source_group")
    if counts_by_group:
        for row in counts_by_group:
            print(f"{row.source_group}: {row.row_count}")
    else:
        print("No source_file rows found.")

    print_section("Most recent source_file rows")
    if recent_source_files:
        for row in recent_source_files:
            print(
                f"[{row.source_file_id}] {row.source_group} | {row.relative_path} | "
                f"size={row.file_size_bytes} | modified={row.file_modified_at} | "
                f"discovered={row.discovered_at}"
            )
    else:
        print("No source_file rows found.")

    print_section("Most recent import_log rows")
    if recent_import_logs:
        for row in recent_import_logs:
            source_group = row.source_group if row.source_group is not None else "ALL"
            finished_at = row.run_finished_at if row.run_finished_at is not None else "-"
            print(
                f"[{row.import_log_id}] status={row.status} | source_group={source_group} | "
                f"files_scanned={row.files_scanned} | files_loaded={row.files_loaded} | "
                f"rows_loaded={row.rows_loaded} | trigger={row.trigger_mode} | "
                f"started={row.run_started_at} | finished={finished_at}"
            )
    else:
        print("No import_log rows found.")


if __name__ == "__main__":
    main()
