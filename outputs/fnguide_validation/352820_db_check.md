# FnGuide DB check

## Row counts
| table_name | row_count |
| --- | --- |
| fnguide_observation | 550 |
| broker_target_price | 23 |
| broker_report_summary | 16 |
| company_shareholder_snapshot | 9 |
| company_business_summary | 1 |
| fnguide_fetch_log | 18 |

## fnguide_observation sample
| raw_metric_name | period_label_raw | value_text | value_numeric | block_type | ifrs_scope | period_scope |
| --- | --- | --- | --- | --- | --- | --- |
| 매출액 | 2023/12 | 21,780.88 | 21780.88 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 매출액 | 2024/12 | 22,556.49 | 22556.49 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 매출액 | 2025/12 | 26,498.70 | 26498.7 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 매출액 | 2026/12(E) | 42,922 | 42922 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 매출액 | 2027/12(E) | 42,659 | 42659 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 매출액 | 2028/12(E) | 27,796 | 27796 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2023/12 | 22.63 | 22.63 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2024/12 | 3.56 | 3.56 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2025/12 | 17.48 | 17.48 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2026/12(E) | 61.98 | 61.98 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2027/12(E) | -0.61 | -0.61 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2028/12(E) | -34.84 | -34.84 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 컨센서스대비 | 2023/12 | -2.66 | -2.66 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 컨센서스대비 | 2024/12 | 2.73 | 2.73 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 컨센서스대비 | 2025/12 | 0.30 | 0.3 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 영업이익 | 2023/12 | 2,956.43 | 2956.43 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 영업이익 | 2024/12 | 1,840.45 | 1840.45 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 영업이익 | 2025/12 | 493.18 | 493.18 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 영업이익 | 2026/12(E) | 5,405 | 5405 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 영업이익 | 2027/12(E) | 5,597 | 5597 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 영업이익 | 2028/12(E) | 4,217 | 4217 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2023/12 | 24.79 | 24.79 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2024/12 | -37.75 | -37.75 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2025/12 | -73.20 | -73.2 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2026/12(E) | 995.99 | 995.99 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2027/12(E) | 3.55 | 3.55 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2028/12(E) | -24.67 | -24.67 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 컨센서스대비 | 2023/12 | -2.77 | -2.77 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 컨센서스대비 | 2024/12 | -9.14 | -9.14 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 컨센서스대비 | 2025/12 | -12.02 | -12.02 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |

## broker_target_price sample
| broker_name | estimate_date | target_price | previous_target_price | rating |
| --- | --- | --- | --- | --- |
| Consensus | None | 464318 | 431316 | 4.00 |
| 신영증권 | 2026/03/25 | 450000 | 450000 | 4.00 |
| LS증권 | 2026/03/25 | 480000 | 460000 | 4.00 |
| 하나증권 | 2026/03/24 | 440000 | 440000 | 4.00 |
| 한국투자증권 | 2026/03/24 | 450000 | 310000 | 4.00 |
| 교보증권 | 2026/03/23 | 455000 | 455000 | 4.00 |
| 유안타증권 | 2026/03/19 | 450000 | 450000 | 4.00 |
| SK증권 | 2026/03/18 | 480000 | None | 4.00 |
| IBK투자증권 | 2026/03/17 | 480000 | 480000 | 4.00 |
| KB증권 | 2026/03/12 | 500000 | None | 4.00 |
| 신한투자증권 | 2026/03/12 | 450000 | 450000 | 4.00 |
| 유진투자증권 | 2026/03/09 | 450000 | 450000 | 4.00 |
| 리딩투자증권 | 2026/03/03 | 550000 | 450000 | 4.00 |
| 삼성증권 | 2026/02/13 | 470000 | 410000 | 4.00 |
| 키움증권 | 2026/02/13 | 450000 | 450000 | 4.00 |
| 메리츠증권 | 2026/02/13 | 450000 | 430000 | 4.00 |
| 흥국증권 | 2026/02/13 | 450000 | 430000 | 4.00 |
| 다올투자증권 | 2026/02/13 | 460000 | 430000 | 4.00 |
| iM증권 | 2026/02/13 | 450000 | 420000 | 4.00 |
| 한화투자증권 | 2026/02/13 | 440000 | 410000 | 4.00 |

## broker_report_summary sample
| report_date | report_title | provider_name | analyst_name | rating_text |
| --- | --- | --- | --- | --- |
| 2026/03/25 | 하이브-모멘텀 선두주자 | LS증권 | 박성호 | BUY |
| 2026/03/25 | 하이브-좋아하는 데 이유 없다 | 신영증권 | 김지현 | 매수 |
| 2026/03/24 | 하이브-방탄소년단 활동 초기 구간, 주가 조정은 매수 기회 | SK증권 | 박준형 | None |
| 2026/03/24 | 하이브-BTS 컴백에 대한 신한생각 | 신한투자증권 | 지인해 | None |
| 2026/03/24 | 하이브-이렇게까지 빠질 일인가? | 하나증권 | 이기훈 | BUY |
| 2026/03/24 | 하이브-올해의 하이브는 역대급 | 한국투자증권 | 정호윤.황인준 | 매수 |
| 2026/03/23 | 하이브-성장의 물결 위로, SWIM | 교보증권 | 장민지 | BUY |
| 2026/03/19 | 하이브-확신의 실적 모멘텀이 시작된다 | 유안타증권 | 이환욱 | BUY |
| 2026/03/19 | 하이브-Start of clear earnings inflection point | 유안타증권 | 이환욱 | None |
| 2026/03/19 | HYBE-Start of clear earnings inflection point | 유안타증권 | 이환욱 | BUY |
| 2026/03/18 | 하이브-‘BTS 완전체’가 불러올 역대급 호황과 국위선양의 정점 | 스터닝밸류리서치 | 오준호 | None |
| 2026/03/18 | 하이브-돌아온 BTS, 완전체 HYBE | SK증권 | 박준형 | 매수 |
| 2026/03/17 | 하이브-BTSnomics 2.0 | IBK투자증권 | 김유혁 | 매수 |
| 2026/03/12 | 하이브-내재화 전략이 옳았다는 걸 증명할 것 | KB증권 | 최용현.이종건 | BUY |
| 2026/03/09 | 하이브-실적추이 및 전망 | 유진투자증권 | 이현지.고수영 | BUY |
| 2026/03/03 | 하이브-BTS 컴백과 본격적인 성장국면 진입 | 리딩투자증권 | 유성만 | BUY |

## company_shareholder_snapshot sample
| holder_name | holder_type | shares | ownership_pct | as_of_date |
| --- | --- | --- | --- | --- |
| 방시혁(외 12인) | holder_detail | 19764296 | 45.89 | 2026/03/03 |
| 국민연금공단 | holder_detail | 3247384 | 7.54 | 2025/03/21 |
| 자사주 | holder_detail | 106337 | 0.25 | 2026/03/03 |
| 최대주주등 (본인+특별관계자) | shareholder_group | 19764296 | 45.89 | 2026/03/03 |
| 10%이상주주 (본인+특별관계자) | shareholder_group | None | None | None |
| 5%이상주주 (본인+특별관계자) | shareholder_group | 3247384 | 7.54 | 2025/03/21 |
| 임원 (5%미만 중, 임원인자) | shareholder_group | 61746 | 0.14 | 2026/01/20 |
| 자기주식 (자사주+자사주신탁) | shareholder_group | 106337 | 0.25 | 2026/03/03 |
| 우리사주조합 | shareholder_group | 18609 | 0.04 | 2025/06/30 |
