# FnGuide DB check

## Row counts
| table_name | row_count |
| --- | --- |
| fnguide_observation | 561 |
| broker_target_price | 8 |
| broker_report_summary | 2 |
| company_shareholder_snapshot | 8 |
| company_business_summary | 1 |
| fnguide_fetch_log | 18 |

## fnguide_observation sample
| raw_metric_name | period_label_raw | value_text | value_numeric | block_type | ifrs_scope | period_scope |
| --- | --- | --- | --- | --- | --- | --- |
| 매출액 | 2022/12 | 11.53 | 11.53 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 매출액 | 2023/12 | 18.85 | 18.85 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 매출액 | 2024/12 | 81.00 | 81 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 매출액 | 2025/12(P) | 482 | 482 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 매출액 | 2026/12(E) | 1,114 | 1114 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 매출액 | 2027/12(E) | 1,535 | 1535 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2022/12 | -16.81 | -16.81 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2023/12 | 63.49 | 63.49 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2024/12 | 329.71 | 329.71 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2025/12(P) | 494.70 | 494.7 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2026/12(E) | 131.21 | 131.21 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2027/12(E) | 37.78 | 37.78 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 컨센서스대비 | 2025/12(P) | 1.73 | 1.73 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 영업이익 | 2022/12 | -79.90 | -79.9 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 영업이익 | 2023/12 | -98.03 | -98.03 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 영업이익 | 2024/12 | -86.82 | -86.82 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 영업이익 | 2025/12(P) | 163 | 163 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 영업이익 | 2026/12(E) | 494 | 494 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 영업이익 | 2027/12(E) | 721 | 721 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2022/12 | 적지 | None | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2023/12 | 적지 | None | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2024/12 | 적지 | None | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2025/12(P) | 흑전 | None | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2026/12(E) | 202.72 | 202.72 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2027/12(E) | 45.78 | 45.78 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 컨센서스대비 | 2025/12(P) | 2.04 | 2.04 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 당기순이익 | 2022/12 | -79.88 | -79.88 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 당기순이익 | 2023/12 | -99.17 | -99.17 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 당기순이익 | 2024/12 | -88.71 | -88.71 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 당기순이익 | 2025/12(P) | 162 | 162 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |

## broker_target_price sample
| broker_name | estimate_date | target_price | previous_target_price | rating |
| --- | --- | --- | --- | --- |
| Consensus | None | 240000 | 165000 | 4.00 |
| 상상인증권 | 2026/03/16 | 260000 | 190000 | 4.00 |
| 신한투자증권 | 2026/02/09 | None | None | None |
| 유진투자증권 | 2026/02/09 | 250000 | 180000 | 4.00 |
| 신영증권 | 2026/02/05 | 250000 | 140000 | 4.00 |
| 다올투자증권 | 2026/02/05 | None | None | None |
| DB증권 | 2026/02/05 | 200000 | 150000 | 4.00 |
| 미래에셋증권 | 2026/02/04 | None | None | None |

## broker_report_summary sample
| report_date | report_title | provider_name | analyst_name | rating_text |
| --- | --- | --- | --- | --- |
| 2026/03/16 | 씨어스테크놀로지-씽크 잠재력 좀 더 공격적으로 보자 | 상상인증권 | 하태기 | BUY |
| 2026/03/11 | 씨어스테크놀로지-회사소개 및 주요 사업현황 | 해당기업 | None | None |

## company_shareholder_snapshot sample
| holder_name | holder_type | shares | ownership_pct | as_of_date |
| --- | --- | --- | --- | --- |
| 이영신(외 4인) | holder_detail | 10752840 | 28.25 | 2026/03/24 |
| 변동준 | holder_detail | 2133960 | 5.61 | 2026/03/24 |
| 최대주주등 (본인+특별관계자) | shareholder_group | 10752840 | 28.25 | 2026/03/24 |
| 10%이상주주 (본인+특별관계자) | shareholder_group | None | None | None |
| 5%이상주주 (본인+특별관계자) | shareholder_group | 2133960 | 5.61 | 2026/03/24 |
| 임원 (5%미만 중, 임원인자) | shareholder_group | 4500 | 0.01 | 2026/03/24 |
| 자기주식 (자사주+자사주신탁) | shareholder_group | None | None | None |
| 우리사주조합 | shareholder_group | None | None | None |
