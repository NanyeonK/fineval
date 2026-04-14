from __future__ import annotations


def map_view_to_action_score(expected_spread: float, dq: float, rl: float, confidence: float, max_abs_score: float = 1.0) -> dict:
    raw = expected_spread * dq * rl
    conf_mult = 0.5 + 0.5 * confidence
    bounded = max(-max_abs_score, min(max_abs_score, raw * conf_mult * 10.0))
    return {
        "raw_action_score": raw,
        "confidence_multiplier": conf_mult,
        "bounded_action_score": bounded,
    }
