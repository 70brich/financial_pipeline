# FnGuide DB check

## Row counts
| table_name | row_count |
| --- | --- |
| fnguide_observation | 527 |
| broker_target_price | 17 |
| broker_report_summary | 4 |
| company_shareholder_snapshot | 9 |
| company_business_summary | 1 |
| fnguide_fetch_log | 18 |

## fnguide_observation sample
| raw_metric_name | period_label_raw | value_text | value_numeric | block_type | ifrs_scope | period_scope |
| --- | --- | --- | --- | --- | --- | --- |
| 매출액 | 2023/12 | 199,463.97 | 199463.97 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 매출액 | 2024/12 | 198,948.10 | 198948.1 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 매출액 | 2025/12 | 184,830.05 | 184830.05 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 매출액 | 2026/12(E) | 201,659 | 201659 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 매출액 | 2027/12(E) | 205,995 | 205995 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 매출액 | 2028/12(E) | 203,000 | 203000 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2023/12 | -10.46 | -10.46 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2024/12 | -0.26 | -0.26 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2025/12 | -7.10 | -7.1 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2026/12(E) | 9.11 | 9.11 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2027/12(E) | 2.15 | 2.15 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2028/12(E) | -1.45 | -1.45 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 컨센서스대비 | 2023/12 | 1.26 | 1.26 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 컨센서스대비 | 2024/12 | -4.14 | -4.14 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 컨센서스대비 | 2025/12 | -1.80 | -1.8 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 영업이익 | 2023/12 | -3,477.02 | -3477.02 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 영업이익 | 2024/12 | -9,145.35 | -9145.35 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 영업이익 | 2025/12 | -9,431.16 | -9431.16 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 영업이익 | 2026/12(E) | -3,663 | -3663 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 영업이익 | 2027/12(E) | 1,959 | 1959 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 영업이익 | 2028/12(E) | 9,290 | 9290 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2023/12 | 적지 | None | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2024/12 | 적지 | None | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2025/12 | 적지 | None | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2026/12(E) | 적지 | None | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2027/12(E) | 흑전 | None | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2028/12(E) | 374.27 | 374.27 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 컨센서스대비 | 2023/12 | 적지 | None | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 컨센서스대비 | 2024/12 | 적지 | None | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 컨센서스대비 | 2025/12 | 적지 | None | CONSENSUS_FINANCIAL | CONNECTED | YEAR |

## broker_target_price sample
| broker_name | estimate_date | target_price | previous_target_price | rating |
| --- | --- | --- | --- | --- |
| Consensus | None | 102938 | 102500 | 3.69 |
| KB증권 | 2026/03/17 | 90000 | 80000 | 4.00 |
| 현대차증권 | 2026/03/06 | 74000 | 77000 | 3.00 |
| 유안타증권 | 2026/03/04 | 165000 | 165000 | 4.00 |
| 삼성증권 | 2026/03/03 | 92000 | 92000 | 3.00 |
| 한국투자증권 | 2026/02/27 | 110000 | 110000 | 4.00 |
| 신한투자증권 | 2026/02/05 | 120000 | 120000 | 4.00 |
| 한화투자증권 | 2026/02/05 | 100000 | 100000 | 4.00 |
| NH투자증권 | 2026/02/05 | 80000 | 80000 | 3.00 |
| 신영증권 | 2026/02/05 | 120000 | 120000 | 4.00 |
| 하나증권 | 2026/02/05 | 100000 | 100000 | 4.00 |
| iM증권 | 2026/02/05 | 110000 | 110000 | 4.00 |
| 유진투자증권 | 2026/02/05 | 115000 | 115000 | 4.00 |
| 미래에셋증권 | 2026/02/04 | 89000 | 89000 | 3.00 |
| IBK투자증권 | 2026/01/15 | 107000 | 107000 | 4.00 |
| 상상인증권 | 2026/01/09 | 115000 | 115000 | 4.00 |
| BNK투자증권 | 2026/01/08 | 60000 | 60000 | 3.00 |

## broker_report_summary sample
| report_date | report_title | provider_name | analyst_name | rating_text |
| --- | --- | --- | --- | --- |
| 2026/03/17 | 롯데케미칼-가동률 조정: 우리보다 급한 건 고객사 | KB증권 | 전우제.송윤주 | BUY |
| 2026/03/06 | 롯데케미칼-대산공장 구조조정 긍정적. 다만, 지금은 중동 불확실성 해소가 중요 | 현대차증권 | 강동진 | MARKETPERFORM |
| 2026/03/04 | 롯데케미칼-대산공장 구조조정으로, 2,000억원 절감 기대! | 유안타증권 | 황규원.서석준 | BUY |
| 2026/02/26 | 롯데케미칼-대산 구조조정, 단기 영업손익 수치 개선될 듯 | LS증권 | 정경희 | Not Rated |

## company_shareholder_snapshot sample
| holder_name | holder_type | shares | ownership_pct | as_of_date |
| --- | --- | --- | --- | --- |
| 롯데지주(외 41인) | holder_detail | 23347791 | 54.58 | 2025/12/30 |
| 국민연금공단 | holder_detail | 3162691 | 7.39 | 2025/03/12 |
| 자사주 | holder_detail | 608272 | 1.42 | 2024/05/10 |
| 최대주주등 (본인+특별관계자) | shareholder_group | 23347791 | 54.58 | 2025/12/30 |
| 10%이상주주 (본인+특별관계자) | shareholder_group | None | None | None |
| 5%이상주주 (본인+특별관계자) | shareholder_group | 3162691 | 7.39 | 2025/03/12 |
| 임원 (5%미만 중, 임원인자) | shareholder_group | 33480 | 0.08 | 2025/12/01 |
| 자기주식 (자사주+자사주신탁) | shareholder_group | 608272 | 1.42 | 2024/05/10 |
| 우리사주조합 | shareholder_group | None | None | None |
