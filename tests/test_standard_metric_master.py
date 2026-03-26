from __future__ import annotations

import unittest

from python.etl.build_integrated_observation_enriched import build_enriched_records
from python.etl.standard_metric_master import (
    STANDARD_METRIC_SEED_ROWS,
    build_metric_name_mapping_seed_rows,
    suggest_standard_metric_candidates,
)


class StandardMetricMasterTest(unittest.TestCase):
    def test_standard_metric_seed_contains_expected_master_rows(self):
        standard_metric_names = {row["standard_metric_name"] for row in STANDARD_METRIC_SEED_ROWS}

        self.assertIn("REVENUE", standard_metric_names)
        self.assertIn("OPERATING_INCOME", standard_metric_names)
        self.assertIn("NET_INCOME", standard_metric_names)
        self.assertIn("TOTAL_ASSETS", standard_metric_names)
        self.assertIn("ROE", standard_metric_names)
        self.assertIn("NET_INCOME_GROWTH_RATE", standard_metric_names)

    def test_metric_name_mapping_seed_rows_include_high_confidence_english_aliases(self):
        standard_metric_lookup = {
            row["standard_metric_name"]: index
            for index, row in enumerate(STANDARD_METRIC_SEED_ROWS, start=1)
        }

        seed_rows = build_metric_name_mapping_seed_rows(standard_metric_lookup)
        by_key = {row["normalized_metric_key"]: row for row in seed_rows}

        self.assertEqual(by_key["revenue"]["standard_metric_name"], "REVENUE")
        self.assertEqual(by_key["sales"]["standard_metric_name"], "REVENUE")
        self.assertEqual(by_key["operating income".casefold()]["standard_metric_name"], "OPERATING_INCOME")
        self.assertEqual(by_key["net income".casefold()]["standard_metric_name"], "NET_INCOME")

    def test_build_enriched_records_populates_standard_metric_id_and_name(self):
        metric_mapping_lookup = {
            "매출액".casefold(): {
                "standard_metric_id": 101,
                "standard_metric_name": "REVENUE",
                "mapping_rule": "curated_exact_alias",
                "mapping_confidence": 1.0,
            },
            "sales".casefold(): {
                "standard_metric_id": 101,
                "standard_metric_name": "REVENUE",
                "mapping_rule": "seed_high_confidence_alias",
                "mapping_confidence": 0.95,
            },
        }

        rows = build_enriched_records(
            [
                {
                    "integrated_observation_id": 1,
                    "company_key": "opasnet",
                    "raw_metric_name": "매출액",
                    "period_type": "YEAR",
                    "fiscal_year": 2025,
                    "fiscal_quarter": None,
                    "date_raw": "2025/01/01",
                    "selected_source_group": "QDATA",
                    "selected_raw_observation_id": 1,
                    "selected_value_numeric": 100.0,
                    "selected_is_estimate": 0,
                },
                {
                    "integrated_observation_id": 2,
                    "company_key": "opasnet",
                    "raw_metric_name": "Sales",
                    "period_type": "YEAR",
                    "fiscal_year": 2025,
                    "fiscal_quarter": None,
                    "date_raw": "2025/01/01",
                    "selected_source_group": "QDATA",
                    "selected_raw_observation_id": 2,
                    "selected_value_numeric": 120.0,
                    "selected_is_estimate": 0,
                },
            ],
            metric_mapping_lookup,
        )

        self.assertEqual(rows[0]["standard_metric_id"], 101)
        self.assertEqual(rows[0]["standard_metric_name"], "REVENUE")
        self.assertEqual(rows[1]["standard_metric_id"], 101)
        self.assertEqual(rows[1]["standard_metric_name"], "REVENUE")

    def test_unmapped_record_keeps_standard_metric_id_null(self):
        rows = build_enriched_records(
            [
                {
                    "integrated_observation_id": 1,
                    "company_key": "opasnet",
                    "raw_metric_name": "지배주주EPS증가율",
                    "period_type": "YEAR",
                    "fiscal_year": 2025,
                    "fiscal_quarter": None,
                    "date_raw": "2025/01/01",
                    "selected_source_group": "QDATA",
                    "selected_raw_observation_id": 1,
                    "selected_value_numeric": 100.0,
                    "selected_is_estimate": 0,
                },
            ],
            {},
        )

        self.assertIsNone(rows[0]["standard_metric_id"])
        self.assertIsNone(rows[0]["standard_metric_name"])

    def test_suggestion_logic_returns_high_confidence_candidates_only(self):
        self.assertEqual(suggest_standard_metric_candidates("Revenue"), ["REVENUE"])
        self.assertEqual(
            suggest_standard_metric_candidates("Operating Income"),
            ["OPERATING_INCOME"],
        )
        self.assertEqual(suggest_standard_metric_candidates("지배주주EPS증가율"), [])


if __name__ == "__main__":
    unittest.main()
