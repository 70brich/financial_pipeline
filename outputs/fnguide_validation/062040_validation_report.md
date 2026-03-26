# FnGuide validation report

## Company
- company_name: 산일전기
- stock_code: 062040

## Source URLs
- consensus: https://comp.fnguide.com/SVO2/ASP/SVD_Consensus.asp?pGB=1&gicode=A062040&cID=&MenuYn=Y&ReportGB=&NewMenuID=108&stkGb=701
- main: https://comp.fnguide.com/SVO2/ASP/SVD_Main.asp?pGB=1&gicode=A062040&cID=&MenuYn=Y&ReportGB=&NewMenuID=101&stkGb=701

## Extracted blocks
- consensus financial long rows: 318
- consensus revision long rows: 353
- broker target rows: 10
- report summary rows: 5
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
- fnguide_observation: 671
- broker_target_price: 10
- broker_report_summary: 5
- company_shareholder_snapshot: 9
- company_business_summary: 1

## 삼성전자 대표 샘플 - consensus financial
| raw_metric_name | period_label_raw | value_text | value_unit | ifrs_scope | period_scope |
| --- | --- | --- | --- | --- | --- |
| 매출액 | 2023/12 | 2,145.38 | 억원 | CONNECTED | YEAR |
| 매출액 | 2024/12 | 3,339.97 | 억원 | CONNECTED | YEAR |
| 매출액 | 2025/12 | 5,019.46 | 억원 | CONNECTED | YEAR |
| 매출액 | 2026/12(E) | 6,607 | 억원 | CONNECTED | YEAR |
| 매출액 | 2027/12(E) | 8,182 | 억원 | CONNECTED | YEAR |
| 매출액 | 2028/12(E) | 9,080 | 억원 | CONNECTED | YEAR |
| 전년동기대비 | 2023/12 | 99.25 | % | CONNECTED | YEAR |
| 전년동기대비 | 2024/12 | 55.68 | % | CONNECTED | YEAR |
| 전년동기대비 | 2025/12 | 50.28 | % | CONNECTED | YEAR |
| 전년동기대비 | 2026/12(E) | 31.63 | % | CONNECTED | YEAR |
| 전년동기대비 | 2027/12(E) | 23.84 | % | CONNECTED | YEAR |
| 전년동기대비 | 2028/12(E) | 10.98 | % | CONNECTED | YEAR |

## 삼성전자 대표 샘플 - consensus revision
| raw_metric_name | period_label_raw | value_text | consensus_year_label | ifrs_scope | period_scope |
| --- | --- | --- | --- | --- | --- |
| 매출액 | 2026/03/25 | 6,607 | FY1 | CONNECTED | YEAR |
| 매출액 | 1개월전 | 6,607 | FY1 | CONNECTED | YEAR |
| 매출액 | 3개월전 | 6,668 | FY1 | CONNECTED | YEAR |
| 영업이익 | 2026/03/25 | 2,464 | FY1 | CONNECTED | YEAR |
| 영업이익 | 1개월전 | 2,477 | FY1 | CONNECTED | YEAR |
| 영업이익 | 3개월전 | 2,522 | FY1 | CONNECTED | YEAR |
| 지배주주순이익 | 2026/03/25 | 1,986 | FY1 | CONNECTED | YEAR |
| 지배주주순이익 | 1개월전 | 1,996 | FY1 | CONNECTED | YEAR |
| 지배주주순이익 | 3개월전 | 2,035 | FY1 | CONNECTED | YEAR |
| EPS | 2026/03/25 | 6,502 | FY1 | CONNECTED | YEAR |
| EPS | 1개월전 | 6,534 | FY1 | CONNECTED | YEAR |
| EPS | 3개월전 | 6,683 | FY1 | CONNECTED | YEAR |

## 삼성전자 대표 샘플 - broker target
| broker_name | estimate_date | target_price | previous_target_price | rating | is_consensus_aggregate |
| --- | --- | --- | --- | --- | --- |
| Consensus | nan | 200000.0 | 180429.0 | 4.00 | 1 |
| LS증권 | 2026/03/20 | 215000.0 | 215000.0 | 4.00 | 0 |
| NH투자증권 | 2026/03/20 | 220000.0 | 190000.0 | 4.00 | 0 |
| KB증권 | 2026/03/10 | nan | nan | nan | 0 |
| 유안타증권 | 2026/03/04 | 200000.0 | 200000.0 | 4.00 | 0 |
| 유진투자증권 | 2026/03/03 | 205000.0 | nan | 4.00 | 0 |
| 리딩투자증권 | 2026/02/23 | 200000.0 | 150000.0 | 4.00 | 0 |
| 교보증권 | 2026/02/10 | 200000.0 | 178000.0 | 4.00 | 0 |

## 삼성전자 대표 샘플 - report summary
| report_date | report_title | provider_name | analyst_name | rating_text |
| --- | --- | --- | --- | --- |
| 2026/03/20 | 산일전기-국내 대형 3사를 대신할 좋은 대안 | NH투자증권 | 이민재.류승원 | BUY |
| 2026/03/10 | 산일전기-특수변압기 수요 강세 지속 | KB증권 | 김선봉.성현동 | Not Rated |
| 2026/03/04 | 산일전기-수급 해소 이후 본격 레벨업 | 유안타증권 | 손현정.김고은 | BUY |
| 2026/03/04 | SANIL ELECTRIC-Full-fledged level-up after supply overhang clears | 유안타증권 | 손현정 | BUY |
| 2026/03/03 | 산일전기-특수변압기 중심 프리미엄 지속 | 유진투자증권 | 허준서 | BUY |

## 삼성전자 대표 샘플 - shareholder
| holder_name | holder_type | shares | ownership_pct | as_of_date |
| --- | --- | --- | --- | --- |
| 박동석(외 2인) | holder_detail | 16851947.0 | 55.17 | 2024/07/29 |
| 국민연금공단 | holder_detail | 2521103.0 | 8.25 | 2025/07/24 |
| 자사주 | holder_detail | 60753.0 | 0.2 | 2024/07/29 |
| 최대주주등 (본인+특별관계자) | shareholder_group | 16851947.0 | 55.17 | 2024/07/29 |
| 10%이상주주 (본인+특별관계자) | shareholder_group | nan | nan | nan |
| 5%이상주주 (본인+특별관계자) | shareholder_group | 2521103.0 | 8.25 | 2025/07/24 |
| 임원 (5%미만 중, 임원인자) | shareholder_group | 161646.0 | 0.53 | 2025/08/20 |
| 자기주식 (자사주+자사주신탁) | shareholder_group | 60753.0 | 0.2 | 2024/07/29 |

## 삼성전자 대표 샘플 - Business Summary
동사는 1994년 산일전기 주식회사로 설립되었으며, 2024년 7월 유가증권시장에 상장함. 당기 중 신재생에너지 사업 확장을 위해 산일에너지 주식회사를 신설하여 연결대상 종속회사로 편입함. 당사는 매출액의 약 72% 이상이 미국에서 발생 하고 있음. 전력기기 제조업과 신재생에너지 사업을 영위하며, 주요 제품인 변압기는 전력망, 신재생에너지, 산업용 분야에 공급되고 있음.
2025년 3분기 누적 전년동기 대비 연결기준 매출액은 59.5% 증가, 영업이익은 67.2% 증가, 당기순이익은 87.0% 증가. 신재생에너지 관련 변압기 수요 증가와 미국 전력망 교체 및 신규 투자 수요 확대로 매출이 크게 증가함. 미국 인플레이션 감축법 시행 이후 태양광 및 풍력 발전 설비 확대에 따른 배전 변압기 수요가 급증하며 실적 개선에 기여하고 있음.
## 다음 작업 제안
- 다종목 확장 시 gicode 리스트 입력과 batch runner를 추가
- DART API를 다음 단계에서 연결해 FnGuide 데이터와 교차 검증
- 필요 시 차트 데이터 XML endpoint까지 확장
