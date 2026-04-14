from __future__ import annotations

from dataclasses import dataclass

from fineval.reports.base import BaseReport


@dataclass
class PortfolioValidationReport(BaseReport):
    portfolio_return: float | None
    n_positions: int | None
    weight_sum: float | None
    long_only: bool | None
    max_weight_observed: float | None
    max_weight_ok: bool | None
    n_months: int | None = None
    mean_return: float | None = None
    cumulative_return: float | None = None
    mean_turnover: float | None = None

    @classmethod
    def from_backtest_result(
        cls,
        result: dict,
        *,
        max_weight: float,
    ) -> 'PortfolioValidationReport':
        if 'monthly_results' in result and 'summary' in result:
            monthly_results = result.get('monthly_results', [])
            all_weights = [
                float(row['weight'])
                for month in monthly_results
                for row in month.get('weights', [])
            ]
            max_weight_observed = max(all_weights, default=0.0)
            latest_month = monthly_results[-1] if monthly_results else {}
            latest_weights = latest_month.get('weights', [])
            raw_weights = [float(row['weight']) for row in latest_weights]
            return cls(
                report_type='portfolio_validation',
                score=None,
                portfolio_return=float(latest_month.get('portfolio_return', 0.0)) if monthly_results else None,
                n_positions=len(latest_weights) if monthly_results else None,
                weight_sum=float(sum(raw_weights)) if monthly_results else None,
                long_only=all(weight >= 0.0 for weight in raw_weights) if monthly_results else None,
                max_weight_observed=max_weight_observed,
                max_weight_ok=max_weight_observed <= max_weight,
                n_months=int(result['summary'].get('n_months', 0)),
                mean_return=float(result['summary'].get('mean_return', 0.0)),
                cumulative_return=float(result['summary'].get('cumulative_return', 0.0)),
                mean_turnover=(
                    float(result['summary']['mean_turnover'])
                    if result['summary'].get('mean_turnover') is not None
                    else None
                ),
            )

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
