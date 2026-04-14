# Extension Architecture

## Purpose

This document explains how to extend `fineval` without breaking the current package shape.
It is an architectural guide for future contributors.

## Current package layers

### 1. Schema layer
Files:
- `src/fineval/schemas/`
- `src/fineval/core/datasets.py`

Role:
- define input objects
- define dataset contracts
- keep metadata explicit

Extension rule:
- add fields only when they clarify point-in-time semantics, provenance, or downstream evaluation behavior
- avoid adding loose optional fields without a clear use case

### 2. Data layer
Files:
- `src/fineval/data/`

Role:
- load point-in-time packets
- load structured panels
- keep data access separate from scoring logic

Extension rule:
- loaders should validate contracts and preserve as-of meaning
- loaders should not compute evaluation scores

### 3. Evaluation layer
Files:
- `src/fineval/eval/`
- `src/fineval/reports/`
- `src/fineval/presets/`
- `src/fineval/testsuites/`

Role:
- compute scores
- structure score outputs
- bundle default evaluation choices
- apply reproducible pass/fail gates

Extension rule:
- raw scoring logic belongs in `eval/`
- human-facing structured outputs belong in `reports/`
- default bundles belong in `presets/`
- threshold gates belong in `testsuites/`

### 4. Translation layer
Files:
- `src/fineval/signals/`
- `src/fineval/translation/`

Role:
- translate evaluated decision objects into bounded action signals

Extension rule:
- keep translation logic separate from both raw evaluation and portfolio validation
- do not bury allocation assumptions inside scoring functions

### 5. Validation layer
Files:
- `src/fineval/portfolio/`
- `src/fineval/backtest/`

Role:
- convert action scores into allocations
- compute toy or future multi-period validation outputs

Extension rule:
- keep portfolio mechanics explicit
- avoid hidden benchmark assumptions

## Recommended new modules

As the package expands, use this layout.

### `src/fineval/diagnostics/`
Use for:
- calibration diagnostics
- attribution summaries
- stability analyses
- perturbation checks

### `src/fineval/benchmarks/`
Use for:
- structured-only baselines
- naive text baselines
- benchmark registry and comparison helpers

### `src/fineval/experiments/`
Use for:
- rolling experiment configs
- run manifests
- output artifact organization

### `src/fineval/plots/`
Use only when plotting becomes necessary.
Keep plotting optional and separate from numerical core logic.

## Anti-patterns to avoid

### Anti-pattern 1 — model-specific code in core package
Bad:
- Claude-specific prompt builders inside `src/fineval/`
- Codex transport assumptions inside score modules

Good:
- runtime-specific wrappers outside package core
- package consumes files or structured objects only

### Anti-pattern 2 — scripts before modules
Bad:
- solving every new need with another top-level script

Good:
- first place reusable logic into `src/fineval/`
- then create a small example or CLI wrapper if needed

### Anti-pattern 3 — aggregate score without traceability
Bad:
- returning only one number when the user needs component interpretation

Good:
- preserve components in reports and diagnostics

### Anti-pattern 4 — validation logic mixed with allocation logic
Bad:
- scoring functions that also choose final portfolio weights

Good:
- score first
- translate second
- validate third

## Recommended documentation growth

As the package expands, docs should grow in this order:

1. input contracts
2. metric definitions
3. benchmark definitions
4. experiment config docs
5. contributor docs

## Recommended test growth

Current tests cover package skeleton and toy behavior.
Next tests should add:
- contract validation for richer packet schemas
- report decomposition tests
- rolling-runner smoke tests
- benchmark comparison tests
- calibration and stability diagnostic tests

## Decision rule for future additions

Before adding a new feature, ask:
1. Is this about input contracts?
2. Is this about evaluation?
3. Is this about translation?
4. Is this about validation?
5. Is this about experiment management?

If the answer is unclear, the design is probably still muddy.

## Bottom line

The package should grow by deepening layers, not by blurring them.
That is the main rule that keeps a prototype extensible.
