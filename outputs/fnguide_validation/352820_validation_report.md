# FnGuide validation report

## Company
- company_name: 하이브
- stock_code: 352820

## Source URLs
- consensus: https://comp.fnguide.com/SVO2/ASP/SVD_Consensus.asp?pGB=1&gicode=A352820&cID=&MenuYn=Y&ReportGB=&NewMenuID=108&stkGb=701
- main: https://comp.fnguide.com/SVO2/ASP/SVD_Main.asp?pGB=1&gicode=A352820&cID=&MenuYn=Y&ReportGB=&NewMenuID=101&stkGb=701

## Extracted blocks
- consensus financial long rows: 290
- consensus revision long rows: 260
- broker target rows: 23
- report summary rows: 16
- shareholder snapshot rows: 9
- business summary present: yes

## 확보 범위
- consensus modes: {'financial_ifrs_modes': [{'value': 'D', 'label': 'CONNECTED'}, {'value': 'B', 'label': 'SEPARATE'}], 'financial_period_modes': [{'value': 'A', 'label': 'YEAR'}, {'value': 'Q', 'label': 'QUARTER'}], 'revision_period_options': {'YEAR': [{'value': 'FY1', 'label': '202612'}, {'value': 'FY2', 'label': '202712'}, {'value': 'FY3', 'label': '202812'}], 'QUARTER': [{'value': 'FQ1', 'label': '202603'}, {'value': 'FQ2', 'label': '202606'}, {'value': 'FQ3', 'label': '202609'}]}, 'detected_select_ids': ['selAccount1', 'selGsym']}
- 확보됨: 연결/별도, 연간/분기, 증권사별 적정주가, 리포트 요약, 주주현황, Business Summary
- 보류: 차트 이미지 자체 저장, Selenium 전용 렌더링 영역

## Requests-only viability
- consensus and broker/report blocks are available through requests-accessible JSON endpoints
- shareholder and Business Summary are available through requests-accessible HTML
- Selenium fallback is not required for the current company implementation

## DB row counts
- fetch_logs: 18
- fnguide_observation: 550
- broker_target_price: 23
- broker_report_summary: 16
- company_shareholder_snapshot: 9
- company_business_summary: 1

## 삼성전자 대표 샘플 - consensus financial
| raw_metric_name | period_label_raw | value_text | value_unit | ifrs_scope | period_scope |
| --- | --- | --- | --- | --- | --- |
| 매출액 | 2023/12 | 21,780.88 | 억원 | CONNECTED | YEAR |
| 매출액 | 2024/12 | 22,556.49 | 억원 | CONNECTED | YEAR |
| 매출액 | 2025/12 | 26,498.70 | 억원 | CONNECTED | YEAR |
| 매출액 | 2026/12(E) | 42,922 | 억원 | CONNECTED | YEAR |
| 매출액 | 2027/12(E) | 42,659 | 억원 | CONNECTED | YEAR |
| 매출액 | 2028/12(E) | 27,796 | 억원 | CONNECTED | YEAR |
| 전년동기대비 | 2023/12 | 22.63 | % | CONNECTED | YEAR |
| 전년동기대비 | 2024/12 | 3.56 | % | CONNECTED | YEAR |
| 전년동기대비 | 2025/12 | 17.48 | % | CONNECTED | YEAR |
| 전년동기대비 | 2026/12(E) | 61.98 | % | CONNECTED | YEAR |
| 전년동기대비 | 2027/12(E) | -0.61 | % | CONNECTED | YEAR |
| 전년동기대비 | 2028/12(E) | -34.84 | % | CONNECTED | YEAR |

## 삼성전자 대표 샘플 - consensus revision
| raw_metric_name | period_label_raw | value_text | consensus_year_label | ifrs_scope | period_scope |
| --- | --- | --- | --- | --- | --- |
| 매출액 | 2026/03/25 | 42,922 | FY1 | CONNECTED | YEAR |
| 매출액 | 1개월전 | 42,321 | FY1 | CONNECTED | YEAR |
| 매출액 | 3개월전 | 38,590 | FY1 | CONNECTED | YEAR |
| 매출액 | 6개월전 | 37,496 | FY1 | CONNECTED | YEAR |
| 매출액 | 1년전 | 34,848 | FY1 | CONNECTED | YEAR |
| 영업이익 | 2026/03/25 | 5,405 | FY1 | CONNECTED | YEAR |
| 영업이익 | 1개월전 | 5,329 | FY1 | CONNECTED | YEAR |
| 영업이익 | 3개월전 | 4,785 | FY1 | CONNECTED | YEAR |
| 영업이익 | 6개월전 | 4,766 | FY1 | CONNECTED | YEAR |
| 영업이익 | 1년전 | 4,745 | FY1 | CONNECTED | YEAR |
| 지배주주순이익 | 2026/03/25 | 4,239 | FY1 | CONNECTED | YEAR |
| 지배주주순이익 | 1개월전 | 4,171 | FY1 | CONNECTED | YEAR |

## 삼성전자 대표 샘플 - broker target
| broker_name | estimate_date | target_price | previous_target_price | rating | is_consensus_aggregate |
| --- | --- | --- | --- | --- | --- |
| Consensus | nan | 464318.0 | 431316.0 | 4.00 | 1 |
| 신영증권 | 2026/03/25 | 450000.0 | 450000.0 | 4.00 | 0 |
| LS증권 | 2026/03/25 | 480000.0 | 460000.0 | 4.00 | 0 |
| 하나증권 | 2026/03/24 | 440000.0 | 440000.0 | 4.00 | 0 |
| 한국투자증권 | 2026/03/24 | 450000.0 | 310000.0 | 4.00 | 0 |
| 교보증권 | 2026/03/23 | 455000.0 | 455000.0 | 4.00 | 0 |
| 유안타증권 | 2026/03/19 | 450000.0 | 450000.0 | 4.00 | 0 |
| SK증권 | 2026/03/18 | 480000.0 | nan | 4.00 | 0 |

## 삼성전자 대표 샘플 - report summary
| report_date | report_title | provider_name | analyst_name | rating_text |
| --- | --- | --- | --- | --- |
| 2026/03/25 | 하이브-모멘텀 선두주자 | LS증권 | 박성호 | BUY |
| 2026/03/25 | 하이브-좋아하는 데 이유 없다 | 신영증권 | 김지현 | 매수 |
| 2026/03/24 | 하이브-방탄소년단 활동 초기 구간, 주가 조정은 매수 기회 | SK증권 | 박준형 | nan |
| 2026/03/24 | 하이브-BTS 컴백에 대한 신한생각 | 신한투자증권 | 지인해 | nan |
| 2026/03/24 | 하이브-이렇게까지 빠질 일인가? | 하나증권 | 이기훈 | BUY |
| 2026/03/24 | 하이브-올해의 하이브는 역대급 | 한국투자증권 | 정호윤.황인준 | 매수 |

## 삼성전자 대표 샘플 - shareholder
| holder_name | holder_type | shares | ownership_pct | as_of_date |
| --- | --- | --- | --- | --- |
| 방시혁(외 12인) | holder_detail | 19764296.0 | 45.89 | 2026/03/03 |
| 국민연금공단 | holder_detail | 3247384.0 | 7.54 | 2025/03/21 |
| 자사주 | holder_detail | 106337.0 | 0.25 | 2026/03/03 |
| 최대주주등 (본인+특별관계자) | shareholder_group | 19764296.0 | 45.89 | 2026/03/03 |
| 10%이상주주 (본인+특별관계자) | shareholder_group | nan | nan | nan |
| 5%이상주주 (본인+특별관계자) | shareholder_group | 3247384.0 | 7.54 | 2025/03/21 |
| 임원 (5%미만 중, 임원인자) | shareholder_group | 61746.0 | 0.14 | 2026/01/20 |
| 자기주식 (자사주+자사주신탁) | shareholder_group | 106337.0 | 0.25 | 2026/03/03 |

## 삼성전자 대표 샘플 - Business Summary
동사는 2005년 설립되어 2020년 상장, 2021년 하이브로 변경함. 음악, 플랫폼, 테크기반으로 사업 운영하며, 14개 독립 레이블을 통해 방탄소년단, 세븐틴 등 글로벌 아티스트 육성하고 위버스 기반 팬 커뮤니티 플랫폼과 AI 솔루션 개발함. 멀티 레이블 전략으로 창작자에 최적 환경과 독립성 보장하며 한국, 일본, 미국 등 글로벌 시장으로 K-POP 프로덕션 확장하고, 음악과 기술 접목으로 팬 경험 확대하고 있음.
2025년 3분기 누적 전년동기 대비 연결기준 매출액은 26.4% 증가, 영업이익은 62.0% 감소, 당기순이익은 26.8% 감소. 공연과 음반/음원 부문 매출 증가로 총 매출은 증가했으나, 일회성 비용과 원가 부담으로 영업이익은 감소했음. 일본과 미국에서 K-POP을 선보이며 다양한 플랫폼과 기술 융합을 추진하고, 멀티 레이블 전략으로 업계 혁신을 주도하고 있음.
## 다음 작업 제안
- 다종목 확장 시 gicode 리스트 입력과 batch runner를 추가
- DART API를 다음 단계에서 연결해 FnGuide 데이터와 교차 검증
- 필요 시 차트 데이터 XML endpoint까지 확장
