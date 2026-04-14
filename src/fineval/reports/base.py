from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from typing import Any


@dataclass(kw_only=True)
class BaseReport:
    report_type: str
    score: float | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), sort_keys=True)
