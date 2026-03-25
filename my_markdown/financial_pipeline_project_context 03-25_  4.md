# Financial Pipeline Project Context (v1 Baseline → v2 Preparation)

## 1. Project Overview

This project builds a **financial data pipeline database** designed to
ingest, normalize, and integrate long‑term corporate financial metrics
from multiple heterogeneous datasets.

Pipeline architecture:

source_file ↓ raw_observation ↓ integrated_observation ↓
integrated_observation_enriched

Goals:

-   Consolidate financial data from multiple sources
-   Normalize metric naming conventions
-   Create a stable integrated observation layer
-   Support long‑term analytics across companies and time
-   Build a maintainable financial data infrastructure

Database engine currently used: SQLite (local development environment)

------------------------------------------------------------------------

# 2. Current Implementation Status

Financial Pipeline **v1 baseline is complete**.

All ingestion, integration, mapping, validation, and documentation work
for v1 has been finalized.

### Raw Data Loaded

  Dataset   Structure                  Rows
  --------- -------------------------- ------
  KDATA1    Row‑wise quarterly table   1086
  KDATA2    Row‑wise yearly table      247
  QDATA     Snapshot/year/quarter      1264

Total raw rows loaded:

2597 raw observations

------------------------------------------------------------------------

# 3. Core Pipeline Tables

## source_file

Stores metadata about ingested source files.

Example fields:

id\
source_group\
file_name\
load_timestamp

Source groups currently used:

KDATA1\
KDATA2\
QDATA

------------------------------------------------------------------------

## raw_observation

Stores raw extracted financial values.

Key fields:

company_code\
raw_metric_name\
period_year\
period_quarter\
value\
source_file_id

Characteristics:

-   Raw metric names preserved
-   No normalization at this layer
-   Dataset‑specific structure retained

------------------------------------------------------------------------

## integrated_observation

First integration layer.

Purpose:

Select a **single canonical observation per metric / company / period**.

Integration rule used in v1:

Exact raw_metric_name matching

Result:

2432 integrated rows generated

------------------------------------------------------------------------

## integrated_observation_enriched

Adds semantic enrichment fields such as:

standard_metric_name\
normalized_metric_key\
metric_family

Purpose:

Prepare integrated observations for standardized analytics.

------------------------------------------------------------------------

# 4. Metric Mapping Pipeline

Metric mapping implemented using:

raw_metric_name\
→ normalized_metric_key\
→ standard_metric_name

Normalization rules include prefix cleanup:

-매출액\
+매출액\
=매출액

All normalize to:

매출액

Handled prefixes:

-   
-   =

------------------------------------------------------------------------

# 5. Metric Coverage (v1)

Coverage achieved after mapping:

Distinct metric coverage: 66.88%\
Row‑level coverage: 85.40%

Meaning:

-   Two‑thirds of unique metric names mapped
-   Majority of observation rows mapped

Remaining metrics are intentionally deferred.

------------------------------------------------------------------------

# 6. Deferred Metrics

Certain metric families intentionally left unmapped in v1:

-   Deferred tax metrics
-   Rare accounting adjustments
-   Unclear or ambiguous financial fields

These remain **unmapped by policy** to avoid incorrect taxonomy
expansion.

------------------------------------------------------------------------

# 7. Validation Status

Pipeline validation complete.

Tests passed:

23 tests

Validation checks include:

-   row count consistency
-   required field validation
-   normalization key generation checks
-   mapping coverage inspection
-   alias validation checks

------------------------------------------------------------------------

# 8. Inspection Tools

Pipeline includes inspection utilities:

inspect_inventory\
inspect_integrated_load\
inspect_standard_metric_mapping

These tools verify:

-   source ingestion
-   integration selection
-   mapping coverage

------------------------------------------------------------------------

# 9. Project Folder Structure

Current directory layout:

CODEX

python/ etl/ run_standard_metric_mapping.py inspect_inventory.py
inspect_integrated_load.py

data/ financial_pipeline.sqlite3

docs/ data_quality_checklist.md metric_taxonomy_v1.md
v1_release_notes.md current_architecture.md current_limitations.md

PROJECT_STATUS.md RUN_LOG.md CONSULTING_REQUEST.md AGENTS.md

------------------------------------------------------------------------

# 10. Documentation

Key documentation files:

data_quality_checklist.md\
Defines validation rules for each pipeline layer.

metric_taxonomy_v1.md\
Defines the current financial metric taxonomy.

v1_release_notes.md\
Summarizes the v1 baseline including coverage and deferred items.

current_architecture.md\
Explains pipeline architecture.

current_limitations.md\
Documents current constraints and known gaps.

------------------------------------------------------------------------

# 11. Current Baseline

Project state:

Financial Pipeline v1 Baseline

Completed:

✔ data ingestion\
✔ integration layer\
✔ metric normalization\
✔ mapping pipeline\
✔ validation checks\
✔ documentation

This version is considered stable.

------------------------------------------------------------------------

# 12. Git Migration (Next Step)

Version control is being introduced.

Steps:

1.  Install Git
2.  Initialize repository

git init\
git add .\
git commit -m "financial pipeline v1 baseline"

3.  Create GitHub repository
4.  Push baseline snapshot

Purpose:

-   Preserve v1 baseline
-   Enable safe v2 experimentation
-   Provide full version history

------------------------------------------------------------------------

# 13. Financial Pipeline v2 Direction

Potential development directions:

## Data Quality Hardening

-   stronger validation rules
-   anomaly detection
-   dataset integrity checks

## Company Identity Resolution

Improve company matching across datasets:

company alias mapping\
ticker normalization\
entity resolution

## Governance Layer

Introduce manual override controls:

manual metric corrections\
mapping overrides\
source priority rules

## Controlled Taxonomy Expansion

Gradually expand metric coverage while maintaining correctness.

## Business Metrics Layer

Add derived analytics metrics such as:

revenue growth\
operating margin\
ROIC

------------------------------------------------------------------------

# 14. Immediate Next Tasks

1.  Install Git
2.  Initialize repository
3.  Commit v1 baseline
4.  Push project to GitHub
5.  Start v2 development branch

------------------------------------------------------------------------

# End of Context
