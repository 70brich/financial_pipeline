# Financial Pipeline v1 release notes

## Purpose

This document is the closeout summary for Financial Pipeline v1.

It summarizes:

- what is implemented
- what is intentionally deferred
- current verified coverage
- current validation status
- recommended future directions for a possible v2

## What is implemented in Financial Pipeline v1

### Core pipeline layers

- `source_file`
  - canonical file inventory for `KDATA1`, `KDATA2`, `QDATA`
- `raw_observation`
  - long-format raw observations
- `integrated_observation`
  - exact `raw_metric_name` based selected layer
- `integrated_observation_enriched`
  - conservative exact-alias `standard_metric_name` enrichment layer

### Canonical source handling

- canonical input folders:
  - `data/input/KDATA1`
  - `data/input/KDATA2`
  - `data/input/QDATA`
- loose files directly under `data/input/` are ignored
- `source_group + relative_path` is preserved as the file identity basis

### Source parsers

- `KDATA1`
  - quarterly parsing
  - `fiscal_year`, `fiscal_quarter`, `period_label_std` handling
- `KDATA2`
  - yearly parsing
  - long-format raw load
- `QDATA`
  - CSV parsing for `overview`, `yearly`, `quarterly` sectors

### Selection and enrichment logic

- integrated selection is implemented as exact-name selection only
- estimate preference and source priority are applied in the integrated layer
- metric enrichment is implemented through:
  - `metric_alias_map`
  - `normalized_metric_key`
  - exact alias mapping only
- `raw_metric_name` is preserved exactly

### Documentation and operational support

- architecture summary
- runbook
- table reference
- script reference
- current limitations
- data quality checklist
- taxonomy v1 reference

## What is intentionally deferred or left unmapped

### Deferred implementation areas

- advanced company matching
- semantic metric merge beyond exact alias mapping
- manual overrides
- UI / Streamlit
- fuzzy or LLM-based mapping

### Deferred metric families

These remain intentionally unmapped in v1:

- turnover-day metrics
- dividend metrics
- supplementary per-share metrics such as `CPS`, `DPS`, `OPS`, `SPS`
- valuation / price expansion metrics such as `EV/EBITDA`, `PCR`, `PEG`,
  `POR`, `PRR`, `PSR`, `ROIC`, `주가`
- score / meta metrics
- 5-year-average metrics
- growth-like metrics not clearly tied 1:1 to an already-approved base metric

Examples:

- `지배주주EPS증가율`
- `지배순익 증가율(%)`
- `주식수증가율(%)`

## Current verified coverage

Latest user-verified result:

- distinct coverage: `103 / 154 = 66.88%`
- row-level coverage: `2077 / 2432 = 85.40%`

Interpretation:

- the v1 target for distinct coverage (`~60%`) is exceeded
- the v1 target for row-level coverage (`~80%`) is exceeded

## Key validation status

Latest verified validation status:

- tests: `23` passed
- `integrated_observation_enriched_rows = 2432`
- `integrated_observation` and `integrated_observation_enriched` remain aligned
- approved exact-alias metric batches are reflected in inspection output
- deferred families remain unmapped as intended

Operationally verified:

- canonical inventory flow
- `KDATA1` raw parsing
- `KDATA2` raw parsing
- `QDATA` raw parsing
- integrated selection rebuild
- enriched metric mapping rebuild
- inspection-based coverage review

## Recommended next-step candidates for a future v2

These are candidates, not approved work for v1.

### 1. Data quality and validation hardening

- add more automated layer-level validation checks
- add anomaly reporting around nulls, duplicates, and unexpected coverage drops
- expand regression checks for source-specific parser edge cases

### 2. Company identity improvement

- design a more robust company resolution workflow
- move beyond simple fallback `company_key`
- preserve raw and standardized identity states separately

### 3. Manual governance layer

- support manual override tables and review workflow
- keep manual decisions separate from automatic source-priority selection

### 4. Controlled taxonomy expansion

If policy approval is given later, possible next families include:

- turnover-day metrics
- dividend metrics
- valuation / price metrics
- supplementary per-share metrics

### 5. Standardized business layer maturation

- strengthen documentation of approved taxonomy
- add richer mapping audit views
- keep exact alias mapping rebuildable and easy to inspect

## Final v1 position

Financial Pipeline v1 should now be treated as a stable documentation and
validation baseline:

- raw data preserved
- integrated exact-name selection working
- conservative exact-alias metric enrichment working
- coverage goals exceeded
- deferred families intentionally left for future policy decisions
