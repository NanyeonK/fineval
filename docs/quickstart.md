# FINEVAL Quickstart

## Install dependencies

Run:
uv sync

If you are not using uv, install the package requirements from pyproject.toml into your environment.

## Run the toy prototype CLI

Run:
PYTHONPATH=src python3 -m fineval.cli.run_prototype

This runs the minimal one-month toy portfolio path and prints JSON with weights and portfolio return.

## Run the toy end-to-end example

Run:
PYTHONPATH=src python3 examples/toy_end_to_end.py

This example shows the current intended workflow:
1. load a stock-month toy panel
2. wrap it as a DecisionDataset
3. score decision quality with a preset
4. build a reliability report
5. run a toy one-month backtest
6. validate portfolio constraints with a preset
7. apply a lightweight TestSuite gate over report outputs

## Run tests

Run:
PYTHONPATH=src pytest tests -q

## Current package focus

fineval is a finance-native evaluation package for turning investment decision objects into:
- quality scores
- reliability summaries
- bounded action scores
- portfolio validation outputs
- reproducible threshold checks

It is package-first and model-agnostic. Claude Code, Codex, APIs, or human annotations may all generate upstream decision objects as long as the file and data contract is stable.
