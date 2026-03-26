# FnGuide DB check

## Row counts
| table_name | row_count |
| --- | --- |
| fnguide_observation | 207 |
| broker_target_price | 0 |
| broker_report_summary | 0 |
| company_shareholder_snapshot | 8 |
| company_business_summary | 1 |
| fnguide_fetch_log | 18 |

## fnguide_observation sample
| raw_metric_name | period_label_raw | value_text | value_numeric | block_type | ifrs_scope | period_scope |
| --- | --- | --- | --- | --- | --- | --- |
| 매출액 | 2022/12 | 1,705.85 | 1705.85 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 매출액 | 2023/12 | 2,249.81 | 2249.81 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 매출액 | 2024/12 | 1,928.85 | 1928.85 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 매출액 | 2025/12(P) | 2,333 | 2333 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2022/12 | 40.10 | 40.1 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2023/12 | 31.89 | 31.89 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2024/12 | -14.27 | -14.27 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2025/12(P) | 20.95 | 20.95 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 영업이익 | 2022/12 | 85.24 | 85.24 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 영업이익 | 2023/12 | 139.51 | 139.51 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 영업이익 | 2024/12 | 106.52 | 106.52 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 영업이익 | 2025/12(P) | 140 | 140 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2022/12 | 47.04 | 47.04 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2023/12 | 63.67 | 63.67 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2024/12 | -23.65 | -23.65 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2025/12(P) | 31.85 | 31.85 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 당기순이익 | 2022/12 | 60.69 | 60.69 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 당기순이익 | 2023/12 | 104.60 | 104.6 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 당기순이익 | 2024/12 | 96.47 | 96.47 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 당기순이익 | 2025/12(P) | 120 | 120 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2022/12 | -2.60 | -2.6 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2023/12 | 72.35 | 72.35 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2024/12 | -7.77 | -7.77 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 전년동기대비 | 2025/12(P) | 24.55 | 24.55 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 지배주주순이익 | 2022/12 | 60.69 | 60.69 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 지배주주순이익 | 2023/12 | 104.54 | 104.54 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 지배주주순이익 | 2024/12 | 95.45 | 95.45 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 비지배주주순이익 | 2023/12 | 0.06 | 0.06 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 비지배주주순이익 | 2024/12 | 1.02 | 1.02 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |
| 자산총계 | 2022/12 | 1,192.91 | 1192.91 | CONSENSUS_FINANCIAL | CONNECTED | YEAR |

## broker_target_price sample
_No rows_

## broker_report_summary sample
_No rows_

## company_shareholder_snapshot sample
| holder_name | holder_type | shares | ownership_pct | as_of_date |
| --- | --- | --- | --- | --- |
| 장수현(외 7인) | holder_detail | 5387915 | 41.3 | 2025/12/23 |
| 자사주 | holder_detail | 3389 | 0.03 | 2024/04/19 |
| 최대주주등 (본인+특별관계자) | shareholder_group | 5387915 | 41.3 | 2025/12/23 |
| 10%이상주주 (본인+특별관계자) | shareholder_group | None | None | None |
| 5%이상주주 (본인+특별관계자) | shareholder_group | None | None | None |
| 임원 (5%미만 중, 임원인자) | shareholder_group | None | None | None |
| 자기주식 (자사주+자사주신탁) | shareholder_group | 3389 | 0.03 | 2024/04/19 |
| 우리사주조합 | shareholder_group | None | None | None |
