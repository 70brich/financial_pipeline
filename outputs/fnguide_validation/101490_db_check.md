# FnGuide DB check

## Row counts
| table_name | row_count |
| --- | --- |
| fnguide_observation | 281 |
| broker_target_price | 0 |
| broker_report_summary | 1 |
| company_shareholder_snapshot | 11 |
| company_business_summary | 1 |
| fnguide_fetch_log | 18 |

## fnguide_observation sample
| raw_metric_name | period_label_raw | value_text | value_numeric | block_type | ifrs_scope | period_scope |
| --- | --- | --- | --- | --- | --- | --- |
| 매출액 | 2023/12 | 1,503.20 | 1503.2 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 매출액 | 2024/12 | 1,760.14 | 1760.14 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 매출액 | 2025/12 | 2,437.33 | 2437.33 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2023/12 | 21.71 | 21.71 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2024/12 | 17.09 | 17.09 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2025/12 | 38.47 | 38.47 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 컨센서스대비 | 2023/12 | 3.31 | 3.31 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 영업이익 | 2023/12 | 250.39 | 250.39 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 영업이익 | 2024/12 | 294.79 | 294.79 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 영업이익 | 2025/12 | 503.90 | 503.9 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2023/12 | 56.37 | 56.37 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2024/12 | 17.73 | 17.73 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2025/12 | 70.94 | 70.94 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 컨센서스대비 | 2023/12 | 2.20 | 2.2 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 당기순이익 | 2023/12 | 258.55 | 258.55 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 당기순이익 | 2024/12 | 303.14 | 303.14 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 당기순이익 | 2025/12 | 580.93 | 580.93 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2023/12 | 48.05 | 48.05 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2024/12 | 17.25 | 17.25 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2025/12 | 91.64 | 91.64 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 컨센서스대비 | 2023/12 | 1.39 | 1.39 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 지배주주순이익 | 2023/12 | 258.55 | 258.55 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 지배주주순이익 | 2024/12 | 304.80 | 304.8 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 지배주주순이익 | 2025/12 | 582.59 | 582.59 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 비지배주주순이익 | 2024/12 | -1.66 | -1.66 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 비지배주주순이익 | 2025/12 | -1.66 | -1.66 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 자산총계 | 2023/12 | 2,567.59 | 2567.59 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 자산총계 | 2024/12 | 2,970.32 | 2970.32 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 자산총계 | 2025/12 | 3,930.42 | 3930.42 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 부채총계 | 2023/12 | 359.60 | 359.6 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |

## broker_target_price sample
_No rows_

## broker_report_summary sample
| report_date | report_title | provider_name | analyst_name | rating_text |
| --- | --- | --- | --- | --- |
| 2026/03/23 | 에스앤에스텍-국내 유일의 블랭크마스크 전문 기업. 공정 국산화의 최전선 파트너 | 그로쓰리서치 | 한용희 외2 | None |

## company_shareholder_snapshot sample
| holder_name | holder_type | shares | ownership_pct | as_of_date |
| --- | --- | --- | --- | --- |
| 정수홍(외 5인) | holder_detail | 4684160 | 21.96 | 2026/01/28 |
| 삼성자산운용 | holder_detail | 1788452 | 8.38 | 2026/02/05 |
| 삼성전자 | holder_detail | 1716116 | 8.04 | 2020/08/31 |
| 국민연금공단 | holder_detail | 1077057 | 5.05 | 2025/09/12 |
| 자사주 | holder_detail | 505275 | 2.37 | 2025/12/01 |
| 최대주주등 (본인+특별관계자) | shareholder_group | 4684160 | 21.96 | 2026/01/28 |
| 10%이상주주 (본인+특별관계자) | shareholder_group | None | None | None |
| 5%이상주주 (본인+특별관계자) | shareholder_group | 4581625 | 21.47 | 2026/02/05 |
| 임원 (5%미만 중, 임원인자) | shareholder_group | 32530 | 0.15 | 2026/01/28 |
| 자기주식 (자사주+자사주신탁) | shareholder_group | 505275 | 2.37 | 2025/12/01 |
| 우리사주조합 | shareholder_group | None | None | None |
