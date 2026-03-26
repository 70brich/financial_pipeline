from __future__ import annotations

from pathlib import Path
import unittest

from sqlalchemy import create_engine, text

from python.etl.db_runtime import ensure_runtime_schema
from python.etl.release_management import (
    ensure_release_management_schema,
    finish_ingest_run,
    register_source_snapshots_from_inventory,
    start_ingest_run,
    upsert_release_registry,
)


class ReleaseManagementTest(unittest.TestCase):
    def setUp(self) -> None:
        self.engine = create_engine("sqlite:///:memory:", future=True)
        ensure_runtime_schema(self.engine)
        ensure_release_management_schema(self.engine)

    def test_release_management_schema_creates_expected_tables(self):
        with self.engine.begin() as connection:
            table_names = {
                row[0]
                for row in connection.execute(
                    text("SELECT name FROM sqlite_master WHERE type = 'table'")
                ).all()
            }

        self.assertIn("ingest_run", table_names)
        self.assertIn("source_snapshot", table_names)
        self.assertIn("series_change_audit", table_names)
        self.assertIn("release_registry", table_names)

    def test_ingest_run_lifecycle_updates_status(self):
        run_id = start_ingest_run(
            self.engine,
            "INCREMENTAL",
            source_group="QDATA",
            target_scope="current",
            notes="test-run",
        )
        finish_ingest_run(self.engine, run_id, status="SKIPPED", notes="no changes")

        with self.engine.begin() as connection:
            row = connection.execute(
                text(
                    """
                    SELECT run_mode, source_group, target_scope, status, notes, finished_at
                    FROM ingest_run
                    WHERE ingest_run_id = :ingest_run_id
                    """
                ),
                {"ingest_run_id": run_id},
            ).mappings().one()

        self.assertEqual(row["run_mode"], "INCREMENTAL")
        self.assertEqual(row["source_group"], "QDATA")
        self.assertEqual(row["target_scope"], "current")
        self.assertEqual(row["status"], "SKIPPED")
        self.assertEqual(row["notes"], "no changes")
        self.assertIsNotNone(row["finished_at"])

    def test_source_snapshots_detect_no_change_on_second_capture(self):
        with self.engine.begin() as connection:
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
                        canonical_input
                    ) VALUES (
                        'KDATA1',
                        'KDATA1/sample.xls',
                        'sample.xls',
                        '.xls',
                        10,
                        '2026-03-26T00:00:00+00:00',
                        'hash-001',
                        1
                    )
                    """
                )
            )

        first_run_id = start_ingest_run(self.engine, "INCREMENTAL", source_group="KDATA1")
        first_count = register_source_snapshots_from_inventory(
            self.engine,
            first_run_id,
            source_group="KDATA1",
        )

        second_run_id = start_ingest_run(self.engine, "INCREMENTAL", source_group="KDATA1")
        second_count = register_source_snapshots_from_inventory(
            self.engine,
            second_run_id,
            source_group="KDATA1",
        )

        with self.engine.begin() as connection:
            rows = connection.execute(
                text(
                    """
                    SELECT detected_change_type, is_identical_to_previous
                    FROM source_snapshot
                    ORDER BY source_snapshot_id
                    """
                )
            ).mappings().all()

        self.assertEqual(first_count, 1)
        self.assertEqual(second_count, 1)
        self.assertEqual(rows[0]["detected_change_type"], "NEW_SOURCE")
        self.assertEqual(rows[0]["is_identical_to_previous"], 0)
        self.assertEqual(rows[1]["detected_change_type"], "NO_CHANGE")
        self.assertEqual(rows[1]["is_identical_to_previous"], 1)

    def test_release_registry_upsert_updates_existing_release(self):
        release_id = upsert_release_registry(
            self.engine,
            release_label="2026Q2_candidate",
            db_path=Path("data/releases/financial_pipeline_2026Q2_candidate.sqlite3"),
            release_type="CANDIDATE",
            status="READY_FOR_VALIDATION",
            notes="candidate",
        )

        updated_id = upsert_release_registry(
            self.engine,
            release_label="2026Q2_candidate",
            db_path=Path("data/financial_pipeline.sqlite3"),
            release_type="CURRENT",
            status="ACTIVE",
            notes="promoted",
        )

        with self.engine.begin() as connection:
            row = connection.execute(
                text(
                    """
                    SELECT release_type, status, notes
                    FROM release_registry
                    WHERE release_label = '2026Q2_candidate'
                    """
                )
            ).mappings().one()

        self.assertEqual(release_id, updated_id)
        self.assertEqual(row["release_type"], "CURRENT")
        self.assertEqual(row["status"], "ACTIVE")
        self.assertEqual(row["notes"], "promoted")


if __name__ == "__main__":
    unittest.main()
