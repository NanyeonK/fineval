from __future__ import annotations

from dataclasses import dataclass

from fineval.eval.fineval import decision_quality_breakdown
from fineval.reports.base import BaseReport


@dataclass
class DecisionQualityReport(BaseReport):
    metrics: dict[str, float]
    weights: dict[str, float]
    weighted_components: dict[str, float]
    flags: list[str]

    @classmethod
    def from_metrics(
        cls,
        metrics: dict[str, float],
        weights: dict[str, float] | None = None,
    ) -> 'DecisionQualityReport':
        breakdown = decision_quality_breakdown(metrics, weights=weights)
        return cls(
            report_type='decision_quality',
            score=breakdown['score'],
            metrics=dict(metrics),
            weights=dict(breakdown['weights']),
            weighted_components=dict(breakdown['weighted_components']),
            flags=list(breakdown['flags']),
        )
