# FnGuide validation report

## Company
- company_name: 씨에스윈드
- stock_code: 112610

## Source URLs
- consensus: https://comp.fnguide.com/SVO2/ASP/SVD_Consensus.asp?pGB=1&gicode=A112610&cID=&MenuYn=Y&ReportGB=&NewMenuID=108&stkGb=701
- main: https://comp.fnguide.com/SVO2/ASP/SVD_Main.asp?pGB=1&gicode=A112610&cID=&MenuYn=Y&ReportGB=&NewMenuID=101&stkGb=701

## Extracted blocks
- consensus financial long rows: 271
- consensus revision long rows: 245
- broker target rows: 9
- report summary rows: 3
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
- fnguide_observation: 516
- broker_target_price: 9
- broker_report_summary: 3
- company_shareholder_snapshot: 9
- company_business_summary: 1

## 삼성전자 대표 샘플 - consensus financial
| raw_metric_name | period_label_raw | value_text | value_unit | ifrs_scope | period_scope |
| --- | --- | --- | --- | --- | --- |
| 매출액 | 2023/12 | 15,201.62 | 억원 | CONNECTED | YEAR |
| 매출액 | 2024/12 | 30,725.29 | 억원 | CONNECTED | YEAR |
| 매출액 | 2025/12 | 29,316.49 | 억원 | CONNECTED | YEAR |
| 매출액 | 2026/12(E) | 29,150 | 억원 | CONNECTED | YEAR |
| 매출액 | 2027/12(E) | 33,807 | 억원 | CONNECTED | YEAR |
| 전년동기대비 | 2023/12 | 10.57 | % | CONNECTED | YEAR |
| 전년동기대비 | 2024/12 | 102.12 | % | CONNECTED | YEAR |
| 전년동기대비 | 2025/12 | -4.59 | % | CONNECTED | YEAR |
| 전년동기대비 | 2026/12(E) | -0.57 | % | CONNECTED | YEAR |
| 전년동기대비 | 2027/12(E) | 15.98 | % | CONNECTED | YEAR |
| 컨센서스대비 | 2023/12 | -4.18 | % | CONNECTED | YEAR |
| 컨센서스대비 | 2024/12 | -2.95 | % | CONNECTED | YEAR |

## 삼성전자 대표 샘플 - consensus revision
| raw_metric_name | period_label_raw | value_text | consensus_year_label | ifrs_scope | period_scope |
| --- | --- | --- | --- | --- | --- |
| 매출액 | 2026/03/25 | 29,150 | FY1 | CONNECTED | YEAR |
| 매출액 | 1개월전 | 29,040 | FY1 | CONNECTED | YEAR |
| 매출액 | 3개월전 | 30,064 | FY1 | CONNECTED | YEAR |
| 매출액 | 6개월전 | 34,081 | FY1 | CONNECTED | YEAR |
| 매출액 | 1년전 | 37,800 | FY1 | CONNECTED | YEAR |
| 영업이익 | 2026/03/25 | 3,101 | FY1 | CONNECTED | YEAR |
| 영업이익 | 1개월전 | 3,067 | FY1 | CONNECTED | YEAR |
| 영업이익 | 3개월전 | 2,955 | FY1 | CONNECTED | YEAR |
| 영업이익 | 6개월전 | 3,377 | FY1 | CONNECTED | YEAR |
| 영업이익 | 1년전 | 3,596 | FY1 | CONNECTED | YEAR |
| 지배주주순이익 | 2026/03/25 | 1,913 | FY1 | CONNECTED | YEAR |
| 지배주주순이익 | 1개월전 | 1,887 | FY1 | CONNECTED | YEAR |

## 삼성전자 대표 샘플 - broker target
| broker_name | estimate_date | target_price | previous_target_price | rating | is_consensus_aggregate |
| --- | --- | --- | --- | --- | --- |
| Consensus | nan | 65875.0 | 66000.0 | 4.00 | 1 |
| 삼성증권 | 2026/03/19 | 79000.0 | 79000.0 | 4.00 | 0 |
| 교보증권 | 2026/03/17 | 67000.0 | nan | 4.00 | 0 |
| 유진투자증권 | 2026/03/03 | 70000.0 | 70000.0 | 4.00 | 0 |
| 하나증권 | 2026/02/19 | 68000.0 | 68000.0 | 4.00 | 0 |
| 키움증권 | 2026/02/19 | 62000.0 | 64000.0 | 4.00 | 0 |
| 미래에셋증권 | 2026/02/13 | 52000.0 | 52000.0 | 4.00 | 0 |
| 메리츠증권 | 2026/02/13 | 64000.0 | 64000.0 | 4.00 | 0 |

## 삼성전자 대표 샘플 - report summary
| report_date | report_title | provider_name | analyst_name | rating_text |
| --- | --- | --- | --- | --- |
| 2026/03/19 | 씨에스윈드-Corporate day 후기: 성장의 토대를 마련하는 중 | 삼성증권 | 허재준 | BUY |
| 2026/03/18 | 씨에스윈드-Corporate day 후기: 성장의 토대를 마련하는 중 | 삼성증권 | 허재준 | BUY |
| 2026/03/17 | 씨에스윈드-콜로라도가 돌아간다 | 교보증권 | 조혜빈 | BUY |

## 삼성전자 대표 샘플 - shareholder
| holder_name | holder_type | shares | ownership_pct | as_of_date |
| --- | --- | --- | --- | --- |
| 김성권(외 14인) | holder_detail | 16774954.0 | 39.78 | 2025/12/30 |
| 국민연금공단 | holder_detail | 3323863.0 | 7.88 | 2025/10/30 |
| 자사주 | holder_detail | 732723.0 | 1.74 | 2024/12/30 |
| 최대주주등 (본인+특별관계자) | shareholder_group | 16774954.0 | 39.78 | 2025/12/30 |
| 10%이상주주 (본인+특별관계자) | shareholder_group | nan | nan | nan |
| 5%이상주주 (본인+특별관계자) | shareholder_group | 3323863.0 | 7.88 | 2025/10/30 |
| 임원 (5%미만 중, 임원인자) | shareholder_group | 27912.0 | 0.07 | 2026/01/01 |
| 자기주식 (자사주+자사주신탁) | shareholder_group | 732723.0 | 1.74 | 2024/12/30 |

## 삼성전자 대표 샘플 - Business Summary
동사는 2006년 중산풍력으로 설립되어 2007년 씨에스윈드로 사명 변경 후 2014년 유가증권시장에 상장됨. 2023년 유럽 해상풍력 하부구조물 생산기업 Bladt Industries 인수로 해상풍력 하부구조물 사업에 진출함. 한국 본사를 기반으로 베트남, 미국, 포르투갈, 중국, 터키, 대만에서 풍력타워 생산법인을 운영하며 전세계 시장에 육상·해상 풍력타워와 하부구조물을 공급하고 있음.
2025년 3분기 누적 전년동기 대비 연결기준 매출액은 10.5% 감소, 영업이익은 13.5% 증가, 당기순이익은 42.8% 증가. 미국 청정에너지 세제 변경에도 재무부의 세액 공제 규정 확정으로 단기 불확실성이 완화되었음. AI 데이터센터 구축과 전력 인프라 확충, 유럽·미국의 해상풍력단지 설치 가속화로 대구경 하부구조물 수요가 급증할 전망이며, Bladt Industries 인수로 글로벌 경쟁력을 강화하고 있음.
## 다음 작업 제안
- 다종목 확장 시 gicode 리스트 입력과 batch runner를 추가
- DART API를 다음 단계에서 연결해 FnGuide 데이터와 교차 검증
- 필요 시 차트 데이터 XML endpoint까지 확장
