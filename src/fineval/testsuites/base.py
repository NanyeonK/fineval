from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class TestSuite:
    __test__ = False
    name: str
    checks: list[dict[str, Any]]

    def run(self, report: Any) -> dict[str, Any]:
        payload = report.to_dict() if hasattr(report, 'to_dict') else dict(report)
        results = []
        for check in self.checks:
            actual = payload[check['field']]
            op = check['op']
            threshold = check['threshold']
            if op == '>=':
                passed = actual >= threshold
            elif op == '<=':
                passed = actual <= threshold
            elif op == '==':
                passed = actual == threshold
            else:
                raise ValueError(f'Unsupported op: {op}')
            results.append(
                {
                    'name': check['name'],
                    'field': check['field'],
                    'op': op,
                    'threshold': threshold,
                    'actual': actual,
                    'passed': passed,
                }
            )
        return {
            'suite_name': self.name,
            'passed': all(result['passed'] for result in results),
            'checks': results,
        }
