from __future__ import annotations

from pathlib import Path

import pandas as pd


AQR_SELECTED_COLUMNS = {
    'DATE': 'date',
    'USA': 'usa',
    'Global': 'global',
    'Global Ex USA': 'global_ex_usa',
    'Europe': 'europe',
    'North America': 'north_america',
    'Pacific': 'pacific',
}


AQR_SHEET_BY_FACTOR = {
    'bab': 'BAB Factors',
    'qmj': 'QMJ Factors',
}


def load_aqr_monthly_sheet(path: str | Path, sheet_name: str) -> pd.DataFrame:
    df = pd.read_excel(path, sheet_name=sheet_name, header=18)
    df = df.loc[:, ~df.columns.isna()].copy()
    return df


def normalize_aqr_monthly_columns(df: pd.DataFrame) -> pd.DataFrame:
    keep = [col for col in AQR_SELECTED_COLUMNS if col in df.columns]
    out = df[keep].rename(columns=AQR_SELECTED_COLUMNS).copy()
    out['date'] = pd.to_datetime(out['date'])
    out = out.dropna(subset=['date']).sort_values('date').reset_index(drop=True)
    return out


def save_aqr_processed_factors(base_dir: str | Path = 'data/external') -> dict[str, str]:
    base = Path(base_dir)
    raw_dir = base / 'aqr_raw'
    processed_dir = base / 'aqr_processed'
    processed_dir.mkdir(parents=True, exist_ok=True)

    outputs: dict[str, str] = {}
    for factor, sheet_name in AQR_SHEET_BY_FACTOR.items():
        raw_path = raw_dir / f'{factor}_monthly_aqr.xlsx'
        parsed = load_aqr_monthly_sheet(raw_path, sheet_name)
        normalized = normalize_aqr_monthly_columns(parsed)
        out_path = processed_dir / f'{factor}_monthly.parquet'
        normalized.to_parquet(out_path, index=False)
        outputs[factor] = str(out_path)
    return outputs
