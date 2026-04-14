from __future__ import annotations

from pathlib import Path

import pandas as pd


REQUIRED_STRUCTURED_COLUMNS = {"date", "ticker", "ret_fwd_1m", "size", "value", "mom", "vol", "sector"}


def load_structured_panel(path: str | Path) -> pd.DataFrame:
    df = pd.read_parquet(path)
    missing = REQUIRED_STRUCTURED_COLUMNS.difference(df.columns)
    if missing:
        raise ValueError(f"missing required structured columns: {sorted(missing)}")
    return df
