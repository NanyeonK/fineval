# FINEVAL API Overview

## Public top-level imports

from fineval import (
    FinancialDecisionObject,
    DecisionDefinition,
    DecisionDataset,
    DecisionQualityReport,
    ReliabilityReport,
    PortfolioValidationReport,
    TestSuite,
)

## Presets

from fineval.presets import DecisionQualityPreset, PortfolioValidationPreset

## Object roles

FinancialDecisionObject
- Schema object for LLM- or human-generated investment decision records.

DecisionDefinition
- Dataset schema/config object describing ticker, date, and target column conventions.

DecisionDataset
- Thin dataset wrapper around a stock-month panel with schema metadata.

DecisionQualityReport
- Structured report over decision-quality metrics such as structural validity, temporal integrity, robustness, and economic coherence.

ReliabilityReport
- Structured report over confidence and reliability components such as self confidence, stability, agreement, and evidence confidence.

PortfolioValidationReport
- Structured report over toy backtest outputs such as portfolio return, number of positions, total weight, long-only status, and max-weight compliance.

TestSuite
- Lightweight threshold-check runner over report payloads.
- Supported first-pass operators: >=, <=, ==

## Recommended workflow

1. build or load a decision object or structured panel
2. evaluate the default decision-quality preset
3. build a reliability report
4. run the backtest
5. evaluate the portfolio-validation preset
6. run threshold checks with TestSuite

## Boundary rule

Core package is model-agnostic.
Do not put Claude-only or Codex-only prompting or orchestration inside src/fineval.
Runtime-specific wrappers should stay outside the core package.
