from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from python.etl.inventory_sources import build_relative_path, derive_source_group, iter_canonical_source_files


class InventorySourcesTest(unittest.TestCase):
    def test_derive_source_group_from_folder_path(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            input_dir = Path(temp_dir) / "data" / "input"
            target = input_dir / "KDATA2" / "sample.xls"
            target.parent.mkdir(parents=True)
            target.write_text("x", encoding="utf-8")

            self.assertEqual(derive_source_group(target, input_dir=input_dir), "KDATA2")

    def test_build_relative_path_from_input_root(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            input_dir = Path(temp_dir) / "data" / "input"
            target = input_dir / "QDATA" / "nested" / "sample.csv"
            target.parent.mkdir(parents=True)
            target.write_text("x", encoding="utf-8")

            self.assertEqual(
                build_relative_path(target, input_dir=input_dir),
                "QDATA/nested/sample.csv",
            )

    def test_iter_canonical_source_files_ignores_loose_input_files(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            input_dir = Path(temp_dir) / "data" / "input"
            canonical = input_dir / "KDATA1" / "sample.xls"
            loose = input_dir / "loose.csv"
            canonical.parent.mkdir(parents=True)
            loose.parent.mkdir(parents=True, exist_ok=True)
            canonical.write_text("canonical", encoding="utf-8")
            loose.write_text("loose", encoding="utf-8")

            discovered = list(iter_canonical_source_files(input_dir=input_dir))

            self.assertEqual(discovered, [canonical])


if __name__ == "__main__":
    unittest.main()
