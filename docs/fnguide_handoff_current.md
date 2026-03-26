# FnGuide Handoff Current

## Current verified state

- Samsung Electronics (`005930`) remains the original validation baseline.
- The full local operating-company universe has now been checked once.
- Current controlled checkpoint size: `14` companies

## Operating rule

- Do not optimize for bypassing blocks.
- Follow site policy.
- Keep the collection low-rate and sequential.
- Stop immediately and record if abnormal responses or block signs appear.
- Leave validation outputs and document updates at each checkpoint.

## 14-company result summary

- blocked or abnormal response detected: `NO`
- all six required blocks present:
  - `9 / 14` companies
- stable all-block additions in later rounds:
  - `하이브 (352820)`
- source-side sparse companies:
  - `에스앤에스텍 (101490)`: missing `broker_target`
  - `플리토 (300080)`: missing `consensus_revision`, `broker_target`,
    `report_summary`
  - `오파스넷 (173130)`: missing `consensus_revision`, `broker_target`,
    `report_summary`
  - `에스텍 (069510)`: missing `consensus_revision`, `broker_target`,
    `report_summary`
  - `영화테크 (265560)`: missing `consensus_revision`, `broker_target`,
    `report_summary`

## Final local-universe additions

- `에스텍 (069510)`: `188 / 188 / 0 / 0 / 0 / 8 / 1`
- `영화테크 (265560)`: `203 / 203 / 0 / 0 / 0 / 8 / 1`

## Important notes

- The full local universe is now classified into:
  - stable all-block companies
  - source-side sparse companies
- `에스텍` and `영화테크` completed fetch logging cleanly but only returned
  `consensus_financial`, `shareholder_snapshot`, and `business_summary`.
- Continue using explicit `company_name:stock_code` input for any future reruns.
- Validation artifacts are company-scoped under `outputs/fnguide_validation/`.

## Key artifacts

- `outputs/fnguide_validation/fnguide_controlled_batch_validation.md`
- `outputs/fnguide_validation/fnguide_company_counts.csv`
- `outputs/fnguide_validation/fnguide_metrics_coverage.csv`
- `outputs/fnguide_validation/fnguide_timeseries_sample.csv`
- `outputs/fnguide_validation/069510_validation_report.md`
- `outputs/fnguide_validation/265560_validation_report.md`
- `outputs/fnguide_validation/069510_db_check.md`
- `outputs/fnguide_validation/265560_db_check.md`

## Next step

- Collection expansion from the current local universe is complete.
- The next logical work is not more crawling, but classification and usage:
  - separate stable all-block companies from sparse companies in docs/reports
  - decide whether sparse companies should remain in the collection allowlist
    for recurring refreshes
  - design downstream usage rules for partial FnGuide coverage

## Reference commands

```powershell
py -3 -m python.etl.debug_fnguide_layout `
  --stock-code 069510

py -3 -m python.etl.debug_fnguide_layout `
  --stock-code 265560

py -3 -m python.etl.run_fnguide_parser `
  --company 에스텍:A069510 `
  --company 영화테크:A265560

py -3 -m python.etl.inspect_fnguide_load `
  --stock-code 069510

py -3 -m python.etl.inspect_fnguide_load `
  --stock-code 265560

py -3 -m python.etl.build_fnguide_controlled_batch_reports
```

## Policy closeout addendum

Current operating classification:

- stable all-block cohort:
  - `고려아연 (010130)`
  - `롯데케미칼 (011170)`
  - `삼성전기 (009150)`
  - `삼성중공업 (010140)`
  - `HD현대 (267250)`
  - `산일전기 (062040)`
  - `씨에스윈드 (112610)`
  - `씨어스테크놀로지 (458870)`
  - `하이브 (352820)`
- source-side sparse cohort:
  - `에스앤에스텍 (101490)`
  - `플리토 (300080)`
  - `오파스넷 (173130)`
  - `에스텍 (069510)`
  - `영화테크 (265560)`

Interpretation rule:

- if fetch logs complete and no blocked or abnormal response is observed,
  missing blocks are treated as source-side sparse success rather than
  technical failure

Recurring refresh draft:

- default allowlist: stable all-block cohort
- partial-coverage cohort: keep in monitored collection history and use only in
  downstream paths that tolerate missing blocks

Current git note:

- the working tree is still dirty with broader local DB, input, output, and
  scratch-file changes
- the policy closeout docs should be committed only as a curated subset, not as
  an all-files commit
