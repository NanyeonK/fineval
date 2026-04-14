# Prototype Expansion Roadmap

## Current status

`fineval` is no longer only a sketch, but it is still a prototype.
Current package strengths are:
- public package surface
- explicit report objects
- preset layer
- lightweight validation gates
- runnable toy example
- model-agnostic package boundary

Current limitations are:
- toy data only
- single-month toy runner
- no experiment registry or result store
- no benchmark suite over real decision-object corpora
- limited diagnostics for calibration, stability, and attribution
- no CI yet

The right expansion path is not to add more code everywhere.
The right path is to extend the package in layers while preserving the current clean boundaries.

## Expansion principle

Keep the package organized around a simple pipeline:

1. input contracts
2. evaluation primitives
3. translation into actionable signals
4. portfolio or decision validation
5. experiment-level reporting

Each new layer should make one part deeper without collapsing all layers together.

## Recommended expansion order

### Phase 1 — Realistic data contracts

Goal:
Move from toy examples into realistic, point-in-time research packets.

Add:
- richer text packet schemas
- point-in-time structured feature blocks
- explicit train/validation/test splits
- metadata for data provenance and as-of timestamps

Why first:
Most future evaluation claims depend on stronger input contracts.
If the input layer is weak, later metrics and backtests look cleaner than they really are.

Deliverables:
- production-style packet examples under `data/examples/`
- stronger loaders under `src/fineval/data/`
- docs for point-in-time packet contracts

### Phase 2 — Richer evaluation decomposition

Goal:
Make decision quality and reliability more informative than a single aggregate number.

Add:
- subscore families for factual grounding, temporal integrity, cross-source coherence, and actionability
- component-level diagnostics and failure flags
- optional score breakdown tables

Why second:
Right now the package can score.
Next it must explain why a decision scored the way it did.

Deliverables:
- richer report payloads
- breakdown helpers
- docs for metric interpretation

### Phase 3 — Multi-period validation runners

Goal:
Move from one-month toy validation into reproducible panel-level experiments.

Add:
- rolling month runners
- turnover tracking
- benchmark comparison hooks
- long-short and neutralized portfolio options if research scope needs them

Why third:
The package should first know how to score and explain a single decision packet well.
Then it can scale to multi-period validation.

Deliverables:
- `src/fineval/backtest/rolling_runner.py`
- cumulative return and turnover outputs
- experiment summary report objects

### Phase 4 — Benchmark datasets and baselines

Goal:
Evaluate decision objects against explicit baselines rather than in isolation.

Add:
- baseline strategies from structured-only signals
- baseline strategies from naive text rules
- benchmark registries for comparison by experiment

Why fourth:
A finance evaluation package becomes much more convincing when it can compare a candidate method against disciplined baselines automatically.

Deliverables:
- baseline registry
- benchmark comparison reports
- benchmark-facing example notebooks or scripts

### Phase 5 — Calibration and stability diagnostics

Goal:
Make confidence and reliability claims auditable.

Add:
- confidence calibration diagnostics
- cross-prompt or cross-model stability checks
- cross-source agreement diagnostics
- robustness sweeps over prompt or source perturbations

Why fifth:
This is where the package becomes more than a scoring wrapper.
It starts to evaluate whether a decision object is trustworthy under perturbation.

Deliverables:
- calibration plots or tables
- stability report object
- robustness preset family

### Phase 6 — Experiment management layer

Goal:
Support reproducible empirical work instead of ad hoc script runs.

Add:
- experiment config objects
- run manifests
- result directories with reproducible outputs
- machine-readable summaries for downstream paper workflows

Why sixth:
Once the metric and validation layers are richer, users need reproducible run orchestration.

Deliverables:
- `src/fineval/experiments/`
- standardized experiment output structure
- docs on run manifests and artifacts

### Phase 7 — Public package hardening

Goal:
Make the repo easier for outside researchers to adopt.

Add:
- CI
- contribution guide
- richer examples
- versioned release discipline
- issue templates and project metadata

Why seventh:
The repo is already public.
But public visibility is not the same as public usability.

Deliverables:
- `.github/workflows/ci.yml`
- `CONTRIBUTING.md`
- first public release tag after CI is green

## What should stay stable

These boundaries should remain stable while the package expands:

### Stable boundary 1 — model-agnostic core
Do not put Claude-specific or Codex-specific orchestration inside `src/fineval/`.

### Stable boundary 2 — explicit object model
Prefer explicit objects like reports, presets, datasets, and experiment configs over loose utility functions.

### Stable boundary 3 — package-first structure
New research logic should enter the package as reusable modules, not as project-local scripts first.

### Stable boundary 4 — point-in-time discipline
All new data-facing features should preserve point-in-time semantics and provenance metadata.

## Immediate next build wave

If development resumes now, the highest-return next wave is:

1. realistic packet contracts
2. richer score decomposition
3. rolling validation runner

That sequence keeps the package honest:
- stronger inputs
- better explanations
- more realistic validation

## Suggested milestone map

### Milestone A — Research-grade input layer
Definition:
- realistic packet schemas
- provenance fields
- stronger data docs

### Milestone B — Explainable evaluation layer
Definition:
- report breakdowns
- component diagnostics
- interpretable failure modes

### Milestone C — Reproducible experiment layer
Definition:
- rolling experiments
- baseline comparisons
- stable result manifests

### Milestone D — External adoption layer
Definition:
- CI
- contribution docs
- public release rhythm

## Bottom line

The prototype is already useful because it proves the package shape.
The next objective is not to make it bigger at random.
The next objective is to make it deeper in the following order:
- realistic inputs
- explainable scoring
- multi-period validation
- baseline comparison
- calibration and robustness
- experiment management
- public package polish
