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

## Notes

- Rebuild scripts are designed to replace their target layer, not append forever.
- `raw_metric_name` is preserved as-is.
- `integrated_observation` remains an exact-name selection layer.
- `integrated_observation_enriched` adds rule-based `standard_metric_name`
  without changing raw or integrated source records.
