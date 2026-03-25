# Current limitations

## Purpose

This document summarizes what is intentionally not implemented yet in the
current pipeline.

## Metric logic

Not implemented:

- semantic metric merge beyond exact alias mapping
- fuzzy metric matching
- LLM-based metric mapping
- automatic handling of ambiguous metrics
- further taxonomy expansion into deferred metric families for the current version

Current behavior:

- `raw_metric_name` is preserved as-is
- `standard_metric_name` is added only when an exact rule exists
- ambiguous metrics remain unmapped
- deferred families remain intentionally unmapped even if they are frequent

Deferred families in the current version:

- turnover-day metrics
- dividend metrics
- supplementary per-share metrics
- valuation / price expansion metrics
- score / meta metrics
- 5-year-average metrics
- growth-like metrics not clearly tied 1:1 to an approved base metric

## Company identity

Not implemented:

- advanced company matching
- multi-step company resolution workflow
- robust cross-source entity linking beyond simple fallback keys

Current behavior:

- integrated selection uses simple fallback company key logic

## Overrides and governance

Not implemented:

- manual override workflow
- source/value override UI
- approval workflow for conflicting selections

## Interfaces

Not implemented:

- Streamlit UI
- dashboard UI
- interactive admin tools

## Recommended next areas

Safe next areas:

- stabilize and document the current taxonomy
- add table-level data quality checks
- add operational docs and validation runbooks
- add targeted tests for source-specific edge cases
