"""Sanctions scenario engine.

The index is an explicit ASSUMPTION-based ordinal model documented in data/sanctions_index.csv.
It is not an official sanctions count.
"""
from pathlib import Path

import pandas as pd

def scenario_penalty(sanctions_file: str | Path = "../data/sanctions_index.csv") -> pd.DataFrame:
    df = pd.read_csv(sanctions_file)
    df["risk_adjustment_factor"] = 1 - (df["sanctions_intensity_index_0_100"] / 100)
    df["payment_access_factor"] = 1 - (df["payment_risk_0_100"] / 100)
    return df

if __name__ == "__main__":
    print(scenario_penalty())
