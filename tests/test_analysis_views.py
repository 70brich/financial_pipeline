from __future__ import annotations

import unittest

from sqlalchemy import create_engine, text

from python.etl.analysis_views import execute_analysis_views
from python.etl.build_integrated_observation import execute_integrated_schema
from python.etl.build_integrated_observation_enriched import execute_metric_mapping_schema
from python.etl.db_runtime import ensure_runtime_schema


class AnalysisViewTest(unittest.TestCase):
    def setUp(self) -> None:
        self.engine = create_engine("sqlite:///:memory:", future=True)
        ensure_runtime_schema(self.engine)
        execute_integrated_schema(self.engine)
        execute_metric_mapping_schema(self.engine)
        execute_analysis_views(self.engine)

    def test_company_metric_timeseries_projects_selected_fields(self):
        with self.engine.begin() as connection:
            connection.execute(
                text(
                    """
                    INSERT INTO raw_observation (
                        raw_observation_id,
                        source_file_id,
                        source_group,
                        raw_company_name,
                        raw_stock_code,
                        normalized_stock_code,
                        company_id,
                        raw_metric_name,
                        value_text,
                        value_numeric,
                        is_estimate,
                        date_raw,
                        period_type,
                        fiscal_year,
                        fiscal_quarter,
                        period_label_std
                    ) VALUES (
                        1,
                        1,
                        'QDATA',
                        'Opasnet Raw',
                        '173130',
                        '173130',
                        NULL,
                        'Revenue',
                        '100',
                        100,
                        0,
                        '2025/01/01',
                        'YEAR',
                        2025,
                        NULL,
                        '2025'
                    )
                    """
                )
            )
            connection.execute(
                text(
                    """
                    INSERT INTO company (
                        company_id,
                        company_name,
                        normalized_stock_code
                    ) VALUES (
                        10,
                        'Opasnet Listed',
                        '173130'
                    )
                    """
                )
            )
            connection.execute(
                text(
                    """
                    INSERT INTO integrated_observation (
                        integrated_observation_id,
                        company_key,
                        raw_metric_name,
                        period_type,
                        fiscal_year,
                        fiscal_quarter,
                        date_raw,
                        period_label_std,
                        selected_raw_observation_id,
                        selected_source_group,
                        selected_value_text,
                        selected_value_numeric,
                        selected_is_estimate,
                        selection_reason
                    ) VALUES (
                        100,
                        'opasnet-key',
                        'Revenue',
                        'YEAR',
                        2025,
                        NULL,
                        '2025/01/01',
                        '2025',
                        1,
                        'QDATA',
                        '100',
                        100,
                        0,
                        'confirmed_qdata'
                    )
                    """
                )
            )
            connection.execute(
                text(
                    """
                    INSERT INTO integrated_observation_enriched (
                        integrated_observation_enriched_id,
                        integrated_observation_id,
                        company_key,
                        raw_metric_name,
                        normalized_metric_key,
                        standard_metric_id,
                        standard_metric_name,
                        metric_variant,
                        period_type,
                        fiscal_year,
                        fiscal_quarter,
                        date_raw,
                        selected_source_group,
                        selected_raw_observation_id,
                        selected_value_numeric,
                        selected_is_estimate
                    ) VALUES (
                        100,
                        100,
                        'opasnet-key',
                        'Revenue',
                        'revenue',
                        1,
                        'REVENUE',
                        NULL,
                        'YEAR',
                        2025,
                        NULL,
                        '2025/01/01',
                        'QDATA',
                        1,
                        100,
                        0
                    )
                    """
                )
            )

            row = connection.execute(
                text("SELECT * FROM company_metric_timeseries")
            ).mappings().one()

        self.assertEqual(row["company_id"], 10)
        self.assertEqual(row["company_name"], "Opasnet Listed")
        self.assertEqual(row["company_key"], "opasnet-key")
        self.assertEqual(row["normalized_stock_code"], "173130")
        self.assertEqual(row["standard_metric_name"], "REVENUE")
        self.assertEqual(row["value_numeric"], 100)
        self.assertEqual(row["selection_reason"], "confirmed_qdata")

    def test_company_metric_timeseries_falls_back_without_company_match(self):
        with self.engine.begin() as connection:
            connection.execute(
                text(
                    """
                    INSERT INTO raw_observation (
                        raw_observation_id,
                        source_file_id,
                        source_group,
                        raw_company_name,
                        raw_metric_name,
                        value_text,
                        value_numeric,
                        is_estimate,
                        date_raw,
                        period_type,
                        fiscal_year,
                        fiscal_quarter,
                        period_label_std
                    ) VALUES (
                        2,
                        1,
                        'KDATA1',
                        'Fallback Co',
                        'Operating Income',
                        '50',
                        50,
                        0,
                        '2025/10/01',
                        'QUARTER',
                        2025,
                        4,
                        '25.4Q'
                    )
                    """
                )
            )
            connection.execute(
                text(
                    """
                    INSERT INTO integrated_observation (
                        integrated_observation_id,
                        company_key,
                        raw_metric_name,
                        period_type,
                        fiscal_year,
                        fiscal_quarter,
                        date_raw,
                        period_label_std,
                        selected_raw_observation_id,
                        selected_source_group,
                        selected_value_text,
                        selected_value_numeric,
                        selected_is_estimate,
                        selection_reason
                    ) VALUES (
                        200,
                        'fallback-key',
                        'Operating Income',
                        'QUARTER',
                        2025,
                        4,
                        '2025/10/01',
                        '25.4Q',
                        2,
                        'KDATA1',
                        '50',
                        50,
                        0,
                        'confirmed_kdata1'
                    )
                    """
                )
            )
            connection.execute(
                text(
                    """
                    INSERT INTO integrated_observation_enriched (
                        integrated_observation_enriched_id,
                        integrated_observation_id,
                        company_key,
                        raw_metric_name,
                        normalized_metric_key,
                        standard_metric_id,
                        standard_metric_name,
                        metric_variant,
                        period_type,
                        fiscal_year,
                        fiscal_quarter,
                        date_raw,
                        selected_source_group,
                        selected_raw_observation_id,
                        selected_value_numeric,
                        selected_is_estimate
                    ) VALUES (
                        200,
                        200,
                        'fallback-key',
                        'Operating Income',
                        'operating income',
                        2,
                        'OPERATING_INCOME',
                        NULL,
                        'QUARTER',
                        2025,
                        4,
                        '2025/10/01',
                        'KDATA1',
                        2,
                        50,
                        0
                    )
                    """
                )
            )

            row = connection.execute(
                text(
                    """
                    SELECT company_id, company_name, company_key, period_type, fiscal_quarter
                    FROM company_metric_timeseries
                    WHERE integrated_observation_id = 200
                    """
                )
            ).mappings().one()

        self.assertIsNone(row["company_id"])
        self.assertEqual(row["company_name"], "Fallback Co")
        self.assertEqual(row["company_key"], "fallback-key")
        self.assertEqual(row["period_type"], "QUARTER")
        self.assertEqual(row["fiscal_quarter"], 4)


if __name__ == "__main__":
    unittest.main()
