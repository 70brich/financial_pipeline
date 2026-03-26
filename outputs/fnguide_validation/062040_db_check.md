# FnGuide DB check

## Row counts
| table_name | row_count |
| --- | --- |
| fnguide_observation | 671 |
| broker_target_price | 10 |
| broker_report_summary | 5 |
| company_shareholder_snapshot | 9 |
| company_business_summary | 1 |
| fnguide_fetch_log | 18 |

## fnguide_observation sample
| raw_metric_name | period_label_raw | value_text | value_numeric | block_type | ifrs_scope | period_scope |
| --- | --- | --- | --- | --- | --- | --- |
| 매출액 | 2023/12 | 2,145.38 | 2145.38 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 매출액 | 2024/12 | 3,339.97 | 3339.97 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 매출액 | 2025/12 | 5,019.46 | 5019.46 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 매출액 | 2026/12(E) | 6,607 | 6607 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 매출액 | 2027/12(E) | 8,182 | 8182 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 매출액 | 2028/12(E) | 9,080 | 9080 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2023/12 | 99.25 | 99.25 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2024/12 | 55.68 | 55.68 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2025/12 | 50.28 | 50.28 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2026/12(E) | 31.63 | 31.63 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2027/12(E) | 23.84 | 23.84 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2028/12(E) | 10.98 | 10.98 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 컨센서스대비 | 2025/12 | -1.37 | -1.37 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 영업이익 | 2023/12 | 466.05 | 466.05 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 영업이익 | 2024/12 | 1,092.32 | 1092.32 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 영업이익 | 2025/12 | 1,786.34 | 1786.34 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 영업이익 | 2026/12(E) | 2,464 | 2464 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 영업이익 | 2027/12(E) | 3,157 | 3157 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 영업이익 | 2028/12(E) | 3,407 | 3407 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2023/12 | 282.54 | 282.54 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2024/12 | 134.38 | 134.38 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2025/12 | 63.54 | 63.54 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2026/12(E) | 37.91 | 37.91 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2027/12(E) | 28.16 | 28.16 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2028/12(E) | 7.91 | 7.91 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 컨센서스대비 | 2025/12 | 0.87 | 0.87 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 당기순이익 | 2023/12 | 390.51 | 390.51 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 당기순이익 | 2024/12 | 836.76 | 836.76 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 당기순이익 | 2025/12 | 1,489.22 | 1489.22 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 당기순이익 | 2026/12(E) | 1,986 | 1986 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |

## broker_target_price sample
| broker_name | estimate_date | target_price | previous_target_price | rating |
| --- | --- | --- | --- | --- |
| Consensus | None | 200000 | 180429 | 4.00 |
| LS증권 | 2026/03/20 | 215000 | 215000 | 4.00 |
| NH투자증권 | 2026/03/20 | 220000 | 190000 | 4.00 |
| KB증권 | 2026/03/10 | None | None | None |
| 유안타증권 | 2026/03/04 | 200000 | 200000 | 4.00 |
| 유진투자증권 | 2026/03/03 | 205000 | None | 4.00 |
| 리딩투자증권 | 2026/02/23 | 200000 | 150000 | 4.00 |
| 교보증권 | 2026/02/10 | 200000 | 178000 | 4.00 |
| 신한투자증권 | 2026/02/09 | 180000 | 180000 | 4.00 |
| IBK투자증권 | 2026/01/20 | 180000 | 150000 | 4.00 |

## broker_report_summary sample
| report_date | report_title | provider_name | analyst_name | rating_text |
| --- | --- | --- | --- | --- |
| 2026/03/20 | 산일전기-국내 대형 3사를 대신할 좋은 대안 | NH투자증권 | 이민재.류승원 | BUY |
| 2026/03/10 | 산일전기-특수변압기 수요 강세 지속 | KB증권 | 김선봉.성현동 | Not Rated |
| 2026/03/04 | 산일전기-수급 해소 이후 본격 레벨업 | 유안타증권 | 손현정.김고은 | BUY |
| 2026/03/04 | SANIL ELECTRIC-Full-fledged level-up after supply overhang clears | 유안타증권 | 손현정 | BUY |
| 2026/03/03 | 산일전기-특수변압기 중심 프리미엄 지속 | 유진투자증권 | 허준서 | BUY |

## company_shareholder_snapshot sample
| holder_name | holder_type | shares | ownership_pct | as_of_date |
| --- | --- | --- | --- | --- |
| 박동석(외 2인) | holder_detail | 16851947 | 55.17 | 2024/07/29 |
| 국민연금공단 | holder_detail | 2521103 | 8.25 | 2025/07/24 |
| 자사주 | holder_detail | 60753 | 0.2 | 2024/07/29 |
| 최대주주등 (본인+특별관계자) | shareholder_group | 16851947 | 55.17 | 2024/07/29 |
| 10%이상주주 (본인+특별관계자) | shareholder_group | None | None | None |
| 5%이상주주 (본인+특별관계자) | shareholder_group | 2521103 | 8.25 | 2025/07/24 |
| 임원 (5%미만 중, 임원인자) | shareholder_group | 161646 | 0.53 | 2025/08/20 |
| 자기주식 (자사주+자사주신탁) | shareholder_group | 60753 | 0.2 | 2024/07/29 |
| 우리사주조합 | shareholder_group | 643914 | 2.11 | 2025/06/30 |
