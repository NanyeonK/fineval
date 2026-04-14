from __future__ import annotations


def reliability_score(self_conf: float, stability: float, agreement: float, evidence_conf: float, weights: tuple[float, float, float, float] = (0.25, 0.25, 0.25, 0.25)) -> float:
    vals = [self_conf, stability, agreement, evidence_conf]
    total = sum(w * v for w, v in zip(weights, vals))
    return max(0.0, min(1.0, total))
