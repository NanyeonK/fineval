# Validation Layer

## Purpose

The validation layer is where `fineval` turns evaluated decision signals into portfolio-style validation outputs.

At the current stage, the validation layer supports two levels:
- one-month validation
- rolling multi-period validation

This is still a prototype validation layer, not the final empirical system described in the research plan.
But it now provides a clean bridge from decision scoring into reproducible portfolio diagnostics.

## Current validation modules

### `src/fineval/portfolio/allocator.py`
Role:
- convert bounded action scores into long-only portfolio weights

Current behavior:
- clips negative scores to zero
- normalizes positive scores
- caps by `max_weight`
- renormalizes to sum to one

### `src/fineval/backtest/monthly_runner.py`
Role:
- validate a single month of portfolio construction

Input:
- one-month panel
- one-month action scores by ticker

Output:
- `weights`
- `portfolio_return`

### `src/fineval/backtest/rolling_runner.py`
Role:
- validate multiple months in sequence

Input:
- multi-month panel
- action scores with `date, ticker, bounded_action_score`

Output:
- `monthly_results`
- `summary`

## One-month validation

Use `run_one_month()` when you want a minimal sanity check on:
- weight construction
- score-to-allocation mapping
- realized one-month portfolio return

Current output shape:
- `weights`
- `portfolio_return`

This is useful for:
- smoke tests
- debugging allocation logic
- validating one month in isolation

## Rolling validation

Use `run_rolling_months()` when you want a first-pass empirical validation over repeated months.

Current monthly output fields:
- `date`
- `portfolio_return`
- `n_positions`
- `turnover`
- `weights`

Current summary fields:
- `n_months`
- `mean_return`
- `cumulative_return`
- `mean_turnover`

## Turnover definition

Turnover is currently defined as:
- sum of absolute weight changes relative to the previous month
- computed over the union of tickers from both months

Rules:
- first month turnover = `None`
- summary `mean_turnover` is computed only over non-null months

This is a simple first-pass definition.
It is adequate for prototype validation but not yet a full transaction-cost model.

## Portfolio validation report

`PortfolioValidationReport` now supports two paths.

### One-month path
For one-month output, it reports:
- `portfolio_return`
- `n_positions`
- `weight_sum`
- `long_only`
- `max_weight_observed`
- `max_weight_ok`

### Rolling path
For rolling output, it additionally reports:
- `n_months`
- `mean_return`
- `cumulative_return`
- `mean_turnover`

It also evaluates `max_weight_observed` across all monthly weight records.

## What the validation layer does not do yet

Not implemented yet:
- factor-adjusted alpha regression
- spanning tests
- benchmark registry
- transaction-cost adjustments beyond turnover
- experiment manifest storage

Those belong to the next expansion waves.

## Recommended use order

1. start with one-month validation while debugging score translation
2. move to rolling validation for repeated-month behavior
3. only after that add factor-adjusted empirical validation

## Next validation-layer extensions

The next justified additions are:
- factor-model validation outputs
- benchmark comparison reports
- transaction-cost-aware summaries
- experiment-level validation artifacts

## Bottom line

The validation layer has moved beyond a toy one-shot run.
It now supports:
- single-month validation
- rolling multi-period validation
- report-level summaries for both

That is enough to support the first empirical extension wave while keeping the package structure clean.
