# DOI Benchmark Replication Plan

## Anchor paper

- DOI: `10.1111/jofi.13395`
- Title: `A Multifactor Perspective on Volatility-Managed Portfolios`
- Journal: *The Journal of Finance*

## Available reference assets

The benchmark is not being designed from the paper text alone.
A replication package has already been downloaded into the fineval workspace.

Reference assets currently available:
- published-version PDF
- replication package zip from Mendeley Data
- nested replication code package containing MATLAB scripts and data

Current local locations:
- benchmark package zip:
  - `data/external/benchmark_refs/doi13395_replication_package.zip`
- AQR factor workbooks:
  - `data/external/aqr_raw/bab_monthly_aqr.xlsx`
  - `data/external/aqr_raw/qmj_monthly_aqr.xlsx`

## What the replication package contains

Observed contents of the nested replication package:
- `ReplicationPackage/Code/`
- `ReplicationPackage/Data/MainDataRep.mat`
- `ReplicationPackage/Manuscript/`
- `ReplicationPackage/README.txt`

Important code files identified:
- `RunAllCodes.m`
- `JF_Table1.m`
- `JF_OOS_FFHXZBAB_Nonnegative_UMCvsCMV.m`
- `VMP_OOS_noshortconst_FFHXZBAB.m`
- `LoadFFHXZBAB_Long.m`

## What the package implies about the benchmark design

### Core data dependence
The MATLAB package loads a proprietary/prepared data object:
- `Data/MainDataRep.mat`

This means a perfect byte-for-byte replication is not the first target inside `fineval`.
The first target should be a faithful benchmark-style port of the benchmark logic using factors we can source cleanly.

### Factor set used in the paper package
From script names and code, the benchmark family uses a multifactor set that includes:
- Fama-French factors
- HXZ-related factors
- BAB
- unmanaged and managed factor variants

For `fineval`, the closest practical benchmark layer should start with:
- `FF6 + BAB + QMJ`

Reason:
- `FF6` is already available
- `BAB` and `QMJ` have now been downloaded from AQR
- this gives a transparent and reproducible factor benchmark without depending on proprietary `.mat` internals

### Volatility-managed structure in the code
Key logic from `VMP_OOS_noshortconst_FFHXZBAB.m`:
- factor returns are split into unmanaged and volatility-managed variants
- managed factor return is scaled by inverse volatility
- scaling uses a variance-normalization adjustment:
  - `ScaleVol = std(raw factor) / std(raw / volatility)`
- the script compares:
  - unmanaged factor
  - volatility-managed factor
  - optimization with and without transaction-cost awareness

### Portfolio construction orientation
The package is not a simple regression-only artifact.
It constructs portfolio returns from factor sleeves and compares:
- unmanaged portfolios
- volatility-managed portfolios
- cost-aware optimized multifactor combinations

This confirms that the DOI benchmark should be treated as a sophisticated factor-allocation competitor, not as a simple alpha-control regression only.

## fineval replication objective

The correct objective is not:
- rebuild the entire MATLAB package immediately

The correct objective is:
- build a `fineval` benchmark layer that is faithful to the benchmark class
- use reproducible inputs we can source and document
- preserve the benchmark hierarchy already adopted in the repo

## Recommended replication tiers

### Tier 1 — Minimal faithful comparator
Build a DOI-style volatility-managed benchmark over factors we can source directly:
- `FF6 + BAB + QMJ`

Target output:
- unmanaged factor bundle return
- volatility-managed factor bundle return
- gross and simple net-of-turnover versions

### Tier 2 — Cost-aware comparator
Add first-pass transaction-cost-aware comparison:
- turnover estimate from weight changes
- simple proportional cost deduction

### Tier 3 — Closer MATLAB-logic port
If needed later, port more of the MATLAB optimization logic:
- constrained multifactor combinations
- unmanaged mean-variance vs cost-aware mean-variance comparisons
- closer alignment with paper tables

## Files to add in fineval

### New docs
- `docs/doi-benchmark-replication-plan.md`

### New code modules
- `src/fineval/benchmarks/factor_data.py`
- `src/fineval/benchmarks/static_factor_benchmark.py`
- `src/fineval/benchmarks/vol_managed_factor_benchmark.py`

### New tests
- `tests/test_aqr_factor_ingestion.py`
- `tests/test_static_factor_benchmark.py`
- `tests/test_vol_managed_factor_benchmark.py`

## Implementation order

### Step 1 — AQR factor ingestion
Build normalized processed BAB/QMJ monthly files.

Goal:
- get clean `date`-indexed factor files from AQR workbooks
- select at least:
  - `USA`
  - `Global`
  - `Global Ex USA`

### Step 2 — Static factor benchmark
Build a static `FF6 + BAB + QMJ` benchmark.

Goal:
- create a factor-only benchmark series
- keep this simpler than the DOI-style benchmark

### Step 3 — Volatility-managed factor benchmark
Build the first DOI-style benchmark port.

Goal:
- add inverse-volatility scaling to factor sleeves
- normalize scaling so managed and unmanaged returns are comparable
- compare unmanaged vs managed bundle returns

### Step 4 — Cost-aware version
Add simple cost-aware reporting.

Goal:
- estimate turnover in factor weights
- compute gross vs net benchmark returns

## Design constraints

### Constraint 1 — Do not depend on opaque `.mat` data for the first benchmark layer
The replication package is useful for understanding logic, but the first public `fineval` benchmark should be reproducible from accessible factor series.

### Constraint 2 — Keep benchmark code simpler than strategy code when possible
Benchmark layers should clarify, not obscure.

### Constraint 3 — Preserve benchmark hierarchy
The DOI-style benchmark is a high-bar comparator.
It should not replace:
- `1/n`
- static factor baselines

## Immediate next task

The next concrete task should be:
- implement AQR factor ingestion into normalized processed files

After that:
- build static `FF6 + BAB + QMJ` benchmark
- then add DOI-style volatility-managed benchmark logic

## Bottom line

The replication package confirms that the DOI benchmark is both relevant and feasible.
But the clean `fineval` path is:
1. ingest BAB and QMJ cleanly
2. build static factor comparator
3. build DOI-style volatility-managed comparator
4. compare against `fineval` strategy family
