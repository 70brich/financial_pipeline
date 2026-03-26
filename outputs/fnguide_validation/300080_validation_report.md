# FnGuide validation report

## Company
- company_name: 플리토
- stock_code: 300080

## Source URLs
- consensus: https://comp.fnguide.com/SVO2/ASP/SVD_Consensus.asp?pGB=1&gicode=A300080&cID=&MenuYn=Y&ReportGB=&NewMenuID=108&stkGb=701
- main: https://comp.fnguide.com/SVO2/ASP/SVD_Main.asp?pGB=1&gicode=A300080&cID=&MenuYn=Y&ReportGB=&NewMenuID=101&stkGb=701

## Extracted blocks
- consensus financial long rows: 200
- consensus revision long rows: 0
- broker target rows: 0
- report summary rows: 0
- shareholder snapshot rows: 7
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
- fnguide_observation: 200
- broker_target_price: 0
- broker_report_summary: 0
- company_shareholder_snapshot: 7
- company_business_summary: 1

## 삼성전자 대표 샘플 - consensus financial
| raw_metric_name | period_label_raw | value_text | value_unit | ifrs_scope | period_scope |
| --- | --- | --- | --- | --- | --- |
| 매출액 | 2022/12 | 136.39 | 억원 | CONNECTED | YEAR |
| 매출액 | 2023/12 | 177.61 | 억원 | CONNECTED | YEAR |
| 매출액 | 2024/12 | 203.01 | 억원 | CONNECTED | YEAR |
| 매출액 | 2025/12(P) | 360 | 억원 | CONNECTED | YEAR |
| 전년동기대비 | 2022/12 | 46.06 | % | CONNECTED | YEAR |
| 전년동기대비 | 2023/12 | 30.22 | % | CONNECTED | YEAR |
| 전년동기대비 | 2024/12 | 14.30 | % | CONNECTED | YEAR |
| 전년동기대비 | 2025/12(P) | 77.23 | % | CONNECTED | YEAR |
| 컨센서스대비 | 2023/12 | 3.87 | % | CONNECTED | YEAR |
| 컨센서스대비 | 2025/12(P) | 5.36 | % | CONNECTED | YEAR |
| 영업이익 | 2022/12 | -65.95 | 억원 | CONNECTED | YEAR |
| 영업이익 | 2023/12 | -50.94 | 억원 | CONNECTED | YEAR |

## 삼성전자 대표 샘플 - consensus revision
_No rows_

## 삼성전자 대표 샘플 - broker target
_No rows_

## 삼성전자 대표 샘플 - report summary
_No rows_

## 삼성전자 대표 샘플 - shareholder
| holder_name | holder_type | shares | ownership_pct | as_of_date |
| --- | --- | --- | --- | --- |
| 이정수(외 2인) | holder_detail | 5170329.0 | 31.32 | 2025/06/24 |
| 최대주주등 (본인+특별관계자) | shareholder_group | 5170329.0 | 31.32 | 2025/06/24 |
| 10%이상주주 (본인+특별관계자) | shareholder_group | nan | nan | nan |
| 5%이상주주 (본인+특별관계자) | shareholder_group | nan | nan | nan |
| 임원 (5%미만 중, 임원인자) | shareholder_group | 4000.0 | 0.02 | 2025/12/08 |
| 자기주식 (자사주+자사주신탁) | shareholder_group | nan | nan | nan |
| 우리사주조합 | shareholder_group | nan | nan | nan |

## 삼성전자 대표 샘플 - Business Summary
동사는 2012년 설립된 AI 언어 데이터 및 솔루션 기업으로, 2019년 기술성장기업으로 코스닥시장에 상장함. 데이터 판매, 플랫폼서비스, 솔루션 사업을 영위하며, 1,400만 명 이상의 유저를 통해 173개국 42개 언어를 지원하는 고품질 데이터를 글로벌 기업에 제공함. 지속적인 플랫폼 개선과 데이터 기술 개발을 통해 기술경쟁력을 확보하고, 안정적인 데이터 구축 및 피드백으로 AI 기술 발전을 지원하고 있음.
2025년 3분기 누적 전년동기 대비 연결기준 매출액은 75.1% 증가, 영업이익 흑자전환, 당기순이익은 1551.8% 증가. 글로벌 빅테크 기업에 금융, 제조, 법률, IT 등 고품질 데이터 세트를 제공하여 데이터 판매 사업 확대로 실적이 개선됨. 글로벌 AI 산업 성장 전망 속 Chat Translation과 Live Translation 판매 시작으로 시장 대응하고 있음.
## 다음 작업 제안
- 다종목 확장 시 gicode 리스트 입력과 batch runner를 추가
- DART API를 다음 단계에서 연결해 FnGuide 데이터와 교차 검증
- 필요 시 차트 데이터 XML endpoint까지 확장
