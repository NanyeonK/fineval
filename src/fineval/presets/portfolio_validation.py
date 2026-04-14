from __future__ import annotations

from dataclasses import dataclass

from fineval.reports.portfolio_validation import PortfolioValidationReport


@dataclass
class PortfolioValidationPreset:
    name: str
    max_weight: float

    @classmethod
    def default(cls, max_weight: float = 0.15) -> 'PortfolioValidationPreset':
        return cls(name='default', max_weight=max_weight)

    def evaluate(self, result: dict) -> PortfolioValidationReport:
        return PortfolioValidationReport.from_backtest_result(result, max_weight=self.max_weight)
