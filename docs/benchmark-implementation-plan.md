# Benchmark Hierarchy Implementation Plan

> For Hermes: execute this plan in order. Keep benchmark construction simpler than the main strategy at each stage. Do not jump to DOI-style volatility-managed benchmarks before static factor baselines are working.

## Goal

Build a benchmark hierarchy for `fineval` that makes validation claims interpretable and fair.

The hierarchy should move from low-bar to high-bar competitors:
1. `1/n`
2. factor-only static benchmark
3. `FF6 + BAB + QMJ` static benchmark
4. DOI-style volatility-managed multifactor benchmark
5. `fineval` strategy family

## Why this plan now

`fineval` now has:
- stronger packet contracts
- richer score diagnostics
- rolling validation runner
- rolling-aware portfolio validation report

Before factor-adjusted alpha outputs and benchmark comparison reports are implemented, the repo needs a clear benchmark hierarchy and an execution order that avoids architecture drift.

## Scope

In scope:
- benchmark hierarchy documentation
- AQR factor ingestion plan and normalized processed files
- static factor benchmark layer design
- DOI-style benchmark design note

Out of scope for this plan:
- full DOI benchmark implementation in the first task
- full factor-regression engine in the first task
- transaction-cost-aware benchmark layer

## Benchmark tiers

### B0 — Equal-weight benchmark
Definition:
- naive `1/n` portfolio across the investable universe

Purpose:
- low-bar benchmark
- investor-intuition baseline

### B1 — Static factor benchmark
Definition:
- factor-only benchmark built without text inputs
- first version can be based on `FF6`

Purpose:
- tests whether text adds value beyond standard factor exposures

### B2 — Static enriched factor benchmark
Definition:
- `FF6 + BAB + QMJ`

Purpose:
- stronger factor-only comparator using defensive and quality dimensions

### B3 — DOI-style sophisticated benchmark
Anchor paper:
- DOI `10.1111/jofi.13395`
- title: `A Multifactor Perspective on Volatility-Managed Portfolios`

Purpose:
- high-bar benchmark
- not the same research question as `fineval`, but a strong competing allocation framework

Role in the hierarchy:
- use as a sophisticated factor-timing comparator
- do not use as the only benchmark

### T-tier — fineval strategies
Definition:
- raw text
- quality-adjusted text
- reliability-adjusted text
- hybrid text + structured strategies

Purpose:
- main evaluated strategy family

## Required fairness rules

All benchmarks should share, as much as possible:
- the same investable universe
- the same rebalance frequency
- the same date alignment
- the same return convention
- the same transaction-cost convention when costs are later added

## Current data state

Already available:
- `FF5 monthly`
- `FF6 monthly`
- `MOM monthly`

Downloaded and ready for ingestion:
- AQR `BAB` monthly workbook
- AQR `QMJ` monthly workbook

Not yet implemented:
- normalized processed BAB/QMJ factor files
- static factor benchmark builder
- DOI-style volatility-managed benchmark builder

## Execution order

### Task 1 — Document the benchmark hierarchy
Add docs that explain:
- why `1/n` is still needed
- why `FF6 + BAB + QMJ` is the main factor-only comparator
- why the DOI benchmark is a high-bar competitor, not the sole main benchmark

Deliverables:
- `docs/benchmark-hierarchy.md`
- README/docs index updates

### Task 2 — Ingest AQR BAB/QMJ
Create a normalized processed factor dataset from downloaded AQR workbooks.

Deliverables:
- processed monthly factor files under `data/external/aqr_processed/`
- parser utility or ingestion script
- schema note for selected columns (`USA`, `Global`, `Global Ex USA`, etc.)

### Task 3 — Static factor benchmark layer
Build the first factor-only benchmark surface:
- `FF6`
- `FF6 + BAB + QMJ`

Deliverables:
- factor benchmark config or helper module
- benchmark result contract
- tests using toy or miniature aligned factor inputs

### Task 4 — DOI-style benchmark plan and implementation
Design then implement the volatility-managed multifactor comparator.

Deliverables:
- DOI benchmark design note
- benchmark implementation module
- validation tests

### Task 5 — Comparison layer
Add comparison reports across benchmark tiers and `fineval` tiers.

## First task to execute now

Task 1 only:
- write benchmark hierarchy docs
- update README and docs index
- do not yet implement factor loaders or DOI benchmark code in this first task

## Verification for Task 1

- docs files exist and are linked
- README accurately states benchmark hierarchy
- `PYTHONPATH=src pytest tests -q` still passes

## Next task after Task 1

Task 2:
- ingest AQR BAB/QMJ into normalized processed files
