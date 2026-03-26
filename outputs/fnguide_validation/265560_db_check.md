# FnGuide DB check

## Row counts
| table_name | row_count |
| --- | --- |
| fnguide_observation | 203 |
| broker_target_price | 0 |
| broker_report_summary | 0 |
| company_shareholder_snapshot | 8 |
| company_business_summary | 1 |
| fnguide_fetch_log | 18 |

## fnguide_observation sample
| raw_metric_name | period_label_raw | value_text | value_numeric | block_type | ifrs_scope | period_scope |
| --- | --- | --- | --- | --- | --- | --- |
| 매출액 | 2022/12 | 479.45 | 479.45 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 매출액 | 2023/12 | 649.20 | 649.2 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 매출액 | 2024/12 | 948.27 | 948.27 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 매출액 | 2025/12(P) | 1,086 | 1086 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2022/12 | 18.02 | 18.02 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2023/12 | 35.41 | 35.41 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2024/12 | 46.07 | 46.07 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2025/12(P) | 14.53 | 14.53 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 영업이익 | 2022/12 | 19.06 | 19.06 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 영업이익 | 2023/12 | 50.14 | 50.14 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 영업이익 | 2024/12 | 153.88 | 153.88 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 영업이익 | 2025/12(P) | 180 | 180 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2022/12 | -17.84 | -17.84 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2023/12 | 163.06 | 163.06 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2024/12 | 206.90 | 206.9 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2025/12(P) | 16.73 | 16.73 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 당기순이익 | 2022/12 | 48.25 | 48.25 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 당기순이익 | 2023/12 | 60.98 | 60.98 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 당기순이익 | 2024/12 | 140.23 | 140.23 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 당기순이익 | 2025/12(P) | 190 | 190 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2022/12 | 88.92 | 88.92 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2023/12 | 26.38 | 26.38 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2024/12 | 129.96 | 129.96 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2025/12(P) | 35.81 | 35.81 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 지배주주순이익 | 2022/12 | 48.25 | 48.25 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 지배주주순이익 | 2023/12 | 60.98 | 60.98 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 지배주주순이익 | 2024/12 | 140.23 | 140.23 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 자산총계 | 2022/12 | 813.05 | 813.05 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 자산총계 | 2023/12 | 864.01 | 864.01 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 자산총계 | 2024/12 | 1,070.72 | 1070.72 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |

## broker_target_price sample
_No rows_

## broker_report_summary sample
_No rows_

## company_shareholder_snapshot sample
| holder_name | holder_type | shares | ownership_pct | as_of_date |
| --- | --- | --- | --- | --- |
| 엄준형(외 5인) | holder_detail | 5253468 | 49.14 | 2021/06/03 |
| 한국단자공업 | holder_detail | 990000 | 9.26 | 2021/06/03 |
| 최대주주등 (본인+특별관계자) | shareholder_group | 5253468 | 49.14 | 2021/06/03 |
| 10%이상주주 (본인+특별관계자) | shareholder_group | None | None | None |
| 5%이상주주 (본인+특별관계자) | shareholder_group | 990000 | 9.26 | 2021/06/03 |
| 임원 (5%미만 중, 임원인자) | shareholder_group | 8600 | 0.08 | 2021/09/10 |
| 자기주식 (자사주+자사주신탁) | shareholder_group | None | None | None |
| 우리사주조합 | shareholder_group | 135798 | 1.27 | 2021/06/03 |
