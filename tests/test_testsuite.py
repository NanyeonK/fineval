from fineval import DecisionQualityReport, TestSuite


def test_testsuite_top_level_import_exists():
    assert TestSuite is not None


def test_testsuite_runs_threshold_checks_on_report_score():
    report = DecisionQualityReport.from_metrics(
        {
            'structural_validity': 1.0,
            'temporal_integrity': 0.8,
            'robustness': 0.6,
            'economic_coherence': 0.9,
        }
    )
    suite = TestSuite(
        name='toy-decision-quality-gate',
        checks=[
            {
                'name': 'dq-score-min',
                'field': 'score',
                'op': '>=',
                'threshold': 0.80,
            },
            {
                'name': 'dq-score-max',
                'field': 'score',
                'op': '<=',
                'threshold': 0.90,
            },
        ],
    )
    result = suite.run(report)
    assert result['suite_name'] == 'toy-decision-quality-gate'
    assert result['passed'] is True
    assert len(result['checks']) == 2
    assert all(check['passed'] for check in result['checks'])


def test_testsuite_flags_failed_threshold_check():
    report = DecisionQualityReport.from_metrics(
        {
            'structural_validity': 1.0,
            'temporal_integrity': 0.8,
            'robustness': 0.6,
            'economic_coherence': 0.9,
        }
    )
    suite = TestSuite(
        name='toy-fail-gate',
        checks=[
            {
                'name': 'dq-too-high',
                'field': 'score',
                'op': '>=',
                'threshold': 0.90,
            }
        ],
    )
    result = suite.run(report)
    assert result['suite_name'] == 'toy-fail-gate'
    assert result['passed'] is False
    assert result['checks'][0]['passed'] is False
