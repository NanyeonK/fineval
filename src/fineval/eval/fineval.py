from __future__ import annotations


def bounded_mean(values: list[float]) -> float:
    if not values:
        return 0.0
    return max(0.0, min(1.0, sum(values) / len(values)))


def _default_decision_quality_weights() -> dict[str, float]:
    return {
        'structural_validity': 0.25,
        'temporal_integrity': 0.20,
        'robustness': 0.20,
        'economic_coherence': 0.35,
    }


def decision_quality_breakdown(metrics: dict[str, float], weights: dict[str, float] | None = None) -> dict:
    resolved_weights = weights or _default_decision_quality_weights()
    weighted_components = {key: resolved_weights[key] * metrics[key] for key in resolved_weights}
    score = max(0.0, min(1.0, sum(weighted_components.values())))
    flags = []
    if metrics.get('temporal_integrity', 1.0) < 0.4:
        flags.append('low_temporal_integrity')
    if metrics.get('robustness', 1.0) < 0.4:
        flags.append('low_robustness')
    return {
        'score': score,
        'components': dict(metrics),
        'weights': dict(resolved_weights),
        'weighted_components': weighted_components,
        'flags': flags,
    }


def decision_quality_score(metrics: dict[str, float], weights: dict[str, float] | None = None) -> float:
    return float(decision_quality_breakdown(metrics, weights=weights)['score'])
