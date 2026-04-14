# Validation Expansion Implementation Plan

> For Hermes: execute this plan task-by-task with strict TDD. Write the failing test first, verify RED, implement minimal code, verify GREEN, then push.

## Goal

Extend `fineval` from toy single-month validation into a first reproducible multi-period validation layer that better matches the empirical design stated in `plan_04_14_1940.md`.

## Why now

The referenced plan prioritizes expansion in this order:
1. schema expansion
2. metric expansion
3. validation expansion

Schema expansion is already underway through stronger packet contracts.
Metric expansion is already underway through score breakdown diagnostics.
The next justified step is validation expansion.

## Scope

In scope for this plan:
- rolling multi-period validation runner
- monthly turnover tracking
- richer portfolio validation report from rolling output
- docs for validation outputs

Out of scope for this plan:
- factor-adjusted alpha regression
- spanning tests
- transaction cost model beyond simple placeholders
- benchmark registry
- experiment management framework

## Files

### Create
- `src/fineval/backtest/rolling_runner.py`
- `tests/test_rolling_runner.py`
- `docs/validation-layer.md`

### Modify
- `src/fineval/reports/portfolio_validation.py`
- `docs/README.md`
- `README.md`

## Task 1: Add failing tests for rolling validation

Objective:
Define the expected contract for multi-period validation before implementing it.

Tests to add in `tests/test_rolling_runner.py`:
- two-month panel runs successfully
- `monthly_results` count matches number of dates
- `summary.n_months` matches number of dates
- first month turnover is `None`
- turnover is zero when weights do not change
- turnover is positive when weights do change
- cumulative return is deterministic

Toy setup:
- use a small two-month panel with repeated tickers
- provide `action_scores` with `date, ticker, bounded_action_score`

Verification command:
- `PYTHONPATH=src pytest tests/test_rolling_runner.py -q`
Expected before implementation:
- FAIL due to missing rolling runner

## Task 2: Implement rolling runner

Objective:
Create a first-pass `run_rolling_months()` over sorted monthly panels.

File:
- `src/fineval/backtest/rolling_runner.py`

Required behavior:
- group panel by `date`
- for each date, merge same-date action scores
- call current one-month allocation logic on the month slice
- store per-month weights and returns
- compute turnover relative to previous month weights
- return:
  - `monthly_results`
  - `summary`

Suggested output contract:
- `monthly_results`
  - `date`
  - `portfolio_return`
  - `n_positions`
  - `turnover`
  - `weights`
- `summary`
  - `n_months`
  - `mean_return`
  - `cumulative_return`
  - `mean_turnover`

Verification command:
- `PYTHONPATH=src pytest tests/test_rolling_runner.py -q`
Expected after implementation:
- PASS

## Task 3: Expand portfolio validation report

Objective:
Allow `PortfolioValidationReport` to summarize either one-month or rolling validation outputs.

File:
- `src/fineval/reports/portfolio_validation.py`

Required additions:
- preserve current one-month fields for backward compatibility
- when rolling output is provided, include:
  - `n_months`
  - `mean_return`
  - `cumulative_return`
  - `mean_turnover`
- keep one-month path working for existing tests

Verification commands:
- `PYTHONPATH=src pytest tests/test_reports.py -q`
- full suite after all validation changes

## Task 4: Document validation layer

Objective:
Explain how the validation layer now progresses from one-month toy runs to rolling validation.

File:
- `docs/validation-layer.md`

Should cover:
- `run_one_month()`
- `run_rolling_months()`
- turnover definition
- summary output interpretation
- current limitations

Also update:
- `docs/README.md`
- `README.md`

## Task 5: Final verification

Run:
- `PYTHONPATH=src pytest tests -q`

Manual checks:
- rolling runner returns the expected monthly count
- turnover logic behaves as documented
- existing one-month validation is not broken
- validation docs are linked from repo docs

## Commit sequence

Recommended commit boundaries:
1. `test: add rolling validation runner contract`
2. `feat: add rolling validation runner`
3. `feat: expand portfolio validation report`
4. `docs: add validation layer docs`

## Next step after this plan

After this validation expansion lands, the next build wave should be:
- factor-adjusted validation outputs
- benchmark comparison layer
- experiment manifests and run artifacts
