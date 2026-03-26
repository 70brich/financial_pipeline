# Derived metrics v1

## Purpose

This document describes the first derived-metric layer built on top of
`company_metric_timeseries`.

The goal is to provide a small set of immediately useful analysis metrics for
Python and pandas workflows without changing the validated source layers.

## Why a view-first approach was chosen

The project starts with a SQLite view because:

- the underlying analysis layer is already validated
- derived calculations are deterministic and rebuild-free
- null handling can stay transparent
- future derived families can be added without mutating raw, integrated, or
  enriched records

## View name

- `company_metric_derived_v1`

## Implemented derived metrics

- `REVENUE_YOY`
- `OPERATING_INCOME_YOY`
- `NET_INCOME_YOY`
- `EPS_YOY`
- `REVENUE_QOQ`
- `OPERATING_INCOME_QOQ`
- `NET_INCOME_QOQ`
- `EPS_QOQ`
- `OPERATING_MARGIN`
- `NET_MARGIN`

## Verified baseline

Latest user-side local verification confirmed:

- `company_metric_derived_v1`: `440` rows
- metric row counts:
  - `EPS_YOY`: `49`
  - `NET_INCOME_YOY`: `49`
  - `NET_MARGIN`: `49`
  - `OPERATING_MARGIN`: `47`
  - `OPERATING_INCOME_YOY`: `46`
  - `REVENUE_YOY`: `46`
  - `EPS_QOQ`: `41`
  - `NET_INCOME_QOQ`: `41`
  - `OPERATING_INCOME_QOQ`: `36`
  - `REVENUE_QOQ`: `36`
- period distribution:
  - `QUARTER`: `378`
  - `YEAR`: `60`
  - `SNAPSHOT`: `2`
- tests:
  - `py -3 -m unittest tests.test_derived_views`
  - result: `2 passed`

Operational note:

- current PowerShell output in the user's environment still shows some Korean
  mojibake
- derived calculations themselves are validated and structurally correct

## Calculation rules

### YoY

- `YEAR`: compare against the previous fiscal year
- `QUARTER`: compare against the same fiscal quarter in the previous fiscal year
- if the previous period is missing or `0`, `value_numeric` is `NULL`

Formula:

```text
(current_value - previous_value) / previous_value
```

### QoQ

- applies only to `QUARTER`
- compares against the immediately previous quarter
- `Q1` compares to the previous year's `Q4`
- if the previous period is missing or `0`, `value_numeric` is `NULL`

Formula:

```text
(current_value - previous_value) / previous_value
```

### Margins

- `OPERATING_MARGIN = OPERATING_INCOME / REVENUE`
- `NET_MARGIN = NET_INCOME / REVENUE`
- calculated for any period where the numerator and `REVENUE` exist on the same
  period key
- if the denominator is missing or `0`, `value_numeric` is `NULL`

## Source design

The derived view is built from `company_metric_timeseries`, not from raw tables
directly.

This keeps the derivation layer aligned with:

- the current exact-name integrated selection rules
- the current `standard_metric` mapping layer
- the current analysis-oriented company / metric / period projection

## Important design note

The derived metric names are exposed as analysis-view labels in
`company_metric_derived_v1`.

They are not written back into:

- `raw_observation`
- `integrated_observation`
- `integrated_observation_enriched`
- `standard_metric`

This keeps the current frozen v2 baseline stable while still making derived
metrics easy to query.

## Main columns

- `anchor_integrated_observation_id`
- `compare_integrated_observation_id`
- `company_id`
- `company_name`
- `company_key`
- `normalized_stock_code`
- `raw_stock_code`
- `standard_metric_name`
- `base_standard_metric_name`
- `compare_standard_metric_name`
- `period_type`
- `fiscal_year`
- `fiscal_quarter`
- `period_label_std`
- `date_raw`
- `value_numeric`
- `current_value_numeric`
- `compare_value_numeric`
- `is_estimate`
- `selected_source_group`
- `calculation_method`

## Example SQL

Quarterly revenue growth and margin:

```sql
SELECT
    company_name,
    standard_metric_name,
    fiscal_year,
    fiscal_quarter,
    value_numeric
FROM company_metric_derived_v1
WHERE company_key = 'your-company-key'
  AND period_type = 'QUARTER'
  AND standard_metric_name IN ('REVENUE_YOY', 'REVENUE_QOQ', 'OPERATING_MARGIN')
ORDER BY fiscal_year DESC, fiscal_quarter DESC, standard_metric_name;
```

Rows where the calculation could not be completed:

```sql
SELECT
    standard_metric_name,
    period_type,
    fiscal_year,
    fiscal_quarter,
    current_value_numeric,
    compare_value_numeric
FROM company_metric_derived_v1
WHERE value_numeric IS NULL
ORDER BY fiscal_year DESC, fiscal_quarter DESC;
```

## Execution

Create or refresh the derived views:

```powershell
py -3 -m python.etl.run_derived_views
```

Inspect the derived layer:

```powershell
py -3 -m python.etl.inspect_company_metric_derived
```

## Future extension path

This view is intended to be the base for future derived analysis work such as:

- CAGR
- rolling margins
- trailing-twelve-month views
- valuation joins
- consensus comparison
- screening and ranking helpers

Those should be added as new derived views or downstream analysis tables, not
by modifying the validated source layers.
