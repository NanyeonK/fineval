from fineval.eval.fineval import decision_quality_score
from fineval.eval.reliability import reliability_score


def test_decision_quality_score_bounded():
    score = decision_quality_score({
        "structural_validity": 1.0,
        "temporal_integrity": 0.8,
        "robustness": 0.6,
        "economic_coherence": 0.9,
    })
    assert 0.0 <= score <= 1.0
    assert round(score, 4) == 0.8450


def test_reliability_score_bounded():
    score = reliability_score(0.7, 0.8, 0.6, 0.9)
    assert 0.0 <= score <= 1.0
    assert round(score, 4) == 0.7500
