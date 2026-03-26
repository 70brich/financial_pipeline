# FnGuide DB check

## Row counts
| table_name | row_count |
| --- | --- |
| fnguide_observation | 188 |
| broker_target_price | 0 |
| broker_report_summary | 0 |
| company_shareholder_snapshot | 8 |
| company_business_summary | 1 |
| fnguide_fetch_log | 18 |

## fnguide_observation sample
| raw_metric_name | period_label_raw | value_text | value_numeric | block_type | ifrs_scope | period_scope |
| --- | --- | --- | --- | --- | --- | --- |
| 매출액 | 2023/12 | 4,145.94 | 4145.94 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 매출액 | 2024/12 | 5,093.74 | 5093.74 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 매출액 | 2025/12 | 4,681.92 | 4681.92 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2023/12 | -11.50 | -11.5 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2024/12 | 22.86 | 22.86 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2025/12 | -8.08 | -8.08 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 영업이익 | 2023/12 | 245.55 | 245.55 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 영업이익 | 2024/12 | 439.82 | 439.82 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 영업이익 | 2025/12 | 458.16 | 458.16 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2023/12 | 181.53 | 181.53 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2024/12 | 79.12 | 79.12 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2025/12 | 4.17 | 4.17 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 당기순이익 | 2023/12 | 216.60 | 216.6 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 당기순이익 | 2024/12 | 462.67 | 462.67 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 당기순이익 | 2025/12 | 416.23 | 416.23 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2023/12 | 127.14 | 127.14 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2024/12 | 113.61 | 113.61 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2025/12 | -10.04 | -10.04 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 지배주주순이익 | 2023/12 | 216.60 | 216.6 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 지배주주순이익 | 2024/12 | 462.67 | 462.67 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 지배주주순이익 | 2025/12 | 416.23 | 416.23 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 자산총계 | 2023/12 | 2,677.72 | 2677.72 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 자산총계 | 2024/12 | 3,879.62 | 3879.62 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 자산총계 | 2025/12 | 3,452.72 | 3452.72 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 부채총계 | 2023/12 | 1,119.97 | 1119.97 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 부채총계 | 2024/12 | 1,844.52 | 1844.52 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 부채총계 | 2025/12 | 1,102.79 | 1102.79 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 자본총계 | 2023/12 | 1,557.75 | 1557.75 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 자본총계 | 2024/12 | 2,035.09 | 2035.09 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 자본총계 | 2025/12 | 2,349.93 | 2349.93 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |

## broker_target_price sample
_No rows_

## broker_report_summary sample
_No rows_

## company_shareholder_snapshot sample
| holder_name | holder_type | shares | ownership_pct | as_of_date |
| --- | --- | --- | --- | --- |
| Foster Electric Co Ltd(외 1인) | holder_detail | 5392913 | 49.43 | 2023/10/24 |
| 자사주 | holder_detail | 2500000 | 22.91 | 2005/03/25 |
| 최대주주등 (본인+특별관계자) | shareholder_group | 5392913 | 49.43 | 2023/10/24 |
| 10%이상주주 (본인+특별관계자) | shareholder_group | None | None | None |
| 5%이상주주 (본인+특별관계자) | shareholder_group | None | None | None |
| 임원 (5%미만 중, 임원인자) | shareholder_group | 4000 | 0.04 | 2018/10/30 |
| 자기주식 (자사주+자사주신탁) | shareholder_group | 2500000 | 22.91 | 2005/03/25 |
| 우리사주조합 | shareholder_group | None | None | None |
