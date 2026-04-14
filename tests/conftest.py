from __future__ import annotations

import pandas as pd
import pytest

TOY_STOCKS = ["AAPL", "MSFT", "NVDA", "JPM"]


@pytest.fixture(scope="session")
def toy_panel() -> pd.DataFrame:
    rows = [
        {"date": "2024-01-31", "ticker": "AAPL", "ret_fwd_1m": 0.03, "size": 10.0, "value": -0.2, "mom": 0.5, "vol": 0.22, "sector": "tech"},
        {"date": "2024-01-31", "ticker": "MSFT", "ret_fwd_1m": 0.02, "size": 10.2, "value": -0.1, "mom": 0.4, "vol": 0.20, "sector": "tech"},
        {"date": "2024-01-31", "ticker": "NVDA", "ret_fwd_1m": 0.06, "size": 9.8, "value": -0.6, "mom": 0.9, "vol": 0.35, "sector": "tech"},
        {"date": "2024-01-31", "ticker": "JPM", "ret_fwd_1m": -0.01, "size": 10.1, "value": 0.3, "mom": -0.1, "vol": 0.18, "sector": "financials"},
    ]
    return pd.DataFrame(rows)


@pytest.fixture(scope="session")
def toy_packet_examples() -> list[dict]:
    return [
        {
            "ticker": "NVDA",
            "as_of_date": "2024-01-31",
            "packet_id": "nvda_2024_01",
            "sources": [
                {"source_type": "earnings_call", "published_at": "2024-01-20", "text": "AI demand remains strong."},
                {"source_type": "news", "published_at": "2024-01-28", "text": "Capex outlook revised upward."},
            ],
        }
    ]
