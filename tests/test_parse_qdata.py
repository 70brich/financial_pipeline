from __future__ import annotations

import unittest

from python.etl.parse_qdata import (
    ANNUAL_SUMMARY_TITLE,
    QUARTERLY_SUMMARY_TITLE,
    YEARLY_SECTION_TITLE,
    QdataFileContext,
    normalize_quarter_period,
    normalize_year_period,
    parse_mixed_summary_block,
    parse_overview_block,
    parse_yearly_block,
    split_blocks,
)


YEAR_24 = "24\ub144"
YEAR_25 = "25\ub144"
YEAR_25_Q4_ANNUALIZED = "25\ub1444Q\uc5f0\ud658\uc0b0"
YEAR_25_Q3_ANNUALIZED = "25\ub1443Q\uc5f0\ud658\uc0b0"


class ParseQdataTest(unittest.TestCase):
    def test_split_blocks(self):
        rows = [
            ["", "company_name", "code"],
            ["", "opasnet", "A173130"],
            ["", "", ""],
            ["", ANNUAL_SUMMARY_TITLE, YEAR_24, YEAR_25, "", "", QUARTERLY_SUMMARY_TITLE, "24.4Q", "25.1Q"],
        ]

        blocks = split_blocks(rows)

        self.assertEqual(len(blocks), 2)
        self.assertEqual(blocks[0][0], 1)
        self.assertEqual(blocks[1][0], 4)

    def test_normalize_year_period(self):
        date_raw, fiscal_year, period_label_std = normalize_year_period(YEAR_25_Q4_ANNUALIZED)
        self.assertEqual(date_raw, "2025/01/01")
        self.assertEqual(fiscal_year, 2025)
        self.assertEqual(period_label_std, "2025")

    def test_normalize_quarter_period(self):
        date_raw, fiscal_year, fiscal_quarter, period_label_std = normalize_quarter_period("24.3Q")
        self.assertEqual(date_raw, "2024/07/01")
        self.assertEqual(fiscal_year, 2024)
        self.assertEqual(fiscal_quarter, 3)
        self.assertEqual(period_label_std, "24.3Q")

    def test_parse_overview_block(self):
        context = QdataFileContext(
            source_file_id=3,
            source_group="QDATA",
            relative_path="QDATA/sample_20260322_184846.csv",
            file_name="sample_20260322_184846.csv",
        )
        block = [
            ["", "company_name", "code", "price"],
            ["", "opasnet", "A173130", "7380"],
        ]

        records = parse_overview_block(2, block, context)

        self.assertEqual(len(records), 3)
        self.assertEqual(records[0]["sector_name"], "overview")
        self.assertEqual(records[0]["period_type"], "SNAPSHOT")
        self.assertEqual(records[0]["date_raw"], "2026/03/22")

    def test_parse_mixed_summary_block(self):
        context = QdataFileContext(
            source_file_id=3,
            source_group="QDATA",
            relative_path="QDATA/sample_20260322_184846.csv",
            file_name="sample_20260322_184846.csv",
        )
        block = [
            ["", ANNUAL_SUMMARY_TITLE, YEAR_24, YEAR_25_Q4_ANNUALIZED, "", "", QUARTERLY_SUMMARY_TITLE, "24.4Q", "25.1Q"],
            ["", "revenue", "100", "120", "", "", "revenue", "30", "40"],
        ]

        records = parse_mixed_summary_block(13, block, context)

        self.assertEqual(len(records), 4)
        self.assertEqual(records[0]["sector_name"], "yearly")
        self.assertEqual(records[0]["period_type"], "YEAR")
        self.assertEqual(records[-1]["sector_name"], "quarterly")
        self.assertEqual(records[-1]["period_type"], "QUARTER")

    def test_parse_yearly_block(self):
        context = QdataFileContext(
            source_file_id=3,
            source_group="QDATA",
            relative_path="QDATA/sample_20260322_184846.csv",
            file_name="sample_20260322_184846.csv",
        )
        block = [
            ["", YEARLY_SECTION_TITLE + "1", YEAR_24, YEAR_25_Q3_ANNUALIZED],
            ["", "EPS", "732", "1111.11"],
        ]

        records = parse_yearly_block(30, block, context)

        self.assertEqual(len(records), 2)
        self.assertEqual(records[0]["raw_metric_name"], "EPS")
        self.assertEqual(records[0]["period_type"], "YEAR")
        self.assertEqual(records[1]["period_label_std"], "2025")


if __name__ == "__main__":
    unittest.main()
