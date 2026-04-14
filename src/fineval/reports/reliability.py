from __future__ import annotations

from dataclasses import dataclass

from fineval.eval.reliability import reliability_score
from fineval.reports.base import BaseReport


@dataclass
class ReliabilityReport(BaseReport):
    components: dict[str, float]
    weights: tuple[float, float, float, float]

    @classmethod
    def from_components(
        cls,
        *,
        self_conf: float,
        stability: float,
        agreement: float,
        evidence_conf: float,
        weights: tuple[float, float, float, float] = (0.25, 0.25, 0.25, 0.25),
    ) -> 'ReliabilityReport':
        score = reliability_score(
            self_conf=self_conf,
            stability=stability,
            agreement=agreement,
            evidence_conf=evidence_conf,
            weights=weights,
        )
        return cls(
            report_type='reliability',
            score=score,
            components={
                'self_conf': self_conf,
                'stability': stability,
                'agreement': agreement,
                'evidence_conf': evidence_conf,
            },
            weights=weights,
        )
