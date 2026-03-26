# FnGuide DB check

## Row counts
| table_name | row_count |
| --- | --- |
| fnguide_observation | 516 |
| broker_target_price | 9 |
| broker_report_summary | 3 |
| company_shareholder_snapshot | 9 |
| company_business_summary | 1 |
| fnguide_fetch_log | 18 |

## fnguide_observation sample
| raw_metric_name | period_label_raw | value_text | value_numeric | block_type | ifrs_scope | period_scope |
| --- | --- | --- | --- | --- | --- | --- |
| 매출액 | 2023/12 | 15,201.62 | 15201.62 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 매출액 | 2024/12 | 30,725.29 | 30725.29 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 매출액 | 2025/12 | 29,316.49 | 29316.49 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 매출액 | 2026/12(E) | 29,150 | 29150 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 매출액 | 2027/12(E) | 33,807 | 33807 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2023/12 | 10.57 | 10.57 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2024/12 | 102.12 | 102.12 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2025/12 | -4.59 | -4.59 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2026/12(E) | -0.57 | -0.57 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2027/12(E) | 15.98 | 15.98 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 컨센서스대비 | 2023/12 | -4.18 | -4.18 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 컨센서스대비 | 2024/12 | -2.95 | -2.95 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 컨센서스대비 | 2025/12 | -0.11 | -0.11 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 영업이익 | 2023/12 | 1,041.96 | 1041.96 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 영업이익 | 2024/12 | 2,554.82 | 2554.82 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 영업이익 | 2025/12 | 3,203.23 | 3203.23 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 영업이익 | 2026/12(E) | 3,101 | 3101 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 영업이익 | 2027/12(E) | 3,688 | 3688 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2023/12 | 147.37 | 147.37 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2024/12 | 145.19 | 145.19 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2025/12 | 25.38 | 25.38 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2026/12(E) | -3.21 | -3.21 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2027/12(E) | 18.95 | 18.95 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 컨센서스대비 | 2023/12 | -27.26 | -27.26 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 컨센서스대비 | 2024/12 | -14.64 | -14.64 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 컨센서스대비 | 2025/12 | 2.14 | 2.14 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 당기순이익 | 2023/12 | 184.42 | 184.42 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 당기순이익 | 2024/12 | 1,436.68 | 1436.68 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 당기순이익 | 2025/12 | 401.33 | 401.33 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 당기순이익 | 2026/12(E) | 1,949 | 1949 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |

## broker_target_price sample
| broker_name | estimate_date | target_price | previous_target_price | rating |
| --- | --- | --- | --- | --- |
| Consensus | None | 65875 | 66000 | 4.00 |
| 삼성증권 | 2026/03/19 | 79000 | 79000 | 4.00 |
| 교보증권 | 2026/03/17 | 67000 | None | 4.00 |
| 유진투자증권 | 2026/03/03 | 70000 | 70000 | 4.00 |
| 하나증권 | 2026/02/19 | 68000 | 68000 | 4.00 |
| 키움증권 | 2026/02/19 | 62000 | 64000 | 4.00 |
| 미래에셋증권 | 2026/02/13 | 52000 | 52000 | 4.00 |
| 메리츠증권 | 2026/02/13 | 64000 | 64000 | 4.00 |
| DS투자증권 | 2026/02/13 | 65000 | 65000 | 4.00 |

## broker_report_summary sample
| report_date | report_title | provider_name | analyst_name | rating_text |
| --- | --- | --- | --- | --- |
| 2026/03/19 | 씨에스윈드-Corporate day 후기: 성장의 토대를 마련하는 중 | 삼성증권 | 허재준 | BUY |
| 2026/03/18 | 씨에스윈드-Corporate day 후기: 성장의 토대를 마련하는 중 | 삼성증권 | 허재준 | BUY |
| 2026/03/17 | 씨에스윈드-콜로라도가 돌아간다 | 교보증권 | 조혜빈 | BUY |

## company_shareholder_snapshot sample
| holder_name | holder_type | shares | ownership_pct | as_of_date |
| --- | --- | --- | --- | --- |
| 김성권(외 14인) | holder_detail | 16774954 | 39.78 | 2025/12/30 |
| 국민연금공단 | holder_detail | 3323863 | 7.88 | 2025/10/30 |
| 자사주 | holder_detail | 732723 | 1.74 | 2024/12/30 |
| 최대주주등 (본인+특별관계자) | shareholder_group | 16774954 | 39.78 | 2025/12/30 |
| 10%이상주주 (본인+특별관계자) | shareholder_group | None | None | None |
| 5%이상주주 (본인+특별관계자) | shareholder_group | 3323863 | 7.88 | 2025/10/30 |
| 임원 (5%미만 중, 임원인자) | shareholder_group | 27912 | 0.07 | 2026/01/01 |
| 자기주식 (자사주+자사주신탁) | shareholder_group | 732723 | 1.74 | 2024/12/30 |
| 우리사주조합 | shareholder_group | 31109 | 0.07 | 2024/12/31 |
