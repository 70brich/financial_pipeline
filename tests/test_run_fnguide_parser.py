from __future__ import annotations

import unittest

from python.etl.parse_fnguide import FnGuideCompanyContext, normalize_stock_code, validation_output_paths
from python.etl.run_fnguide_parser import _parse_company_spec


class RunFnGuideParserTest(unittest.TestCase):
    def test_parse_company_spec_supports_name_only(self) -> None:
        company_name, stock_code = _parse_company_spec("하이브")
        self.assertEqual(company_name, "하이브")
        self.assertIsNone(stock_code)

    def test_parse_company_spec_supports_name_and_stock_code(self) -> None:
        company_name, stock_code = _parse_company_spec("오파스넷:173130")
        self.assertEqual(company_name, "오파스넷")
        self.assertEqual(stock_code, "173130")

    def test_normalize_stock_code_strips_gicode_prefix(self) -> None:
        self.assertEqual(normalize_stock_code("A005930"), "005930")
        self.assertEqual(normalize_stock_code("005930"), "005930")
        self.assertEqual(normalize_stock_code(""), "")

    def test_validation_output_paths_use_stock_code_stem_for_batch(self) -> None:
        company = FnGuideCompanyContext(company_name="하이브", stock_code="352820", gicode="A352820")
        paths = validation_output_paths(company, output_stem="352820")
        self.assertTrue(str(paths["validation_report_md"]).endswith("352820_validation_report.md"))
        self.assertTrue(str(paths["layout_debug_md"]).endswith("352820_layout_debug.md"))


if __name__ == "__main__":
    unittest.main()
