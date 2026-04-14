import pandas as pd

from fineval.backtest.monthly_runner import run_one_month



def test_toy_runner_smoke(toy_panel):
    action_scores = pd.DataFrame([
        {"ticker": "AAPL", "bounded_action_score": 0.2},
        {"ticker": "MSFT", "bounded_action_score": 0.1},
        {"ticker": "NVDA", "bounded_action_score": 0.8},
        {"ticker": "JPM", "bounded_action_score": -0.1},
    ])
    out = run_one_month(toy_panel, action_scores, max_weight=0.8)
    assert "portfolio_return" in out
    assert len(out["weights"]) == 4
