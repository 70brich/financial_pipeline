# Data rules

## Source priority
Integrated selection must allow:
1. confirmed value first (is_estimate = 0)
2. source priority next
3. estimate fallback only if no confirmed value exists

## Metric normalization
Examples:
- 영업이익률 -> operating_margin
- OPM(%) -> operating_margin

## Company code normalization
- QDATA stock code removes leading A
- normalized stock code should be 6 digits
- if missing, resolve from official source workflow later

## Period normalization
- KDATA1 -> QUARTER
- KDATA2 -> YEAR
- QDATA overview -> SNAPSHOT
- QDATA yearly -> YEAR
- QDATA quarterly -> QUARTER
- annualized labels preserved separately
