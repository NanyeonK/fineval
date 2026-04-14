from __future__ import annotations

import json
import pandas as pd

from fineval.data.structured_block import load_structured_panel
from fineval.backtest.monthly_runner import run_one_month



def main() -> None:
    panel = load_structured_panel("data/toy/stock_month_panel.parquet")
    action_scores = pd.DataFrame([
        {"ticker": "AAPL", "bounded_action_score": 0.2},
        {"ticker": "MSFT", "bounded_action_score": 0.1},
        {"ticker": "NVDA", "bounded_action_score": 0.8},
        {"ticker": "JPM", "bounded_action_score": -0.1},
    ])
    out = run_one_month(panel, action_scores, max_weight=0.8)
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
