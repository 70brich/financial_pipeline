# FnGuide validation report

## Company
- company_name: 에스앤에스텍
- stock_code: 101490

## Source URLs
- consensus: https://comp.fnguide.com/SVO2/ASP/SVD_Consensus.asp?pGB=1&gicode=A101490&cID=&MenuYn=Y&ReportGB=&NewMenuID=108&stkGb=701
- main: https://comp.fnguide.com/SVO2/ASP/SVD_Main.asp?pGB=1&gicode=A101490&cID=&MenuYn=Y&ReportGB=&NewMenuID=101&stkGb=701

## Extracted blocks
- consensus financial long rows: 202
- consensus revision long rows: 79
- broker target rows: 0
- report summary rows: 1
- shareholder snapshot rows: 11
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
- fnguide_observation: 281
- broker_target_price: 0
- broker_report_summary: 1
- company_shareholder_snapshot: 11
- company_business_summary: 1

## 삼성전자 대표 샘플 - consensus financial
| raw_metric_name | period_label_raw | value_text | value_unit | ifrs_scope | period_scope |
| --- | --- | --- | --- | --- | --- |
| 매출액 | 2023/12 | 1,503.20 | 억원 | CONNECTED | YEAR |
| 매출액 | 2024/12 | 1,760.14 | 억원 | CONNECTED | YEAR |
| 매출액 | 2025/12 | 2,437.33 | 억원 | CONNECTED | YEAR |
| 전년동기대비 | 2023/12 | 21.71 | % | CONNECTED | YEAR |
| 전년동기대비 | 2024/12 | 17.09 | % | CONNECTED | YEAR |
| 전년동기대비 | 2025/12 | 38.47 | % | CONNECTED | YEAR |
| 컨센서스대비 | 2023/12 | 3.31 | % | CONNECTED | YEAR |
| 영업이익 | 2023/12 | 250.39 | 억원 | CONNECTED | YEAR |
| 영업이익 | 2024/12 | 294.79 | 억원 | CONNECTED | YEAR |
| 영업이익 | 2025/12 | 503.90 | 억원 | CONNECTED | YEAR |
| 전년동기대비 | 2023/12 | 56.37 | % | CONNECTED | YEAR |
| 전년동기대비 | 2024/12 | 17.73 | % | CONNECTED | YEAR |

## 삼성전자 대표 샘플 - consensus revision
| raw_metric_name | period_label_raw | value_text | consensus_year_label | ifrs_scope | period_scope |
| --- | --- | --- | --- | --- | --- |
| 매출액 | 3개월전 | 2,888 | FY1 | CONNECTED | YEAR |
| 매출액 | 6개월전 | 2,824 | FY1 | CONNECTED | YEAR |
| 영업이익 | 3개월전 | 583 | FY1 | CONNECTED | YEAR |
| 영업이익 | 6개월전 | 564 | FY1 | CONNECTED | YEAR |
| 지배주주순이익 | 3개월전 | 540 | FY1 | CONNECTED | YEAR |
| 지배주주순이익 | 6개월전 | 530 | FY1 | CONNECTED | YEAR |
| EPS | 3개월전 | 2,531 | FY1 | CONNECTED | YEAR |
| EPS | 6개월전 | 2,471 | FY1 | CONNECTED | YEAR |
| PER | 3개월전 | 18.9 | FY1 | CONNECTED | YEAR |
| PER | 6개월전 | 20.8 | FY1 | CONNECTED | YEAR |
| 12M PER | 3개월전 | 18.91 | FY1 | CONNECTED | YEAR |
| 12M PER | 6개월전 | 21.73 | FY1 | CONNECTED | YEAR |

## 삼성전자 대표 샘플 - broker target
_No rows_

## 삼성전자 대표 샘플 - report summary
| report_date | report_title | provider_name | analyst_name | rating_text |
| --- | --- | --- | --- | --- |
| 2026/03/23 | 에스앤에스텍-국내 유일의 블랭크마스크 전문 기업. 공정 국산화의 최전선 파트너 | 그로쓰리서치 | 한용희 외2 | None |

## 삼성전자 대표 샘플 - shareholder
| holder_name | holder_type | shares | ownership_pct | as_of_date |
| --- | --- | --- | --- | --- |
| 정수홍(외 5인) | holder_detail | 4684160.0 | 21.96 | 2026/01/28 |
| 삼성자산운용 | holder_detail | 1788452.0 | 8.38 | 2026/02/05 |
| 삼성전자 | holder_detail | 1716116.0 | 8.04 | 2020/08/31 |
| 국민연금공단 | holder_detail | 1077057.0 | 5.05 | 2025/09/12 |
| 자사주 | holder_detail | 505275.0 | 2.37 | 2025/12/01 |
| 최대주주등 (본인+특별관계자) | shareholder_group | 4684160.0 | 21.96 | 2026/01/28 |
| 10%이상주주 (본인+특별관계자) | shareholder_group | nan | nan | nan |
| 5%이상주주 (본인+특별관계자) | shareholder_group | 4581625.0 | 21.47 | 2026/02/05 |

## 삼성전자 대표 샘플 - Business Summary
동사는 2001년 반도체 및 디스플레이용 블랭크마스크 제조·판매를 목적으로 설립되어 2009년 코스닥에 상장함. 대구 사업장과 용인 EUV 센터를 운영하며 반도체, FPD용 블랭크마스크 제조, 신기술사업금융업, 바이오 및 과학기술 서비스업을 영위하고 있음. 국내 삼성전자, SK하이닉스 등과 지리적 이점을 확보하고 있으며, 차세대 반도체 노광 기술인 EUV 공정 소재 기술 개발 및 양산화에 최선을 다하고 있음.
2025년 3분기 누적 전년동기 대비 연결기준 매출액은 37.7% 증가, 영업이익은 45.5% 증가, 당기순이익은 46.0% 증가. AI 반도체와 IT용 OLED 디스플레이 산업 성장으로 블랭크마스크 수요 증가하고 있으며, 중국의 첨단산업 공급망 내재화로 관련 기업 성장 가속화되고 있음. 반도체 하이엔드 제품과 OLED 수요 확대 예상되며, EUV 블랭크마스크와 펠리클 양산 위한 신규 시설 투자 진행 중.
## 다음 작업 제안
- 다종목 확장 시 gicode 리스트 입력과 batch runner를 추가
- DART API를 다음 단계에서 연결해 FnGuide 데이터와 교차 검증
- 필요 시 차트 데이터 XML endpoint까지 확장
