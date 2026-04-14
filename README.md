# fineval

Finance-native evaluation framework for investment decision objects.

## What it is

fineval is a package-first research framework for turning investment decision objects into:
- decision-quality scores
- reliability summaries
- bounded action scores
- simple portfolio validation outputs
- reproducible threshold-based validation checks

The package is model-agnostic.
Claude Code, Codex, direct APIs, and human-curated annotations can all sit upstream as long as they produce a stable file and data contract.

## Current package surface

Top-level imports:
- FinancialDecisionObject
- DecisionDefinition
- DecisionDataset
- DecisionQualityReport
- ReliabilityReport
- PortfolioValidationReport
- TestSuite

Preset imports:
- DecisionQualityPreset
- PortfolioValidationPreset

## Install and run

Dependencies:
- Python 3.11+
- package requirements listed in pyproject.toml

Run prototype CLI:
- PYTHONPATH=src python3 -m fineval.cli.run_prototype

Run toy end-to-end example:
- PYTHONPATH=src python3 examples/toy_end_to_end.py

Run tests:
- PYTHONPATH=src pytest tests -q

## Repository status

This package is currently being prepared for split into an independent repository.
The code already follows a package-first layout and now includes a release-oriented README, license, changelog, examples, and docs.

## Docs

- docs/quickstart.md
- docs/api-overview.md
- docs/model_agnostic_runtime.md
- examples/README.md

## Current scope

Included now:
- stock-month toy panel workflow
- structured reports and presets
- lightweight validation gates
- runnable toy example

Out of scope for current release candidate:
- production dashboards
- cloud orchestration
- multi-model runtime logic inside core package
- large-scale empirical ingestion

## Design boundary

Keep runtime-specific prompting and orchestration outside src/fineval.
The core package should consume stable data objects, not model-specific transport logic.

## Working location

Current development location:
- /home/nanyeon99/project/llm_blackliterman

Planned next step:
- split fineval into an independent git repository with the public-facing subset only
