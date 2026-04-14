from fineval.eval.fineval import decision_quality_breakdown
from fineval.eval.reliability import reliability_breakdown
from fineval import DecisionQualityReport, ReliabilityReport


def test_decision_quality_breakdown_exposes_weighted_components_and_flags():
    breakdown = decision_quality_breakdown(
        {
            'structural_validity': 1.0,
            'temporal_integrity': 0.3,
            'robustness': 0.6,
            'economic_coherence': 0.9,
        }
    )
    assert round(breakdown['score'], 4) == 0.7450
    assert round(breakdown['weighted_components']['economic_coherence'], 4) == 0.3150
    assert 'low_temporal_integrity' in breakdown['flags']


def test_reliability_breakdown_exposes_weighted_components_and_flags():
    breakdown = reliability_breakdown(
        {
            'self_conf': 0.7,
            'stability': 0.3,
            'agreement': 0.6,
            'evidence_conf': 0.2,
        }
    )
    assert round(breakdown['score'], 4) == 0.4500
    assert round(breakdown['weighted_components']['self_conf'], 4) == 0.1750
    assert 'low_stability' in breakdown['flags']
    assert 'low_evidence_confidence' in breakdown['flags']


def test_decision_quality_report_includes_breakdown_fields():
    report = DecisionQualityReport.from_metrics(
        {
            'structural_validity': 1.0,
            'temporal_integrity': 0.3,
            'robustness': 0.6,
            'economic_coherence': 0.9,
        }
    )
    payload = report.to_dict()
    assert 'weighted_components' in payload
    assert 'flags' in payload
    assert payload['flags'] == ['low_temporal_integrity']


def test_reliability_report_includes_breakdown_fields():
    report = ReliabilityReport.from_components(
        self_conf=0.7,
        stability=0.3,
        agreement=0.6,
        evidence_conf=0.2,
    )
    payload = report.to_dict()
    assert 'weighted_components' in payload
    assert 'flags' in payload
    assert 'low_stability' in payload['flags']
