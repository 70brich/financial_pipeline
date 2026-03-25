from __future__ import annotations

import unittest

from python.etl.build_integrated_observation import build_integrated_records


def raw_row(
    raw_observation_id: int,
    source_group: str,
    period_type: str,
    raw_metric_name: str,
    *,
    normalized_stock_code: str | None = None,
    raw_stock_code: str | None = None,
    raw_company_name: str | None = "opasnet",
    fiscal_year: int | None = None,
    fiscal_quarter: int | None = None,
    date_raw: str | None = None,
    value_text: str = "1",
    value_numeric: float | None = 1.0,
    is_estimate: int = 0,
    ingested_at: str = "2026-03-25T00:00:00+00:00",
) -> dict:
    return {
        "raw_observation_id": raw_observation_id,
        "source_file_id": 1,
        "source_group": source_group,
        "raw_company_name": raw_company_name,
        "raw_stock_code": raw_stock_code,
        "normalized_stock_code": normalized_stock_code,
        "raw_metric_name": raw_metric_name,
        "value_text": value_text,
        "value_numeric": value_numeric,
        "is_estimate": is_estimate,
        "date_raw": date_raw,
        "period_type": period_type,
        "fiscal_year": fiscal_year,
        "fiscal_quarter": fiscal_quarter,
        "period_label_std": date_raw or str(fiscal_year or ""),
        "ingested_at": ingested_at,
    }


class BuildIntegratedObservationTest(unittest.TestCase):
    def test_exact_raw_metric_name_only(self):
        records = build_integrated_records(
            [
                raw_row(1, "QDATA", "QUARTER", "revenue", fiscal_year=2025, fiscal_quarter=4, date_raw="2025/10/01"),
                raw_row(2, "KDATA1", "QUARTER", "opm_percent", fiscal_year=2025, fiscal_quarter=4, date_raw="2025/10/01"),
            ]
        )

        self.assertEqual(len(records), 2)

    def test_non_estimate_beats_estimate(self):
        records = build_integrated_records(
            [
                raw_row(1, "QDATA", "YEAR", "revenue", fiscal_year=2025, date_raw="2025/01/01", is_estimate=1),
                raw_row(2, "KDATA2", "YEAR", "revenue", fiscal_year=2025, date_raw="2025/01/01", is_estimate=0),
            ]
        )

        self.assertEqual(records[0]["selected_raw_observation_id"], 2)
        self.assertEqual(records[0]["selection_reason"], "confirmed_kdata2")

    def test_year_priority_qdata_then_kdata2_then_kdata1(self):
        records = build_integrated_records(
            [
                raw_row(1, "KDATA1", "YEAR", "revenue", fiscal_year=2025, date_raw="2025/01/01"),
                raw_row(2, "KDATA2", "YEAR", "revenue", fiscal_year=2025, date_raw="2025/01/01"),
                raw_row(3, "QDATA", "YEAR", "revenue", fiscal_year=2025, date_raw="2025/01/01"),
            ]
        )

        self.assertEqual(records[0]["selected_source_group"], "QDATA")

    def test_quarter_priority_qdata_then_kdata1_then_kdata2(self):
        records = build_integrated_records(
            [
                raw_row(1, "KDATA2", "QUARTER", "revenue", fiscal_year=2025, fiscal_quarter=4, date_raw="2025/10/01"),
                raw_row(2, "KDATA1", "QUARTER", "revenue", fiscal_year=2025, fiscal_quarter=4, date_raw="2025/10/01"),
                raw_row(3, "QDATA", "QUARTER", "revenue", fiscal_year=2025, fiscal_quarter=4, date_raw="2025/10/01"),
            ]
        )

        self.assertEqual(records[0]["selected_source_group"], "QDATA")

    def test_snapshot_priority_qdata_first(self):
        records = build_integrated_records(
            [
                raw_row(1, "KDATA2", "SNAPSHOT", "price", date_raw="2026/03/22"),
                raw_row(2, "QDATA", "SNAPSHOT", "price", date_raw="2026/03/22"),
            ]
        )

        self.assertEqual(records[0]["selected_source_group"], "QDATA")

    def test_duplicate_rows_tie_break_to_latest_and_numeric(self):
        records = build_integrated_records(
            [
                raw_row(1, "KDATA2", "YEAR", "eps", fiscal_year=2025, date_raw="2025/01/01", value_numeric=None, ingested_at="2026-03-25T00:00:00+00:00"),
                raw_row(2, "KDATA2", "YEAR", "eps", fiscal_year=2025, date_raw="2025/01/01", value_numeric=100.0, ingested_at="2026-03-24T00:00:00+00:00"),
                raw_row(3, "KDATA2", "YEAR", "eps", fiscal_year=2025, date_raw="2025/01/01", value_numeric=100.0, ingested_at="2026-03-26T00:00:00+00:00"),
            ]
        )

        self.assertEqual(records[0]["selected_raw_observation_id"], 3)


if __name__ == "__main__":
    unittest.main()
