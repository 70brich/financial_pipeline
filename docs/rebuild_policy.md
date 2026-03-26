# Rebuild policy

## Purpose

This document defines when the project should stop patching the active current
database and instead create a separate candidate database for a full rebuild.

## When to create a candidate rebuild

Use a full-rebuild candidate when one or more of these are true:

- a source layout changed enough that period-level patching is unreliable
- validated selection logic must be re-run for most of the dataset
- the canonical input universe changed materially
- schema additions need broad replay validation
- update evidence is too large or too ambiguous for a safe incremental patch

## Candidate workflow

1. Create a candidate SQLite database outside the active current slot.
2. Re-run rebuild logic against the candidate only.
3. Validate row counts, table counts, and targeted business checks.
4. Compare current vs candidate before promotion.
5. Promote only after validation succeeds.

## Current release slots

- current: `data/financial_pipeline.sqlite3`
- candidate copies: `data/releases/*.sqlite3`
- archive copies: `data/archive/*.sqlite3`

## Validation checklist

- core table counts look plausible
- targeted source snapshots are recorded
- no unexpected loss in raw / integrated / enriched rows
- candidate comparison output is reviewed before promotion
- release metadata reflects the candidate status clearly

## Guardrails

- never rebuild in-place on the active current DB
- keep promotion and rollback as explicit operator steps
- preserve an archive copy before replacing the current DB
- treat `series_change_audit` as evidence, not as a substitute for validation

## Current implementation note

`python.etl.run_full_rebuild` currently creates the non-destructive candidate
scaffold only.

What it does today:

- copies the current DB to a candidate path
- ensures release-management tables exist on the copy
- registers the candidate in `release_registry`

What it does not do yet:

- replay all canonical sources into a fresh empty database
- re-run the full ETL chain automatically
- produce a full release validation report by itself
