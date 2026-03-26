# FnGuide validation report

## Company
- company_name: 영화테크
- stock_code: 265560

## Source URLs
- consensus: https://comp.fnguide.com/SVO2/ASP/SVD_Consensus.asp?pGB=1&gicode=A265560&cID=&MenuYn=Y&ReportGB=&NewMenuID=108&stkGb=701
- main: https://comp.fnguide.com/SVO2/ASP/SVD_Main.asp?pGB=1&gicode=A265560&cID=&MenuYn=Y&ReportGB=&NewMenuID=101&stkGb=701

## Extracted blocks
- consensus financial long rows: 203
- consensus revision long rows: 0
- broker target rows: 0
- report summary rows: 0
- shareholder snapshot rows: 8
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
- fnguide_observation: 203
- broker_target_price: 0
- broker_report_summary: 0
- company_shareholder_snapshot: 8
- company_business_summary: 1

## 삼성전자 대표 샘플 - consensus financial
| raw_metric_name | period_label_raw | value_text | value_unit | ifrs_scope | period_scope |
| --- | --- | --- | --- | --- | --- |
| 매출액 | 2022/12 | 479.45 | 억원 | CONNECTED | YEAR |
| 매출액 | 2023/12 | 649.20 | 억원 | CONNECTED | YEAR |
| 매출액 | 2024/12 | 948.27 | 억원 | CONNECTED | YEAR |
| 매출액 | 2025/12(P) | 1,086 | 억원 | CONNECTED | YEAR |
| 전년동기대비 | 2022/12 | 18.02 | % | CONNECTED | YEAR |
| 전년동기대비 | 2023/12 | 35.41 | % | CONNECTED | YEAR |
| 전년동기대비 | 2024/12 | 46.07 | % | CONNECTED | YEAR |
| 전년동기대비 | 2025/12(P) | 14.53 | % | CONNECTED | YEAR |
| 영업이익 | 2022/12 | 19.06 | 억원 | CONNECTED | YEAR |
| 영업이익 | 2023/12 | 50.14 | 억원 | CONNECTED | YEAR |
| 영업이익 | 2024/12 | 153.88 | 억원 | CONNECTED | YEAR |
| 영업이익 | 2025/12(P) | 180 | 억원 | CONNECTED | YEAR |

## 삼성전자 대표 샘플 - consensus revision
_No rows_

## 삼성전자 대표 샘플 - broker target
_No rows_

## 삼성전자 대표 샘플 - report summary
_No rows_

## 삼성전자 대표 샘플 - shareholder
| holder_name | holder_type | shares | ownership_pct | as_of_date |
| --- | --- | --- | --- | --- |
| 엄준형(외 5인) | holder_detail | 5253468.0 | 49.14 | 2021/06/03 |
| 한국단자공업 | holder_detail | 990000.0 | 9.26 | 2021/06/03 |
| 최대주주등 (본인+특별관계자) | shareholder_group | 5253468.0 | 49.14 | 2021/06/03 |
| 10%이상주주 (본인+특별관계자) | shareholder_group | nan | nan | nan |
| 5%이상주주 (본인+특별관계자) | shareholder_group | 990000.0 | 9.26 | 2021/06/03 |
| 임원 (5%미만 중, 임원인자) | shareholder_group | 8600.0 | 0.08 | 2021/09/10 |
| 자기주식 (자사주+자사주신탁) | shareholder_group | nan | nan | nan |
| 우리사주조합 | shareholder_group | 135798.0 | 1.27 | 2021/06/03 |

## 삼성전자 대표 샘플 - Business Summary
동사는 2000년 설립되어 자동차용 정션박스와 전기차 부품을 자체 개발/제조하여 글로벌 업체에 공급하고 있음. 정션박스는 자동차 부품의 전원/신호 공급 및 회로 보호 기능을 하는 중요한 시스템 부품으로, 전기차 관련 핵심 부품을 개발/공급하고 있음. SDV의 Zone Controller 연구개발과 전력변환 제어모듈 양산화를 추진하며 다양한 고객 포트폴리오를 구성하고 있음.
2025년 3분기 누적 전년동기 대비 연결기준 매출액은 19.4% 증가, 영업이익은 22.0% 증가, 당기순이익은 3.3% 증가. 차량용 반도체 공급망 불확실성 해소와 유럽·미국 회복세, 전기차 수요 증가로 내수·수출 이익성이 개선되었음. 글로벌 환경 규제 강화로 전기차 시장은 연평균 33.6% 성장 예상되며, IT기술 융합으로 차량 전자부품 시장도 67% 증가 전망임.
## 다음 작업 제안
- 다종목 확장 시 gicode 리스트 입력과 batch runner를 추가
- DART API를 다음 단계에서 연결해 FnGuide 데이터와 교차 검증
- 필요 시 차트 데이터 XML endpoint까지 확장
