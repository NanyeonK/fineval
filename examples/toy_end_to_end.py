from __future__ import annotations

import json

import pandas as pd

from fineval import DecisionDataset, DecisionDefinition, ReliabilityReport, TestSuite
from fineval.backtest.monthly_runner import run_one_month
from fineval.data.structured_block import load_structured_panel
from fineval.presets import DecisionQualityPreset, PortfolioValidationPreset



def main() -> None:
    panel = load_structured_panel('data/toy/stock_month_panel.parquet')
    dataset = DecisionDataset.from_pandas(panel, DecisionDefinition())

    metrics = {
        'structural_validity': 1.0,
        'temporal_integrity': 0.8,
        'robustness': 0.6,
        'economic_coherence': 0.9,
    }
    decision_quality_report = DecisionQualityPreset.default().evaluate(metrics)
    reliability_report = ReliabilityReport.from_components(
        self_conf=0.7,
        stability=0.8,
        agreement=0.6,
        evidence_conf=0.9,
    )

    action_scores = pd.DataFrame(
        [
            {'ticker': 'AAPL', 'bounded_action_score': 0.2},
            {'ticker': 'MSFT', 'bounded_action_score': 0.1},
            {'ticker': 'NVDA', 'bounded_action_score': 0.8},
            {'ticker': 'JPM', 'bounded_action_score': -0.1},
        ]
    )
    backtest_result = run_one_month(panel, action_scores, max_weight=0.8)
    portfolio_validation_report = PortfolioValidationPreset.default(max_weight=0.8).evaluate(backtest_result)

    test_suite = TestSuite(
        name='toy-end-to-end-gate',
        checks=[
            {'name': 'dq-min', 'field': 'score', 'op': '>=', 'threshold': 0.80},
            {'name': 'dq-max', 'field': 'score', 'op': '<=', 'threshold': 0.90},
        ],
    )
    test_suite_result = test_suite.run(decision_quality_report)

    payload = {
        'dataset': {
            'n_rows': int(len(dataset.as_dataframe())),
            'tickers': dataset.tickers(),
            'target_column': dataset.definition.target_column,
        },
        'decision_quality_report': decision_quality_report.to_dict(),
        'reliability_report': reliability_report.to_dict(),
        'portfolio_validation_report': portfolio_validation_report.to_dict(),
        'test_suite_result': test_suite_result,
    }
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
