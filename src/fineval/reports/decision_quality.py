from __future__ import annotations

from dataclasses import dataclass

from fineval.eval.fineval import decision_quality_score
from fineval.reports.base import BaseReport


@dataclass
class DecisionQualityReport(BaseReport):
    metrics: dict[str, float]
    weights: dict[str, float]

    @classmethod
    def from_metrics(
        cls,
        metrics: dict[str, float],
        weights: dict[str, float] | None = None,
    ) -> 'DecisionQualityReport':
        resolved_weights = weights or {
            'structural_validity': 0.25,
            'temporal_integrity': 0.20,
            'robustness': 0.20,
            'economic_coherence': 0.35,
        }
        score = decision_quality_score(metrics, weights=resolved_weights)
        return cls(
            report_type='decision_quality',
            score=score,
            metrics=dict(metrics),
            weights=dict(resolved_weights),
        )
