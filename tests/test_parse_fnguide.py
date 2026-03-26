from __future__ import annotations

import unittest

from python.etl.parse_fnguide import (
    FnGuideCompanyContext,
    normalize_fnguide_numeric,
    normalize_period_label,
    parse_consensus_financial_table,
)


class ParseFnGuideTest(unittest.TestCase):
    def test_normalize_fnguide_numeric_handles_common_text(self) -> None:
        self.assertEqual(normalize_fnguide_numeric("1,234.50"), 1234.5)
        self.assertEqual(normalize_fnguide_numeric("12.3%"), 12.3)
        self.assertEqual(normalize_fnguide_numeric("320,000원"), 320000.0)
        self.assertIsNone(normalize_fnguide_numeric("-"))

    def test_normalize_period_label_for_year_quarter_and_snapshot(self) -> None:
        year_info = normalize_period_label("2026/12(E)", "YEAR")
        self.assertEqual(year_info["period_type"], "YEAR")
        self.assertEqual(year_info["fiscal_year"], 2026)
        self.assertEqual(year_info["is_estimate"], 1)

        quarter_info = normalize_period_label("2026/03(E)", "QUARTER")
        self.assertEqual(quarter_info["period_type"], "QUARTER")
        self.assertEqual(quarter_info["fiscal_year"], 2026)
        self.assertEqual(quarter_info["fiscal_quarter"], 1)
        self.assertEqual(quarter_info["period_label_std"], "26.1Q")

        snapshot_info = normalize_period_label("2026/03/25")
        self.assertEqual(snapshot_info["period_type"], "SNAPSHOT")
        self.assertEqual(snapshot_info["date_raw"], "2026/03/25")

    def test_parse_consensus_financial_table_to_long_rows(self) -> None:
        payload = {
            "comp": [
                {
                    "ACCOUNT_NM": "항목",
                    "D_2": "2025/12",
                    "D_3": "2026/12(E)",
                },
                {
                    "SORT_ORDER": "1",
                    "GB": "0",
                    "PARENT_YN": "Y",
                    "ACCOUNT_NM": "매출액(억원)",
                    "D_2": "100",
                    "D_3": "120",
                },
                {
                    "SORT_ORDER": "2",
                    "GB": "0",
                    "PARENT_YN": "Y",
                    "ACCOUNT_NM": "영업이익(억원)",
                    "D_2": "10",
                    "D_3": "-",
                },
            ]
        }
        company = FnGuideCompanyContext(company_name="삼성전자", stock_code="005930", gicode="A005930")
        records = parse_consensus_financial_table(
            payload,
            company=company,
            source_url="https://example.test/consensus",
            ifrs_scope="CONNECTED",
            period_scope="YEAR",
        )

        self.assertEqual(len(records), 3)
        self.assertEqual(records[0]["raw_metric_name"], "매출액")
        self.assertEqual(records[0]["value_unit"], "억원")
        self.assertEqual(records[0]["fiscal_year"], 2025)
        self.assertEqual(records[1]["is_estimate"], 1)
        self.assertEqual(records[2]["raw_metric_name"], "영업이익")


if __name__ == "__main__":
    unittest.main()
