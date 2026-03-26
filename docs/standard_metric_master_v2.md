# Standard metric master v2

## Purpose

This document describes the non-destructive v2 extension that introduces a
`standard_metric` master structure on top of the validated v1 pipeline.

Related docs:

- `docs/current_architecture.md`
- `docs/v1_release_notes.md`
- `PROJECT_STATUS.md`

The design goal is:

- keep `raw_observation` and `integrated_observation` unchanged
- preserve current `integrated_observation_enriched` behavior
- add a master-keyed standard metric layer that can group same-meaning metric
  names under one stable `standard_metric`

## Design choice

The project now uses:

- `standard_metric`
  - master list of approved standard metrics
- `metric_name_mapping`
  - authoritative normalized metric-key to standard metric mapping table
- `metric_alias_map`
  - legacy compatibility table mirrored from `metric_name_mapping`
- `integrated_observation_enriched`
  - still preserved as the main enriched output
  - now also carries `standard_metric_id`

Why this approach was chosen:

- it preserves the current project shape and existing consumers
- it avoids rewriting the validated `integrated_observation` logic
- it keeps `standard_metric_name` string access for compatibility
- it adds a stable master key for future company matching, overrides, and
  derived-metric work

## New and updated tables

### `standard_metric`

Role:

- stores the approved standard metric master list

Key fields:

- `standard_metric_id`
- `standard_metric_name`
- `metric_family`
- `description`
- `active_flag`
- `created_at`
- `updated_at`

### `metric_name_mapping`

Role:

- stores the authoritative `normalized_metric_key -> standard_metric` mapping

Key fields:

- `metric_name_mapping_id`
- `normalized_metric_key`
- `raw_metric_name_example`
- `standard_metric_id`
- `standard_metric_name`
- `mapping_rule`
- `mapping_confidence`
- `is_active`
- `created_at`
- `updated_at`

### `metric_alias_map`

Role:

- retained for backward compatibility
- mirrored from `metric_name_mapping`

Updated field:

- `standard_metric_id`

### `integrated_observation_enriched`

Role:

- still preserves the v1 enriched output shape
- now also stores the stable master link

Updated field:

- `standard_metric_id`

## Seed and mapping strategy

### Seeded standard metrics

The master table is seeded from the approved taxonomy and includes:

- v1 conservative exact-alias metrics
- approved ratio metrics
- approved growth-rate metrics
- master rows with `0` current data rows when the taxonomy name is approved but
  not yet used by a current exact alias

### Mapping sources

The seed mapping is built from two sources:

1. curated exact aliases
   - existing approved `DEFAULT_ALIAS_MAP`
2. high-confidence seed aliases
   - exact English/Korean equivalents such as:
     - `Revenue`, `Sales`
     - `Operating Income`
     - `Net Income`
     - `Total Assets`
     - `Total Equity`

### Important guardrails

- mapping remains deterministic and idempotent
- `raw_metric_name` is never modified
- `normalized_metric_key` remains the lookup key
- no fuzzy matching
- no semantic merge beyond approved high-confidence seed aliases
- ambiguous or deferred families remain unmapped

## Execution flow

### Seed only

```powershell
py -3 -m python.etl.seed_standard_metric_master
```

### Full rebuild

```powershell
py -3 -m python.etl.run_standard_metric_mapping
```

This now performs:

1. ensure v1 metric schema
2. ensure v2 master schema
3. seed `standard_metric`
4. seed `metric_name_mapping`
5. sync legacy `metric_alias_map`
6. rebuild `integrated_observation_enriched` with `standard_metric_id`

## Inspection workflow

### Standard metric master inspection

```powershell
py -3 -m python.etl.inspect_standard_metric_master
```

Use this to verify:

- `standard_metric` row count
- `metric_name_mapping` row count
- `metric_alias_map` compatibility row count
- enriched rows linked to `standard_metric_id`
- master row counts by `standard_metric_name`

### Unmapped metric inspection

```powershell
py -3 -m python.etl.inspect_unmapped_metrics
```

Use this to verify:

- unmapped raw metric counts
- deferred family concentration
- high-confidence suggestion candidates
- ambiguous candidates that still require review

## Manual review points

Future reviewers should look at:

- high-confidence English seed aliases that may need tightening or expansion
- still-unmapped growth-like metrics such as `지배주주EPS증가율`
- deferred families that remain intentionally outside v2 scope
- whether `metric_name_mapping` should later support manual overrides or source-
  specific exceptions

## Handoff note

This implementation is intended as a bridge from v1 string-based enrichment to
a master-keyed standard metric system, while preserving the validated v1 data
and rebuild flow.

## Current verified baseline

Latest user-side local verification confirmed:

- `standard_metric`: `79` rows
- active `metric_name_mapping`: `141` rows
- mirrored `metric_alias_map`: `141` rows
- `integrated_observation_enriched`: `2432` rows
- rows linked to `standard_metric_id`: `2077`
- distinct coverage: `103 / 154 = 66.88%`
- row-level coverage: `2077 / 2432 = 85.40%`
- tests:
  - `py -3 -m unittest tests.test_metric_mapping tests.test_standard_metric_master`
  - result: `28 passed`

Compact baseline snapshot:

- `79 / 141 / 2432 / 2077 / 66.88% / 85.40% / 28 passed`

Meaning:

- `standard_metric` / active `metric_name_mapping` /
  `integrated_observation_enriched` / rows linked to `standard_metric_id` /
  distinct coverage / row-level coverage / tests passed

Compatibility note:

- the enriched rebuild supports both:
  - legacy string-only alias maps used by older tests
  - v2 structured mapping rows carrying `standard_metric_id`
- this keeps the v1 test surface stable while allowing v2 master linking

## Baseline snapshot

The current frozen `Financial Pipeline v2 baseline` can be checked with this
single snapshot:

- `standard_metric`: `79`
- active `metric_name_mapping`: `141`
- `integrated_observation_enriched`: `2432`
- rows linked to `standard_metric_id`: `2077`
- distinct coverage: `66.88%`
- row-level coverage: `85.40%`
- tests: `28 passed`

Compact form:

- `79 / 141 / 2432 / 2077 / 66.88% / 85.40% / 28 passed`
