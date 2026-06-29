"""ROI helper for scenario comparisons."""
from pathlib import Path

import pandas as pd

def roi_table(simulation_file: str | Path = "../data/processed/air_liquide_russia_simulation.csv", output_file: str | Path = "../data/processed/roi_summary.csv") -> pd.DataFrame:
    df = pd.read_csv(simulation_file)
    df["decision_gate"] = df["roi_adjusted_pct"].apply(lambda x: "INVEST" if x >= 12 else "WAIT" if x >= 6 else "AVOID")
    df.to_csv(output_file, index=False)
    return df

if __name__ == "__main__":
    print(roi_table())
