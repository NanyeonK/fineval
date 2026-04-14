from __future__ import annotations

import pandas as pd

from fineval.portfolio.allocator import long_only_allocator



def run_one_month(panel: pd.DataFrame, action_scores: pd.DataFrame, max_weight: float = 0.15) -> dict:
    merged = panel.merge(action_scores, on="ticker", how="left")
    merged["bounded_action_score"] = merged["bounded_action_score"].fillna(0.0)
    weights = long_only_allocator(merged.set_index("ticker")["bounded_action_score"], max_weight=max_weight)
    merged = merged.set_index("ticker")
    port_ret = float((weights * merged["ret_fwd_1m"]).sum())
    return {
        "weights": weights.rename("weight").reset_index().to_dict("records"),
        "portfolio_return": port_ret,
    }
