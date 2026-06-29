"""Clean source data into country-year tables."""
from pathlib import Path

import pandas as pd

def pivot_world_bank(input_file: str | Path = "../data/raw/world_bank_tidy.csv", output_file: str | Path = "../data/processed/macro_indicators_clean.csv") -> pd.DataFrame:
    df = pd.read_csv(input_file)
    clean = df.pivot_table(index=["country_code", "country", "year"], columns="field", values="value", aggfunc="first").reset_index()
    clean.columns.name = None
    clean["macro_source"] = "World Bank API"
    clean["data_quality_notes"] = "blank means no public World Bank value for that country-year-indicator"
    Path(output_file).parent.mkdir(parents=True, exist_ok=True)
    clean.to_csv(output_file, index=False)
    return clean

if __name__ == "__main__":
    print(pivot_world_bank().tail())
