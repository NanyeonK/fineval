from __future__ import annotations

import pandas as pd



def long_only_allocator(scores: pd.Series, max_weight: float = 0.15) -> pd.Series:
    positive = scores.clip(lower=0)
    if positive.sum() == 0:
        return pd.Series(1.0 / len(scores), index=scores.index)
    weights = positive / positive.sum()
    weights = weights.clip(upper=max_weight)
    weights = weights / weights.sum()
    return weights
