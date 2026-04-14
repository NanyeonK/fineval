# Changelog

All notable changes to fineval will be documented in this file.

The format is based on Keep a Changelog.
Versioning is currently pre-release and follows the package version declared in pyproject.toml.

## [0.1.0] - 2026-04-14

Initial internal release candidate for independent repo split.

Added
- package-first src/fineval layout
- FinancialDecisionObject schema
- DecisionDefinition and DecisionDataset
- decision-quality and reliability scoring utilities
- bounded action mapping, allocator, and one-month backtest runner
- report objects:
  - DecisionQualityReport
  - ReliabilityReport
  - PortfolioValidationReport
- preset layer:
  - DecisionQualityPreset
  - PortfolioValidationPreset
- lightweight TestSuite threshold checks
- toy CLI entrypoint
- toy end-to-end example
- quickstart and API overview docs
- model-agnostic runtime guidance for Claude Code, Codex, and other upstream runtimes

Verified
- full test suite passing under PYTHONPATH=src pytest tests -q
