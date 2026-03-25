from __future__ import annotations

import unittest

import pandas as pd
from sqlalchemy import create_engine, text

from python.etl.db_runtime import ensure_runtime_schema
from python.etl.parse_kdata2 import (
    Kdata2FileContext,
    contains_estimate_hint,
    derive_year_fields,
    get_metric_columns,
    melt_kdata2_sheet,
    replace_kdata2_raw_observations,
)


class ParseKdata2Test(unittest.TestCase):
    def test_derive_year_fields_from_date(self):
        date_raw, fiscal_year, period_label_std = derive_year_fields("2025/01/02")

        self.assertEqual(date_raw, "2025/01/02")
        self.assertEqual(fiscal_year, 2025)
        self.assertEqual(period_label_std, "2025")

    def test_contains_estimate_hint(self):
        self.assertTrue(contains_estimate_hint("Revenue (E)"))
        self.assertTrue(contains_estimate_hint("추정"))
        self.assertFalse(contains_estimate_hint("Revenue"))

    def test_get_metric_columns_from_row_wise_header(self):
        metric_columns = get_metric_columns(
            ["date", "open", "high", "close", "revenue", "operating_profit", ""]
        )

        self.assertEqual(
            metric_columns,
            [
                (1, "open"),
                (2, "high"),
                (3, "close"),
                (4, "revenue"),
                (5, "operating_profit"),
            ],
        )

    def test_melt_kdata2_sheet_generates_long_format_rows(self):
        dataframe = pd.DataFrame(
            [
                ["date", "close", "revenue (E)", "eps"],
                ["2026/01/02", 10250, 1234, 321],
                ["2025/01/02", 9800, 1200, 300],
            ]
        )
        context = Kdata2FileContext(
            source_file_id=2,
            source_group="KDATA2",
            relative_path="KDATA2/sample.xls",
            file_name="sample.xls",
        )

        rows = melt_kdata2_sheet(dataframe, context=context, sheet_name="Sheet1")

        self.assertEqual(len(rows), 6)
        self.assertEqual(rows[0]["source_group"], "KDATA2")
        self.assertEqual(rows[0]["raw_metric_name"], "close")
        self.assertEqual(rows[0]["date_raw"], "2026/01/02")
        self.assertEqual(rows[0]["fiscal_year"], 2026)
        self.assertIsNone(rows[0]["fiscal_quarter"])
        self.assertEqual(rows[0]["period_type"], "YEAR")
        self.assertEqual(rows[0]["period_label_std"], "2026")
        self.assertEqual(rows[1]["raw_metric_name"], "revenue (E)")
        self.assertEqual(rows[1]["is_estimate"], 1)

    def test_replace_kdata2_rows_inserts_into_raw_observation(self):
        engine = create_engine("sqlite:///:memory:", future=True)
        ensure_runtime_schema(engine)

        with engine.begin() as connection:
            connection.execute(
                text(
                    """
                    INSERT INTO source_file (
                        source_file_id,
                        source_group,
                        relative_path,
                        file_name,
                        file_extension,
                        canonical_input,
                        discovered_at
                    ) VALUES (
                        2,
                        'KDATA2',
                        'KDATA2/sample.xls',
                        'sample.xls',
                        '.xls',
                        1,
                        '2026-03-24T00:00:00+00:00'
                    )
                    """
                )
            )

            replace_kdata2_raw_observations(
                connection,
                source_file_id=2,
                records=[
                    {
                        "source_file_id": 2,
                        "source_group": "KDATA2",
                        "sheet_name": "Sheet1",
                        "source_row_number": 2,
                        "raw_company_name": "sample",
                        "raw_stock_code": None,
                        "normalized_stock_code": None,
                        "company_id": None,
                        "raw_metric_name": "close",
                        "standard_metric_name": None,
                        "value_text": "100",
                        "value_numeric": 100.0,
                        "value_unit": None,
                        "value_nature": None,
                        "is_estimate": 0,
                        "date_raw": "2025/01/02",
                        "raw_period_label": "2025/01/02",
                        "period_label_raw": "2025/01/02",
                        "period_type": "YEAR",
                        "fiscal_year": 2025,
                        "fiscal_quarter": None,
                        "normalized_quarter_label": None,
                        "period_label_std": "2025",
                        "ingested_at": "2026-03-24T00:00:00+00:00",
                    }
                ],
            )

            row_count = connection.execute(
                text("SELECT COUNT(*) FROM raw_observation WHERE source_group = 'KDATA2'")
            ).scalar_one()
            stored = connection.execute(
                text(
                    """
                    SELECT raw_metric_name, date_raw, fiscal_year, fiscal_quarter, period_label_std, is_estimate
                    FROM raw_observation
                    WHERE source_file_id = 2
                    """
                )
            ).one()

        self.assertEqual(row_count, 1)
        self.assertEqual(stored.raw_metric_name, "close")
        self.assertEqual(stored.date_raw, "2025/01/02")
        self.assertEqual(stored.fiscal_year, 2025)
        self.assertIsNone(stored.fiscal_quarter)
        self.assertEqual(stored.period_label_std, "2025")
        self.assertEqual(stored.is_estimate, 0)


if __name__ == "__main__":
    unittest.main()
