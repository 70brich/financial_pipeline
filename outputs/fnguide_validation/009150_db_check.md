# FnGuide DB check

## Row counts
| table_name | row_count |
| --- | --- |
| fnguide_observation | 566 |
| broker_target_price | 23 |
| broker_report_summary | 17 |
| company_shareholder_snapshot | 10 |
| company_business_summary | 1 |
| fnguide_fetch_log | 18 |

## fnguide_observation sample
| raw_metric_name | period_label_raw | value_text | value_numeric | block_type | ifrs_scope | period_scope |
| --- | --- | --- | --- | --- | --- | --- |
| 매출액 | 2023/12 | 88,924.12 | 88924.12 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 매출액 | 2024/12 | 102,941.03 | 102941.03 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 매출액 | 2025/12 | 113,144.59 | 113144.59 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 매출액 | 2026/12(E) | 127,831 | 127831 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 매출액 | 2027/12(E) | 144,033 | 144033 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 매출액 | 2028/12(E) | 153,668 | 153668 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2023/12 | -5.65 | -5.65 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2024/12 | 15.76 | 15.76 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2025/12 | 9.91 | 9.91 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2026/12(E) | 12.98 | 12.98 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2027/12(E) | 12.67 | 12.67 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2028/12(E) | 6.69 | 6.69 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 컨센서스대비 | 2023/12 | 1.62 | 1.62 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 컨센서스대비 | 2024/12 | 1.24 | 1.24 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 컨센서스대비 | 2025/12 | 0.55 | 0.55 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 영업이익 | 2023/12 | 6,605.44 | 6605.44 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 영업이익 | 2024/12 | 7,350.06 | 7350.06 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 영업이익 | 2025/12 | 9,133.31 | 9133.31 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 영업이익 | 2026/12(E) | 13,601 | 13601 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 영업이익 | 2027/12(E) | 18,081 | 18081 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 영업이익 | 2028/12(E) | 22,918 | 22918 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2023/12 | -44.16 | -44.16 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2024/12 | 11.27 | 11.27 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2025/12 | 24.26 | 24.26 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2026/12(E) | 48.92 | 48.92 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2027/12(E) | 32.94 | 32.94 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2028/12(E) | 26.75 | 26.75 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 컨센서스대비 | 2023/12 | 1.62 | 1.62 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 컨센서스대비 | 2024/12 | -2.99 | -2.99 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 컨센서스대비 | 2025/12 | 1.23 | 1.23 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |

## broker_target_price sample
| broker_name | estimate_date | target_price | previous_target_price | rating |
| --- | --- | --- | --- | --- |
| Consensus | None | 470455 | 366364 | 4.00 |
| 대신증권 | 2026/03/25 | 550000 | 350000 | 4.00 |
| 하나증권 | 2026/03/25 | 550000 | 340000 | 4.00 |
| 교보증권 | 2026/03/24 | 600000 | 310000 | 4.00 |
| 메리츠증권 | 2026/03/23 | 590000 | 550000 | 4.00 |
| 다올투자증권 | 2026/03/20 | 600000 | 470000 | 4.00 |
| KB증권 | 2026/03/18 | 600000 | 460000 | 4.00 |
| 한국투자증권 | 2026/03/13 | 440000 | 440000 | 4.00 |
| 유안타증권 | 2026/03/12 | 540000 | 370000 | 4.00 |
| 신한투자증권 | 2026/03/11 | 500000 | 400000 | 4.00 |
| NH투자증권 | 2026/03/10 | 460000 | 360000 | 4.00 |
| 미래에셋증권 | 2026/03/05 | 500000 | 400000 | 4.00 |
| iM증권 | 2026/03/03 | 600000 | 350000 | 4.00 |
| DB증권 | 2026/02/27 | 570000 | 350000 | 4.00 |
| 삼성증권 | 2026/02/20 | 450000 | 350000 | 4.00 |
| BNK투자증권 | 2026/02/03 | 360000 | 340000 | 4.00 |
| 키움증권 | 2026/01/26 | 340000 | 320000 | 4.00 |
| DS투자증권 | 2026/01/26 | 350000 | 330000 | 4.00 |
| 현대차증권 | 2026/01/26 | 340000 | 340000 | 4.00 |
| SK증권 | 2026/01/26 | 410000 | 400000 | 4.00 |

## broker_report_summary sample
| report_date | report_title | provider_name | analyst_name | rating_text |
| --- | --- | --- | --- | --- |
| 2026/03/25 | 삼성전기-새로운 역사가 진행, 추가로 도약을 예상 | 대신증권 | 박강호.서지원 | BUY |
| 2026/03/25 | 삼성전기-아직 호황의 초입 | 하나증권 | 김민경 | BUY |
| 2026/03/24 | 삼성전기-1Q26 Preview: 일회성 비용 제거 시 컨센상회 | 교보증권 | 최보영 | BUY |
| 2026/03/23 | 삼성전기-북미 NV사와의 FC-BGA 연결고리, 구조적 진화 중 | 메리츠증권 | 양승수 | BUY |
| 2026/03/20 | 삼성전기-화룡점정의 시간 | 다올투자증권 | 김연미 | BUY |
| 2026/03/18 | 삼성전기-AI를 넘어, 우주로 | KB증권 | 이창민.김연수 | BUY |
| 2026/03/13 | 삼성전기-Servers shift supply/demand equation | 유안타증권 | 고선영 | None |
| 2026/03/12 | SamsungElecMech-Servers shift supply/demand equation | 유안타증권 | 고선영 | BUY |
| 2026/03/12 | 삼성전기-서버가 바꾼 수급 방정식, P의 시작과 예고된 Q | 유안타증권 | 고선영 | BUY |
| 2026/03/11 | 삼성전기-실적 추이 및 전망 | 신한투자증권 | 오강호 외4 | 매수 |
| 2026/03/10 | 삼성전기-Inflection Point | NH투자증권 | 황지현 | BUY |
| 2026/03/06 | 삼성전기-새 술은 새 부대에 | 메리츠증권 | 양승수 | BUY |
| 2026/03/05 | SamsungElecMech-Strong upside to substrates | 미래에셋증권 | 박준서 | 매수 |
| 2026/03/05 | 삼성전기-기판, 살판 났다 | 미래에셋증권 | 박준서 | 매수 |
| 2026/03/05 | 삼성전기-두려움보다는 설렘으로 | 다올투자증권 | 김연미 | BUY |
| 2026/03/03 | 삼성전기-새로운 전기를 맞이하다 | iM증권 | 고의영.박정하 | BUY |
| 2026/02/27 | 삼성전기-성장은 추세, 상승은 기세 | DB증권 | 조현지 | BUY |

## company_shareholder_snapshot sample
| holder_name | holder_type | shares | ownership_pct | as_of_date |
| --- | --- | --- | --- | --- |
| 삼성전자(외 5인) | holder_detail | 17770523 | 23.79 | 2026/02/25 |
| 국민연금공단 | holder_detail | 8213036 | 11 | 2025/12/26 |
| BlackRock Fund Advisors(외 12인) | holder_detail | 3739817 | 5.01 | 2026/02/12 |
| 자사주 | holder_detail | 2000000 | 2.68 | 2015/04/01 |
| 최대주주등 (본인+특별관계자) | shareholder_group | 17770523 | 23.79 | 2026/02/25 |
| 10%이상주주 (본인+특별관계자) | shareholder_group | 8213036 | 11 | 2025/12/26 |
| 5%이상주주 (본인+특별관계자) | shareholder_group | 3739817 | 5.01 | 2026/02/12 |
| 임원 (5%미만 중, 임원인자) | shareholder_group | 15611 | 0.02 | 2026/02/03 |
| 자기주식 (자사주+자사주신탁) | shareholder_group | 2000000 | 2.68 | 2015/04/01 |
| 우리사주조합 | shareholder_group | None | None | None |
