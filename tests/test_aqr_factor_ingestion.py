from pathlib import Path

from fineval.benchmarks.aqr_ingestion import load_aqr_monthly_sheet, normalize_aqr_monthly_columns



def test_load_aqr_monthly_sheet_reads_expected_columns_for_bab():
    path = Path('data/external/aqr_raw/bab_monthly_aqr.xlsx')
    df = load_aqr_monthly_sheet(path, 'BAB Factors')
    assert 'DATE' in df.columns
    assert 'USA' in df.columns
    assert 'Global' in df.columns



def test_normalize_aqr_monthly_columns_returns_expected_schema_for_qmj():
    path = Path('data/external/aqr_raw/qmj_monthly_aqr.xlsx')
    df = load_aqr_monthly_sheet(path, 'QMJ Factors')
    out = normalize_aqr_monthly_columns(df)
    expected = {'date', 'usa', 'global', 'global_ex_usa', 'europe', 'north_america', 'pacific'}
    assert expected.issubset(set(out.columns))
    assert out['date'].notna().all()
    assert out['date'].is_monotonic_increasing
