# FnGuide validation report

## Company
- company_name: 삼성중공업
- stock_code: 010140

## Source URLs
- consensus: https://comp.fnguide.com/SVO2/ASP/SVD_Consensus.asp?pGB=1&gicode=A010140&cID=&MenuYn=Y&ReportGB=&NewMenuID=108&stkGb=701
- main: https://comp.fnguide.com/SVO2/ASP/SVD_Main.asp?pGB=1&gicode=A010140&cID=&MenuYn=Y&ReportGB=&NewMenuID=101&stkGb=701

## Extracted blocks
- consensus financial long rows: 281
- consensus revision long rows: 295
- broker target rows: 23
- report summary rows: 1
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
- fnguide_observation: 576
- broker_target_price: 23
- broker_report_summary: 1
- company_shareholder_snapshot: 9
- company_business_summary: 1

## 삼성전자 대표 샘플 - consensus financial
| raw_metric_name | period_label_raw | value_text | value_unit | ifrs_scope | period_scope |
| --- | --- | --- | --- | --- | --- |
| 매출액 | 2023/12 | 80,094.30 | 억원 | CONNECTED | YEAR |
| 매출액 | 2024/12 | 99,030.78 | 억원 | CONNECTED | YEAR |
| 매출액 | 2025/12 | 106,500.11 | 억원 | CONNECTED | YEAR |
| 매출액 | 2026/12(E) | 126,866 | 억원 | CONNECTED | YEAR |
| 매출액 | 2027/12(E) | 142,807 | 억원 | CONNECTED | YEAR |
| 매출액 | 2028/12(E) | 151,147 | 억원 | CONNECTED | YEAR |
| 전년동기대비 | 2023/12 | 34.73 | % | CONNECTED | YEAR |
| 전년동기대비 | 2024/12 | 23.64 | % | CONNECTED | YEAR |
| 전년동기대비 | 2025/12 | 7.54 | % | CONNECTED | YEAR |
| 전년동기대비 | 2026/12(E) | 19.12 | % | CONNECTED | YEAR |
| 전년동기대비 | 2027/12(E) | 12.57 | % | CONNECTED | YEAR |
| 전년동기대비 | 2028/12(E) | 5.84 | % | CONNECTED | YEAR |

## 삼성전자 대표 샘플 - consensus revision
| raw_metric_name | period_label_raw | value_text | consensus_year_label | ifrs_scope | period_scope |
| --- | --- | --- | --- | --- | --- |
| 매출액 | 2026/03/25 | 126,866 | FY1 | CONNECTED | YEAR |
| 매출액 | 1개월전 | 126,866 | FY1 | CONNECTED | YEAR |
| 매출액 | 3개월전 | 125,122 | FY1 | CONNECTED | YEAR |
| 매출액 | 6개월전 | 126,555 | FY1 | CONNECTED | YEAR |
| 매출액 | 1년전 | 123,299 | FY1 | CONNECTED | YEAR |
| 영업이익 | 2026/03/25 | 15,691 | FY1 | CONNECTED | YEAR |
| 영업이익 | 1개월전 | 15,691 | FY1 | CONNECTED | YEAR |
| 영업이익 | 3개월전 | 14,503 | FY1 | CONNECTED | YEAR |
| 영업이익 | 6개월전 | 12,796 | FY1 | CONNECTED | YEAR |
| 영업이익 | 1년전 | 10,852 | FY1 | CONNECTED | YEAR |
| 지배주주순이익 | 2026/03/25 | 12,401 | FY1 | CONNECTED | YEAR |
| 지배주주순이익 | 1개월전 | 12,401 | FY1 | CONNECTED | YEAR |

## 삼성전자 대표 샘플 - broker target
| broker_name | estimate_date | target_price | previous_target_price | rating | is_consensus_aggregate |
| --- | --- | --- | --- | --- | --- |
| Consensus | nan | 38182.0 | 34650.0 | 4.00 | 1 |
| LS증권 | 2026/03/11 | 40000.0 | 40000.0 | 4.00 | 0 |
| 한국투자증권 | 2026/03/10 | 34000.0 | 34000.0 | 4.00 | 0 |
| 유안타증권 | 2026/03/09 | 36000.0 | nan | 4.00 | 0 |
| 다올투자증권 | 2026/03/05 | 41000.0 | 41000.0 | 4.00 | 0 |
| 신영증권 | 2026/03/03 | 43000.0 | 43000.0 | 4.00 | 0 |
| 상상인증권 | 2026/02/24 | 39000.0 | 39000.0 | 4.00 | 0 |
| 현대차증권 | 2026/02/20 | 35000.0 | nan | 4.00 | 0 |

## 삼성전자 대표 샘플 - report summary
| report_date | report_title | provider_name | analyst_name | rating_text |
| --- | --- | --- | --- | --- |
| 2026/03/11 | 삼성중공업-26년 수주와 실적 두 마리 토끼 | LS증권 | 이재혁 | BUY |

## 삼성전자 대표 샘플 - shareholder
| holder_name | holder_type | shares | ownership_pct | as_of_date |
| --- | --- | --- | --- | --- |
| 삼성전자(외 7인) | holder_detail | 183501568.0 | 20.85 | 2026/02/25 |
| 국민연금공단 | holder_detail | 70235377.0 | 7.98 | 2025/03/14 |
| 자사주 | holder_detail | 25964429.0 | 2.95 | 2014/11/17 |
| 최대주주등 (본인+특별관계자) | shareholder_group | 183501568.0 | 20.85 | 2026/02/25 |
| 10%이상주주 (본인+특별관계자) | shareholder_group | nan | nan | nan |
| 5%이상주주 (본인+특별관계자) | shareholder_group | 70235377.0 | 7.98 | 2025/03/14 |
| 임원 (5%미만 중, 임원인자) | shareholder_group | 485658.0 | 0.06 | 2025/11/27 |
| 자기주식 (자사주+자사주신탁) | shareholder_group | 25964429.0 | 2.95 | 2014/11/17 |

## 삼성전자 대표 샘플 - Business Summary
동사는 1974년 설립되어 1994년 상장, 성남시 분당구에 본사를 두고 거제조선소와 R&D센터를 운영하고 있음. 선박 및 해양플랫폼을 건조·판매하는 조선해양부문과 건축·토목공사를 수행하는 토건부문을 영위하고 있으며, 8개 해외 종속회사가 선박블록 제작 및 해양설비 설계를 담당하고 있음. 조선해양부문에서 신제품 개발 및 성능·품질 차별화 연구개발을 집중하며, 해외사와의 네트워크 강화를 위해 5개 해외사무소를 운영하고 있음.
2025년 3분기 누적 전년동기 대비 연결기준 매출액은 8.5% 증가, 영업이익은 72.3% 증가, 당기순이익은 179.3% 증가. 조선해양부문은 무역분쟁으로 가스선과 대형 탱커 발주가 감소했으나 3분기 후반부터 회복되고 있음. 미국 트럼프 취임에 따른 Non-FTA 국가 수출 승인 재개로 4분기 LNG선 발주가 회복 예상되며, OPEC+ 감산 완화로 원유 수출 증가와 함께 탱커 수요 증가 기대됨.
## 다음 작업 제안
- 다종목 확장 시 gicode 리스트 입력과 batch runner를 추가
- DART API를 다음 단계에서 연결해 FnGuide 데이터와 교차 검증
- 필요 시 차트 데이터 XML endpoint까지 확장
