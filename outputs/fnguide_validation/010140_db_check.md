# FnGuide DB check

## Row counts
| table_name | row_count |
| --- | --- |
| fnguide_observation | 576 |
| broker_target_price | 23 |
| broker_report_summary | 1 |
| company_shareholder_snapshot | 9 |
| company_business_summary | 1 |
| fnguide_fetch_log | 18 |

## fnguide_observation sample
| raw_metric_name | period_label_raw | value_text | value_numeric | block_type | ifrs_scope | period_scope |
| --- | --- | --- | --- | --- | --- | --- |
| 매출액 | 2023/12 | 80,094.30 | 80094.3 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 매출액 | 2024/12 | 99,030.78 | 99030.78 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 매출액 | 2025/12 | 106,500.11 | 106500.11 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 매출액 | 2026/12(E) | 126,866 | 126866 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 매출액 | 2027/12(E) | 142,807 | 142807 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 매출액 | 2028/12(E) | 151,147 | 151147 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2023/12 | 34.73 | 34.73 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2024/12 | 23.64 | 23.64 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2025/12 | 7.54 | 7.54 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2026/12(E) | 19.12 | 19.12 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2027/12(E) | 12.57 | 12.57 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2028/12(E) | 5.84 | 5.84 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 컨센서스대비 | 2023/12 | 1.92 | 1.92 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 컨센서스대비 | 2024/12 | 1.61 | 1.61 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 컨센서스대비 | 2025/12 | -0.72 | -0.72 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 영업이익 | 2023/12 | 2,333.45 | 2333.45 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 영업이익 | 2024/12 | 5,026.99 | 5026.99 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 영업이익 | 2025/12 | 8,622.11 | 8622.11 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 영업이익 | 2026/12(E) | 15,691 | 15691 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 영업이익 | 2027/12(E) | 20,100 | 20100 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 영업이익 | 2028/12(E) | 23,898 | 23898 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2023/12 | 흑전 | None | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2024/12 | 115.43 | 115.43 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2025/12 | 71.52 | 71.52 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2026/12(E) | 81.99 | 81.99 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2027/12(E) | 28.10 | 28.1 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2028/12(E) | 18.89 | 18.89 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 컨센서스대비 | 2023/12 | 2.90 | 2.9 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 컨센서스대비 | 2024/12 | 5.30 | 5.3 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 컨센서스대비 | 2025/12 | -1.33 | -1.33 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |

## broker_target_price sample
| broker_name | estimate_date | target_price | previous_target_price | rating |
| --- | --- | --- | --- | --- |
| Consensus | None | 38182 | 34650 | 4.00 |
| LS증권 | 2026/03/11 | 40000 | 40000 | 4.00 |
| 한국투자증권 | 2026/03/10 | 34000 | 34000 | 4.00 |
| 유안타증권 | 2026/03/09 | 36000 | None | 4.00 |
| 다올투자증권 | 2026/03/05 | 41000 | 41000 | 4.00 |
| 신영증권 | 2026/03/03 | 43000 | 43000 | 4.00 |
| 상상인증권 | 2026/02/24 | 39000 | 39000 | 4.00 |
| 현대차증권 | 2026/02/20 | 35000 | None | 4.00 |
| 메리츠증권 | 2026/02/02 | 40000 | 39000 | 4.00 |
| NH투자증권 | 2026/02/02 | 37000 | 37000 | 4.00 |
| 하나증권 | 2026/02/02 | 36000 | 30000 | 4.00 |
| iM증권 | 2026/02/02 | 35000 | 30000 | 4.00 |
| 유진투자증권 | 2026/02/02 | 41000 | 41000 | 4.00 |
| 미래에셋증권 | 2026/02/02 | 36000 | 31000 | 4.00 |
| 키움증권 | 2026/02/02 | 39000 | 29000 | 4.00 |
| DB증권 | 2026/02/02 | 38000 | 38000 | 4.00 |
| 삼성증권 | 2026/02/02 | 43000 | 33000 | 4.00 |
| IBK투자증권 | 2026/01/27 | 36000 | 34000 | 4.00 |
| 한화투자증권 | 2026/01/21 | 40000 | 28000 | 4.00 |
| KB증권 | 2026/01/19 | 35000 | 25000 | 4.00 |

## broker_report_summary sample
| report_date | report_title | provider_name | analyst_name | rating_text |
| --- | --- | --- | --- | --- |
| 2026/03/11 | 삼성중공업-26년 수주와 실적 두 마리 토끼 | LS증권 | 이재혁 | BUY |

## company_shareholder_snapshot sample
| holder_name | holder_type | shares | ownership_pct | as_of_date |
| --- | --- | --- | --- | --- |
| 삼성전자(외 7인) | holder_detail | 183501568 | 20.85 | 2026/02/25 |
| 국민연금공단 | holder_detail | 70235377 | 7.98 | 2025/03/14 |
| 자사주 | holder_detail | 25964429 | 2.95 | 2014/11/17 |
| 최대주주등 (본인+특별관계자) | shareholder_group | 183501568 | 20.85 | 2026/02/25 |
| 10%이상주주 (본인+특별관계자) | shareholder_group | None | None | None |
| 5%이상주주 (본인+특별관계자) | shareholder_group | 70235377 | 7.98 | 2025/03/14 |
| 임원 (5%미만 중, 임원인자) | shareholder_group | 485658 | 0.06 | 2025/11/27 |
| 자기주식 (자사주+자사주신탁) | shareholder_group | 25964429 | 2.95 | 2014/11/17 |
| 우리사주조합 | shareholder_group | 2295 | 0 | 2025/06/30 |
