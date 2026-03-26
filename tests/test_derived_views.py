from __future__ import annotations

import unittest

from sqlalchemy import create_engine, text

from python.etl.analysis_views import execute_analysis_views
from python.etl.build_integrated_observation import execute_integrated_schema
from python.etl.build_integrated_observation_enriched import execute_metric_mapping_schema
from python.etl.db_runtime import ensure_runtime_schema
from python.etl.derived_views import execute_derived_views


class DerivedViewTest(unittest.TestCase):
    def setUp(self) -> None:
        self.engine = create_engine("sqlite:///:memory:", future=True)
        ensure_runtime_schema(self.engine)
        execute_integrated_schema(self.engine)
        execute_metric_mapping_schema(self.engine)
        execute_analysis_views(self.engine)
        execute_derived_views(self.engine)

    def _insert_company(self, connection) -> None:
        connection.execute(
            text(
                """
                INSERT INTO company (company_id, company_name, normalized_stock_code)
                VALUES (10, 'Opasnet Listed', '173130')
                """
            )
        )

    def _insert_metric_row(
        self,
        connection,
        *,
        raw_id: int,
        integrated_id: int,
        metric_name: str,
        normalized_key: str,
        standard_metric_id: int,
        standard_metric_name: str,
        period_type: str,
        fiscal_year: int,
        fiscal_quarter: int | None,
        date_raw: str,
        value_numeric: float,
    ) -> None:
        period_label_std = (
            f"{str(fiscal_year)[-2:]}.{fiscal_quarter}Q"
            if period_type == "QUARTER"
            else str(fiscal_year)
        )
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
                    :raw_observation_id,
                    1,
                    'QDATA',
                    'Opasnet Raw',
                    '173130',
                    '173130',
                    NULL,
                    :raw_metric_name,
                    :value_text,
                    :value_numeric,
                    0,
                    :date_raw,
                    :period_type,
                    :fiscal_year,
                    :fiscal_quarter,
                    :period_label_std
                )
                """
            ),
            {
                "raw_observation_id": raw_id,
                "raw_metric_name": metric_name,
                "value_text": str(value_numeric),
                "value_numeric": value_numeric,
                "date_raw": date_raw,
                "period_type": period_type,
                "fiscal_year": fiscal_year,
                "fiscal_quarter": fiscal_quarter,
                "period_label_std": period_label_std,
            },
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
                    :integrated_observation_id,
                    'opasnet-key',
                    :raw_metric_name,
                    :period_type,
                    :fiscal_year,
                    :fiscal_quarter,
                    :date_raw,
                    :period_label_std,
                    :raw_observation_id,
                    'QDATA',
                    :value_text,
                    :value_numeric,
                    0,
                    'confirmed_qdata'
                )
                """
            ),
            {
                "integrated_observation_id": integrated_id,
                "raw_metric_name": metric_name,
                "period_type": period_type,
                "fiscal_year": fiscal_year,
                "fiscal_quarter": fiscal_quarter,
                "date_raw": date_raw,
                "period_label_std": period_label_std,
                "raw_observation_id": raw_id,
                "value_text": str(value_numeric),
                "value_numeric": value_numeric,
            },
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
                    :integrated_observation_id,
                    :integrated_observation_id,
                    'opasnet-key',
                    :raw_metric_name,
                    :normalized_metric_key,
                    :standard_metric_id,
                    :standard_metric_name,
                    NULL,
                    :period_type,
                    :fiscal_year,
                    :fiscal_quarter,
                    :date_raw,
                    'QDATA',
                    :raw_observation_id,
                    :value_numeric,
                    0
                )
                """
            ),
            {
                "integrated_observation_id": integrated_id,
                "raw_metric_name": metric_name,
                "normalized_metric_key": normalized_key,
                "standard_metric_id": standard_metric_id,
                "standard_metric_name": standard_metric_name,
                "period_type": period_type,
                "fiscal_year": fiscal_year,
                "fiscal_quarter": fiscal_quarter,
                "date_raw": date_raw,
                "raw_observation_id": raw_id,
                "value_numeric": value_numeric,
            },
        )

    def test_derived_view_calculates_yoy_qoq_and_margin(self):
        with self.engine.begin() as connection:
            self._insert_company(connection)
            rows = [
                (1, 101, "Revenue", "revenue", 1, "REVENUE", "QUARTER", 2024, 4, "2024/10/01", 100.0),
                (2, 102, "Revenue", "revenue", 1, "REVENUE", "QUARTER", 2025, 3, "2025/07/01", 150.0),
                (3, 103, "Revenue", "revenue", 1, "REVENUE", "QUARTER", 2025, 4, "2025/10/01", 200.0),
                (4, 104, "Operating Income", "operating income", 2, "OPERATING_INCOME", "QUARTER", 2024, 4, "2024/10/01", 10.0),
                (5, 105, "Operating Income", "operating income", 2, "OPERATING_INCOME", "QUARTER", 2025, 4, "2025/10/01", 20.0),
                (6, 106, "Net Income", "net income", 3, "NET_INCOME", "QUARTER", 2024, 4, "2024/10/01", 8.0),
                (7, 107, "Net Income", "net income", 3, "NET_INCOME", "QUARTER", 2025, 4, "2025/10/01", 15.0),
                (8, 108, "EPS", "eps", 4, "EPS", "QUARTER", 2024, 4, "2024/10/01", 1.0),
                (9, 109, "EPS", "eps", 4, "EPS", "QUARTER", 2025, 4, "2025/10/01", 2.0),
                (10, 110, "Revenue", "revenue", 1, "REVENUE", "YEAR", 2024, None, "2024/01/01", 1000.0),
                (11, 111, "Revenue", "revenue", 1, "REVENUE", "YEAR", 2025, None, "2025/01/01", 1200.0),
            ]
            for row in rows:
                self._insert_metric_row(
                    connection,
                    raw_id=row[0],
                    integrated_id=row[1],
                    metric_name=row[2],
                    normalized_key=row[3],
                    standard_metric_id=row[4],
                    standard_metric_name=row[5],
                    period_type=row[6],
                    fiscal_year=row[7],
                    fiscal_quarter=row[8],
                    date_raw=row[9],
                    value_numeric=row[10],
                )

            execute_analysis_views(self.engine)
            execute_derived_views(self.engine)

            revenue_yoy = connection.execute(
                text(
                    """
                    SELECT value_numeric
                    FROM company_metric_derived_v1
                    WHERE standard_metric_name = 'REVENUE_YOY'
                      AND period_type = 'QUARTER'
                      AND fiscal_year = 2025
                      AND fiscal_quarter = 4
                    """
                )
            ).scalar_one()
            revenue_qoq = connection.execute(
                text(
                    """
                    SELECT value_numeric
                    FROM company_metric_derived_v1
                    WHERE standard_metric_name = 'REVENUE_QOQ'
                      AND fiscal_year = 2025
                      AND fiscal_quarter = 4
                    """
                )
            ).scalar_one()
            operating_margin = connection.execute(
                text(
                    """
                    SELECT value_numeric
                    FROM company_metric_derived_v1
                    WHERE standard_metric_name = 'OPERATING_MARGIN'
                      AND fiscal_year = 2025
                      AND fiscal_quarter = 4
                    """
                )
            ).scalar_one()
            eps_yoy = connection.execute(
                text(
                    """
                    SELECT value_numeric
                    FROM company_metric_derived_v1
                    WHERE standard_metric_name = 'EPS_YOY'
                      AND fiscal_year = 2025
                      AND fiscal_quarter = 4
                    """
                )
            ).scalar_one()
            year_revenue_yoy = connection.execute(
                text(
                    """
                    SELECT value_numeric
                    FROM company_metric_derived_v1
                    WHERE standard_metric_name = 'REVENUE_YOY'
                      AND period_type = 'YEAR'
                      AND fiscal_year = 2025
                    """
                )
            ).scalar_one()

        self.assertAlmostEqual(revenue_yoy, 1.0)
        self.assertAlmostEqual(revenue_qoq, (200.0 - 150.0) / 150.0)
        self.assertAlmostEqual(operating_margin, 20.0 / 200.0)
        self.assertAlmostEqual(eps_yoy, 1.0)
        self.assertAlmostEqual(year_revenue_yoy, 0.2)

    def test_derived_view_keeps_null_when_prior_or_denominator_missing(self):
        with self.engine.begin() as connection:
            self._insert_company(connection)
            rows = [
                (21, 201, "Revenue", "revenue", 1, "REVENUE", "QUARTER", 2025, 1, "2025/01/01", 0.0),
                (22, 202, "Operating Income", "operating income", 2, "OPERATING_INCOME", "QUARTER", 2025, 1, "2025/01/01", 5.0),
                (23, 203, "EPS", "eps", 4, "EPS", "QUARTER", 2025, 1, "2025/01/01", 3.0),
            ]
            for row in rows:
                self._insert_metric_row(
                    connection,
                    raw_id=row[0],
                    integrated_id=row[1],
                    metric_name=row[2],
                    normalized_key=row[3],
                    standard_metric_id=row[4],
                    standard_metric_name=row[5],
                    period_type=row[6],
                    fiscal_year=row[7],
                    fiscal_quarter=row[8],
                    date_raw=row[9],
                    value_numeric=row[10],
                )

            execute_analysis_views(self.engine)
            execute_derived_views(self.engine)

            operating_margin = connection.execute(
                text(
                    """
                    SELECT value_numeric, current_value_numeric, compare_value_numeric
                    FROM company_metric_derived_v1
                    WHERE standard_metric_name = 'OPERATING_MARGIN'
                      AND fiscal_year = 2025
                      AND fiscal_quarter = 1
                    """
                )
            ).mappings().one()
            eps_qoq = connection.execute(
                text(
                    """
                    SELECT value_numeric
                    FROM company_metric_derived_v1
                    WHERE standard_metric_name = 'EPS_QOQ'
                      AND fiscal_year = 2025
                      AND fiscal_quarter = 1
                    """
                )
            ).scalar_one()

        self.assertIsNone(operating_margin["value_numeric"])
        self.assertEqual(operating_margin["current_value_numeric"], 5.0)
        self.assertEqual(operating_margin["compare_value_numeric"], 0.0)
        self.assertIsNone(eps_qoq)


if __name__ == "__main__":
    unittest.main()
