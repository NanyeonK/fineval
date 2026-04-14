from __future__ import annotations

from dataclasses import dataclass

from fineval.reports.decision_quality import DecisionQualityReport


@dataclass
class DecisionQualityPreset:
    name: str
    weights: dict[str, float]

    @classmethod
    def default(cls) -> 'DecisionQualityPreset':
        return cls(
            name='default',
            weights={
                'structural_validity': 0.25,
                'temporal_integrity': 0.20,
                'robustness': 0.20,
                'economic_coherence': 0.35,
            },
        )

    def evaluate(self, metrics: dict[str, float]) -> DecisionQualityReport:
        return DecisionQualityReport.from_metrics(metrics, weights=self.weights)
