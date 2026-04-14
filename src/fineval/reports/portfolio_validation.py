from __future__ import annotations

from dataclasses import dataclass

from fineval.reports.base import BaseReport


@dataclass
class PortfolioValidationReport(BaseReport):
    portfolio_return: float
    n_positions: int
    weight_sum: float
    long_only: bool
    max_weight_observed: float
    max_weight_ok: bool

    @classmethod
    def from_backtest_result(
        cls,
        result: dict,
        *,
        max_weight: float,
    ) -> 'PortfolioValidationReport':
        weights = result.get('weights', [])
        raw_weights = [float(row['weight']) for row in weights]
        weight_sum = float(sum(raw_weights))
        max_weight_observed = max(raw_weights, default=0.0)
        return cls(
            report_type='portfolio_validation',
            score=None,
            portfolio_return=float(result.get('portfolio_return', 0.0)),
            n_positions=len(weights),
            weight_sum=weight_sum,
            long_only=all(weight >= 0.0 for weight in raw_weights),
            max_weight_observed=max_weight_observed,
            max_weight_ok=max_weight_observed <= max_weight,
        )
