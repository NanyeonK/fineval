from __future__ import annotations

import pandas as pd
import statsmodels.api as sm



def fit_stock_level_regression(df: pd.DataFrame, y: str = "ret_fwd_1m"):
    X = df[["struct_score", "text_score", "dq", "rl"]].copy()
    X["text_x_dq"] = df["text_score"] * df["dq"]
    X["text_x_rl"] = df["text_score"] * df["rl"]
    X = sm.add_constant(X)
    model = sm.OLS(df[y], X).fit()
    return model
