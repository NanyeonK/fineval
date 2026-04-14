import pytest

from fineval.schemas.decision_object import FinancialDecisionObject


def valid_payload():
    return {
        "view_id": "rv_001",
        "timestamp": "2024-01-31T00:00:00Z",
        "model": "test-model",
        "prompt_version": "v1",
        "view_type": "relative",
        "horizon": {"unit": "month", "value": 1},
        "target_universe": ["NVDA", "JPM"],
        "statement": "NVDA should outperform JPM over the next month.",
        "evidence_bundle": [{"type": "news", "source_id": "n1", "source_summary": "chip demand strong", "relevance": "supports tech strength"}],
        "view_payload": {"long_asset": "NVDA", "short_asset": "JPM", "relation": "outperform", "target_metric": "relative_return", "expected_spread": 0.05, "direction_only": False},
        "confidence": {"score": 0.7, "scale": "0_to_1", "confidence_type": "model_judgement", "calibration_status": "uncalibrated", "reason": "aligned evidence", "uncertainty_notes": "macro shock risk"},
        "audit": {"generated_from": "prompt + evidence bundle"},
    }


def test_valid_financial_decision_object():
    obj = FinancialDecisionObject(**valid_payload())
    assert obj.view_payload.long_asset == "NVDA"


def test_requires_evidence():
    payload = valid_payload()
    payload["evidence_bundle"] = []
    with pytest.raises(Exception):
        FinancialDecisionObject(**payload)


def test_rejects_implausible_spread():
    payload = valid_payload()
    payload["view_payload"]["expected_spread"] = 0.40
    with pytest.raises(Exception):
        FinancialDecisionObject(**payload)
