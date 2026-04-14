from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path



def test_toy_end_to_end_example_runs_and_emits_reports():
    repo_root = Path(__file__).resolve().parents[1]
    example_path = repo_root / 'examples' / 'toy_end_to_end.py'
    result = subprocess.run(
        [sys.executable, str(example_path)],
        cwd=repo_root,
        env={'PYTHONPATH': 'src'},
        capture_output=True,
        text=True,
        check=True,
    )
    payload = json.loads(result.stdout)
    assert 'dataset' in payload
    assert 'decision_quality_report' in payload
    assert 'reliability_report' in payload
    assert 'portfolio_validation_report' in payload
    assert 'test_suite_result' in payload
