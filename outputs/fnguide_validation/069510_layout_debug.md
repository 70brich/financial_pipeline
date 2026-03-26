# FnGuide layout debug

- company_name: 069510
- stock_code: 069510
- consensus_url: https://comp.fnguide.com/SVO2/ASP/SVD_Consensus.asp?pGB=1&gicode=A069510&cID=&MenuYn=Y&ReportGB=&NewMenuID=108&stkGb=701
- main_url: https://comp.fnguide.com/SVO2/ASP/SVD_Main.asp?pGB=1&gicode=A069510&cID=&MenuYn=Y&ReportGB=&NewMenuID=101&stkGb=701

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
- columns: 확정실적(영업이익, 억원), 예상실적(영업이익, 억원), 3개월전예상실적대비(%), 전년동기대비(%)

| 확정실적(영업이익, 억원) | 예상실적(영업이익, 억원) | 3개월전예상실적대비(%) | 전년동기대비(%) |
| --- | --- | --- | --- |
| 458 |  | - | 4.09 |

### Table 2
- shape: (3, 5)
- columns: 운용사명, 보유수량, 시가평가액, 상장주식수내비중, 운용사내비중

| 운용사명 | 보유수량 | 시가평가액 | 상장주식수내비중 | 운용사내비중 |
| --- | --- | --- | --- | --- |
| 브이아이피자산운용 | 54.86 | 7.99 | 0.5 | 0.08 |
| 마이다스에셋자산운용 | 4.42 | 0.64 | 0.04 | 0.0 |
| 에이치디씨자산운용 | 1.25 | 0.18 | 0.01 | 0.01 |

### Table 3
- shape: (6, 4)
- columns: 항목, 보통주, 지분율, 최종변동일

| 항목 | 보통주 | 지분율 | 최종변동일 |
| --- | --- | --- | --- |
| Foster Electric Co Ltd(외 1인) | 5392913.0 | 49.43 | 2023/10/24 |
| 자사주 | 2500000.0 | 22.91 | 2005/03/25 |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |

### Table 4
- shape: (6, 5)
- columns: 주주구분, 대표주주수, 보통주, 지분율, 최종변동일

| 주주구분 | 대표주주수 | 보통주 | 지분율 | 최종변동일 |
| --- | --- | --- | --- | --- |
| 최대주주등 (본인+특별관계자) | 1.0 | 5392913.0 | 49.43 | 2023/10/24 |
| 10%이상주주 (본인+특별관계자) |  |  |  |  |
| 5%이상주주 (본인+특별관계자) |  |  |  |  |
| 임원 (5%미만 중, 임원인자) | 1.0 | 4000.0 | 0.04 | 2018/10/30 |
| 자기주식 (자사주+자사주신탁) | 1.0 | 2500000.0 | 22.91 | 2005/03/25 |

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
- columns: 구분, 에스텍, 코스닥 전기·전자, KOSDAQ

| 구분 | 에스텍 | 코스닥 전기·전자 | KOSDAQ |
| --- | --- | --- | --- |
| 시가총액 | 1629.0 | 1242299.0 | 6311209.0 |
| 매출액 | 4682.0 | 587392.0 | 3315932.0 |
| 영업이익 | 458.0 | 8471.0 | 110431.0 |
| EPS(원) | 3815.0 | -218.02 | 387.38 |
| PER | 3.82 |  | 200.48 |

### Table 9
- shape: (9, 4)
- columns: 구분, 에스텍, 코스닥 전기·전자, KOSDAQ

| 구분 | 에스텍 | 코스닥 전기·전자 | KOSDAQ |
| --- | --- | --- | --- |
| 시가총액 | 1629.0 | 1242299.0 | 6311209.0 |
| 매출액 | 3169.0 | 337577.0 | 1905357.0 |
| 영업이익 | 68.0 | 3558.0 | 74418.0 |
| EPS(원) | 1145.0 | 146.91 | 313.68 |
| PER | 12.72 | 555.57 | 247.58 |

### Table 10
- shape: (25, 9)
- columns: ('IFRS(연결)', 'IFRS(연결)'), ('Annual', '2023/12'), ('Annual', '2024/12'), ('Annual', '2025/12'), ('Annual', '2026/12(E)'), ('Net Quarter', '2025/06'), ('Net Quarter', '2025/09'), ('Net Quarter', '2025/12')

| ('IFRS(연결)', 'IFRS(연결)') | ('Annual', '2023/12') | ('Annual', '2024/12') | ('Annual', '2025/12') | ('Annual', '2026/12(E)') | ('Net Quarter', '2025/06') |
| --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |
|  |  |  |  |  |  |
|  |  |  |  |  |  |
|  |  |  |  |  |  |
|  |  |  |  |  |  |

### Table 11
- shape: (25, 9)
- columns: ('IFRS(연결)', 'IFRS(연결)'), ('Annual', '2021/12'), ('Annual', '2022/12'), ('Annual', '2023/12'), ('Annual', '2024/12'), ('Annual', '2025/12'), ('Annual', '2026/12(E)'), ('Annual', '2027/12(E)')

| ('IFRS(연결)', 'IFRS(연결)') | ('Annual', '2021/12') | ('Annual', '2022/12') | ('Annual', '2023/12') | ('Annual', '2024/12') | ('Annual', '2025/12') |
| --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |
|  |  |  |  |  |  |
|  |  |  |  |  |  |
|  |  |  |  |  |  |
|  |  |  |  |  |  |

### Table 12
- shape: (25, 9)
- columns: ('IFRS(연결)', 'IFRS(연결)'), ('Net Quarter', '2024/12'), ('Net Quarter', '2025/03'), ('Net Quarter', '2025/06'), ('Net Quarter', '2025/09'), ('Net Quarter', '2025/12'), ('Net Quarter', '2026/03(E)'), ('Net Quarter', '2026/06(E)')

| ('IFRS(연결)', 'IFRS(연결)') | ('Net Quarter', '2024/12') | ('Net Quarter', '2025/03') | ('Net Quarter', '2025/06') | ('Net Quarter', '2025/09') | ('Net Quarter', '2025/12') |
| --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |
|  |  |  |  |  |  |
|  |  |  |  |  |  |
|  |  |  |  |  |  |
|  |  |  |  |  |  |

### Table 13
- shape: (21, 9)
- columns: ('IFRS(별도)', 'IFRS(별도)'), ('Annual', '2023/12'), ('Annual', '2024/12'), ('Annual', '2025/12'), ('Annual', '2026/12(E)'), ('Net Quarter', '2025/06'), ('Net Quarter', '2025/09'), ('Net Quarter', '2025/12')

| ('IFRS(별도)', 'IFRS(별도)') | ('Annual', '2023/12') | ('Annual', '2024/12') | ('Annual', '2025/12') | ('Annual', '2026/12(E)') | ('Net Quarter', '2025/06') |
| --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |
|  |  |  |  |  |  |
|  |  |  |  |  |  |
|  |  |  |  |  |  |
|  |  |  |  |  |  |

### Table 14
- shape: (21, 9)
- columns: ('IFRS(별도)', 'IFRS(별도)'), ('Annual', '2021/12'), ('Annual', '2022/12'), ('Annual', '2023/12'), ('Annual', '2024/12'), ('Annual', '2025/12'), ('Annual', '2026/12(E)'), ('Annual', '2027/12(E)')

| ('IFRS(별도)', 'IFRS(별도)') | ('Annual', '2021/12') | ('Annual', '2022/12') | ('Annual', '2023/12') | ('Annual', '2024/12') | ('Annual', '2025/12') |
| --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |
|  |  |  |  |  |  |
|  |  |  |  |  |  |
|  |  |  |  |  |  |
|  |  |  |  |  |  |

### Table 15
- shape: (21, 9)
- columns: ('IFRS(별도)', 'IFRS(별도)'), ('Net Quarter', '2024/12'), ('Net Quarter', '2025/03'), ('Net Quarter', '2025/06'), ('Net Quarter', '2025/09'), ('Net Quarter', '2025/12'), ('Net Quarter', '2026/03(E)'), ('Net Quarter', '2026/06(E)')

| ('IFRS(별도)', 'IFRS(별도)') | ('Net Quarter', '2024/12') | ('Net Quarter', '2025/03') | ('Net Quarter', '2025/06') | ('Net Quarter', '2025/09') | ('Net Quarter', '2025/12') |
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

