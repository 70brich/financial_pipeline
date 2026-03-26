# FnGuide validation report

## Company
- company_name: 고려아연
- stock_code: 010130

## Source URLs
- consensus: https://comp.fnguide.com/SVO2/ASP/SVD_Consensus.asp?pGB=1&gicode=A010130&cID=&MenuYn=Y&ReportGB=&NewMenuID=108&stkGb=701
- main: https://comp.fnguide.com/SVO2/ASP/SVD_Main.asp?pGB=1&gicode=A010130&cID=&MenuYn=Y&ReportGB=&NewMenuID=101&stkGb=701

## Extracted blocks
- consensus financial long rows: 326
- consensus revision long rows: 341
- broker target rows: 6
- report summary rows: 2
- shareholder snapshot rows: 12
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
- fnguide_observation: 667
- broker_target_price: 6
- broker_report_summary: 2
- company_shareholder_snapshot: 12
- company_business_summary: 1

## 삼성전자 대표 샘플 - consensus financial
| raw_metric_name | period_label_raw | value_text | value_unit | ifrs_scope | period_scope |
| --- | --- | --- | --- | --- | --- |
| 매출액 | 2023/12 | 97,045.21 | 억원 | CONNECTED | YEAR |
| 매출액 | 2024/12 | 120,529.18 | 억원 | CONNECTED | YEAR |
| 매출액 | 2025/12 | 165,878.51 | 억원 | CONNECTED | YEAR |
| 매출액 | 2026/12(E) | 214,349 | 억원 | CONNECTED | YEAR |
| 매출액 | 2027/12(E) | 223,015 | 억원 | CONNECTED | YEAR |
| 매출액 | 2028/12(E) | 256,910 | 억원 | CONNECTED | YEAR |
| 전년동기대비 | 2023/12 | -13.50 | % | CONNECTED | YEAR |
| 전년동기대비 | 2024/12 | 24.20 | % | CONNECTED | YEAR |
| 전년동기대비 | 2025/12 | 37.63 | % | CONNECTED | YEAR |
| 전년동기대비 | 2026/12(E) | 29.22 | % | CONNECTED | YEAR |
| 전년동기대비 | 2027/12(E) | 4.04 | % | CONNECTED | YEAR |
| 전년동기대비 | 2028/12(E) | 15.20 | % | CONNECTED | YEAR |

## 삼성전자 대표 샘플 - consensus revision
| raw_metric_name | period_label_raw | value_text | consensus_year_label | ifrs_scope | period_scope |
| --- | --- | --- | --- | --- | --- |
| 매출액 | 2026/03/25 | 214,349 | FY1 | CONNECTED | YEAR |
| 매출액 | 1개월전 | 210,677 | FY1 | CONNECTED | YEAR |
| 매출액 | 3개월전 | 186,112 | FY1 | CONNECTED | YEAR |
| 매출액 | 6개월전 | 157,955 | FY1 | CONNECTED | YEAR |
| 매출액 | 1년전 | 143,350 | FY1 | CONNECTED | YEAR |
| 영업이익 | 2026/03/25 | 18,813 | FY1 | CONNECTED | YEAR |
| 영업이익 | 1개월전 | 18,909 | FY1 | CONNECTED | YEAR |
| 영업이익 | 3개월전 | 11,581 | FY1 | CONNECTED | YEAR |
| 영업이익 | 6개월전 | 10,041 | FY1 | CONNECTED | YEAR |
| 영업이익 | 1년전 | 7,864 | FY1 | CONNECTED | YEAR |
| 지배주주순이익 | 2026/03/25 | 12,984 | FY1 | CONNECTED | YEAR |
| 지배주주순이익 | 1개월전 | 12,850 | FY1 | CONNECTED | YEAR |

## 삼성전자 대표 샘플 - broker target
| broker_name | estimate_date | target_price | previous_target_price | rating | is_consensus_aggregate |
| --- | --- | --- | --- | --- | --- |
| Consensus | nan | 1905000.0 | 1700000.0 | 4.00 | 1 |
| 현대차증권 | 2026/03/13 | 2010000.0 | nan | 4.00 | 0 |
| DB증권 | 2026/03/03 | nan | nan | nan | 0 |
| iM증권 | 2026/02/11 | nan | nan | nan | 0 |
| 메리츠증권 | 2026/02/11 | nan | nan | nan | 0 |
| 신한투자증권 | 2026/02/11 | 1800000.0 | 1700000.0 | 4.00 | 0 |

## 삼성전자 대표 샘플 - report summary
| report_date | report_title | provider_name | analyst_name | rating_text |
| --- | --- | --- | --- | --- |
| 2026/03/13 | 고려아연-올해 아연 및 귀금속 가격 상승으로 실적 증가 기대 | 현대차증권 | 박현욱 | BUY |
| 2026/03/03 | 고려아연-미국 갈륨/게르마늄 확보의 대체불가 파트너 | DB증권 | 안회수 | Not Rated |

## 삼성전자 대표 샘플 - shareholder
| holder_name | holder_type | shares | ownership_pct | as_of_date |
| --- | --- | --- | --- | --- |
| 와이피씨(외 16인) | holder_detail | 8585655.0 | 41.13 | 2025/03/10 |
| 최윤범(외 52인) | holder_detail | 3696899.0 | 17.71 | 2025/07/16 |
| 크루서블제이브이유한책임회사 | holder_detail | 2209716.0 | 10.59 | 2026/01/09 |
| 한화에이치투에너지 유에스에이 코퍼레이션(외 2인) | holder_detail | 1605336.0 | 7.69 | 2022/11/24 |
| HMG Global LLC | holder_detail | 1045430.0 | 5.01 | 2023/10/06 |
| 자사주 | holder_detail | 479737.0 | 2.3 | 2025/12/26 |
| 최대주주등 (본인+특별관계자) | shareholder_group | 8585655.0 | 41.13 | 2025/03/10 |
| 10%이상주주 (본인+특별관계자) | shareholder_group | 5906615.0 | 28.3 | 2026/01/09 |

## 삼성전자 대표 샘플 - Business Summary
동사는 1974년 종합비철금속 제련회사로 설립, 1990년 기업공개를 했으며, 국내외 종속회사 83개사를 보유하고 있음. 아연, 연, 금, 은, 동 등 비철금속 제조 및 판매를 주력으로 하며, 자원순환 및 전해동박 생산업 등을 영위하고 있음. 해외에서는 신재생에너지 및 수소개발 등 신사업을 확대하며, 제련업을 기반으로 2차전지 소재 사업 등 미래 성장 동력을 강화하고 있음.
2025년 3분기 누적 전년동기 대비 연결기준 매출액은 36.8% 증가, 영업이익은 33.2% 증가, 당기순이익은 28.7% 증가. 귀금속 가격 강세로 금과 은의 매출이 증가하였으며, 지정학적 불확실성 확대에 따른 안전자산 수요 증가와 각국 중앙은행의 금 매입 증가로 귀금속 보유 매력도가 상승함. 아연은 글로벌 건설 경기 악화와 미국 관세 정책으로 수요세가 둔화되었으나, 타이트한 실물 수급으로 가격 상승세를 보이고 있음.
## 다음 작업 제안
- 다종목 확장 시 gicode 리스트 입력과 batch runner를 추가
- DART API를 다음 단계에서 연결해 FnGuide 데이터와 교차 검증
- 필요 시 차트 데이터 XML endpoint까지 확장
