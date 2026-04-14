# Wave 1 Implementation Spec

> Goal: move `fineval` from a clean prototype into the first research-grade extension wave by upgrading three weak points in order:
> 1. stronger point-in-time packet contracts
> 2. richer score decomposition
> 3. rolling multi-period validation

## Why this wave comes first

The current prototype already proves package shape, but it is still weak in three places:
- input contracts are toy-level
- score outputs are too aggregated
- validation is only one-month and toy-scale

If we expand in the wrong order, the package will look more advanced than it really is.
This wave fixes the foundations first.

## Scope

In scope:
- richer monthly packet schema and loader validation
- decomposition-aware decision-quality and reliability scoring
- richer report payloads with breakdowns and flags
- rolling validation runner over multi-month panels
- docs and tests for the new contracts

Out of scope:
- CI
- benchmark registry
- calibration plots
- experiment management framework
- public release tagging

## Deliverables

### Deliverable A — stronger packet contracts
Add a richer packet schema with explicit provenance and point-in-time fields.

Target additions:
- source-level metadata
- packet-level provenance
- point-in-time validation helpers
- stricter loader checks

### Deliverable B — richer score decomposition
Add explicit component decomposition instead of only scalar scores.

Target additions:
- subscore computation helpers
- structured breakdown payloads
- diagnostic flags for weak components

### Deliverable C — rolling validation runner
Add a multi-period runner for panel experiments.

Target additions:
- month-by-month execution over a panel
- cumulative and average return summaries
- turnover tracking
- monthly result records

## File plan

### New files
- `src/fineval/data/contracts.py`
- `src/fineval/backtest/rolling_runner.py`
- `tests/test_packet_contracts.py`
- `tests/test_score_breakdowns.py`
- `tests/test_rolling_runner.py`
- `docs/input-contracts.md`
- `docs/metric-breakdowns.md`

### Files to modify
- `src/fineval/data/monthly_packet.py`
- `src/fineval/eval/fineval.py`
- `src/fineval/eval/reliability.py`
- `src/fineval/reports/decision_quality.py`
- `src/fineval/reports/reliability.py`
- `src/fineval/backtest/__init__.py` if added later
- `docs/README.md`
- `README.md`

## Design details

### A. Stronger packet contracts

#### Current weakness
Current packet loader is too permissive:
- `MonthlyTextPacket` only has ticker, date, packet_id, sources
- `sources` is just `list[dict]`
- there is no provenance or validation beyond published date filtering

#### Target object model

Introduce explicit dataclasses for packet contracts.

Suggested objects:
- `PacketSource`
- `PacketProvenance`
- `MonthlyTextPacket`

Suggested fields:

`PacketSource`
- `source_id: str`
- `source_type: str`
- `published_at: str`
- `text: str`
- `author: str | None = None`
- `provider: str | None = None`
- `title: str | None = None`
- `url: str | None = None`
- `as_of_date: str | None = None`
- `metadata: dict | None = None`

`PacketProvenance`
- `built_at: str`
- `builder: str`
- `source_count: int`
- `dataset_version: str | None = None`
- `notes: str | None = None`

`MonthlyTextPacket`
- `ticker: str`
- `as_of_date: str`
- `packet_id: str`
- `sources: list[PacketSource]`
- `provenance: PacketProvenance | None = None`
- `metadata: dict | None = None`

#### Required helper functions
- `validate_packet_point_in_time(packet)`
  - every source `published_at <= packet.as_of_date`
- `validate_packet_source_count(packet)`
  - provenance count must match actual source count if provenance exists
- `packet_to_dict(packet)` for report/debug convenience

#### Loader behavior
Update `load_packet_examples()` so it:
- parses dict records into explicit dataclasses
- validates required fields
- raises clear `ValueError` on missing or invalid contracts

#### Test cases
Add tests for:
- successful parse of richer packet records
- failure when required source field is missing
- failure when a source is published after `as_of_date`
- failure when provenance source count mismatches

### B. Richer score decomposition

#### Current weakness
Current scoring functions only return scalar aggregates:
- `decision_quality_score(metrics)` -> float
- `reliability_score(...)` -> float

This is too thin for diagnosis.

#### Target behavior
Add decomposition helpers that preserve both aggregate and components.

Suggested functions:
- `decision_quality_breakdown(metrics, weights=None) -> dict`
- `reliability_breakdown(components, weights=None) -> dict`

#### Suggested output shape

Decision quality breakdown:
- `score`
- `components`
- `weights`
- `weighted_components`
- `flags`

Reliability breakdown:
- `score`
- `components`
- `weights`
- `weighted_components`
- `flags`

#### Flag logic
Add simple first-pass failure flags such as:
- `low_temporal_integrity`
- `low_robustness`
- `low_agreement`
- `low_evidence_confidence`

Rule style:
- flag any component below a threshold like `0.4`
- keep thresholds explicit and documented

#### Report integration
Update reports so `to_dict()` includes breakdown content.

`DecisionQualityReport`
- `report_type`
- `score`
- `metrics`
- `weights`
- `weighted_components`
- `flags`

`ReliabilityReport`
- `report_type`
- `score`
- `components`
- `weights`
- `weighted_components`
- `flags`

#### Test cases
Add tests for:
- expected weighted component values
- score remains bounded
- low-component flags appear correctly
- report payloads expose breakdowns

### C. Rolling multi-period validation runner

#### Current weakness
The package only has:
- `run_one_month(panel, action_scores)`

This is not enough for realistic empirical evaluation.

#### Target behavior
Add a rolling runner that works over multiple month observations.

Suggested function:
- `run_rolling_months(panel, action_scores, max_weight=0.15) -> dict`

Assumptions for first version:
- `panel` contains repeated months by `date`
- `action_scores` contains one row per `date, ticker`
- runner loops over sorted dates
- each month reuses current allocator and one-month return logic

#### Suggested output shape
- `monthly_results`
  - list of month records with:
    - `date`
    - `portfolio_return`
    - `n_positions`
    - `turnover`
- `summary`
  - `n_months`
  - `mean_return`
  - `cumulative_return`
  - `mean_turnover`

#### Turnover logic
For first version:
- turnover at month t = sum(abs(w_t - w_{t-1}))
- first month turnover = 1.0 or `None`
- choose one and document it explicitly

Recommended first version:
- first month turnover = `None`
- summary mean_turnover computed over non-null months only

#### Test cases
Add tests for:
- two-month toy panel runs successfully
- monthly result count matches number of dates
- cumulative return is computed deterministically
- turnover is zero when weights do not change
- turnover is positive when weights change

## Documentation additions

### `docs/input-contracts.md`
Should explain:
- packet schema
- source-level required fields
- provenance expectations
- point-in-time validation rules

### `docs/metric-breakdowns.md`
Should explain:
- scalar score vs breakdown
- flag logic
- interpretation of weighted components

### README/docs index updates
Add links to the new docs and describe Wave 1 as the first post-prototype build wave.

## Recommended execution order

1. packet contract dataclasses and validation
2. loader upgrade and packet tests
3. decision-quality breakdown helpers
4. reliability breakdown helpers
5. report payload expansion
6. rolling runner tests
7. rolling runner implementation
8. input-contract docs
9. metric-breakdown docs
10. full verification and push

## Verification gate

At the end of Wave 1, all of the following should be true:
- packet loader rejects invalid point-in-time records
- reports expose breakdowns and flags, not only scalar scores
- rolling runner works over multi-month toy data
- docs explain the new packet and metric contracts
- `PYTHONPATH=src pytest tests -q` passes

## Future handoff

After Wave 1 lands, the next wave should be:
- benchmark registry
- calibration/stability diagnostics
- experiment management

That keeps the roadmap sequence intact and avoids architecture drift.
