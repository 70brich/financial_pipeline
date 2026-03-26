# Analysis layer v1

## Purpose

This document describes the first analysis-oriented layer added on top of the
frozen `Financial Pipeline v2 baseline`.

The goal is to make Python and pandas analysis easier without changing the
validated raw, integrated, or enriched layers.

## Why a view-first approach was chosen

The project starts with a SQLite view instead of a new persisted table because:

- the current enriched layer is already validated
- a view is non-destructive and rebuild-free
- analysis consumers can query a stable company / metric / period / value shape
- future derived layers can be added on top without duplicating source records

## View name

- `company_metric_timeseries`

## Main purpose

This view provides a directly queryable analysis shape centered on:

- company
- metric
- period
- numeric/text value
- selected source and selection reason

It is designed as the first analysis layer for personal investing workflows and
later extension into:

- derived metrics
- factor models
- screening logic
- consensus and market data joins

## Verified baseline

Latest user-side local verification confirmed:

- `company_metric_timeseries`: `2432` rows
- period distribution:
  - `YEAR`: `1247`
  - `QUARTER`: `1158`
  - `SNAPSHOT`: `27`
- tests:
  - `py -3 -m unittest tests.test_analysis_views`
  - result: `2 passed`

Operational note:

- current PowerShell output in the user's environment still shows some Korean
  mojibake
- this affects terminal readability, but the view row counts and structure are
  valid

## Source joins

The view is built from:

- `integrated_observation_enriched`
- `integrated_observation`
- `raw_observation`
- `company`

Join behavior:

- `integrated_observation_enriched` is the main driver
- `integrated_observation` supplies selection fields and period labels
- `raw_observation` supplies company identifier fallbacks and raw value context
- `company` is joined with a left-join fallback strategy so the view still works
  even when company matching is incomplete

## Main columns

- `integrated_observation_id`
- `company_id`
- `company_name`
- `company_key`
- `normalized_stock_code`
- `raw_stock_code`
- `standard_metric_id`
- `standard_metric_name`
- `raw_metric_name`
- `normalized_metric_key`
- `fiscal_year`
- `fiscal_quarter`
- `period_type`
- `period_label_std`
- `date_raw`
- `value_numeric`
- `value_text`
- `is_estimate`
- `selected_source_group`
- `selection_reason`

## Example SQL

Recent quarterly operating metrics for one company:

```sql
SELECT
    company_name,
    standard_metric_name,
    fiscal_year,
    fiscal_quarter,
    value_numeric
FROM company_metric_timeseries
WHERE company_key = 'your-company-key'
  AND period_type = 'QUARTER'
  AND standard_metric_name IN ('REVENUE', 'OPERATING_INCOME', 'NET_INCOME')
ORDER BY fiscal_year DESC, fiscal_quarter DESC;
```

Annual balance sheet metrics:

```sql
SELECT
    company_name,
    standard_metric_name,
    fiscal_year,
    value_numeric
FROM company_metric_timeseries
WHERE period_type = 'YEAR'
  AND standard_metric_name IN ('TOTAL_ASSETS', 'TOTAL_EQUITY', 'TOTAL_LIABILITIES')
ORDER BY fiscal_year DESC;
```

Rows still unmapped at the standard metric layer:

```sql
SELECT
    raw_metric_name,
    normalized_metric_key,
    COUNT(*) AS row_count
FROM company_metric_timeseries
WHERE standard_metric_name IS NULL
GROUP BY raw_metric_name, normalized_metric_key
ORDER BY row_count DESC, raw_metric_name;
```

## Recommended execution

Create or refresh the analysis views:

```powershell
py -3 -m python.etl.run_analysis_views
```

Inspect the analysis shape:

```powershell
py -3 -m python.etl.inspect_company_metric_timeseries
```

## Next-step extension path

This view is intended to be the base for future derived analysis work such as:

- YoY growth columns
- QoQ change columns
- CAGR helper views
- valuation joins
- market price and consensus joins

Those should be added as separate derived views or materialized analysis tables
later, not by mutating the validated source layers.

See also:

- `docs/derived_metrics_v1.md`
