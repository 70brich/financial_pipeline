# FnGuide validation report

## Company
- company_name: 에스텍
- stock_code: 069510

## Source URLs
- consensus: https://comp.fnguide.com/SVO2/ASP/SVD_Consensus.asp?pGB=1&gicode=A069510&cID=&MenuYn=Y&ReportGB=&NewMenuID=108&stkGb=701
- main: https://comp.fnguide.com/SVO2/ASP/SVD_Main.asp?pGB=1&gicode=A069510&cID=&MenuYn=Y&ReportGB=&NewMenuID=101&stkGb=701

## Extracted blocks
- consensus financial long rows: 188
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
- fnguide_observation: 188
- broker_target_price: 0
- broker_report_summary: 0
- company_shareholder_snapshot: 8
- company_business_summary: 1

## 삼성전자 대표 샘플 - consensus financial
| raw_metric_name | period_label_raw | value_text | value_unit | ifrs_scope | period_scope |
| --- | --- | --- | --- | --- | --- |
| 매출액 | 2023/12 | 4,145.94 | 억원 | CONNECTED | YEAR |
| 매출액 | 2024/12 | 5,093.74 | 억원 | CONNECTED | YEAR |
| 매출액 | 2025/12 | 4,681.92 | 억원 | CONNECTED | YEAR |
| 전년동기대비 | 2023/12 | -11.50 | % | CONNECTED | YEAR |
| 전년동기대비 | 2024/12 | 22.86 | % | CONNECTED | YEAR |
| 전년동기대비 | 2025/12 | -8.08 | % | CONNECTED | YEAR |
| 영업이익 | 2023/12 | 245.55 | 억원 | CONNECTED | YEAR |
| 영업이익 | 2024/12 | 439.82 | 억원 | CONNECTED | YEAR |
| 영업이익 | 2025/12 | 458.16 | 억원 | CONNECTED | YEAR |
| 전년동기대비 | 2023/12 | 181.53 | % | CONNECTED | YEAR |
| 전년동기대비 | 2024/12 | 79.12 | % | CONNECTED | YEAR |
| 전년동기대비 | 2025/12 | 4.17 | % | CONNECTED | YEAR |

## 삼성전자 대표 샘플 - consensus revision
_No rows_

## 삼성전자 대표 샘플 - broker target
_No rows_

## 삼성전자 대표 샘플 - report summary
_No rows_

## 삼성전자 대표 샘플 - shareholder
| holder_name | holder_type | shares | ownership_pct | as_of_date |
| --- | --- | --- | --- | --- |
| Foster Electric Co Ltd(외 1인) | holder_detail | 5392913.0 | 49.43 | 2023/10/24 |
| 자사주 | holder_detail | 2500000.0 | 22.91 | 2005/03/25 |
| 최대주주등 (본인+특별관계자) | shareholder_group | 5392913.0 | 49.43 | 2023/10/24 |
| 10%이상주주 (본인+특별관계자) | shareholder_group | nan | nan | nan |
| 5%이상주주 (본인+특별관계자) | shareholder_group | nan | nan | nan |
| 임원 (5%미만 중, 임원인자) | shareholder_group | 4000.0 | 0.04 | 2018/10/30 |
| 자기주식 (자사주+자사주신탁) | shareholder_group | 2500000.0 | 22.91 | 2005/03/25 |
| 우리사주조합 | shareholder_group | nan | nan | nan |

## 삼성전자 대표 샘플 - Business Summary
동사는 1999년 LG이노텍으로부터 분사해 설립되었으며, 2003년 코스닥시장에 상장함. 음향기기 제조 및 판매를 하며, 차량용 스피커, TV 스피커, 기타 오디오 부품을 주로 생산 및 판매하고 있음. 베트남, 중국 등 4개국에 5개의 자회사를 보유하고 있으며, 초Slim Speaker, 자동차용 프리미엄 Speaker 연구개발 및 경쟁력 강화에 노력하고 있음.
2025년 3분기 누적 전년동기 대비 연결기준 매출액은 6.9% 감소, 영업이익은 9.3% 감소, 당기순이익은 15.2% 감소. 자동차 사업부문은 안정적 매출을 유지하나, 가전 산업은 경기 영향으로 매출 감소함. 생산성 향상과 경비 절감으로 매출총이익 개선됨. 전기차와 자율주행차 확산으로 고급 자동차용 스피커 수요 증가, 회로제품 및 S/W 인력 확충으로 신사업 복합회로제품 개발에 투자 중임.
## 다음 작업 제안
- 다종목 확장 시 gicode 리스트 입력과 batch runner를 추가
- DART API를 다음 단계에서 연결해 FnGuide 데이터와 교차 검증
- 필요 시 차트 데이터 XML endpoint까지 확장
