# FnGuide DB check

## Row counts
| table_name | row_count |
| --- | --- |
| fnguide_observation | 200 |
| broker_target_price | 0 |
| broker_report_summary | 0 |
| company_shareholder_snapshot | 7 |
| company_business_summary | 1 |
| fnguide_fetch_log | 18 |

## fnguide_observation sample
| raw_metric_name | period_label_raw | value_text | value_numeric | block_type | ifrs_scope | period_scope |
| --- | --- | --- | --- | --- | --- | --- |
| 매출액 | 2022/12 | 136.39 | 136.39 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 매출액 | 2023/12 | 177.61 | 177.61 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 매출액 | 2024/12 | 203.01 | 203.01 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 매출액 | 2025/12(P) | 360 | 360 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2022/12 | 46.06 | 46.06 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2023/12 | 30.22 | 30.22 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2024/12 | 14.30 | 14.3 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2025/12(P) | 77.23 | 77.23 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 컨센서스대비 | 2023/12 | 3.87 | 3.87 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 컨센서스대비 | 2025/12(P) | 5.36 | 5.36 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 영업이익 | 2022/12 | -65.95 | -65.95 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 영업이익 | 2023/12 | -50.94 | -50.94 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 영업이익 | 2024/12 | -3.96 | -3.96 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 영업이익 | 2025/12(P) | 62 | 62 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2022/12 | 적지 | None | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2023/12 | 적지 | None | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2024/12 | 적지 | None | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2025/12(P) | 흑전 | None | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 컨센서스대비 | 2023/12 | 적지 | None | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 컨센서스대비 | 2025/12(P) | -12.09 | -12.09 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 당기순이익 | 2022/12 | -58.68 | -58.68 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 당기순이익 | 2023/12 | -67.93 | -67.93 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 당기순이익 | 2024/12 | 8.09 | 8.09 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 당기순이익 | 2025/12(P) | 65 | 65 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2022/12 | 적지 | None | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2023/12 | 적지 | None | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2024/12 | 흑전 | None | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2025/12(P) | 697.53 | 697.53 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 컨센서스대비 | 2023/12 | 적지 | None | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 컨센서스대비 | 2025/12(P) | -8.48 | -8.48 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |

## broker_target_price sample
_No rows_

## broker_report_summary sample
_No rows_

## company_shareholder_snapshot sample
| holder_name | holder_type | shares | ownership_pct | as_of_date |
| --- | --- | --- | --- | --- |
| 이정수(외 2인) | holder_detail | 5170329 | 31.32 | 2025/06/24 |
| 최대주주등 (본인+특별관계자) | shareholder_group | 5170329 | 31.32 | 2025/06/24 |
| 10%이상주주 (본인+특별관계자) | shareholder_group | None | None | None |
| 5%이상주주 (본인+특별관계자) | shareholder_group | None | None | None |
| 임원 (5%미만 중, 임원인자) | shareholder_group | 4000 | 0.02 | 2025/12/08 |
| 자기주식 (자사주+자사주신탁) | shareholder_group | None | None | None |
| 우리사주조합 | shareholder_group | None | None | None |
