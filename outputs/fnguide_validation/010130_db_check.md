# FnGuide DB check

## Row counts
| table_name | row_count |
| --- | --- |
| fnguide_observation | 667 |
| broker_target_price | 6 |
| broker_report_summary | 2 |
| company_shareholder_snapshot | 12 |
| company_business_summary | 1 |
| fnguide_fetch_log | 18 |

## fnguide_observation sample
| raw_metric_name | period_label_raw | value_text | value_numeric | block_type | ifrs_scope | period_scope |
| --- | --- | --- | --- | --- | --- | --- |
| 매출액 | 2023/12 | 97,045.21 | 97045.21 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 매출액 | 2024/12 | 120,529.18 | 120529.18 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 매출액 | 2025/12 | 165,878.51 | 165878.51 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 매출액 | 2026/12(E) | 214,349 | 214349 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 매출액 | 2027/12(E) | 223,015 | 223015 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 매출액 | 2028/12(E) | 256,910 | 256910 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2023/12 | -13.50 | -13.5 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2024/12 | 24.20 | 24.2 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2025/12 | 37.63 | 37.63 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2026/12(E) | 29.22 | 29.22 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2027/12(E) | 4.04 | 4.04 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2028/12(E) | 15.20 | 15.2 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 컨센서스대비 | 2023/12 | -1.17 | -1.17 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 컨센서스대비 | 2025/12 | 0.61 | 0.61 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 영업이익 | 2023/12 | 6,599.35 | 6599.35 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 영업이익 | 2024/12 | 7,234.72 | 7234.72 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 영업이익 | 2025/12 | 12,319.27 | 12319.27 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 영업이익 | 2026/12(E) | 18,813 | 18813 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 영업이익 | 2027/12(E) | 19,760 | 19760 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2023/12 | -28.20 | -28.2 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2024/12 | 9.63 | 9.63 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2025/12 | 70.28 | 70.28 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2026/12(E) | 52.72 | 52.72 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2027/12(E) | 5.03 | 5.03 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 컨센서스대비 | 2023/12 | 0.17 | 0.17 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 컨센서스대비 | 2025/12 | 4.52 | 4.52 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 당기순이익 | 2023/12 | 5,333.79 | 5333.79 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 당기순이익 | 2024/12 | 1,947.82 | 1947.82 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 당기순이익 | 2025/12 | 7,702.49 | 7702.49 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 당기순이익 | 2026/12(E) | 12,933 | 12933 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |

## broker_target_price sample
| broker_name | estimate_date | target_price | previous_target_price | rating |
| --- | --- | --- | --- | --- |
| Consensus | None | 1905000 | 1700000 | 4.00 |
| 현대차증권 | 2026/03/13 | 2010000 | None | 4.00 |
| DB증권 | 2026/03/03 | None | None | None |
| iM증권 | 2026/02/11 | None | None | None |
| 메리츠증권 | 2026/02/11 | None | None | None |
| 신한투자증권 | 2026/02/11 | 1800000 | 1700000 | 4.00 |

## broker_report_summary sample
| report_date | report_title | provider_name | analyst_name | rating_text |
| --- | --- | --- | --- | --- |
| 2026/03/13 | 고려아연-올해 아연 및 귀금속 가격 상승으로 실적 증가 기대 | 현대차증권 | 박현욱 | BUY |
| 2026/03/03 | 고려아연-미국 갈륨/게르마늄 확보의 대체불가 파트너 | DB증권 | 안회수 | Not Rated |

## company_shareholder_snapshot sample
| holder_name | holder_type | shares | ownership_pct | as_of_date |
| --- | --- | --- | --- | --- |
| 와이피씨(외 16인) | holder_detail | 8585655 | 41.13 | 2025/03/10 |
| 최윤범(외 52인) | holder_detail | 3696899 | 17.71 | 2025/07/16 |
| 크루서블제이브이유한책임회사 | holder_detail | 2209716 | 10.59 | 2026/01/09 |
| 한화에이치투에너지 유에스에이 코퍼레이션(외 2인) | holder_detail | 1605336 | 7.69 | 2022/11/24 |
| HMG Global LLC | holder_detail | 1045430 | 5.01 | 2023/10/06 |
| 자사주 | holder_detail | 479737 | 2.3 | 2025/12/26 |
| 최대주주등 (본인+특별관계자) | shareholder_group | 8585655 | 41.13 | 2025/03/10 |
| 10%이상주주 (본인+특별관계자) | shareholder_group | 5906615 | 28.3 | 2026/01/09 |
| 5%이상주주 (본인+특별관계자) | shareholder_group | 2650766 | 12.7 | 2023/10/06 |
| 임원 (5%미만 중, 임원인자) | shareholder_group | 2763 | 0.01 | 2026/01/12 |
| 자기주식 (자사주+자사주신탁) | shareholder_group | 479737 | 2.3 | 2025/12/26 |
| 우리사주조합 | shareholder_group | None | None | None |
