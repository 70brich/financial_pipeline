# Runbook

## Purpose

This document summarizes the current safe execution order for rebuilding the
SQLite pipeline from canonical inputs.

## Database file

- `data/financial_pipeline.sqlite3`

## Recommended rebuild order

1. Inventory canonical files

```powershell
py -3 -m python.etl.run_inventory
```

2. Parse `KDATA1`

```powershell
py -3 -m python.etl.run_kdata1_parser
```

3. Parse `KDATA2`

```powershell
py -3 -m python.etl.run_kdata2_parser
```

4. Parse `QDATA`

```powershell
py -3 -m python.etl.run_qdata_parser
```

5. Rebuild integrated selection

```powershell
py -3 -m python.etl.run_integrated_selection
```

6. Rebuild standard metric enrichment

```powershell
py -3 -m python.etl.run_standard_metric_mapping
```

7. Create analysis views

```powershell
py -3 -m python.etl.run_analysis_views
```

8. Create derived metric views

```powershell
py -3 -m python.etl.run_derived_views
```

9. FnGuide Samsung sample ingestion

```powershell
py -3 -m python.etl.debug_fnguide_layout
py -3 -m python.etl.run_fnguide_parser
py -3 -m python.etl.inspect_fnguide_load
```

10. Optional release-management metadata capture

```powershell
py -3 -m python.etl.run_incremental_update
```

11. Optional candidate rebuild scaffold

```powershell
py -3 -m python.etl.run_full_rebuild --release-label 2026Q2_candidate
```

Optional seed-only step:

```powershell
py -3 -m python.etl.seed_standard_metric_master
```

## Validation commands

Inventory:

```powershell
py -3 -m python.etl.inspect_inventory
```

KDATA1:

```powershell
py -3 -m python.etl.inspect_kdata1_load
```

KDATA2:

```powershell
py -3 -m python.etl.inspect_kdata2_load
```

QDATA debug:

```powershell
py -3 -m python.etl.debug_qdata_layout
```

Integrated selection:

```powershell
py -3 -m python.etl.inspect_integrated_load
```

Standard metric enrichment:

```powershell
py -3 -m python.etl.inspect_standard_metric_mapping
```

Standard metric master:

```powershell
py -3 -m python.etl.inspect_standard_metric_master
```

Unmapped metric review:

```powershell
py -3 -m python.etl.inspect_unmapped_metrics
```

Analysis layer:

```powershell
py -3 -m python.etl.inspect_company_metric_timeseries
```

Derived layer:

```powershell
py -3 -m python.etl.inspect_company_metric_derived
```

FnGuide:

```powershell
py -3 -m python.etl.inspect_fnguide_load
```

Release metadata:

```powershell
py -3 -m python.etl.inspect_release
```

Release comparison:

```powershell
py -3 -m python.etl.compare_release_series --release-label 2026Q2_candidate
```

## Notes

- Rebuild scripts are designed to replace their target layer, not append forever.
- `raw_metric_name` is preserved as-is.
- `integrated_observation` remains an exact-name selection layer.
- `integrated_observation_enriched` adds rule-based `standard_metric_name`
  without changing raw or integrated source records.
- `standard_metric` and `metric_name_mapping` are seeded idempotently before the
  enriched layer is rebuilt.
- `company_metric_timeseries` is a non-destructive SQLite view designed for
  direct analysis and pandas use.
- `company_metric_derived_v1` is a non-destructive SQLite view built on top of
  `company_metric_timeseries`.
- FnGuide is currently a sidecar web-ingestion source and does not yet feed
  `integrated_observation`.
- release-management scripts are metadata-first scaffolds; promotion and
  rollback are dry-run unless `--apply` is explicitly set.
