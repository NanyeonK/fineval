from fineval.signals.text_score import text_score, adjusted_text_score
from fineval.signals.hybrid import hybrid_score
from fineval.translation.action_mapping import map_view_to_action_score


def test_text_score_formula():
    assert round(text_score(1.0, 0.0, 0.0), 4) == 0.5000


def test_adjusted_text_score_formula():
    assert round(adjusted_text_score(0.8, 0.5, 0.5), 4) == 0.2000


def test_hybrid_score_formula():
    assert round(hybrid_score(0.6, 0.2, lam=0.75), 4) == 0.5000


def test_action_mapping_bounded():
    out = map_view_to_action_score(expected_spread=0.05, dq=0.8, rl=0.9, confidence=0.7)
    assert out["bounded_action_score"] <= 1.0
    assert out["bounded_action_score"] > 0
