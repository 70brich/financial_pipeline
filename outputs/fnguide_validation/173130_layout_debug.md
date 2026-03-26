# FnGuide layout debug

- company_name: 173130
- stock_code: 173130
- consensus_url: https://comp.fnguide.com/SVO2/ASP/SVD_Consensus.asp?pGB=1&gicode=A173130&cID=&MenuYn=Y&ReportGB=&NewMenuID=108&stkGb=701
- main_url: https://comp.fnguide.com/SVO2/ASP/SVD_Main.asp?pGB=1&gicode=A173130&cID=&MenuYn=Y&ReportGB=&NewMenuID=101&stkGb=701

## Detected consensus modes
- financial_ifrs_modes: [{'value': 'D', 'label': 'CONNECTED'}, {'value': 'B', 'label': 'SEPARATE'}]
- financial_period_modes: [{'value': 'A', 'label': 'YEAR'}, {'value': 'Q', 'label': 'QUARTER'}]
- revision_period_options: {'YEAR': [{'value': 'FY1', 'label': '202612'}, {'value': 'FY2', 'label': '202712'}, {'value': 'FY3', 'label': '202812'}], 'QUARTER': [{'value': 'FQ1', 'label': '202603'}, {'value': 'FQ2', 'label': '202606'}, {'value': 'FQ3', 'label': '202609'}]}
- detected_select_ids: ['selAccount1', 'selGsym']

## Consensus pandas.read_html tables

### Table 0
- shape: (0, 7)
- columns: ('추정기관', '추정기관'), ('추정일자', '추정일자'), ('적정주가', '적정주가'), ('적정주가', '직전 적정주가'), ('적정주가', '증감율'), ('투자의견', '투자의견'), ('투자의견', '직전 투자의견')

### Table 1
- shape: (0, 6)
- columns: 일자, 종목명 - 리포트 요약, 투자의견, 목표주가, 전일종가, 제공처/작성자

## Main pandas.read_html tables

### Table 0
- shape: (8, 4)
- columns: 0, 1, 2, 3

| 0 | 1 | 2 | 3 |
| --- | --- | --- | --- |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |

### Table 1
- shape: (1, 4)
- columns: 잠정실적발표일, 잠정실적(영업이익, 억원), 예상실적대비(%), 전년동기대비(%)

| 잠정실적발표일 | 잠정실적(영업이익, 억원) | 예상실적대비(%) | 전년동기대비(%) |
| --- | --- | --- | --- |
| 2026/02/27 | 140 | - | 31.26 |

### Table 2
- shape: (1, 5)
- columns: 운용사명, 보유수량, 시가평가액, 상장주식수내비중, 운용사내비중

| 운용사명 | 보유수량 | 시가평가액 | 상장주식수내비중 | 운용사내비중 |
| --- | --- | --- | --- | --- |
| 관련 데이터가 없습니다. | 관련 데이터가 없습니다. | 관련 데이터가 없습니다. | 관련 데이터가 없습니다. | 관련 데이터가 없습니다. |

### Table 3
- shape: (6, 4)
- columns: 항목, 보통주, 지분율, 최종변동일

| 항목 | 보통주 | 지분율 | 최종변동일 |
| --- | --- | --- | --- |
| 장수현(외 7인) | 5387915.0 | 41.3 | 2025/12/23 |
| 자사주 | 3389.0 | 0.03 | 2024/04/19 |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |

### Table 4
- shape: (6, 5)
- columns: 주주구분, 대표주주수, 보통주, 지분율, 최종변동일

| 주주구분 | 대표주주수 | 보통주 | 지분율 | 최종변동일 |
| --- | --- | --- | --- | --- |
| 최대주주등 (본인+특별관계자) | 1.0 | 5387915.0 | 41.3 | 2025/12/23 |
| 10%이상주주 (본인+특별관계자) |  |  |  |  |
| 5%이상주주 (본인+특별관계자) |  |  |  |  |
| 임원 (5%미만 중, 임원인자) |  |  |  |  |
| 자기주식 (자사주+자사주신탁) | 1.0 | 3389.0 | 0.03 | 2024/04/19 |

### Table 5
- shape: (1, 3)
- columns: KIS, KR, NICE

| KIS | KR | NICE |
| --- | --- | --- |
| 관련 데이터가 없습니다. | 관련 데이터가 없습니다. | 관련 데이터가 없습니다. |

### Table 6
- shape: (1, 3)
- columns: KIS, KR, NICE

| KIS | KR | NICE |
| --- | --- | --- |
| 관련 데이터가 없습니다. | 관련 데이터가 없습니다. | 관련 데이터가 없습니다. |

### Table 7
- shape: (1, 5)
- columns: 투자의견, 목표주가, EPS, PER, 추정기관수

| 투자의견 | 목표주가 | EPS | PER | 추정기관수 |
| --- | --- | --- | --- | --- |
| 관련 데이터가 없습니다. | 관련 데이터가 없습니다. | 관련 데이터가 없습니다. | 관련 데이터가 없습니다. | 관련 데이터가 없습니다. |

### Table 8
- shape: (9, 4)
- columns: 구분, 오파스넷, 코스닥 IT 서비스, KOSDAQ

| 구분 | 오파스넷 | 코스닥 IT 서비스 | KOSDAQ |
| --- | --- | --- | --- |
| 시가총액 | 994.0 | 407688.0 | 6311209.0 |
| 매출액 | 1929.0 | 284801.0 | 3315932.0 |
| 영업이익 | 107.0 | 6484.0 | 110431.0 |
| EPS(원) | 732.0 | 149.33 | 387.38 |
| PER | 11.54 | 554.92 | 200.48 |

### Table 9
- shape: (9, 4)
- columns: 구분, 오파스넷, 코스닥 IT 서비스, KOSDAQ

| 구분 | 오파스넷 | 코스닥 IT 서비스 | KOSDAQ |
| --- | --- | --- | --- |
| 시가총액 | 994.0 | 407688.0 | 6311209.0 |
| 매출액 | 1902.0 | 146634.0 | 1905357.0 |
| 영업이익 | 103.0 | 8819.0 | 74418.0 |
| EPS(원) | 714.0 | 1067.13 | 313.68 |
| PER | 11.81 | 77.66 | 247.58 |

### Table 10
- shape: (25, 9)
- columns: ('IFRS(연결)', 'IFRS(연결)'), ('Annual', '2022/12'), ('Annual', '2023/12'), ('Annual', '2024/12'), ('Annual', '2025/12(P)'), ('Net Quarter', '2025/03'), ('Net Quarter', '2025/06'), ('Net Quarter', '2025/09')

| ('IFRS(연결)', 'IFRS(연결)') | ('Annual', '2022/12') | ('Annual', '2023/12') | ('Annual', '2024/12') | ('Annual', '2025/12(P)') | ('Net Quarter', '2025/03') |
| --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |
|  |  |  |  |  |  |
|  |  |  |  |  |  |
|  |  |  |  |  |  |
|  |  |  |  |  |  |

### Table 11
- shape: (25, 9)
- columns: ('IFRS(연결)', 'IFRS(연결)'), ('Annual', '2020/12'), ('Annual', '2021/12'), ('Annual', '2022/12'), ('Annual', '2023/12'), ('Annual', '2024/12'), ('Annual', '2025/12(P)'), ('Annual', '2026/12(E)')

| ('IFRS(연결)', 'IFRS(연결)') | ('Annual', '2020/12') | ('Annual', '2021/12') | ('Annual', '2022/12') | ('Annual', '2023/12') | ('Annual', '2024/12') |
| --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |
|  |  |  |  |  |  |
|  |  |  |  |  |  |
|  |  |  |  |  |  |
|  |  |  |  |  |  |

### Table 12
- shape: (25, 9)
- columns: ('IFRS(연결)', 'IFRS(연결)'), ('Net Quarter', '2024/09'), ('Net Quarter', '2024/12'), ('Net Quarter', '2025/03'), ('Net Quarter', '2025/06'), ('Net Quarter', '2025/09'), ('Net Quarter', '2025/12(P)'), ('Net Quarter', '2026/03(E)')

| ('IFRS(연결)', 'IFRS(연결)') | ('Net Quarter', '2024/09') | ('Net Quarter', '2024/12') | ('Net Quarter', '2025/03') | ('Net Quarter', '2025/06') | ('Net Quarter', '2025/09') |
| --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |
|  |  |  |  |  |  |
|  |  |  |  |  |  |
|  |  |  |  |  |  |
|  |  |  |  |  |  |

### Table 13
- shape: (21, 9)
- columns: ('IFRS(별도)', 'IFRS(별도)'), ('Annual', '2022/12'), ('Annual', '2023/12'), ('Annual', '2024/12'), ('Annual', '2025/12(P)'), ('Net Quarter', '2025/03'), ('Net Quarter', '2025/06'), ('Net Quarter', '2025/09')

| ('IFRS(별도)', 'IFRS(별도)') | ('Annual', '2022/12') | ('Annual', '2023/12') | ('Annual', '2024/12') | ('Annual', '2025/12(P)') | ('Net Quarter', '2025/03') |
| --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |
|  |  |  |  |  |  |
|  |  |  |  |  |  |
|  |  |  |  |  |  |
|  |  |  |  |  |  |

### Table 14
- shape: (21, 9)
- columns: ('IFRS(별도)', 'IFRS(별도)'), ('Annual', '2020/12'), ('Annual', '2021/12'), ('Annual', '2022/12'), ('Annual', '2023/12'), ('Annual', '2024/12'), ('Annual', '2025/12(P)'), ('Annual', '2026/12(E)')

| ('IFRS(별도)', 'IFRS(별도)') | ('Annual', '2020/12') | ('Annual', '2021/12') | ('Annual', '2022/12') | ('Annual', '2023/12') | ('Annual', '2024/12') |
| --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |
|  |  |  |  |  |  |
|  |  |  |  |  |  |
|  |  |  |  |  |  |
|  |  |  |  |  |  |

### Table 15
- shape: (21, 9)
- columns: ('IFRS(별도)', 'IFRS(별도)'), ('Net Quarter', '2024/09'), ('Net Quarter', '2024/12'), ('Net Quarter', '2025/03'), ('Net Quarter', '2025/06'), ('Net Quarter', '2025/09'), ('Net Quarter', '2025/12(P)'), ('Net Quarter', '2026/03(E)')

| ('IFRS(별도)', 'IFRS(별도)') | ('Net Quarter', '2024/09') | ('Net Quarter', '2024/12') | ('Net Quarter', '2025/03') | ('Net Quarter', '2025/06') | ('Net Quarter', '2025/09') |
| --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |
|  |  |  |  |  |  |
|  |  |  |  |  |  |
|  |  |  |  |  |  |
|  |  |  |  |  |  |

### Table 16
- shape: (4, 2)
- columns: 헤더, 헤더.1

| 헤더 | 헤더.1 |
| --- | --- |
| 내용 | 내용 |
| 내용 | 내용 |
| 내용 | 내용 |
| 내용 | 내용 |

