import pandas as pd

from fineval import DecisionDataset, DecisionDefinition, FinancialDecisionObject



def test_top_level_imports_exist():
    assert DecisionDataset is not None
    assert DecisionDefinition is not None
    assert FinancialDecisionObject is not None



def test_decision_dataset_from_pandas():
    df = pd.DataFrame([
        {"date": "2024-01-31", "ticker": "AAPL", "ret_fwd_1m": 0.03},
        {"date": "2024-01-31", "ticker": "MSFT", "ret_fwd_1m": 0.02},
    ])
    ds = DecisionDataset.from_pandas(df, DecisionDefinition())
    assert ds.tickers() == ["AAPL", "MSFT"]
    assert list(ds.as_dataframe().columns) == ["date", "ticker", "ret_fwd_1m"]
