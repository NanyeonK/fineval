# Model-Agnostic Runtime Note

## Short Answer
Yes. `fineval` can be used from both Claude Code and Codex.

## Why
`fineval` is being built as a Python package, not as a model-specific agent skill.
The package does not need to know whether an upstream decision object came from:
- Claude Code
- Codex
- direct API calls
- batch JSON generation
- human-curated annotations

It only needs a valid, point-in-time input contract.

## Boundary Rule
Model runtimes generate or curate:
- text packets
- structured decision objects
- optional confidence metadata

`fineval` consumes:
- stock-month structured panel
- Financial Decision Objects
- configuration for evaluation and action mapping

This separation keeps the framework portable.

## Recommended Integration Pattern
### Upstream runtime layer
Either Claude Code or Codex may be used to:
1. read the monthly text packet
2. emit a `FinancialDecisionObject`
3. save it as JSON/JSONL

### Package layer
`fineval` then:
1. validates the object schema
2. computes FINEVAL scores
3. maps views into bounded action scores
4. runs constrained allocation and backtests
5. generates reports/tests later

## Required Practical Rule
Do not embed Claude-specific or Codex-specific prompting logic inside core package modules.

Allowed:
- `examples/claude_code_workflow.md`
- `examples/codex_workflow.md`
- thin wrappers outside `src/fineval/`

Not allowed inside core package:
- hard-coded Claude prompt templates
- Codex-only transport logic
- runtime-specific API assumptions

## Stable Shared Contract
To support both runtimes, keep the shared contract at the file/data level:
- point-in-time packet JSON
- Financial Decision Object JSON
- structured stock-month panel parquet/csv

This is the main portability mechanism.

## Current Conclusion
Using both Claude Code and Codex is feasible if `fineval` remains package-first and input-contract-first.
Core package stays model-agnostic. Runtime-specific wrappers stay outside the core package.
