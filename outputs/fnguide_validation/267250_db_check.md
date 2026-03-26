# FnGuide DB check

## Row counts
| table_name | row_count |
| --- | --- |
| fnguide_observation | 611 |
| broker_target_price | 5 |
| broker_report_summary | 3 |
| company_shareholder_snapshot | 9 |
| company_business_summary | 1 |
| fnguide_fetch_log | 18 |

## fnguide_observation sample
| raw_metric_name | period_label_raw | value_text | value_numeric | block_type | ifrs_scope | period_scope |
| --- | --- | --- | --- | --- | --- | --- |
| 매출액 | 2023/12 | 613,313.03 | 613313.03 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 매출액 | 2024/12 | 677,656.26 | 677656.26 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 매출액 | 2025/12 | 712,594.38 | 712594.38 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 매출액 | 2026/12(E) | 803,454 | 803454 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 매출액 | 2027/12(E) | 838,603 | 838603 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2023/12 | 0.79 | 0.79 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2024/12 | 10.49 | 10.49 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2025/12 | 5.16 | 5.16 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2026/12(E) | 12.75 | 12.75 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2027/12(E) | 4.37 | 4.37 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 컨센서스대비 | 2023/12 | -0.93 | -0.93 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 컨센서스대비 | 2024/12 | 0.07 | 0.07 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 컨센서스대비 | 2025/12 | 0.65 | 0.65 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 영업이익 | 2023/12 | 20,315.64 | 20315.64 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 영업이익 | 2024/12 | 29,831.63 | 29831.63 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 영업이익 | 2025/12 | 60,996.36 | 60996.36 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 영업이익 | 2026/12(E) | 79,774 | 79774 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 영업이익 | 2027/12(E) | 99,083 | 99083 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2023/12 | -40.02 | -40.02 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2024/12 | 46.84 | 46.84 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2025/12 | 104.47 | 104.47 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2026/12(E) | 30.78 | 30.78 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2027/12(E) | 24.21 | 24.21 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 컨센서스대비 | 2023/12 | -9.04 | -9.04 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 컨센서스대비 | 2024/12 | 4.68 | 4.68 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 컨센서스대비 | 2025/12 | 8.40 | 8.4 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 당기순이익 | 2023/12 | 7,858.32 | 7858.32 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 당기순이익 | 2024/12 | 19,301.79 | 19301.79 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 당기순이익 | 2025/12 | 36,754.83 | 36754.83 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 당기순이익 | 2026/12(E) | 57,504 | 57504 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |

## broker_target_price sample
| broker_name | estimate_date | target_price | previous_target_price | rating |
| --- | --- | --- | --- | --- |
| Consensus | None | 345500 | 337333 | 4.00 |
| LS증권 | 2026/03/20 | 415000 | 440000 | 4.00 |
| 흥국증권 | 2026/03/16 | 370000 | 330000 | 4.00 |
| 삼성증권 | 2026/02/13 | 300000 | 242000 | 4.00 |
| 키움증권 | 2026/01/27 | 297000 | None | 4.00 |

## broker_report_summary sample
| report_date | report_title | provider_name | analyst_name | rating_text |
| --- | --- | --- | --- | --- |
| 2026/03/20 | HD현대-HD현대오일뱅크와 로봇 | LS증권 | 정경희 | BUY |
| 2026/03/16 | HD현대-자회사의 고성장과 낙수효과의 본격화 | 흥국증권 | 박종렬.김지은 | BUY |
| 2026/03/03 | HD현대-정유와 로봇은요? | LS증권 | 정경희 | BUY |

## company_shareholder_snapshot sample
| holder_name | holder_type | shares | ownership_pct | as_of_date |
| --- | --- | --- | --- | --- |
| 정몽준(외 8인) | holder_detail | 29374587 | 37.19 | 2024/07/15 |
| 자사주 | holder_detail | 8324655 | 10.54 | 2021/04/13 |
| 국민연금공단 | holder_detail | 5902972 | 7.47 | 2025/08/21 |
| 최대주주등 (본인+특별관계자) | shareholder_group | 29374587 | 37.19 | 2024/07/15 |
| 10%이상주주 (본인+특별관계자) | shareholder_group | None | None | None |
| 5%이상주주 (본인+특별관계자) | shareholder_group | 5902972 | 7.47 | 2025/08/21 |
| 임원 (5%미만 중, 임원인자) | shareholder_group | 3381 | 0 | 2022/01/21 |
| 자기주식 (자사주+자사주신탁) | shareholder_group | 8324655 | 10.54 | 2021/04/13 |
| 우리사주조합 | shareholder_group | None | None | None |
