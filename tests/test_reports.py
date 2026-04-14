from fineval import DecisionQualityReport, PortfolioValidationReport, ReliabilityReport


def test_top_level_report_imports_exist():
    assert DecisionQualityReport is not None
    assert ReliabilityReport is not None
    assert PortfolioValidationReport is not None


def test_decision_quality_report_to_dict():
    report = DecisionQualityReport.from_metrics(
        {
            'structural_validity': 1.0,
            'temporal_integrity': 0.8,
            'robustness': 0.6,
            'economic_coherence': 0.9,
        }
    )
    payload = report.to_dict()
    assert payload['report_type'] == 'decision_quality'
    assert round(payload['score'], 4) == 0.8450
    assert payload['metrics']['economic_coherence'] == 0.9


def test_reliability_report_to_dict():
    report = ReliabilityReport.from_components(
        self_conf=0.7,
        stability=0.8,
        agreement=0.6,
        evidence_conf=0.9,
    )
    payload = report.to_dict()
    assert payload['report_type'] == 'reliability'
    assert round(payload['score'], 4) == 0.7500
    assert payload['components']['stability'] == 0.8


def test_portfolio_validation_report_to_dict():
    report = PortfolioValidationReport.from_backtest_result(
        {
            'weights': [
                {'ticker': 'AAPL', 'weight': 0.6},
                {'ticker': 'MSFT', 'weight': 0.4},
            ],
            'portfolio_return': 0.025,
        },
        max_weight=0.7,
    )
    payload = report.to_dict()
    assert payload['report_type'] == 'portfolio_validation'
    assert payload['n_positions'] == 2
    assert round(payload['weight_sum'], 6) == 1.0
    assert payload['long_only'] is True
    assert round(payload['max_weight_observed'], 4) == 0.6
    assert payload['max_weight_ok'] is True
