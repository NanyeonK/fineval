from __future__ import annotations


def _default_reliability_weights() -> dict[str, float]:
    return {
        'self_conf': 0.25,
        'stability': 0.25,
        'agreement': 0.25,
        'evidence_conf': 0.25,
    }


def reliability_breakdown(components: dict[str, float], weights: dict[str, float] | None = None) -> dict:
    resolved_weights = weights or _default_reliability_weights()
    weighted_components = {key: resolved_weights[key] * components[key] for key in resolved_weights}
    score = max(0.0, min(1.0, sum(weighted_components.values())))
    flags = []
    if components.get('stability', 1.0) < 0.4:
        flags.append('low_stability')
    if components.get('agreement', 1.0) < 0.4:
        flags.append('low_agreement')
    if components.get('evidence_conf', 1.0) < 0.4:
        flags.append('low_evidence_confidence')
    return {
        'score': score,
        'components': dict(components),
        'weights': dict(resolved_weights),
        'weighted_components': weighted_components,
        'flags': flags,
    }


def reliability_score(
    self_conf: float,
    stability: float,
    agreement: float,
    evidence_conf: float,
    weights: tuple[float, float, float, float] = (0.25, 0.25, 0.25, 0.25),
) -> float:
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
    return float(reliability_breakdown(components, weights=mapped_weights)['score'])
