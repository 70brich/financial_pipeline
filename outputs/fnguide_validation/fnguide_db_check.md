# FnGuide DB check

## Row counts
| table_name | row_count |
| --- | --- |
| fnguide_observation | 566 |
| broker_target_price | 26 |
| broker_report_summary | 23 |
| company_shareholder_snapshot | 10 |
| company_business_summary | 1 |
| fnguide_fetch_log | 18 |

## fnguide_observation sample
| raw_metric_name | period_label_raw | value_text | value_numeric | block_type | ifrs_scope | period_scope |
| --- | --- | --- | --- | --- | --- | --- |
| 매출액 | 2023/12 | 2,589,354.94 | 2589354.94 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 매출액 | 2024/12 | 3,008,709.03 | 3008709.03 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 매출액 | 2025/12 | 3,336,059.38 | 3336059.38 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 매출액 | 2026/12(E) | 5,231,547 | 5231547 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 매출액 | 2027/12(E) | 5,758,509 | 5758509 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 매출액 | 2028/12(E) | 6,676,497 | 6676497 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2023/12 | -14.33 | -14.33 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2024/12 | 16.20 | 16.2 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2025/12 | 10.88 | 10.88 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2026/12(E) | 56.82 | 56.82 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2027/12(E) | 10.07 | 10.07 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2028/12(E) | 15.94 | 15.94 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 컨센서스대비 | 2023/12 | -1.00 | -1 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 컨센서스대비 | 2024/12 | -0.56 | -0.56 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 컨센서스대비 | 2025/12 | 0.74 | 0.74 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 영업이익 | 2023/12 | 65,669.76 | 65669.76 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 영업이익 | 2024/12 | 327,259.61 | 327259.61 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 영업이익 | 2025/12 | 436,010.51 | 436010.51 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 영업이익 | 2026/12(E) | 1,979,997 | 1979997 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 영업이익 | 2027/12(E) | 2,258,088 | 2258088 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 영업이익 | 2028/12(E) | 2,470,953 | 2470953 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2023/12 | -84.86 | -84.86 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2024/12 | 398.34 | 398.34 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2025/12 | 33.23 | 33.23 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2026/12(E) | 354.12 | 354.12 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2027/12(E) | 14.05 | 14.05 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2028/12(E) | 9.43 | 9.43 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 컨센서스대비 | 2023/12 | -11.95 | -11.95 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 컨센서스대비 | 2024/12 | -4.48 | -4.48 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 컨센서스대비 | 2025/12 | 3.72 | 3.72 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |

## broker_target_price sample
| broker_name | estimate_date | target_price | previous_target_price | rating |
| --- | --- | --- | --- | --- |
| Consensus | None | 252720 | 224543 | 4.00 |
| KB증권 | 2026/03/25 | 320000 | 320000 | 4.00 |
| 한국투자증권 | 2026/03/23 | 270000 | 270000 | 4.00 |
| 미래에셋증권 | 2026/03/23 | 300000 | 300000 | 4.00 |
| 대신증권 | 2026/03/19 | 270000 | 270000 | 4.00 |
| 유안타증권 | 2026/03/19 | 270000 | 270000 | 4.00 |
| DS투자증권 | 2026/03/16 | 270000 | 183000 | 4.00 |
| 하나증권 | 2026/03/13 | 300000 | 250000 | 4.00 |
| IBK투자증권 | 2026/03/11 | 240000 | 240000 | 4.00 |
| 현대차증권 | 2026/03/11 | 258000 | 258500 | 4.00 |
| 다올투자증권 | 2026/03/11 | 290000 | 270000 | 4.00 |
| BNK투자증권 | 2026/03/10 | 250000 | 200000 | 4.00 |
| DB증권 | 2026/03/10 | 230000 | 190000 | 4.00 |
| 키움증권 | 2026/03/03 | 260000 | 210000 | 4.00 |
| 한화투자증권 | 2026/02/24 | 260000 | None | 4.00 |
| LS증권 | 2026/02/24 | 260000 | None | 4.00 |
| SK증권 | 2026/02/24 | 300000 | 260000 | 4.00 |
| NH투자증권 | 2026/02/23 | 250000 | 205000 | 4.00 |
| 교보증권 | 2026/02/11 | 220000 | 220000 | 4.00 |
| 삼성증권 | 2026/02/04 | 230000 | 230000 | 4.00 |

## broker_report_summary sample
| report_date | report_title | provider_name | analyst_name | rating_text |
| --- | --- | --- | --- | --- |
| 2026/03/25 | 삼성전자-피지컬 AI 시장 진입 가시화 | KB증권 | 김동원 | BUY |
| 2026/03/23 | 삼성전자-긍정적 흐름의 연속 | 미래에셋증권 | 김영건 | 매수 |
| 2026/03/23 | SamsungElec-Positive momentum continues | 미래에셋증권 | 김영건 | 매수 |
| 2026/03/20 | 삼성전자-재고는 바닥, 주문은 최대 | KB증권 | 김동원 | BUY |
| 2026/03/19 | 삼성전자-추가 상승 여력 충분 | KB증권 | 김동원 | BUY |
| 2026/03/18 | 삼성전자-진정한 풀스택 | 미래에셋증권 | 김영건 | 매수 |
| 2026/03/18 | SamsungElec-A true full-stack player | 미래에셋증권 | 김영건 | 매수 |
| 2026/03/16 | 삼성전자-파운드리도 봐야 할 때 | DS투자증권 | 이수림 | BUY |
| 2026/03/16 | 삼성전자-지금이라도 사야 하는 이유 | 대신증권 | 류형근.서지원 | BUY |
| 2026/03/13 | 삼성전자-실적 상향과 밸류업 기대감 | 하나증권 | 김록호.김영규 | BUY |
| 2026/03/12 | 삼성전자-내년까지 완판, 실적 성장 본격화 | KB증권 | 김동원 | BUY |
| 2026/03/11 | 삼성전자-6G와 Optical I/O 수요가 메모리에 긍정적인 이유 주목 | 현대차증권 | 노근창 | BUY |
| 2026/03/11 | 삼성전자-모든 모멘텀 재료가 조화로운 구간 | 다올투자증권 | 고영민.김연미 | BUY |
| 2026/03/11 | 삼성전자-자사주 취득, 처분, 소각 계획 공시 | IBK투자증권 | 김운호 | 매수 |
| 2026/03/10 | 삼성전자-HBM4 시장 내 입지 확대 | DB증권 | 서승연 | BUY |
| 2026/03/10 | 삼성전자-반도체 업황 호전과 사업 경쟁력 제고 동시에 진행 | BNK투자증권 | 이민희 | 매수 |
| 2026/03/09 | 삼성전자-주가 매력도가 더 높아졌다 | 미래에셋증권 | 김영건 | 매수 |
| 2026/03/09 | SamsungElec-Valuation appeal has increased | 미래에셋증권 | 김영건 | 매수 |
| 2026/03/04 | 삼성전자-후퇴가 아닌 진격을 할 때 | 미래에셋증권 | 김영건 | 매수 |
| 2026/03/04 | SamsungElec-Sharp pullback presents an opportunity | 미래에셋증권 | 김영건 | 매수 |

## company_shareholder_snapshot sample
| holder_name | holder_type | shares | ownership_pct | as_of_date |
| --- | --- | --- | --- | --- |
| 삼성생명보험(외 15인) | holder_detail | 1162793388 | 19.64 | 2026/03/20 |
| 국민연금공단 | holder_detail | 458637667 | 7.75 | 2022/08/16 |
| BlackRock Fund Advisors(외 15인) | holder_detail | 300391061 | 5.07 | 2019/01/28 |
| 자사주 | holder_detail | 124013769 | 2.09 | 2026/03/24 |
| 최대주주등 (본인+특별관계자) | shareholder_group | 1162793388 | 19.64 | 2026/03/20 |
| 10%이상주주 (본인+특별관계자) | shareholder_group | None | None | None |
| 5%이상주주 (본인+특별관계자) | shareholder_group | 759028728 | 12.82 | 2022/08/16 |
| 임원 (5%미만 중, 임원인자) | shareholder_group | 4780149 | 0.08 | 2026/03/09 |
| 자기주식 (자사주+자사주신탁) | shareholder_group | 124013769 | 2.09 | 2026/03/24 |
| 우리사주조합 | shareholder_group | None | None | None |
