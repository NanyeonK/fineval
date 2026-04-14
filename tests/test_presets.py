from fineval.presets import DecisionQualityPreset, PortfolioValidationPreset


def test_preset_imports_exist():
    assert DecisionQualityPreset is not None
    assert PortfolioValidationPreset is not None


def test_decision_quality_preset_runs_default_report():
    preset = DecisionQualityPreset.default()
    report = preset.evaluate(
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
    assert payload['weights']['economic_coherence'] == 0.35


def test_portfolio_validation_preset_runs_default_report():
    preset = PortfolioValidationPreset.default(max_weight=0.7)
    report = preset.evaluate(
        {
            'weights': [
                {'ticker': 'AAPL', 'weight': 0.6},
                {'ticker': 'MSFT', 'weight': 0.4},
            ],
            'portfolio_return': 0.025,
        }
    )
    payload = report.to_dict()
    assert payload['report_type'] == 'portfolio_validation'
    assert payload['max_weight_ok'] is True
    assert round(payload['weight_sum'], 6) == 1.0
