from __future__ import annotations

from dataclasses import dataclass

from fineval.eval.reliability import reliability_breakdown
from fineval.reports.base import BaseReport


@dataclass
class ReliabilityReport(BaseReport):
    components: dict[str, float]
    weights: dict[str, float]
    weighted_components: dict[str, float]
    flags: list[str]

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
        components = {
            'self_conf': self_conf,
            'stability': stability,
            'agreement': agreement,
            'evidence_conf': evidence_conf,
        }
        mapped_weights = {
            'self_conf': weights[0],
            'stability': weights[1],
            'agreement': weights[2],
            'evidence_conf': weights[3],
        }
        breakdown = reliability_breakdown(components, weights=mapped_weights)
        return cls(
            report_type='reliability',
            score=breakdown['score'],
            components=dict(components),
            weights=dict(breakdown['weights']),
            weighted_components=dict(breakdown['weighted_components']),
            flags=list(breakdown['flags']),
        )
