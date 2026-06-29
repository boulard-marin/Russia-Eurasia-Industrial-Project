"""Generate lightweight visual outputs for the project."""
from pathlib import Path

import pandas as pd

def chart_ready_tables(scores_file: str | Path = "../data/processed/eirm_scores.csv", output_dir: str | Path = "../data/processed") -> None:
    scores = pd.read_csv(scores_file)
    output_dir = Path(output_dir)
    pivot = scores.pivot(index="country", columns="scenario_id", values="eirm_score_0_100").reset_index()
    pivot.to_csv(output_dir / "eirm_scores_pivot.csv", index=False)

if __name__ == "__main__":
    chart_ready_tables()
