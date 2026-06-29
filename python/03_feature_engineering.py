"""Feature engineering for EIRM scoring."""
from pathlib import Path

import numpy as np
import pandas as pd

POSITIVE_FEATURES = ["gdp_current_usd", "fdi_inflows_usd", "industry_value_added_pct_gdp", "manufacturing_value_added_pct_gdp", "lpi_overall_score", "exports_goods_services_usd"]
NEGATIVE_FEATURES = ["inflation_pct"]
LOG_FEATURES = {"gdp_current_usd", "fdi_inflows_usd", "exports_goods_services_usd"}

def minmax(series: pd.Series, log_scale: bool = False) -> pd.Series:
    series = pd.to_numeric(series, errors="coerce")
    if log_scale:
        series = series.where(series > 0)
        series = np.log10(series)
    if series.notna().sum() <= 1 or series.max() == series.min():
        return pd.Series([50 if pd.notna(x) else None for x in series], index=series.index)
    return (series - series.min()) / (series.max() - series.min()) * 100

def build_features(input_file: str | Path = "../data/processed/latest_macro_snapshot.csv", output_file: str | Path = "../data/processed/eirm_features.csv") -> pd.DataFrame:
    df = pd.read_csv(input_file)
    for col in POSITIVE_FEATURES:
        if col in df:
            df[f"{col}_score"] = minmax(df[col], log_scale=col in LOG_FEATURES)
    for col in NEGATIVE_FEATURES:
        if col in df:
            df[f"{col}_score"] = 100 - minmax(df[col])
    Path(output_file).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_file, index=False)
    return df

if __name__ == "__main__":
    print(build_features())
