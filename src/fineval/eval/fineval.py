from __future__ import annotations


def bounded_mean(values: list[float]) -> float:
    if not values:
        return 0.0
    return max(0.0, min(1.0, sum(values) / len(values)))


def decision_quality_score(metrics: dict[str, float], weights: dict[str, float] | None = None) -> float:
    weights = weights or {
        "structural_validity": 0.25,
        "temporal_integrity": 0.20,
        "robustness": 0.20,
        "economic_coherence": 0.35,
    }
    total = sum(weights[k] * metrics[k] for k in weights)
    return max(0.0, min(1.0, total))
