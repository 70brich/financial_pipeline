# FnGuide validation report

## Company
- company_name: 오파스넷
- stock_code: 173130

## Source URLs
- consensus: https://comp.fnguide.com/SVO2/ASP/SVD_Consensus.asp?pGB=1&gicode=A173130&cID=&MenuYn=Y&ReportGB=&NewMenuID=108&stkGb=701
- main: https://comp.fnguide.com/SVO2/ASP/SVD_Main.asp?pGB=1&gicode=A173130&cID=&MenuYn=Y&ReportGB=&NewMenuID=101&stkGb=701

## Extracted blocks
- consensus financial long rows: 207
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
- fnguide_observation: 207
- broker_target_price: 0
- broker_report_summary: 0
- company_shareholder_snapshot: 8
- company_business_summary: 1

## 삼성전자 대표 샘플 - consensus financial
| raw_metric_name | period_label_raw | value_text | value_unit | ifrs_scope | period_scope |
| --- | --- | --- | --- | --- | --- |
| 매출액 | 2022/12 | 1,705.85 | 억원 | CONNECTED | YEAR |
| 매출액 | 2023/12 | 2,249.81 | 억원 | CONNECTED | YEAR |
| 매출액 | 2024/12 | 1,928.85 | 억원 | CONNECTED | YEAR |
| 매출액 | 2025/12(P) | 2,333 | 억원 | CONNECTED | YEAR |
| 전년동기대비 | 2022/12 | 40.10 | % | CONNECTED | YEAR |
| 전년동기대비 | 2023/12 | 31.89 | % | CONNECTED | YEAR |
| 전년동기대비 | 2024/12 | -14.27 | % | CONNECTED | YEAR |
| 전년동기대비 | 2025/12(P) | 20.95 | % | CONNECTED | YEAR |
| 영업이익 | 2022/12 | 85.24 | 억원 | CONNECTED | YEAR |
| 영업이익 | 2023/12 | 139.51 | 억원 | CONNECTED | YEAR |
| 영업이익 | 2024/12 | 106.52 | 억원 | CONNECTED | YEAR |
| 영업이익 | 2025/12(P) | 140 | 억원 | CONNECTED | YEAR |

## 삼성전자 대표 샘플 - consensus revision
_No rows_

## 삼성전자 대표 샘플 - broker target
_No rows_

## 삼성전자 대표 샘플 - report summary
_No rows_

## 삼성전자 대표 샘플 - shareholder
| holder_name | holder_type | shares | ownership_pct | as_of_date |
| --- | --- | --- | --- | --- |
| 장수현(외 7인) | holder_detail | 5387915.0 | 41.3 | 2025/12/23 |
| 자사주 | holder_detail | 3389.0 | 0.03 | 2024/04/19 |
| 최대주주등 (본인+특별관계자) | shareholder_group | 5387915.0 | 41.3 | 2025/12/23 |
| 10%이상주주 (본인+특별관계자) | shareholder_group | nan | nan | nan |
| 5%이상주주 (본인+특별관계자) | shareholder_group | nan | nan | nan |
| 임원 (5%미만 중, 임원인자) | shareholder_group | nan | nan | nan |
| 자기주식 (자사주+자사주신탁) | shareholder_group | 3389.0 | 0.03 | 2024/04/19 |
| 우리사주조합 | shareholder_group | nan | nan | nan |

## 삼성전자 대표 샘플 - Business Summary
동사는 2004년 설립, 네트워크 및 시스템 통합을 주요 사업으로 영위하며, 2018년 코스닥에 상장함. SK그룹, 삼성, 넥슨 등 대기업과 삼성SDS, LG CNS 등의 IT업체 및 글로벌 기업, 공공기관을 대상으로 네트워크 설계 및 유지보수 제공함. 다양한 솔루션을 활용한 채널 다변화를 통해 수익성을 개선하며, IT 시장 분석과 선제적 대응으로 경영 전략을 실천하고 있음.
2025년 3분기 누적 전년동기 대비 연결기준 매출액은 24.7% 증가, 영업이익은 121.2% 증가, 당기순이익은 154.3% 증가. 유지보수 사업의 안정적 매출과 네트워크 구축 사업 수주가 확대되어 실적이 개선됨. 디지털 전환의 가속화로 AI, 클라우드 등 신기술을 활용한 데이터센터와 IT서비스 시장 성장이 예상되며, 고객안심 데이터센터로 디지털 트랜스포메이션을 뒷받침하고 있음.
## 다음 작업 제안
- 다종목 확장 시 gicode 리스트 입력과 batch runner를 추가
- DART API를 다음 단계에서 연결해 FnGuide 데이터와 교차 검증
- 필요 시 차트 데이터 XML endpoint까지 확장
