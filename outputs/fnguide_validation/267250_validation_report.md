# FnGuide validation report

## Company
- company_name: HD현대
- stock_code: 267250

## Source URLs
- consensus: https://comp.fnguide.com/SVO2/ASP/SVD_Consensus.asp?pGB=1&gicode=A267250&cID=&MenuYn=Y&ReportGB=&NewMenuID=108&stkGb=701
- main: https://comp.fnguide.com/SVO2/ASP/SVD_Main.asp?pGB=1&gicode=A267250&cID=&MenuYn=Y&ReportGB=&NewMenuID=101&stkGb=701

## Extracted blocks
- consensus financial long rows: 303
- consensus revision long rows: 308
- broker target rows: 5
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
- fnguide_observation: 611
- broker_target_price: 5
- broker_report_summary: 3
- company_shareholder_snapshot: 9
- company_business_summary: 1

## 삼성전자 대표 샘플 - consensus financial
| raw_metric_name | period_label_raw | value_text | value_unit | ifrs_scope | period_scope |
| --- | --- | --- | --- | --- | --- |
| 매출액 | 2023/12 | 613,313.03 | 억원 | CONNECTED | YEAR |
| 매출액 | 2024/12 | 677,656.26 | 억원 | CONNECTED | YEAR |
| 매출액 | 2025/12 | 712,594.38 | 억원 | CONNECTED | YEAR |
| 매출액 | 2026/12(E) | 803,454 | 억원 | CONNECTED | YEAR |
| 매출액 | 2027/12(E) | 838,603 | 억원 | CONNECTED | YEAR |
| 전년동기대비 | 2023/12 | 0.79 | % | CONNECTED | YEAR |
| 전년동기대비 | 2024/12 | 10.49 | % | CONNECTED | YEAR |
| 전년동기대비 | 2025/12 | 5.16 | % | CONNECTED | YEAR |
| 전년동기대비 | 2026/12(E) | 12.75 | % | CONNECTED | YEAR |
| 전년동기대비 | 2027/12(E) | 4.37 | % | CONNECTED | YEAR |
| 컨센서스대비 | 2023/12 | -0.93 | % | CONNECTED | YEAR |
| 컨센서스대비 | 2024/12 | 0.07 | % | CONNECTED | YEAR |

## 삼성전자 대표 샘플 - consensus revision
| raw_metric_name | period_label_raw | value_text | consensus_year_label | ifrs_scope | period_scope |
| --- | --- | --- | --- | --- | --- |
| 매출액 | 2026/03/25 | 803,454 | FY1 | CONNECTED | YEAR |
| 매출액 | 1개월전 | 770,919 | FY1 | CONNECTED | YEAR |
| 매출액 | 3개월전 | 747,017 | FY1 | CONNECTED | YEAR |
| 매출액 | 6개월전 | 735,202 | FY1 | CONNECTED | YEAR |
| 매출액 | 1년전 | 753,528 | FY1 | CONNECTED | YEAR |
| 영업이익 | 2026/03/25 | 79,774 | FY1 | CONNECTED | YEAR |
| 영업이익 | 1개월전 | 73,989 | FY1 | CONNECTED | YEAR |
| 영업이익 | 3개월전 | 73,976 | FY1 | CONNECTED | YEAR |
| 영업이익 | 6개월전 | 62,262 | FY1 | CONNECTED | YEAR |
| 영업이익 | 1년전 | 54,093 | FY1 | CONNECTED | YEAR |
| 지배주주순이익 | 2026/03/25 | 15,062 | FY1 | CONNECTED | YEAR |
| 지배주주순이익 | 1개월전 | 13,779 | FY1 | CONNECTED | YEAR |

## 삼성전자 대표 샘플 - broker target
| broker_name | estimate_date | target_price | previous_target_price | rating | is_consensus_aggregate |
| --- | --- | --- | --- | --- | --- |
| Consensus | nan | 345500.0 | 337333.0 | 4.00 | 1 |
| LS증권 | 2026/03/20 | 415000.0 | 440000.0 | 4.00 | 0 |
| 흥국증권 | 2026/03/16 | 370000.0 | 330000.0 | 4.00 | 0 |
| 삼성증권 | 2026/02/13 | 300000.0 | 242000.0 | 4.00 | 0 |
| 키움증권 | 2026/01/27 | 297000.0 | nan | 4.00 | 0 |

## 삼성전자 대표 샘플 - report summary
| report_date | report_title | provider_name | analyst_name | rating_text |
| --- | --- | --- | --- | --- |
| 2026/03/20 | HD현대-HD현대오일뱅크와 로봇 | LS증권 | 정경희 | BUY |
| 2026/03/16 | HD현대-자회사의 고성장과 낙수효과의 본격화 | 흥국증권 | 박종렬.김지은 | BUY |
| 2026/03/03 | HD현대-정유와 로봇은요? | LS증권 | 정경희 | BUY |

## 삼성전자 대표 샘플 - shareholder
| holder_name | holder_type | shares | ownership_pct | as_of_date |
| --- | --- | --- | --- | --- |
| 정몽준(외 8인) | holder_detail | 29374587.0 | 37.19 | 2024/07/15 |
| 자사주 | holder_detail | 8324655.0 | 10.54 | 2021/04/13 |
| 국민연금공단 | holder_detail | 5902972.0 | 7.47 | 2025/08/21 |
| 최대주주등 (본인+특별관계자) | shareholder_group | 29374587.0 | 37.19 | 2024/07/15 |
| 10%이상주주 (본인+특별관계자) | shareholder_group | nan | nan | nan |
| 5%이상주주 (본인+특별관계자) | shareholder_group | 5902972.0 | 7.47 | 2025/08/21 |
| 임원 (5%미만 중, 임원인자) | shareholder_group | 3381.0 | 0.0 | 2022/01/21 |
| 자기주식 (자사주+자사주신탁) | shareholder_group | 8324655.0 | 10.54 | 2021/04/13 |

## 삼성전자 대표 샘플 - Business Summary
동사는 2017년 HD한국조선해양㈜의 인적분할로 출범한 지주회사로, 조선해양, 정유, 전기전자, 건설기계 등 다양한 사업을 영위하고 있음. 조선해양부문은 원유운반선, 컨테이너선, LNG선 등을 건조하고, 정유부문은 52만 배럴 규모 원유정제시설로 각종 정유제품과 윤활기유, 폴리머제품 등을 생산함. 동사는 친환경 선박기술 개발, 바이오디젤 및 SAF 생산, 무인자동화·친환경 건설기계 개발 등으로 지속가능한 성장기반을 구축하고 있음.
2025년 3분기 누적 전년동기 대비 연결기준 매출액은 3.7% 증가, 영업이익은 96.1% 증가, 당기순이익은 68.1% 증가. 조선해양부문은 친환경 선박 수요 증가와 노후 선대 교체로 수주 증가, 실적 개선에 기여함. 정유부문은 유가 상승, 경유 시황 개선에도 휘발유 수요 둔화 및 원가 부담으로 수익성 제한적이며, 전기전자부문은 북미 데이터센터 및 신재생에너지 프로젝트로 전력기기 수주 확대됨.
## 다음 작업 제안
- 다종목 확장 시 gicode 리스트 입력과 batch runner를 추가
- DART API를 다음 단계에서 연결해 FnGuide 데이터와 교차 검증
- 필요 시 차트 데이터 XML endpoint까지 확장
