# FnGuide validation report

## Company
- company_name: 롯데케미칼
- stock_code: 011170

## Source URLs
- consensus: https://comp.fnguide.com/SVO2/ASP/SVD_Consensus.asp?pGB=1&gicode=A011170&cID=&MenuYn=Y&ReportGB=&NewMenuID=108&stkGb=701
- main: https://comp.fnguide.com/SVO2/ASP/SVD_Main.asp?pGB=1&gicode=A011170&cID=&MenuYn=Y&ReportGB=&NewMenuID=101&stkGb=701

## Extracted blocks
- consensus financial long rows: 292
- consensus revision long rows: 235
- broker target rows: 17
- report summary rows: 4
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
- fnguide_observation: 527
- broker_target_price: 17
- broker_report_summary: 4
- company_shareholder_snapshot: 9
- company_business_summary: 1

## 삼성전자 대표 샘플 - consensus financial
| raw_metric_name | period_label_raw | value_text | value_unit | ifrs_scope | period_scope |
| --- | --- | --- | --- | --- | --- |
| 매출액 | 2023/12 | 199,463.97 | 억원 | CONNECTED | YEAR |
| 매출액 | 2024/12 | 198,948.10 | 억원 | CONNECTED | YEAR |
| 매출액 | 2025/12 | 184,830.05 | 억원 | CONNECTED | YEAR |
| 매출액 | 2026/12(E) | 201,659 | 억원 | CONNECTED | YEAR |
| 매출액 | 2027/12(E) | 205,995 | 억원 | CONNECTED | YEAR |
| 매출액 | 2028/12(E) | 203,000 | 억원 | CONNECTED | YEAR |
| 전년동기대비 | 2023/12 | -10.46 | % | CONNECTED | YEAR |
| 전년동기대비 | 2024/12 | -0.26 | % | CONNECTED | YEAR |
| 전년동기대비 | 2025/12 | -7.10 | % | CONNECTED | YEAR |
| 전년동기대비 | 2026/12(E) | 9.11 | % | CONNECTED | YEAR |
| 전년동기대비 | 2027/12(E) | 2.15 | % | CONNECTED | YEAR |
| 전년동기대비 | 2028/12(E) | -1.45 | % | CONNECTED | YEAR |

## 삼성전자 대표 샘플 - consensus revision
| raw_metric_name | period_label_raw | value_text | consensus_year_label | ifrs_scope | period_scope |
| --- | --- | --- | --- | --- | --- |
| 매출액 | 2026/03/25 | 201,659 | FY1 | CONNECTED | YEAR |
| 매출액 | 1개월전 | 200,975 | FY1 | CONNECTED | YEAR |
| 매출액 | 3개월전 | 201,825 | FY1 | CONNECTED | YEAR |
| 매출액 | 6개월전 | 191,758 | FY1 | CONNECTED | YEAR |
| 매출액 | 1년전 | 215,164 | FY1 | CONNECTED | YEAR |
| 영업이익 | 2026/03/25 | -3,663 | FY1 | CONNECTED | YEAR |
| 영업이익 | 1개월전 | -3,977 | FY1 | CONNECTED | YEAR |
| 영업이익 | 3개월전 | -1,328 | FY1 | CONNECTED | YEAR |
| 영업이익 | 6개월전 | -496 | FY1 | CONNECTED | YEAR |
| 영업이익 | 1년전 | 2,686 | FY1 | CONNECTED | YEAR |
| 지배주주순이익 | 2026/03/25 | -5,409 | FY1 | CONNECTED | YEAR |
| 지배주주순이익 | 1개월전 | -5,729 | FY1 | CONNECTED | YEAR |

## 삼성전자 대표 샘플 - broker target
| broker_name | estimate_date | target_price | previous_target_price | rating | is_consensus_aggregate |
| --- | --- | --- | --- | --- | --- |
| Consensus | nan | 102938.0 | 102500.0 | 3.69 | 1 |
| KB증권 | 2026/03/17 | 90000.0 | 80000.0 | 4.00 | 0 |
| 현대차증권 | 2026/03/06 | 74000.0 | 77000.0 | 3.00 | 0 |
| 유안타증권 | 2026/03/04 | 165000.0 | 165000.0 | 4.00 | 0 |
| 삼성증권 | 2026/03/03 | 92000.0 | 92000.0 | 3.00 | 0 |
| 한국투자증권 | 2026/02/27 | 110000.0 | 110000.0 | 4.00 | 0 |
| 신한투자증권 | 2026/02/05 | 120000.0 | 120000.0 | 4.00 | 0 |
| 한화투자증권 | 2026/02/05 | 100000.0 | 100000.0 | 4.00 | 0 |

## 삼성전자 대표 샘플 - report summary
| report_date | report_title | provider_name | analyst_name | rating_text |
| --- | --- | --- | --- | --- |
| 2026/03/17 | 롯데케미칼-가동률 조정: 우리보다 급한 건 고객사 | KB증권 | 전우제.송윤주 | BUY |
| 2026/03/06 | 롯데케미칼-대산공장 구조조정 긍정적. 다만, 지금은 중동 불확실성 해소가 중요 | 현대차증권 | 강동진 | MARKETPERFORM |
| 2026/03/04 | 롯데케미칼-대산공장 구조조정으로, 2,000억원 절감 기대! | 유안타증권 | 황규원.서석준 | BUY |
| 2026/02/26 | 롯데케미칼-대산 구조조정, 단기 영업손익 수치 개선될 듯 | LS증권 | 정경희 | Not Rated |

## 삼성전자 대표 샘플 - shareholder
| holder_name | holder_type | shares | ownership_pct | as_of_date |
| --- | --- | --- | --- | --- |
| 롯데지주(외 41인) | holder_detail | 23347791.0 | 54.58 | 2025/12/30 |
| 국민연금공단 | holder_detail | 3162691.0 | 7.39 | 2025/03/12 |
| 자사주 | holder_detail | 608272.0 | 1.42 | 2024/05/10 |
| 최대주주등 (본인+특별관계자) | shareholder_group | 23347791.0 | 54.58 | 2025/12/30 |
| 10%이상주주 (본인+특별관계자) | shareholder_group | nan | nan | nan |
| 5%이상주주 (본인+특별관계자) | shareholder_group | 3162691.0 | 7.39 | 2025/03/12 |
| 임원 (5%미만 중, 임원인자) | shareholder_group | 33480.0 | 0.08 | 2025/12/01 |
| 자기주식 (자사주+자사주신탁) | shareholder_group | 608272.0 | 1.42 | 2024/05/10 |

## 삼성전자 대표 샘플 - Business Summary
동사는 1976년 설립된 종합 석유화학 기업으로, 상장 및 비상장 포함 28개 종속회사를 보유하고 있음. 기초화학, 첨단소재, 정밀화학, 전지소재, 수소에너지로 사업영역을 구분하며, 여수·대산·울산에 생산시설을 보유하고 PE, PP, ABS, PC 및 고부가 스페셜티 제품을 생산함. 중국, 멕시코, 헝가리, 베트남 등 해외에 사업장을 두고 다양한 제품을 제조·판매하고 있음.
2025년 3분기 누적 전년동기 대비 연결기준 매출액은 8.8% 감소, 영업손실은 25.1% 감소, 당기순손실은 11.1% 증가. 기초화학 사업부문은 글로벌 경기침체와 중국의 공급 과잉, 지정학적 리스크, 미국 관세 정책 불확실성으로 실적 부진 지속됨. 첨단소재 사업부문은 Specialty 확대로 수익성 방어하고, 울산공장 폐PET 재활용과 대산공장 수소출하센터, 울산 수소 연료전지 발전사업으로 친환경 사업 기반 확보함.
## 다음 작업 제안
- 다종목 확장 시 gicode 리스트 입력과 batch runner를 추가
- DART API를 다음 단계에서 연결해 FnGuide 데이터와 교차 검증
- 필요 시 차트 데이터 XML endpoint까지 확장
