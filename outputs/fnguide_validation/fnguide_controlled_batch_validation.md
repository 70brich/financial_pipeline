# FnGuide controlled batch validation

## Scope
- Single-company validation target: 고려아연 (010130)
- Controlled batch targets: 고려아연 (010130), 롯데케미칼 (011170), 삼성전기 (009150), 삼성중공업 (010140), HD현대 (267250), 산일전기 (062040), 씨에스윈드 (112610), 에스앤에스텍 (101490), 씨어스테크놀로지 (458870), 플리토 (300080), 하이브 (352820), 오파스넷 (173130), 에스텍 (069510), 영화테크 (265560)

## Result
- 고려아연 single-company validation success: YES
- 14-company controlled checkpoint all-block success: NO
- blocked or abnormal response detected: NO
- next controlled expansion readiness: YES

## Per-company block counts
| company_name | stock_code | financial | revision | broker_target | report_summary | shareholder | business_summary | fetch_logs |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 고려아연 | 010130 | 326 | 341 | 6 | 2 | 12 | 1 | 18 |
| 롯데케미칼 | 011170 | 292 | 235 | 17 | 4 | 9 | 1 | 18 |
| 삼성전기 | 009150 | 290 | 276 | 23 | 17 | 10 | 1 | 18 |
| 삼성중공업 | 010140 | 281 | 295 | 23 | 1 | 9 | 1 | 18 |
| HD현대 | 267250 | 303 | 308 | 5 | 3 | 9 | 1 | 18 |
| 산일전기 | 062040 | 318 | 353 | 10 | 5 | 9 | 1 | 18 |
| 씨에스윈드 | 112610 | 271 | 245 | 9 | 3 | 9 | 1 | 18 |
| 에스앤에스텍 | 101490 | 202 | 79 | 0 | 1 | 11 | 1 | 18 |
| 씨어스테크놀로지 | 458870 | 267 | 294 | 8 | 2 | 8 | 1 | 18 |
| 플리토 | 300080 | 200 | 0 | 0 | 0 | 7 | 1 | 18 |
| 하이브 | 352820 | 290 | 260 | 23 | 16 | 9 | 1 | 18 |
| 오파스넷 | 173130 | 207 | 0 | 0 | 0 | 8 | 1 | 18 |
| 에스텍 | 069510 | 188 | 0 | 0 | 0 | 8 | 1 | 18 |
| 영화테크 | 265560 | 203 | 0 | 0 | 0 | 8 | 1 | 18 |

## Missing or zero-count blocks
- 고려아연 (010130): none
- 롯데케미칼 (011170): none
- 삼성전기 (009150): none
- 삼성중공업 (010140): none
- HD현대 (267250): none
- 산일전기 (062040): none
- 씨에스윈드 (112610): none
- 에스앤에스텍 (101490): broker_target
- 씨어스테크놀로지 (458870): none
- 플리토 (300080): consensus_revision, broker_target, report_summary
- 하이브 (352820): none
- 오파스넷 (173130): consensus_revision, broker_target, report_summary
- 에스텍 (069510): consensus_revision, broker_target, report_summary
- 영화테크 (265560): consensus_revision, broker_target, report_summary

## Sparse but non-zero rows
- 고려아연 (010130): broker_target null target/rating rows = 3
- 산일전기 (062040): broker_target null target/rating rows = 1
- 씨어스테크놀로지 (458870): broker_target null target/rating rows = 3

## Notes
- 9 of 14 companies produced all six required blocks.
- No blocked or abnormal response was observed in this batch.
- Collection remained low-rate and sequential.
- Some companies returned source-side sparse coverage even though fetches completed:
  - 에스앤에스텍 (101490): missing broker_target
  - 플리토 (300080): missing consensus_revision, broker_target, report_summary
  - 오파스넷 (173130): missing consensus_revision, broker_target, report_summary
  - 에스텍 (069510): missing consensus_revision, broker_target, report_summary
  - 영화테크 (265560): missing consensus_revision, broker_target, report_summary

## Commands used
```powershell
py -3 -m python.etl.debug_fnguide_layout `
  --stock-code 062040

py -3 -m python.etl.debug_fnguide_layout `
  --stock-code 112610

py -3 -m python.etl.debug_fnguide_layout `
  --stock-code 101490

py -3 -m python.etl.debug_fnguide_layout `
  --stock-code 458870

py -3 -m python.etl.debug_fnguide_layout `
  --stock-code 300080

py -3 -m python.etl.run_fnguide_parser `
  --company 산일전기:A062040 `
  --company 씨에스윈드:A112610 `
  --company 에스앤에스텍:A101490 `
  --company 씨어스테크놀로지:A458870 `
  --company 플리토:A300080 `
  --company 하이브:A352820 `
  --company 오파스넷:A173130 `
  --company 에스텍:A069510 `
  --company 영화테크:A265560

py -3 -m python.etl.inspect_fnguide_load `
  --stock-code 062040

py -3 -m python.etl.inspect_fnguide_load `
  --stock-code 112610

py -3 -m python.etl.inspect_fnguide_load `
  --stock-code 101490

py -3 -m python.etl.inspect_fnguide_load `
  --stock-code 458870

py -3 -m python.etl.inspect_fnguide_load `
  --stock-code 300080

py -3 -m python.etl.inspect_fnguide_load `
  --stock-code 352820

py -3 -m python.etl.inspect_fnguide_load `
  --stock-code 173130

py -3 -m python.etl.inspect_fnguide_load `
  --stock-code 069510

py -3 -m python.etl.inspect_fnguide_load `
  --stock-code 265560

py -3 -m python.etl.build_fnguide_controlled_batch_reports
```
