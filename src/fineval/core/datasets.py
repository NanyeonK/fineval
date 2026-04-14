from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

import pandas as pd


@dataclass
class DecisionDefinition:
    ticker_column: str = "ticker"
    date_column: str = "date"
    target_column: str = "ret_fwd_1m"
    task_type: Literal["stock_month_decision"] = "stock_month_decision"
    metadata: dict = field(default_factory=dict)


@dataclass
class DecisionDataset:
    data: pd.DataFrame
    definition: DecisionDefinition

    @classmethod
    def from_pandas(cls, data: pd.DataFrame, definition: DecisionDefinition | None = None) -> "DecisionDataset":
        definition = definition or DecisionDefinition()
        required = [definition.ticker_column, definition.date_column, definition.target_column]
        missing = [col for col in required if col not in data.columns]
        if missing:
            raise ValueError(f"DecisionDataset missing required columns: {missing}")
        return cls(data=data.copy(), definition=definition)

    def as_dataframe(self) -> pd.DataFrame:
        return self.data.copy()

    def tickers(self) -> list[str]:
        return sorted(self.data[self.definition.ticker_column].astype(str).unique().tolist())
