# AGENTS.md

## Mission
You are operating as a local coding agent for the financial pipeline DB project.
Work autonomously in small safe loops: inspect -> modify -> run -> verify -> log.
Preserve source truth, avoid risky semantic merges, and escalate only policy decisions.

---

## Project summary
This project builds a local-first financial data pipeline on SQLite, while keeping schema and SQL reasonably portable to PostgreSQL later.

Current implemented layers:
- `source_file`
- `raw_observation`
- `integrated_observation` (minimum exact-name selection layer)
- `integrated_observation_enriched` (standard metric enrichment layer)

Current source groups:
- `KDATA1`
- `KDATA2`
- `QDATA`

Current canonical inputs live under:
- `data/input/KDATA1/`
- `data/input/KDATA2/`
- `data/input/QDATA/`

Ignore loose files directly under `data/input/`.

---

## Current known project state
Treat the following as the current baseline unless code/tests/inspect prove otherwise.

### Raw load status
- KDATA1 raw loaded: 1086 rows
- KDATA2 raw loaded: 247 rows
- QDATA raw loaded: 1264 rows

### Integrated status
- `integrated_observation`: 2432 rows
- Current integrated is NOT semantic merge.
- It is an exact `raw_metric_name`-based minimum selection layer.

### Current standard metric status
- `integrated_observation_enriched` exists
- Standard metric mapping is rule-based and conservative
- Recent known coverage baseline:
  - distinct raw metric coverage around 40.26%
  - row-level coverage around 61.88%
- Coverage may increase as safe aliases are added, but risky merges are forbidden

### Known small issue
- `inspect_integrated_load` may have a conflict sample display issue caused by NULL comparison in inspection SQL
- Treat this as an inspection-display issue unless proven to affect actual integrated data

---

## Non-negotiable design rules
1. Preserve raw source data separately from integrated data.
2. Preserve `raw_metric_name` exactly as original text. Never overwrite it.
3. Use long-format observation storage.
4. Preserve raw identifiers and normalized identifiers separately.
5. Preserve estimate vs confirmed using `is_estimate`.
6. Keep automatic selection separate from future manual override logic.
7. Keep the project SQLite-first but PostgreSQL-portable where practical.
8. Never identify a source file by filename alone. Use `source_group + relative_path`.
9. Do not do unsafe semantic merges to inflate coverage.
10. When in doubt, leave a metric unmapped.

---

## Hard restrictions
Do NOT change the following casually:
- parser behavior already validated for KDATA1 / KDATA2 / QDATA
- raw loading semantics already validated
- integrated selection priority / tie-break logic
- exact meaning of already validated raw rows
- existing DB truth without inspection/test evidence

Do NOT introduce:
- fuzzy match
- embedding similarity
- LLM-based metric classification
- broad semantic grouping
- large schema redesign without explicit need
- aggressive normalization that may erase metric meaning

---

## Integrated layer meaning
`integrated_observation` is currently a minimum exact-name selection layer.

Interpretation:
- same company
- same exact `raw_metric_name`
- same period key

Then choose one representative row using existing priority/tie-break logic.

This means:
- no metric semantic merge yet at integrated stage
- no advanced company matching yet
- no broad standardization at integrated stage

Keep this meaning intact.

---

## Standard metric enrichment policy
`integrated_observation_enriched` is the place for conservative standard metric mapping.

### Allowed mapping style
Only allow:
- exact alias mapping
- exact normalized-key mapping
- obvious symbol/prefix cleanup that does NOT change meaning

### Current normalized-key intent
`normalized_metric_key` is internal lookup support only.
It must not replace `raw_metric_name`.

Allowed minimal normalization examples:
- `(개별)`
- `(연결)`
- `개별`
- `연결`
- `분기`
- `연간`

These may be removed for lookup only, while preserving the original metric text and storing variant meaning separately where applicable.

### Not allowed for automatic merge
Do NOT automatically merge:
- 5-year average metrics into base metrics
- growth rate metrics into level metrics
- margin metrics into earnings metrics
- policy-ambiguous items
- score/ranking/meta labels
- metrics whose meaning differs by nuance unless exact policy already exists

Examples to keep conservative unless policy is explicitly defined:
- `PER(5년평균)`
- `PBR(5년평균)`
- `ROE(5년평균)`
- `OPM(5년평균)`
- `NPM`
- `NPM(%)`
- `지배주주ROE`
- `세전계속사업손익`
- `세전계속사업이익률`
- growth-rate families
- turnover-day families
- score families
- YOY labels

---

## Autonomous work loop
Work autonomously without waiting for the user after every small milestone.

Use this loop:

1. Inspect current state
   - review coverage
   - review unmapped top metrics
   - review recent enriched rows
   - review existing tests/logs

2. Choose a small safe task
   Prefer:
   - exact alias additions
   - obvious normalization cleanup
   - inspect helper improvements
   - test additions
   - documentation/log refresh

3. Implement minimal change
   - keep scope small
   - avoid touching unrelated logic

4. Run verification
   - rebuild standard metric layer if relevant
   - run inspection
   - run targeted tests
   - compare before/after coverage
   - confirm no obvious regressions

5. Decide next action
   - continue if next step is still safe
   - stop and escalate if a policy decision is needed

Repeat until:
- safe exact alias opportunities are mostly exhausted, or
- remaining high-value items are policy-dependent, or
- a larger structural design decision is required

---

## What to prioritize now
Current recommended priority order:

1. safe exact alias expansion
2. harmless normalization cleanup
3. inspect/reporting improvements
4. test coverage improvements
5. policy-needed metric separation
6. documentation refresh

Near-term likely candidate class:
- symbol-prefixed formula-like metrics such as `-매출원가`, `-판관비`, `=매출총이익`, `=영업이익`, `=순이익`, `=세전순익`
- only when removing the symbol preserves an exact already-known metric meaning

Keep conservative on:
- growth metrics
- turnover-day metrics
- score/meta fields
- 5Y averages
- ambiguous profitability variants

---

## Required verification habits
For each meaningful change, run the smallest relevant verification set.

Typical commands to use when relevant:
- rebuild enriched layer
- inspect standard metric mapping
- run targeted tests
- inspect recent enriched rows
- compare unmapped top list before/after

Prefer evidence from execution over assumptions.

---

## Required project files to maintain
Keep these files updated as working memory for the project.

### 1. `PROJECT_STATUS.md`
Update frequently with:
- current coverage snapshot
- most recent completed work
- current top unmapped candidates
- next recommended tasks
- known risks / blockers

### 2. `RUN_LOG.md`
Append concise run history:
- commands executed
- important outputs
- failures encountered
- what was changed to fix them

### 3. `CONSULTING_REQUEST.md`
Use this only when automatic continuation becomes risky or inefficient.

Required format:
- Background
- Current observations
- Why autonomous decision is risky
- 2 to 3 possible choices
- Recommended choice
- Short question to paste into ChatGPT

When this file is updated due to a real blocker, stop autonomous expansion and wait for the user to bring that question to ChatGPT.

---

## When to escalate instead of guessing
Stop and write `CONSULTING_REQUEST.md` when any of the following happens:

1. A new `standard_metric_name` policy must be defined
2. Two or more plausible meanings exist for one metric
3. Existing aliases conflict with new evidence
4. Coverage can increase only by using risky semantic merges
5. Test results and inspect output disagree
6. A schema redesign looks necessary
7. A change would alter validated raw/integrated meaning
8. The task becomes too broad for safe incremental progress

---

## Logging style
Do not produce noisy logs.
Prefer concise evidence-based notes.

Good:
- what changed
- why it was safe
- what command verified it
- before/after coverage if relevant
- remaining unmapped items worth attention

Avoid:
- long self-commentary
- repeated restatement of obvious facts
- speculative claims without execution evidence

---

## File and code style
- Prefer Python for ETL and inspection helpers
- Prefer SQLAlchemy and pandas when already used in the project
- Keep SQL and schema readable and portable where practical
- Keep scripts rebuildable and idempotent when possible
- Add or update tests with each meaningful mapping-rule expansion
- Keep changes minimal and easy to diff

---

## User preference
- PowerShell commands shown to the user must be one line
- When the user asks for Codex instructions, present them in multi-line form
- The user may ask ChatGPT for policy consulting; prepare concise consulting prompts when needed

---

## Completion rule for an autonomous round
A round is considered complete when one of the following is true:

1. Safe exact alias additions are largely exhausted
2. Remaining important unmapped metrics are mostly policy-driven
3. Tests and inspection are stable
4. `PROJECT_STATUS.md`, `RUN_LOG.md`, and `CONSULTING_REQUEST.md` are current

At that point, summarize the round in `PROJECT_STATUS.md` and stop.

---

## First action when starting in this repo
1. Read this file
2. Read `PROJECT_STATUS.md` if present
3. Inspect current DB/result state
4. Verify that the expected input files and DB exist
5. Continue with the next safe autonomous task
6. Escalate only via `CONSULTING_REQUEST.md` when needed