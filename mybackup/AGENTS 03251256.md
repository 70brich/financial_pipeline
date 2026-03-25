# Project instructions

## Goal
Build a local-first financial data pipeline using SQLite first, with schema and code kept portable to PostgreSQL later.

## Source groups
The input files are under `data/input/` and source groups are:
- KDATA1
- KDATA2
- QDATA

Do not use filename alone as an identifier.
The same filename may exist under different source groups such as KDATA1 and KDATA2.
Always preserve and use folder-based source_group together with relative path and file metadata.

## Data model rules
- Preserve raw source data separately from integrated data.
- Use long-format storage for observations.
- Keep raw metric names and standardized metric names separately.
- Keep raw company identifiers and standardized identifiers separately.
- Support manual override separately from automatic source-priority selection.
- Keep schema and SQL portable to PostgreSQL.

## Period rules
- KDATA1 is quarterly data. Derive fiscal_year and fiscal_quarter from the leading date column.
- Store normalized quarter labels like 24.1Q, 24.2Q.
- KDATA2 is yearly data. Use the year of the leading date as fiscal_year.
- KDATA2 values must preserve value nature such as annual cumulative, year-end close, year-high, or year-low.
- QDATA has three sectors: overview, yearly data, quarterly data.
- Year-labeled values in QDATA belong to yearly data.
- Preserve both raw period labels and normalized period fields.

## Estimate rules
- Keep estimate rows.
- Prefer confirmed values over estimates in integrated output.
- Use is_estimate to distinguish them.

## Identifier rules
- If QDATA has stock code like A173130, normalize to 173130.
- If stock code is missing, prepare a company identifier resolution workflow.
- Preserve both raw and normalized stock codes.

## Implementation preference
- Use Python.
- Prefer SQLAlchemy and pandas.
- Start with SQLite.
- Organize parsers by source group: KDATA1, KDATA2, QDATA.
- Add tests for parsing and normalization logic.
- Before creating or modifying major files, propose a short plan and ask for confirmation.
- After each milestone, stop and wait for user review.
