import pandas as pd

from fineval.portfolio.allocator import long_only_allocator



def test_allocator_sums_to_one():
    s = pd.Series([0.5, 0.2, -0.1], index=["A", "B", "C"])
    w = long_only_allocator(s, max_weight=0.8)
    assert round(float(w.sum()), 8) == 1.0
    assert (w >= 0).all()
