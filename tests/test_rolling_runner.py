import pandas as pd

from fineval.backtest.rolling_runner import run_rolling_months



def make_two_month_panel() -> pd.DataFrame:
    return pd.DataFrame([
        {'date': '2024-01-31', 'ticker': 'AAPL', 'ret_fwd_1m': 0.03},
        {'date': '2024-01-31', 'ticker': 'MSFT', 'ret_fwd_1m': 0.01},
        {'date': '2024-02-29', 'ticker': 'AAPL', 'ret_fwd_1m': 0.02},
        {'date': '2024-02-29', 'ticker': 'MSFT', 'ret_fwd_1m': 0.04},
    ])



def test_run_rolling_months_returns_monthly_results_and_summary():
    panel = make_two_month_panel()
    action_scores = pd.DataFrame([
        {'date': '2024-01-31', 'ticker': 'AAPL', 'bounded_action_score': 0.8},
        {'date': '2024-01-31', 'ticker': 'MSFT', 'bounded_action_score': 0.2},
        {'date': '2024-02-29', 'ticker': 'AAPL', 'bounded_action_score': 0.8},
        {'date': '2024-02-29', 'ticker': 'MSFT', 'bounded_action_score': 0.2},
    ])
    out = run_rolling_months(panel, action_scores, max_weight=0.8)
    assert len(out['monthly_results']) == 2
    assert out['summary']['n_months'] == 2
    assert out['monthly_results'][0]['turnover'] is None
    assert round(out['monthly_results'][1]['turnover'], 6) == 0.0



def test_run_rolling_months_detects_weight_change_turnover():
    panel = make_two_month_panel()
    action_scores = pd.DataFrame([
        {'date': '2024-01-31', 'ticker': 'AAPL', 'bounded_action_score': 0.8},
        {'date': '2024-01-31', 'ticker': 'MSFT', 'bounded_action_score': 0.2},
        {'date': '2024-02-29', 'ticker': 'AAPL', 'bounded_action_score': 0.2},
        {'date': '2024-02-29', 'ticker': 'MSFT', 'bounded_action_score': 0.8},
    ])
    out = run_rolling_months(panel, action_scores, max_weight=0.8)
    assert out['monthly_results'][1]['turnover'] > 0.0
    assert round(out['summary']['cumulative_return'], 6) == 0.062936
