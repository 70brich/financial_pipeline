from __future__ import annotations

import unittest

from python.etl.build_integrated_observation_enriched import build_enriched_records
from python.etl.metric_mapping import DEFAULT_ALIAS_MAP, normalize_metric_key


def integrated_row(
    integrated_observation_id: int,
    raw_metric_name: str,
    *,
    period_type: str = "YEAR",
    company_key: str = "opasnet",
) -> dict:
    return {
        "integrated_observation_id": integrated_observation_id,
        "company_key": company_key,
        "raw_metric_name": raw_metric_name,
        "period_type": period_type,
        "fiscal_year": 2025,
        "fiscal_quarter": 4 if period_type == "QUARTER" else None,
        "date_raw": "2025/10/01" if period_type == "QUARTER" else "2025/01/01",
        "selected_source_group": "QDATA",
        "selected_raw_observation_id": integrated_observation_id,
        "selected_value_numeric": 100.0,
        "selected_is_estimate": 0,
    }


class MetricMappingTest(unittest.TestCase):
    def test_revenue_aliases_map_with_prefix_handling(self):
        metric_alias_map = DEFAULT_ALIAS_MAP
        records = build_enriched_records(
            [
                integrated_row(1, "\ub9e4\ucd9c\uc561"),
                integrated_row(2, "\ubd84\uae30 \ub9e4\ucd9c\uc561", period_type="QUARTER"),
                integrated_row(3, "(\uac1c\ubcc4)\ub9e4\ucd9c\uc561"),
            ],
            metric_alias_map,
        )

        self.assertEqual(records[0]["standard_metric_name"], "REVENUE")
        self.assertEqual(records[1]["standard_metric_name"], "REVENUE")
        self.assertEqual(records[2]["standard_metric_name"], "REVENUE")
        self.assertEqual(records[2]["metric_variant"], "\uac1c\ubcc4")

    def test_cosmetic_symbol_prefixes_are_removed_for_lookup_only(self):
        metric_alias_map = DEFAULT_ALIAS_MAP
        records = build_enriched_records(
            [
                integrated_row(1, "- \ub9e4\ucd9c\uc561"),
                integrated_row(2, "+ \ubd84\uae30 \ub9e4\ucd9c\uc561", period_type="QUARTER"),
                integrated_row(3, "=(\uac1c\ubcc4)\uc720\ub3d9\uc790\uc0b0"),
                integrated_row(4, "- OPM(%)"),
            ],
            metric_alias_map,
        )

        self.assertEqual(records[0]["raw_metric_name"], "- \ub9e4\ucd9c\uc561")
        self.assertEqual(records[0]["normalized_metric_key"], "\ub9e4\ucd9c\uc561".casefold())
        self.assertEqual(records[0]["standard_metric_name"], "REVENUE")
        self.assertEqual(records[1]["normalized_metric_key"], "\ub9e4\ucd9c\uc561".casefold())
        self.assertEqual(records[1]["standard_metric_name"], "REVENUE")
        self.assertEqual(records[2]["raw_metric_name"], "=(\uac1c\ubcc4)\uc720\ub3d9\uc790\uc0b0")
        self.assertEqual(records[2]["normalized_metric_key"], "\uc720\ub3d9\uc790\uc0b0".casefold())
        self.assertEqual(records[2]["metric_variant"], "\uac1c\ubcc4")
        self.assertEqual(records[2]["standard_metric_name"], "CURRENT_ASSETS")
        self.assertEqual(records[3]["normalized_metric_key"], "opm(%)".casefold())
        self.assertEqual(records[3]["standard_metric_name"], "OPERATING_MARGIN")

    def test_operating_margin_aliases_map(self):
        metric_alias_map = DEFAULT_ALIAS_MAP
        records = build_enriched_records(
            [
                integrated_row(0, "OPM"),
                integrated_row(1, "\uc601\uc5c5\uc774\uc775\ub960"),
                integrated_row(2, "OPM(%)"),
                integrated_row(3, "(\uac1c\ubcc4)OPM(%)"),
            ],
            metric_alias_map,
        )

        self.assertEqual(records[0]["standard_metric_name"], "OPERATING_MARGIN")
        self.assertEqual(records[1]["standard_metric_name"], "OPERATING_MARGIN")
        self.assertEqual(records[2]["standard_metric_name"], "OPERATING_MARGIN")
        self.assertEqual(records[3]["standard_metric_name"], "OPERATING_MARGIN")
        self.assertEqual(records[3]["metric_variant"], "\uac1c\ubcc4")

    def test_gpm_and_gross_margin_percent_do_not_collapse_to_same_standard_name(self):
        metric_alias_map = DEFAULT_ALIAS_MAP
        records = build_enriched_records(
            [
                integrated_row(1, "GPM"),
                integrated_row(2, "\ub9e4\ucd9c\ucd1d\uc774\uc775\ub960(%)"),
            ],
            metric_alias_map,
        )

        self.assertEqual(records[0]["standard_metric_name"], "GROSS_MARGIN")
        self.assertEqual(records[1]["standard_metric_name"], "GROSS_MARGIN")
        self.assertEqual(records[0]["raw_metric_name"], "GPM")
        self.assertEqual(records[1]["raw_metric_name"], "\ub9e4\ucd9c\ucd1d\uc774\uc775\ub960(%)")

    def test_per_five_year_average_does_not_merge_with_per(self):
        per_key, _ = normalize_metric_key("PER")
        avg_key, _ = normalize_metric_key("PER(5\ub144\ud3c9\uade0)")

        self.assertEqual(DEFAULT_ALIAS_MAP[per_key], "PER")
        self.assertNotEqual(per_key, avg_key)
        self.assertNotIn(avg_key, DEFAULT_ALIAS_MAP)

    def test_unmapped_metric_preserves_raw_name(self):
        records = build_enriched_records(
            [integrated_row(1, "PER(5\ub144\ud3c9\uade0)")],
            DEFAULT_ALIAS_MAP,
        )

        self.assertEqual(records[0]["raw_metric_name"], "PER(5\ub144\ud3c9\uade0)")
        self.assertEqual(records[0]["standard_metric_name"], None)
        self.assertEqual(records[0]["normalized_metric_key"], "per(5\ub144\ud3c9\uade0)".casefold())

    def test_balance_sheet_totals_preserve_raw_name_and_map(self):
        records = build_enriched_records(
            [
                integrated_row(1, "\ucd1d\uc790\uc0b0"),
                integrated_row(2, "\uc790\ubcf8\ucd1d\uacc4"),
                integrated_row(3, "\ubd80\ucc44\ucd1d\uacc4"),
            ],
            DEFAULT_ALIAS_MAP,
        )

        self.assertEqual(records[0]["raw_metric_name"], "\ucd1d\uc790\uc0b0")
        self.assertEqual(records[0]["standard_metric_name"], "TOTAL_ASSETS")
        self.assertEqual(records[1]["raw_metric_name"], "\uc790\ubcf8\ucd1d\uacc4")
        self.assertEqual(records[1]["standard_metric_name"], "TOTAL_EQUITY")
        self.assertEqual(records[2]["raw_metric_name"], "\ubd80\ucc44\ucd1d\uacc4")
        self.assertEqual(records[2]["standard_metric_name"], "TOTAL_LIABILITIES")

    def test_free_cash_flow_aliases_map(self):
        records = build_enriched_records(
            [
                integrated_row(1, "FCF"),
                integrated_row(2, "\uc789\uc5ec\ud604\uae08\ud750\ub984"),
            ],
            DEFAULT_ALIAS_MAP,
        )

        self.assertEqual(records[0]["standard_metric_name"], "FREE_CASH_FLOW")
        self.assertEqual(records[1]["standard_metric_name"], "FREE_CASH_FLOW")

    def test_quick_ratio_aliases_map(self):
        records = build_enriched_records(
            [
                integrated_row(1, "\ub2f9\uc88c\ube44\uc728"),
                integrated_row(2, "\ub2f9\uc88c\ube44\uc728(%)"),
            ],
            DEFAULT_ALIAS_MAP,
        )

        self.assertEqual(records[0]["standard_metric_name"], "QUICK_RATIO")
        self.assertEqual(records[1]["standard_metric_name"], "QUICK_RATIO")

    def test_accounts_payable_and_receivable_map(self):
        records = build_enriched_records(
            [
                integrated_row(1, "\ub9e4\uc785\ucc44\ubb34"),
                integrated_row(2, "\ub9e4\ucd9c\ucc44\uad8c"),
            ],
            DEFAULT_ALIAS_MAP,
        )

        self.assertEqual(records[0]["standard_metric_name"], "ACCOUNTS_PAYABLE")
        self.assertEqual(records[1]["standard_metric_name"], "ACCOUNTS_RECEIVABLE")

    def test_current_and_non_current_assets_and_liabilities_map(self):
        records = build_enriched_records(
            [
                integrated_row(1, "\uc720\ub3d9\uc790\uc0b0"),
                integrated_row(2, "\uc720\ub3d9\ubd80\ucc44"),
                integrated_row(3, "\ube44\uc720\ub3d9\uc790\uc0b0"),
                integrated_row(4, "\ube44\uc720\ub3d9\ubd80\ucc44"),
            ],
            DEFAULT_ALIAS_MAP,
        )

        self.assertEqual(records[0]["standard_metric_name"], "CURRENT_ASSETS")
        self.assertEqual(records[1]["standard_metric_name"], "CURRENT_LIABILITIES")
        self.assertEqual(records[2]["standard_metric_name"], "NON_CURRENT_ASSETS")
        self.assertEqual(records[3]["standard_metric_name"], "NON_CURRENT_LIABILITIES")

    def test_asset_cash_and_inventory_aliases_map(self):
        records = build_enriched_records(
            [
                integrated_row(1, "\uc720\ud615\uc790\uc0b0"),
                integrated_row(2, "\ubb34\ud615\uc790\uc0b0"),
                integrated_row(3, "\uc7ac\uace0\uc790\uc0b0"),
                integrated_row(4, "\ud604\uae08\uc131\uc790\uc0b0"),
            ],
            DEFAULT_ALIAS_MAP,
        )

        self.assertEqual(records[0]["standard_metric_name"], "PROPERTY_PLANT_EQUIPMENT")
        self.assertEqual(records[1]["standard_metric_name"], "INTANGIBLE_ASSETS")
        self.assertEqual(records[2]["standard_metric_name"], "INVENTORIES")
        self.assertEqual(records[3]["standard_metric_name"], "CASH_EQUIVALENTS")

    def test_retained_earnings_maps(self):
        records = build_enriched_records(
            [integrated_row(1, "\uc774\uc775\uc789\uc5ec\uae08")],
            DEFAULT_ALIAS_MAP,
        )

        self.assertEqual(records[0]["standard_metric_name"], "RETAINED_EARNINGS")

    def test_borrowings_and_net_debt_map(self):
        records = build_enriched_records(
            [
                integrated_row(1, "\ucc28\uc785\uae08"),
                integrated_row(2, "\uc21c\ucc28\uc785\uae08"),
            ],
            DEFAULT_ALIAS_MAP,
        )

        self.assertEqual(records[0]["standard_metric_name"], "BORROWINGS")
        self.assertEqual(records[1]["standard_metric_name"], "NET_DEBT")

    def test_choice2_policy_metrics_map_by_exact_alias_only(self):
        records = build_enriched_records(
            [
                integrated_row(1, "\uc138\uc804\uacc4\uc18d\uc0ac\uc5c5\uc190\uc775"),
                integrated_row(2, "\uc138\uc804\uacc4\uc18d\uc0ac\uc5c5\uc774\uc775\ub960"),
                integrated_row(3, "\uc9c0\ubc30\uc8fc\uc8fcROE"),
                integrated_row(4, "NPM"),
                integrated_row(5, "NPM(%)"),
                integrated_row(6, "(\uac1c\ubcc4)\uc9c0\ubc30\uc8fc\uc8fcROE"),
            ],
            DEFAULT_ALIAS_MAP,
        )

        self.assertEqual(records[0]["standard_metric_name"], "PRE_TAX_CONTINUING_INCOME")
        self.assertEqual(records[1]["standard_metric_name"], "PRE_TAX_CONTINUING_MARGIN")
        self.assertEqual(records[2]["standard_metric_name"], "SHAREHOLDER_ROE")
        self.assertEqual(records[3]["standard_metric_name"], "NET_MARGIN")
        self.assertEqual(records[4]["standard_metric_name"], "NET_MARGIN")
        self.assertEqual(records[5]["raw_metric_name"], "(\uac1c\ubcc4)\uc9c0\ubc30\uc8fc\uc8fcROE")
        self.assertEqual(records[5]["metric_variant"], "\uac1c\ubcc4")
        self.assertEqual(records[5]["normalized_metric_key"], "\uc9c0\ubc30\uc8fc\uc8fcroe".casefold())
        self.assertEqual(records[5]["standard_metric_name"], "SHAREHOLDER_ROE")

    def test_growth_rate_and_five_year_average_stay_unmapped_under_choice2(self):
        records = build_enriched_records(
            [
                integrated_row(1, "ROE(5\ub144\ud3c9\uade0)"),
            ],
            DEFAULT_ALIAS_MAP,
        )

        self.assertIsNone(records[0]["standard_metric_name"])

    def test_choice2_income_component_metrics_map_by_exact_alias_only(self):
        records = build_enriched_records(
            [
                integrated_row(1, "\uc138\uc804\uc21c\uc774\uc775"),
                integrated_row(2, "\uc138\uc804\uc21c\uc775"),
                integrated_row(3, "\ubc95\uc778\uc138"),
                integrated_row(4, "\uad00\uacc4\uae30\uc5c5\uc190\uc775"),
                integrated_row(5, "\uae08\uc735\uc190\uc775"),
                integrated_row(6, "\uae30\ud0c0\uc601\uc5c5\uc678\uc190\uc775"),
                integrated_row(7, "=\uc138\uc804\uc21c\uc775"),
                integrated_row(8, "- \ubc95\uc778\uc138"),
                integrated_row(9, "+-\uad00\uacc4\uae30\uc5c5\uc190\uc775"),
            ],
            DEFAULT_ALIAS_MAP,
        )

        self.assertEqual(records[0]["standard_metric_name"], "PRE_TAX_INCOME")
        self.assertEqual(records[1]["standard_metric_name"], "PRE_TAX_INCOME")
        self.assertEqual(records[2]["standard_metric_name"], "CORPORATE_TAX")
        self.assertEqual(records[3]["standard_metric_name"], "AFFILIATE_INCOME")
        self.assertEqual(records[4]["standard_metric_name"], "FINANCIAL_INCOME")
        self.assertEqual(records[5]["standard_metric_name"], "NON_OPERATING_INCOME")
        self.assertEqual(records[6]["standard_metric_name"], "PRE_TAX_INCOME")
        self.assertEqual(records[7]["standard_metric_name"], "CORPORATE_TAX")
        self.assertEqual(records[8]["standard_metric_name"], "AFFILIATE_INCOME")

    def test_supplementary_per_share_and_valuation_metrics_stay_unmapped(self):
        records = build_enriched_records(
            [
                integrated_row(1, "CPS"),
                integrated_row(2, "DPS"),
                integrated_row(3, "OPS"),
                integrated_row(4, "SPS"),
                integrated_row(5, "EV/EBITDA"),
                integrated_row(6, "ROIC"),
            ],
            DEFAULT_ALIAS_MAP,
        )

        for record in records:
            self.assertIsNone(record["standard_metric_name"])

    def test_choice2_accounting_investment_metrics_map_by_exact_alias_only(self):
        records = build_enriched_records(
            [
                integrated_row(1, "\ube44\uc9c0\ubc30\uc21c\uc774\uc775"),
                integrated_row(2, "\uac10\uac00\uc0c1\uac01\ube44"),
                integrated_row(3, "\uc124\ube44\ud22c\uc790"),
                integrated_row(4, "\ud22c\uc790\uc790\uc0b0"),
                integrated_row(5, "\ud22c\ud558\uc790\ubcf8"),
                integrated_row(6, "- \uac10\uac00\uc0c1\uac01\ube44"),
            ],
            DEFAULT_ALIAS_MAP,
        )

        self.assertEqual(records[0]["standard_metric_name"], "NON_CONTROLLING_PROFIT")
        self.assertEqual(records[1]["standard_metric_name"], "DEPRECIATION_EXPENSE")
        self.assertEqual(records[2]["standard_metric_name"], "CAPEX")
        self.assertEqual(records[3]["standard_metric_name"], "INVESTMENT_ASSETS")
        self.assertEqual(records[4]["standard_metric_name"], "INVESTED_CAPITAL")
        self.assertEqual(records[5]["standard_metric_name"], "DEPRECIATION_EXPENSE")

    def test_choice2_ratio_metrics_map_by_exact_alias_only(self):
        records = build_enriched_records(
            [
                integrated_row(1, "\uac10\uac00\uc0c1\uac01\ube44\uc728"),
                integrated_row(2, "\ud310\uad00\ube44\uc728"),
                integrated_row(3, "\uc5f0\uad6c\ube44\uc728"),
                integrated_row(4, "\ucc28\uc785\ub960(%)"),
                integrated_row(5, "\uc601\uc5c5\uc774\uc775/\ucc28\uc785\uae08(%)"),
                integrated_row(6, "- \uac10\uac00\uc0c1\uac01\ube44\uc728"),
            ],
            DEFAULT_ALIAS_MAP,
        )

        self.assertEqual(records[0]["standard_metric_name"], "DEPRECIATION_RATIO")
        self.assertEqual(records[1]["standard_metric_name"], "SGA_RATIO")
        self.assertEqual(records[2]["standard_metric_name"], "RND_RATIO")
        self.assertEqual(records[3]["standard_metric_name"], "BORROWING_RATIO")
        self.assertEqual(records[4]["standard_metric_name"], "OPERATING_INCOME_TO_BORROWINGS_RATIO")
        self.assertEqual(records[5]["standard_metric_name"], "DEPRECIATION_RATIO")

    def test_growth_dividend_turnover_and_per_share_metrics_stay_unmapped_after_ratio_batch(self):
        records = build_enriched_records(
            [
                integrated_row(1, "\uc9c0\ubc30\uc8fc\uc8fceps\uc99d\uac00\uc728"),
                integrated_row(2, "\uc9c0\ubc30\uc21c\uc775 \uc99d\uac00\uc728(%)"),
                integrated_row(3, "\ub9e4\uc785\ucc44\ubb34\ud68c\uc804\uc77c\uc218"),
                integrated_row(4, "\ubc30\ub2f9\uc131\ud5a5(%)"),
                integrated_row(5, "DPS"),
                integrated_row(6, "EV/EBITDA"),
                integrated_row(7, "ROE(5\ub144\ud3c9\uade0)"),
            ],
            DEFAULT_ALIAS_MAP,
        )

        for record in records:
            self.assertIsNone(record["standard_metric_name"])

    def test_choice2_growth_rate_metrics_map_by_exact_alias_only(self):
        records = build_enriched_records(
            [
                integrated_row(1, "\ub9e4\ucd9c\uc561\uc99d\uac00\uc728"),
                integrated_row(2, "\ub9e4\ucd9c\uc561 \uc99d\uac00\uc728(%)"),
                integrated_row(3, "\ud310\uad00\ube44\uc99d\uac00\uc728"),
                integrated_row(4, "\uc601\uc5c5\uc774\uc775\uc99d\uac00\uc728"),
                integrated_row(5, "\uc601\uc5c5\uc774\uc775 \uc99d\uac00\uc728(%)"),
                integrated_row(6, "BPS\uc99d\uac00\uc728(%)"),
                integrated_row(7, "EPS\uc99d\uac00\uc728(%)"),
                integrated_row(8, "FCF\uc99d\uac00\uc728(%)"),
                integrated_row(9, "NPM\uc99d\uac00\uc728(%)"),
                integrated_row(10, "OPM\uc99d\uac00\uc728(%)"),
                integrated_row(11, "ROA\uc99d\uac00\uc728(%)"),
                integrated_row(12, "ROE\uc99d\uac00\uc728(%)"),
                integrated_row(13, "\uc124\ube44\ud22c\uc790\uc99d\uac00\uc728(%)"),
                integrated_row(14, "\uc601\uc5c5\ud604\uae08\uc99d\uac00\uc728(%)"),
                integrated_row(15, "\uc790\ubcf8\uc99d\uac00\uc728(%)"),
                integrated_row(16, "\uc790\uc0b0\uc99d\uac00\uc728(%)"),
                integrated_row(17, "- \ub9e4\ucd9c\uc561\uc99d\uac00\uc728"),
            ],
            DEFAULT_ALIAS_MAP,
        )

        self.assertEqual(records[0]["standard_metric_name"], "REVENUE_GROWTH_RATE")
        self.assertEqual(records[1]["standard_metric_name"], "REVENUE_GROWTH_RATE")
        self.assertEqual(records[2]["standard_metric_name"], "SGA_GROWTH_RATE")
        self.assertEqual(records[3]["standard_metric_name"], "OPERATING_INCOME_GROWTH_RATE")
        self.assertEqual(records[4]["standard_metric_name"], "OPERATING_INCOME_GROWTH_RATE")
        self.assertEqual(records[5]["standard_metric_name"], "BPS_GROWTH_RATE")
        self.assertEqual(records[6]["standard_metric_name"], "EPS_GROWTH_RATE")
        self.assertEqual(records[7]["standard_metric_name"], "FCF_GROWTH_RATE")
        self.assertEqual(records[8]["standard_metric_name"], "NPM_GROWTH_RATE")
        self.assertEqual(records[9]["standard_metric_name"], "OPM_GROWTH_RATE")
        self.assertEqual(records[10]["standard_metric_name"], "ROA_GROWTH_RATE")
        self.assertEqual(records[11]["standard_metric_name"], "ROE_GROWTH_RATE")
        self.assertEqual(records[12]["standard_metric_name"], "CAPEX_GROWTH_RATE")
        self.assertEqual(records[13]["standard_metric_name"], "OPERATING_CASHFLOW_GROWTH_RATE")
        self.assertEqual(records[14]["standard_metric_name"], "EQUITY_GROWTH_RATE")
        self.assertEqual(records[15]["standard_metric_name"], "ASSET_GROWTH_RATE")
        self.assertEqual(records[16]["standard_metric_name"], "REVENUE_GROWTH_RATE")

    def test_raw_metric_name_preserved_with_variant_prefix(self):
        records = build_enriched_records(
            [integrated_row(1, "(\uac1c\ubcc4)\uc720\ub3d9\uc790\uc0b0")],
            DEFAULT_ALIAS_MAP,
        )

        self.assertEqual(records[0]["raw_metric_name"], "(\uac1c\ubcc4)\uc720\ub3d9\uc790\uc0b0")
        self.assertEqual(records[0]["normalized_metric_key"], "\uc720\ub3d9\uc790\uc0b0".casefold())
        self.assertEqual(records[0]["metric_variant"], "\uac1c\ubcc4")
        self.assertEqual(records[0]["standard_metric_name"], "CURRENT_ASSETS")


if __name__ == "__main__":
    unittest.main()
