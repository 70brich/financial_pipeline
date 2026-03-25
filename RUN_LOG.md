# Run Log

## 2026-03-25

### Latest verified result
- User-side local verification after the conservative growth-rate batch succeeded:
  - tests: `23` passed
  - distinct coverage: `103 / 154 = 66.88%`
  - row-level coverage: `2077 / 2432 = 85.40%`
  - `REVENUE_GROWTH_RATE`: `44` rows
  - `SGA_GROWTH_RATE`: `28` rows
  - `OPERATING_INCOME_GROWTH_RATE`: `40` rows
  - `BPS_GROWTH_RATE`: `10` rows
  - `EPS_GROWTH_RATE`: `10` rows
  - `FCF_GROWTH_RATE`: `10` rows
  - `NPM_GROWTH_RATE`: `10` rows
  - `OPM_GROWTH_RATE`: `10` rows
  - `ROA_GROWTH_RATE`: `10` rows
  - `ROE_GROWTH_RATE`: `10` rows
  - `CAPEX_GROWTH_RATE`: `10` rows
  - `OPERATING_CASHFLOW_GROWTH_RATE`: `10` rows
  - `EQUITY_GROWTH_RATE`: `10` rows
  - `ASSET_GROWTH_RATE`: `10` rows

### Recent changes
- Updated [python/etl/metric_mapping.py](C:\Users\slpar\OneDrive\문서\CODEX\python\etl\metric_mapping.py)
  - added exact aliases for the approved conservative growth-rate family
  - preserved exact-alias-only policy
  - preserved lookup-only stripping for leading cosmetic prefixes `-`, `+`, `=`
  - intentionally left growth-like but policy-risk metrics unmapped:
    - `지배주주EPS증가율`
    - `지배순익 증가율(%)`
    - `주식수증가율(%)`
- Updated [tests/test_metric_mapping.py](C:\Users\slpar\OneDrive\문서\CODEX\tests\test_metric_mapping.py)
  - added coverage for the approved growth-rate mappings
  - kept still-deferred families unmapped in tests
- Updated [python/etl/inspect_standard_metric_mapping.py](C:\Users\slpar\OneDrive\문서\CODEX\python\etl\inspect_standard_metric_mapping.py)
  - added `Choice 2 growth-rate row counts`

### Commands attempted in Codex environment
- `py -3 -m unittest tests.test_metric_mapping`
- `py -3 -m python.etl.run_standard_metric_mapping`
- `py -3 -m python.etl.inspect_standard_metric_mapping`
- `Get-Command python -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Source`
- `Get-Command py -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Source`

### Important environment note
- This Codex environment does not expose `py` or `python` on `PATH`.
- Verification therefore depends on user-side local runs.

### Next action
- Coverage targets have now been exceeded.
- Remaining high-volume unmapped metrics sit in explicitly deferred policy families.
- The next move should be another narrow policy decision, not autonomous taxonomy expansion.
