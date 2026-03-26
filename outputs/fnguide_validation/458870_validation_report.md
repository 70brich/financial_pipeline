# FnGuide validation report

## Company
- company_name: 씨어스테크놀로지
- stock_code: 458870

## Source URLs
- consensus: https://comp.fnguide.com/SVO2/ASP/SVD_Consensus.asp?pGB=1&gicode=A458870&cID=&MenuYn=Y&ReportGB=&NewMenuID=108&stkGb=701
- main: https://comp.fnguide.com/SVO2/ASP/SVD_Main.asp?pGB=1&gicode=A458870&cID=&MenuYn=Y&ReportGB=&NewMenuID=101&stkGb=701

## Extracted blocks
- consensus financial long rows: 267
- consensus revision long rows: 294
- broker target rows: 8
- report summary rows: 2
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
- fnguide_observation: 561
- broker_target_price: 8
- broker_report_summary: 2
- company_shareholder_snapshot: 8
- company_business_summary: 1

## 삼성전자 대표 샘플 - consensus financial
| raw_metric_name | period_label_raw | value_text | value_unit | ifrs_scope | period_scope |
| --- | --- | --- | --- | --- | --- |
| 매출액 | 2022/12 | 11.53 | 억원 | CONNECTED | YEAR |
| 매출액 | 2023/12 | 18.85 | 억원 | CONNECTED | YEAR |
| 매출액 | 2024/12 | 81.00 | 억원 | CONNECTED | YEAR |
| 매출액 | 2025/12(P) | 482 | 억원 | CONNECTED | YEAR |
| 매출액 | 2026/12(E) | 1,114 | 억원 | CONNECTED | YEAR |
| 매출액 | 2027/12(E) | 1,535 | 억원 | CONNECTED | YEAR |
| 전년동기대비 | 2022/12 | -16.81 | % | CONNECTED | YEAR |
| 전년동기대비 | 2023/12 | 63.49 | % | CONNECTED | YEAR |
| 전년동기대비 | 2024/12 | 329.71 | % | CONNECTED | YEAR |
| 전년동기대비 | 2025/12(P) | 494.70 | % | CONNECTED | YEAR |
| 전년동기대비 | 2026/12(E) | 131.21 | % | CONNECTED | YEAR |
| 전년동기대비 | 2027/12(E) | 37.78 | % | CONNECTED | YEAR |

## 삼성전자 대표 샘플 - consensus revision
| raw_metric_name | period_label_raw | value_text | consensus_year_label | ifrs_scope | period_scope |
| --- | --- | --- | --- | --- | --- |
| 매출액 | 2026/03/25 | 1,114 | FY1 | CONNECTED | YEAR |
| 매출액 | 1개월전 | 973 | FY1 | CONNECTED | YEAR |
| 매출액 | 3개월전 | 854 | FY1 | CONNECTED | YEAR |
| 영업이익 | 2026/03/25 | 494 | FY1 | CONNECTED | YEAR |
| 영업이익 | 1개월전 | 409 | FY1 | CONNECTED | YEAR |
| 영업이익 | 3개월전 | 331 | FY1 | CONNECTED | YEAR |
| 지배주주순이익 | 2026/03/25 | 450 | FY1 | CONNECTED | YEAR |
| 지배주주순이익 | 1개월전 | 350 | FY1 | CONNECTED | YEAR |
| 지배주주순이익 | 3개월전 | 283 | FY1 | CONNECTED | YEAR |
| EPS | 2026/03/25 | 1,181 | FY1 | CONNECTED | YEAR |
| EPS | 1개월전 | 2,759 | FY1 | CONNECTED | YEAR |
| EPS | 3개월전 | 2,236 | FY1 | CONNECTED | YEAR |

## 삼성전자 대표 샘플 - broker target
| broker_name | estimate_date | target_price | previous_target_price | rating | is_consensus_aggregate |
| --- | --- | --- | --- | --- | --- |
| Consensus | nan | 240000.0 | 165000.0 | 4.00 | 1 |
| 상상인증권 | 2026/03/16 | 260000.0 | 190000.0 | 4.00 | 0 |
| 신한투자증권 | 2026/02/09 | nan | nan | nan | 0 |
| 유진투자증권 | 2026/02/09 | 250000.0 | 180000.0 | 4.00 | 0 |
| 신영증권 | 2026/02/05 | 250000.0 | 140000.0 | 4.00 | 0 |
| 다올투자증권 | 2026/02/05 | nan | nan | nan | 0 |
| DB증권 | 2026/02/05 | 200000.0 | 150000.0 | 4.00 | 0 |
| 미래에셋증권 | 2026/02/04 | nan | nan | nan | 0 |

## 삼성전자 대표 샘플 - report summary
| report_date | report_title | provider_name | analyst_name | rating_text |
| --- | --- | --- | --- | --- |
| 2026/03/16 | 씨어스테크놀로지-씽크 잠재력 좀 더 공격적으로 보자 | 상상인증권 | 하태기 | BUY |
| 2026/03/11 | 씨어스테크놀로지-회사소개 및 주요 사업현황 | 해당기업 | nan | nan |

## 삼성전자 대표 샘플 - shareholder
| holder_name | holder_type | shares | ownership_pct | as_of_date |
| --- | --- | --- | --- | --- |
| 이영신(외 4인) | holder_detail | 10752840.0 | 28.25 | 2026/03/24 |
| 변동준 | holder_detail | 2133960.0 | 5.61 | 2026/03/24 |
| 최대주주등 (본인+특별관계자) | shareholder_group | 10752840.0 | 28.25 | 2026/03/24 |
| 10%이상주주 (본인+특별관계자) | shareholder_group | nan | nan | nan |
| 5%이상주주 (본인+특별관계자) | shareholder_group | 2133960.0 | 5.61 | 2026/03/24 |
| 임원 (5%미만 중, 임원인자) | shareholder_group | 4500.0 | 0.01 | 2026/03/24 |
| 자기주식 (자사주+자사주신탁) | shareholder_group | nan | nan | nan |
| 우리사주조합 | shareholder_group | nan | nan | nan |

## 삼성전자 대표 샘플 - Business Summary
동사는 2009년 설립, 2024년 코스닥 기술성장기업 특례상장, 2025년에는 씨어스바이오와 SEERS MENA LIMITED를 종속회사로 편입함. 생체신호 분석 인공지능 알고리즘과 웨어러블 의료기기 기반 IoMT 플랫폼 기술로 mobiCARE™와 thynC™를 제공하고 있음. 순환기내과 중심의 웨어러블 심전도 분석서비스를 주력 시장으로 신경과, 호흡기내과 등 다양한 분야의 진단지원 서비스를 목표하고 있음.
2025년 3분기 누적 전년동기 대비 연결기준 매출액은 961.5% 증가, 영업이익 흑자전환, 당기순이익 흑자전환. 1,000개 이상 의료기관이 동사 서비스를 도입하며 58만 건 이상의 홀터 심전도 분석 검사가 시행됨. 고령화에 따른 만성질환 증가와 스마트병원 확산 등으로 지속 성장 예상 함. 한림대성심병원, 순천향대서울병원, 화순전남대병원 등에서 실증 및 임상연구를 통해 편의성, 유효성, 경제성을 검증해 2024년부터 도입됨.
## 다음 작업 제안
- 다종목 확장 시 gicode 리스트 입력과 batch runner를 추가
- DART API를 다음 단계에서 연결해 FnGuide 데이터와 교차 검증
- 필요 시 차트 데이터 XML endpoint까지 확장
