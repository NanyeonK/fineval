from fineval.data.monthly_packet import load_packet_examples, filter_sources_point_in_time
from fineval.data.structured_block import load_structured_panel


def test_load_packet_examples():
    packets = load_packet_examples("data/toy/text_packet_examples.json")
    assert packets[0].ticker == "NVDA"


def test_point_in_time_filter():
    packets = load_packet_examples("data/toy/text_packet_examples.json")
    kept = filter_sources_point_in_time(packets[0].sources, "2024-01-25")
    assert len(kept) == 1
    assert kept[0]["source_type"] == "earnings_call"


def test_load_structured_panel():
    df = load_structured_panel("data/toy/stock_month_panel.parquet")
    assert set(["date", "ticker", "ret_fwd_1m"]).issubset(df.columns)
    assert len(df) == 4
