# FnGuide validation report

## Company
- company_name: 삼성전기
- stock_code: 009150

## Source URLs
- consensus: https://comp.fnguide.com/SVO2/ASP/SVD_Consensus.asp?pGB=1&gicode=A009150&cID=&MenuYn=Y&ReportGB=&NewMenuID=108&stkGb=701
- main: https://comp.fnguide.com/SVO2/ASP/SVD_Main.asp?pGB=1&gicode=A009150&cID=&MenuYn=Y&ReportGB=&NewMenuID=101&stkGb=701

## Extracted blocks
- consensus financial long rows: 290
- consensus revision long rows: 276
- broker target rows: 23
- report summary rows: 17
- shareholder snapshot rows: 10
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
- fnguide_observation: 566
- broker_target_price: 23
- broker_report_summary: 17
- company_shareholder_snapshot: 10
- company_business_summary: 1

## 삼성전자 대표 샘플 - consensus financial
| raw_metric_name | period_label_raw | value_text | value_unit | ifrs_scope | period_scope |
| --- | --- | --- | --- | --- | --- |
| 매출액 | 2023/12 | 88,924.12 | 억원 | CONNECTED | YEAR |
| 매출액 | 2024/12 | 102,941.03 | 억원 | CONNECTED | YEAR |
| 매출액 | 2025/12 | 113,144.59 | 억원 | CONNECTED | YEAR |
| 매출액 | 2026/12(E) | 127,831 | 억원 | CONNECTED | YEAR |
| 매출액 | 2027/12(E) | 144,033 | 억원 | CONNECTED | YEAR |
| 매출액 | 2028/12(E) | 153,668 | 억원 | CONNECTED | YEAR |
| 전년동기대비 | 2023/12 | -5.65 | % | CONNECTED | YEAR |
| 전년동기대비 | 2024/12 | 15.76 | % | CONNECTED | YEAR |
| 전년동기대비 | 2025/12 | 9.91 | % | CONNECTED | YEAR |
| 전년동기대비 | 2026/12(E) | 12.98 | % | CONNECTED | YEAR |
| 전년동기대비 | 2027/12(E) | 12.67 | % | CONNECTED | YEAR |
| 전년동기대비 | 2028/12(E) | 6.69 | % | CONNECTED | YEAR |

## 삼성전자 대표 샘플 - consensus revision
| raw_metric_name | period_label_raw | value_text | consensus_year_label | ifrs_scope | period_scope |
| --- | --- | --- | --- | --- | --- |
| 매출액 | 2026/03/25 | 127,831 | FY1 | CONNECTED | YEAR |
| 매출액 | 1개월전 | 127,109 | FY1 | CONNECTED | YEAR |
| 매출액 | 3개월전 | 124,908 | FY1 | CONNECTED | YEAR |
| 매출액 | 6개월전 | 119,827 | FY1 | CONNECTED | YEAR |
| 매출액 | 1년전 | 118,885 | FY1 | CONNECTED | YEAR |
| 영업이익 | 2026/03/25 | 13,601 | FY1 | CONNECTED | YEAR |
| 영업이익 | 1개월전 | 13,097 | FY1 | CONNECTED | YEAR |
| 영업이익 | 3개월전 | 11,889 | FY1 | CONNECTED | YEAR |
| 영업이익 | 6개월전 | 10,268 | FY1 | CONNECTED | YEAR |
| 영업이익 | 1년전 | 10,816 | FY1 | CONNECTED | YEAR |
| 지배주주순이익 | 2026/03/25 | 10,893 | FY1 | CONNECTED | YEAR |
| 지배주주순이익 | 1개월전 | 10,376 | FY1 | CONNECTED | YEAR |

## 삼성전자 대표 샘플 - broker target
| broker_name | estimate_date | target_price | previous_target_price | rating | is_consensus_aggregate |
| --- | --- | --- | --- | --- | --- |
| Consensus | nan | 470455.0 | 366364.0 | 4.00 | 1 |
| 대신증권 | 2026/03/25 | 550000.0 | 350000.0 | 4.00 | 0 |
| 하나증권 | 2026/03/25 | 550000.0 | 340000.0 | 4.00 | 0 |
| 교보증권 | 2026/03/24 | 600000.0 | 310000.0 | 4.00 | 0 |
| 메리츠증권 | 2026/03/23 | 590000.0 | 550000.0 | 4.00 | 0 |
| 다올투자증권 | 2026/03/20 | 600000.0 | 470000.0 | 4.00 | 0 |
| KB증권 | 2026/03/18 | 600000.0 | 460000.0 | 4.00 | 0 |
| 한국투자증권 | 2026/03/13 | 440000.0 | 440000.0 | 4.00 | 0 |

## 삼성전자 대표 샘플 - report summary
| report_date | report_title | provider_name | analyst_name | rating_text |
| --- | --- | --- | --- | --- |
| 2026/03/25 | 삼성전기-새로운 역사가 진행, 추가로 도약을 예상 | 대신증권 | 박강호.서지원 | BUY |
| 2026/03/25 | 삼성전기-아직 호황의 초입 | 하나증권 | 김민경 | BUY |
| 2026/03/24 | 삼성전기-1Q26 Preview: 일회성 비용 제거 시 컨센상회 | 교보증권 | 최보영 | BUY |
| 2026/03/23 | 삼성전기-북미 NV사와의 FC-BGA 연결고리, 구조적 진화 중 | 메리츠증권 | 양승수 | BUY |
| 2026/03/20 | 삼성전기-화룡점정의 시간 | 다올투자증권 | 김연미 | BUY |
| 2026/03/18 | 삼성전기-AI를 넘어, 우주로 | KB증권 | 이창민.김연수 | BUY |

## 삼성전자 대표 샘플 - shareholder
| holder_name | holder_type | shares | ownership_pct | as_of_date |
| --- | --- | --- | --- | --- |
| 삼성전자(외 5인) | holder_detail | 17770523.0 | 23.79 | 2026/02/25 |
| 국민연금공단 | holder_detail | 8213036.0 | 11.0 | 2025/12/26 |
| BlackRock Fund Advisors(외 12인) | holder_detail | 3739817.0 | 5.01 | 2026/02/12 |
| 자사주 | holder_detail | 2000000.0 | 2.68 | 2015/04/01 |
| 최대주주등 (본인+특별관계자) | shareholder_group | 17770523.0 | 23.79 | 2026/02/25 |
| 10%이상주주 (본인+특별관계자) | shareholder_group | 8213036.0 | 11.0 | 2025/12/26 |
| 5%이상주주 (본인+특별관계자) | shareholder_group | 3739817.0 | 5.01 | 2026/02/12 |
| 임원 (5%미만 중, 임원인자) | shareholder_group | 15611.0 | 0.02 | 2026/02/03 |

## 삼성전자 대표 샘플 - Business Summary
동사는 1973년 설립, 1979년 상장한 삼성그룹 계열사로 국내외 13개 자회사와 1개 손자회사를 운영하고 있음. 수동소자, 반도체패키지기판, 카메라모듈을 각각 생산하는 3개 사업부문으로 구성되어 있으며, 6개 생산거점을 보유하고 있음. 초소형·고용량 재료기술과 핵심공정기술을 고도화해 경쟁우위 선점, IT용 최선단품 및 전장용 고온·고압·고신뢰성 제품 개발로 글로벌 시장 점유율 확대하고 있음.
2025년 3분기 누적 전년동기 대비 연결기준 매출액은 7.8% 증가, 영업이익은 8.7% 증가, 당기순이익은 2.7% 증가. 컴포넌트 사업부문은 IT 제품 고기능화와 서버 확산으로 MLCC 소요원수 확대 및 고온·고압 제품 수요 증가로 실적 개선했음. 패키지솔루션 사업부문은 반도체 고성능화로 기판 대형화 및 고밀도화로 High-End 제품 매출 증가하며, 스마트폰 카메라와 ADAS 고도화에 따른 수요 증가에 대응 중임.
## 다음 작업 제안
- 다종목 확장 시 gicode 리스트 입력과 batch runner를 추가
- DART API를 다음 단계에서 연결해 FnGuide 데이터와 교차 검증
- 필요 시 차트 데이터 XML endpoint까지 확장
