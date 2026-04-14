from __future__ import annotations

import pandas as pd

from fineval.backtest.monthly_runner import run_one_month


def _weights_to_series(weights: list[dict]) -> pd.Series:
    if not weights:
        return pd.Series(dtype=float)
    data = {row['ticker']: float(row['weight']) for row in weights}
    return pd.Series(data, dtype=float).sort_index()


def _turnover(prev_weights: pd.Series | None, current_weights: pd.Series) -> float | None:
    if prev_weights is None:
        return None
    union_index = prev_weights.index.union(current_weights.index)
    prev_aligned = prev_weights.reindex(union_index, fill_value=0.0)
    curr_aligned = current_weights.reindex(union_index, fill_value=0.0)
    return float((curr_aligned - prev_aligned).abs().sum())


def run_rolling_months(panel: pd.DataFrame, action_scores: pd.DataFrame, max_weight: float = 0.15) -> dict:
    monthly_results: list[dict] = []
    prev_weights: pd.Series | None = None

    for date in sorted(panel['date'].astype(str).unique().tolist()):
        month_panel = panel[panel['date'].astype(str) == date].copy()
        month_scores = action_scores[action_scores['date'].astype(str) == date].drop(columns=['date']).copy()
        one_month = run_one_month(month_panel, month_scores, max_weight=max_weight)
        current_weights = _weights_to_series(one_month['weights'])
        monthly_results.append(
            {
                'date': date,
                'portfolio_return': float(one_month['portfolio_return']),
                'n_positions': len(one_month['weights']),
                'turnover': _turnover(prev_weights, current_weights),
                'weights': one_month['weights'],
            }
        )
        prev_weights = current_weights

    returns = [row['portfolio_return'] for row in monthly_results]
    non_null_turnover = [row['turnover'] for row in monthly_results if row['turnover'] is not None]
    cumulative_return = 1.0
    for ret in returns:
        cumulative_return *= (1.0 + ret)
    cumulative_return -= 1.0

    return {
        'monthly_results': monthly_results,
        'summary': {
            'n_months': len(monthly_results),
            'mean_return': float(sum(returns) / len(returns)) if returns else 0.0,
            'cumulative_return': float(cumulative_return),
            'mean_turnover': float(sum(non_null_turnover) / len(non_null_turnover)) if non_null_turnover else None,
        },
    }
