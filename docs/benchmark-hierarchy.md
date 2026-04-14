# Benchmark Hierarchy

## Purpose

`fineval` should not compare itself against only one weak benchmark.
The validation layer should compare strategy families against a hierarchy of baselines with increasing difficulty.

The right structure is:
- B0: `1/n`
- B1: static factor benchmark
- B2: enriched static factor benchmark (`FF6 + BAB + QMJ`)
- B3: DOI-style volatility-managed multifactor benchmark
- T-tier: `fineval` strategy family

## Why a hierarchy is needed

A single benchmark often answers only one objection.
A hierarchy answers several objections in order:
- Is the strategy better than naive diversification?
- Is it better than standard factor exposure?
- Is it better than a richer factor-only specification?
- Is it better than a sophisticated factor-timing competitor?

This is especially important for `fineval`, because its claim is not just that text can produce a signal.
Its claim is that evaluated and reliability-aware text decisions add incremental value beyond standard structured alternatives.

## B0 — Equal-weight benchmark

Definition:
- naive `1/n` portfolio across the investable universe

Why include it:
- interpretable low-bar baseline
- useful for intuitive performance comparison
- standard reader-friendly benchmark

What it does not test:
- whether text adds value beyond factor models
- whether `fineval` beats other intelligent allocation rules

## B1 — Static factor benchmark

Definition:
- factor-only benchmark with no text inputs
- first practical version can use `FF6`

Why include it:
- isolates whether standard factor structure explains the returns already
- gives a simple structured-only comparator before adding more factors

## B2 — Enriched static factor benchmark

Definition:
- `FF6 + BAB + QMJ`

Why this is the main factor-only comparator:
- `FF6` gives standard market, size, value, profitability, investment, and momentum coverage
- `BAB` adds defensive / low-beta structure
- `QMJ` adds explicit quality structure

Why it matters:
- if `fineval` cannot beat this tier, then its incremental value claim is weak
- if it can, the claim becomes much more convincing

## B3 — DOI-style sophisticated benchmark

Anchor paper:
- DOI `10.1111/jofi.13395`
- `A Multifactor Perspective on Volatility-Managed Portfolios`

Role:
- high-bar benchmark
- sophisticated factor-timing competitor

Why not make it the only benchmark:
- the research question is not identical to `fineval`
- the DOI benchmark is about multifactor and volatility-managed allocation, not text-based decision evaluation
- therefore it should be treated as a strong alternative comparator, not the only main benchmark

## T-tier — fineval strategies

The `fineval` family should include, at minimum:
- raw text signal
- quality-adjusted text signal
- reliability-adjusted text signal
- hybrid text + structured signal

Optional later robustness tier:
- volatility-managed fineval hybrid

## Fair comparison rules

All benchmark tiers should use, as much as possible:
- the same investable universe
- the same rebalance frequency
- the same date alignment
- the same return definition
- the same transaction-cost convention when costs are added

Without these controls, benchmark comparisons become difficult to interpret.

## Current implementation order

The correct implementation order is:
1. document the hierarchy
2. ingest AQR BAB/QMJ
3. build static factor benchmark layer
4. build DOI-style volatility-managed benchmark
5. compare benchmark tiers against `fineval`

## Current recommendation

At the present stage, the most important benchmark to implement first is not the DOI-style benchmark.
It is the enriched static factor comparator:
- `FF6 + BAB + QMJ`

Reason:
- it is closer to the immediate incremental-value question
- it is simpler to implement cleanly
- it creates a solid factor-only baseline before adding a more sophisticated timing competitor

## Bottom line

The benchmark story should not be:
- `fineval` versus one weak benchmark

It should be:
- `fineval` versus a benchmark ladder

That ladder should move from:
- naive diversification
- to standard factor exposure
- to enriched factor exposure
- to sophisticated factor timing

Only then is it clear what kind of value `fineval` actually adds.
