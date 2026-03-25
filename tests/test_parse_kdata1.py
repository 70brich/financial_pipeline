from __future__ import annotations

import unittest

import pandas as pd
from sqlalchemy import create_engine, text

from python.etl.db_runtime import ensure_runtime_schema
from python.etl.parse_kdata1 import (
    Kdata1FileContext,
    choose_excel_engine,
    derive_quarter_fields,
    get_metric_columns,
    melt_kdata1_sheet,
    replace_kdata1_raw_observations,
)


class ParseKdata1Test(unittest.TestCase):
    def test_choose_excel_engine_by_extension(self):
        self.assertEqual(choose_excel_engine("sample.xls"), "xlrd")
        self.assertEqual(choose_excel_engine("sample.xlsx"), "openpyxl")
        self.assertEqual(choose_excel_engine("sample.xlsm"), "openpyxl")

    def test_derive_quarter_fields_from_date(self):
        date_raw, fiscal_year, fiscal_quarter, period_label_std = derive_quarter_fields(
            "2024/04/01"
        )

        self.assertEqual(date_raw, "2024/04/01")
        self.assertEqual(fiscal_year, 2024)
        self.assertEqual(fiscal_quarter, 2)
        self.assertEqual(period_label_std, "24.2Q")

    def test_get_metric_columns_from_row_wise_header(self):
        metric_columns = get_metric_columns(
            ["date", "open", "high", "low", "close", "revenue", "operating_profit", ""]
        )

        self.assertEqual(
            metric_columns,
            [
                (1, "open"),
                (2, "high"),
                (3, "low"),
                (4, "close"),
                (5, "revenue"),
                (6, "operating_profit"),
            ],
        )

    def test_melt_kdata1_sheet_generates_long_format_rows(self):
        dataframe = pd.DataFrame(
            [
                ["date", "revenue", "operating_profit", "eps"],
                ["2025/10/01", 1234, 98, 321],
                ["2025/07/01", 1200, 95, 300],
            ]
        )
        context = Kdata1FileContext(
            source_file_id=1,
            source_group="KDATA1",
            relative_path="KDATA1/sample.xls",
            file_name="sample.xls",
        )

        rows = melt_kdata1_sheet(dataframe, context=context, sheet_name="Sheet1")

        self.assertEqual(len(rows), 6)
        self.assertEqual(rows[0]["source_file_id"], 1)
        self.assertEqual(rows[0]["source_group"], "KDATA1")
        self.assertEqual(rows[0]["raw_metric_name"], "revenue")
        self.assertEqual(rows[0]["value_text"], "1234")
        self.assertEqual(rows[0]["value_numeric"], 1234.0)
        self.assertEqual(rows[0]["date_raw"], "2025/10/01")
        self.assertEqual(rows[0]["fiscal_year"], 2025)
        self.assertEqual(rows[0]["fiscal_quarter"], 4)
        self.assertEqual(rows[0]["period_type"], "QUARTER")
        self.assertEqual(rows[0]["period_label_std"], "25.4Q")
        self.assertEqual(rows[1]["raw_metric_name"], "operating_profit")
        self.assertEqual(rows[2]["raw_metric_name"], "eps")

    def test_replace_kdata1_rows_inserts_into_raw_observation(self):
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
                        1,
                        'KDATA1',
                        'KDATA1/sample.xls',
                        'sample.xls',
                        '.xls',
                        1,
                        '2026-03-24T00:00:00+00:00'
                    )
                    """
                )
            )

            replace_kdata1_raw_observations(
                connection,
                source_file_id=1,
                records=[
                    {
                        "source_file_id": 1,
                        "source_group": "KDATA1",
                        "sheet_name": "Sheet1",
                        "source_row_number": 2,
                        "raw_company_name": "sample",
                        "raw_stock_code": None,
                        "normalized_stock_code": None,
                        "company_id": None,
                        "raw_metric_name": "revenue",
                        "standard_metric_name": None,
                        "value_text": "100",
                        "value_numeric": 100.0,
                        "value_unit": None,
                        "value_nature": None,
                        "is_estimate": 0,
                        "date_raw": "2024/01/02",
                        "raw_period_label": "2024/01/02",
                        "period_label_raw": "2024/01/02",
                        "period_type": "QUARTER",
                        "fiscal_year": 2024,
                        "fiscal_quarter": 1,
                        "normalized_quarter_label": "24.1Q",
                        "period_label_std": "24.1Q",
                        "ingested_at": "2026-03-24T00:00:00+00:00",
                    }
                ],
            )

            row_count = connection.execute(
                text("SELECT COUNT(*) FROM raw_observation")
            ).scalar_one()
            stored = connection.execute(
                text(
                    """
                    SELECT raw_metric_name, date_raw, fiscal_year, fiscal_quarter, period_label_std
                    FROM raw_observation
                    WHERE source_file_id = 1
                    """
                )
            ).one()

        self.assertEqual(row_count, 1)
        self.assertEqual(stored.raw_metric_name, "revenue")
        self.assertEqual(stored.date_raw, "2024/01/02")
        self.assertEqual(stored.fiscal_year, 2024)
        self.assertEqual(stored.fiscal_quarter, 1)
        self.assertEqual(stored.period_label_std, "24.1Q")


if __name__ == "__main__":
    unittest.main()
