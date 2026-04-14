# AQR Ingestion Implementation Plan

> For Hermes: execute this plan in order with strict TDD. Write the failing test first, verify RED, implement minimal code, verify GREEN, then push.

## Goal

Turn the downloaded AQR monthly BAB and QMJ workbooks into normalized processed factor files that `fineval` can use as benchmark inputs.

## Why this plan now

The benchmark hierarchy is already fixed:
- `1/n`
- static factor benchmark
- `FF6 + BAB + QMJ`
- DOI-style volatility-managed benchmark
- `fineval` strategy family

To build the static `FF6 + BAB + QMJ` comparator, BAB and QMJ must first be normalized into reproducible machine-readable files.

## Current raw assets

Already available in the repo:
- `data/external/aqr_raw/bab_monthly_aqr.xlsx`
- `data/external/aqr_raw/qmj_monthly_aqr.xlsx`

Observed workbook structure:
- BAB sheet name: `BAB Factors`
- QMJ sheet name: `QMJ Factors`
- header row begins at row 19
- data columns include:
  - `DATE`
  - country columns including `USA`
  - aggregate columns including:
    - `Global`
    - `Global Ex USA`
    - `Europe`
    - `North America`
    - `Pacific`

## Scope

In scope:
- parse the two AQR monthly workbooks
- extract selected monthly series
- normalize dates and column names
- save processed files under `data/external/aqr_processed/`
- add tests for parsing and processed file shape

Out of scope:
- DB ingestion
- factor benchmark construction
- DOI-style volatility-managed benchmark

## Target outputs

### Processed files
- `data/external/aqr_processed/bab_monthly.parquet`
- `data/external/aqr_processed/qmj_monthly.parquet`

### Expected columns
- `date`
- `usa`
- `global`
- `global_ex_usa`
- `europe`
- `north_america`
- `pacific`

## Files

### Create
- `src/fineval/benchmarks/aqr_ingestion.py`
- `tests/test_aqr_factor_ingestion.py`
- `docs/aqr-factor-ingestion.md`

### Modify
- `docs/README.md`
- `README.md`

## Task 1 — Add failing ingestion tests

Objective:
Define the parsing/output contract before implementing the loader.

Tests should verify:
- workbook parser reads the expected columns from BAB
- workbook parser reads the expected columns from QMJ
- parsed `date` column is monotone and non-null
- `usa` column exists
- processed DataFrame contains normalized lowercase names

Verification command:
- `PYTHONPATH=src pytest tests/test_aqr_factor_ingestion.py -q`
Expected before implementation:
- FAIL because ingestion module does not exist

## Task 2 — Implement workbook parser

Objective:
Build a parser for AQR monthly factor sheets.

File:
- `src/fineval/benchmarks/aqr_ingestion.py`

Required functions:
- `load_aqr_monthly_sheet(path, sheet_name) -> pd.DataFrame`
- `normalize_aqr_monthly_columns(df) -> pd.DataFrame`
- `save_aqr_processed_factors() -> dict[str, str]`

Behavior:
- read header from row 19
- drop trailing blank column
- rename columns to snake_case
- convert `DATE` to a month-end timestamp or pandas datetime
- keep only selected columns
- preserve NaNs where AQR has no early coverage

## Task 3 — Save processed files

Objective:
Materialize normalized parquet outputs for BAB and QMJ.

Output directory:
- `data/external/aqr_processed/`

Verification:
- processed parquet files exist
- row counts are positive
- columns match expected output contract

## Task 4 — Document ingestion contract

Objective:
Explain source workbooks and processed outputs.

File:
- `docs/aqr-factor-ingestion.md`

Should cover:
- source files
- selected sheet names
- selected output columns
- why `USA` is the default main series and global aggregates are kept for robustness

## Verification gate

At the end of this plan:
- `tests/test_aqr_factor_ingestion.py` passes
- processed BAB and QMJ parquet files exist
- `PYTHONPATH=src pytest tests -q` passes
- docs point to the ingestion layer

## Next step after this plan

After ingestion lands:
- build the static `FF6 + BAB + QMJ` benchmark layer
