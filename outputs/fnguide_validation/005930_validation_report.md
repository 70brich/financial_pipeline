# FnGuide validation report

## Company
- company_name: 삼성전자
- stock_code: 005930

## Source URLs
- consensus: https://comp.fnguide.com/SVO2/ASP/SVD_Consensus.asp?pGB=1&gicode=A005930&cID=&MenuYn=Y&ReportGB=&NewMenuID=108&stkGb=701
- main: https://comp.fnguide.com/SVO2/ASP/SVD_Main.asp?pGB=1&gicode=A005930&cID=&MenuYn=Y&ReportGB=&NewMenuID=101&stkGb=701

## Extracted blocks
- consensus financial long rows: 294
- consensus revision long rows: 272
- broker target rows: 26
- report summary rows: 23
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
- broker_target_price: 26
- broker_report_summary: 23
- company_shareholder_snapshot: 10
- company_business_summary: 1

## 삼성전자 대표 샘플 - consensus financial
| raw_metric_name | period_label_raw | value_text | value_unit | ifrs_scope | period_scope |
| --- | --- | --- | --- | --- | --- |
| 매출액 | 2023/12 | 2,589,354.94 | 억원 | CONNECTED | YEAR |
| 매출액 | 2024/12 | 3,008,709.03 | 억원 | CONNECTED | YEAR |
| 매출액 | 2025/12 | 3,336,059.38 | 억원 | CONNECTED | YEAR |
| 매출액 | 2026/12(E) | 5,231,547 | 억원 | CONNECTED | YEAR |
| 매출액 | 2027/12(E) | 5,758,509 | 억원 | CONNECTED | YEAR |
| 매출액 | 2028/12(E) | 6,676,497 | 억원 | CONNECTED | YEAR |
| 전년동기대비 | 2023/12 | -14.33 | % | CONNECTED | YEAR |
| 전년동기대비 | 2024/12 | 16.20 | % | CONNECTED | YEAR |
| 전년동기대비 | 2025/12 | 10.88 | % | CONNECTED | YEAR |
| 전년동기대비 | 2026/12(E) | 56.82 | % | CONNECTED | YEAR |
| 전년동기대비 | 2027/12(E) | 10.07 | % | CONNECTED | YEAR |
| 전년동기대비 | 2028/12(E) | 15.94 | % | CONNECTED | YEAR |

## 삼성전자 대표 샘플 - consensus revision
| raw_metric_name | period_label_raw | value_text | consensus_year_label | ifrs_scope | period_scope |
| --- | --- | --- | --- | --- | --- |
| 매출액 | 2026/03/25 | 5,231,547 | FY1 | CONNECTED | YEAR |
| 매출액 | 1개월전 | 5,029,614 | FY1 | CONNECTED | YEAR |
| 매출액 | 3개월전 | 3,925,451 | FY1 | CONNECTED | YEAR |
| 매출액 | 6개월전 | 3,434,388 | FY1 | CONNECTED | YEAR |
| 매출액 | 1년전 | 3,436,860 | FY1 | CONNECTED | YEAR |
| 영업이익 | 2026/03/25 | 1,979,997 | FY1 | CONNECTED | YEAR |
| 영업이익 | 1개월전 | 1,797,644 | FY1 | CONNECTED | YEAR |
| 영업이익 | 3개월전 | 854,387 | FY1 | CONNECTED | YEAR |
| 영업이익 | 6개월전 | 457,305 | FY1 | CONNECTED | YEAR |
| 영업이익 | 1년전 | 432,416 | FY1 | CONNECTED | YEAR |
| 지배주주순이익 | 2026/03/25 | 1,648,765 | FY1 | CONNECTED | YEAR |
| 지배주주순이익 | 1개월전 | 1,487,201 | FY1 | CONNECTED | YEAR |

## 삼성전자 대표 샘플 - broker target
| broker_name | estimate_date | target_price | previous_target_price | rating | is_consensus_aggregate |
| --- | --- | --- | --- | --- | --- |
| Consensus | nan | 252720.0 | 224543.0 | 4.00 | 1 |
| KB증권 | 2026/03/25 | 320000.0 | 320000.0 | 4.00 | 0 |
| 한국투자증권 | 2026/03/23 | 270000.0 | 270000.0 | 4.00 | 0 |
| 미래에셋증권 | 2026/03/23 | 300000.0 | 300000.0 | 4.00 | 0 |
| 대신증권 | 2026/03/19 | 270000.0 | 270000.0 | 4.00 | 0 |
| 유안타증권 | 2026/03/19 | 270000.0 | 270000.0 | 4.00 | 0 |
| DS투자증권 | 2026/03/16 | 270000.0 | 183000.0 | 4.00 | 0 |
| 하나증권 | 2026/03/13 | 300000.0 | 250000.0 | 4.00 | 0 |

## 삼성전자 대표 샘플 - report summary
| report_date | report_title | provider_name | analyst_name | rating_text |
| --- | --- | --- | --- | --- |
| 2026/03/25 | 삼성전자-피지컬 AI 시장 진입 가시화 | KB증권 | 김동원 | BUY |
| 2026/03/23 | 삼성전자-긍정적 흐름의 연속 | 미래에셋증권 | 김영건 | 매수 |
| 2026/03/23 | SamsungElec-Positive momentum continues | 미래에셋증권 | 김영건 | 매수 |
| 2026/03/20 | 삼성전자-재고는 바닥, 주문은 최대 | KB증권 | 김동원 | BUY |
| 2026/03/19 | 삼성전자-추가 상승 여력 충분 | KB증권 | 김동원 | BUY |
| 2026/03/18 | 삼성전자-진정한 풀스택 | 미래에셋증권 | 김영건 | 매수 |

## 삼성전자 대표 샘플 - shareholder
| holder_name | holder_type | shares | ownership_pct | as_of_date |
| --- | --- | --- | --- | --- |
| 삼성생명보험(외 15인) | holder_detail | 1162793388.0 | 19.64 | 2026/03/20 |
| 국민연금공단 | holder_detail | 458637667.0 | 7.75 | 2022/08/16 |
| BlackRock Fund Advisors(외 15인) | holder_detail | 300391061.0 | 5.07 | 2019/01/28 |
| 자사주 | holder_detail | 124013769.0 | 2.09 | 2026/03/24 |
| 최대주주등 (본인+특별관계자) | shareholder_group | 1162793388.0 | 19.64 | 2026/03/20 |
| 10%이상주주 (본인+특별관계자) | shareholder_group | nan | nan | nan |
| 5%이상주주 (본인+특별관계자) | shareholder_group | 759028728.0 | 12.82 | 2022/08/16 |
| 임원 (5%미만 중, 임원인자) | shareholder_group | 4780149.0 | 0.08 | 2026/03/09 |

## 삼성전자 대표 샘플 - Business Summary
동사는 1969년 설립되어 1975년 유가증권시장에 상장하였으며, 2017년 Harman 인수로 전장부품 사업을 확장함. DX 부문은 TV, 냉장고, 스마트폰을, DS 부문은 DRAM, NAND Flash, 모바일AP를, SDC는 OLED 패널을, Harman은 디지털 콕핏과 카오디오를 생산·판매하고 있음. 업계 최고 수준의 R&D 역량으로 지속적 기술 혁신, 미래 준비를 통해 고객에게 새로운 가치를 제공하고 있음.
2025년 3분기 누적 전년동기 대비 연결기준 매출액은 6.5% 증가, 영업이익은 10.3% 감소, 당기순이익은 4.1% 감소. DS부문은 분기 최대 매출을 달성했으나, 재고평가손실 환입 축소와 성과급 충당 등 일회성 비용으로 수익성은 제한적. 고성능 메모리 수요 증가 추세가 지속되고, 성장하는 IT OLED 시장을 선점하고 Auto용, 워치용 등으로 매출 구조를 다변화하여 사업 포트폴리오 안정성을 강화해 나갈 것임.
## 다음 작업 제안
- 다종목 확장 시 gicode 리스트 입력과 batch runner를 추가
- DART API를 다음 단계에서 연결해 FnGuide 데이터와 교차 검증
- 필요 시 차트 데이터 XML endpoint까지 확장
