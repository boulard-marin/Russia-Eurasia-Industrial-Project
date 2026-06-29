"""Country scoring model: Eurasia Industrial Re-Entry Model (EIRM)."""
from pathlib import Path

import pandas as pd

WEIGHTS = {
    "market_size": 0.20,
    "industry_depth": 0.25,
    "energy_trade_position": 0.15,
    "logistics": 0.15,
    "macro_stability": 0.10,
    "risk_penalty": 0.15,
}

def score(input_features: str | Path = "../data/processed/eirm_features.csv", sanctions_file: str | Path = "../data/sanctions_index.csv", output_file: str | Path = "../data/processed/eirm_scores.csv") -> pd.DataFrame:
    features = pd.read_csv(input_features)
    sanctions = pd.read_csv(sanctions_file)
    rows = []
    def neutral(value, default=50):
        return default if pd.isna(value) else value
    for _, f in features.iterrows():
        market = neutral(f.get("gdp_current_usd_score", 50))
        industry = neutral(pd.Series([f.get("industry_value_added_pct_gdp_score"), f.get("manufacturing_value_added_pct_gdp_score")]).mean(skipna=True))
        energy_trade = neutral(f.get("exports_goods_services_usd_score", 50))
        logistics = neutral(f.get("lpi_overall_score_score", 50))
        stability = neutral(f.get("inflation_pct_score", 50))
        for _, s in sanctions[sanctions["country"] == f["country"]].iterrows():
            risk = 100 - s["sanctions_intensity_index_0_100"]
            total = (
                market * WEIGHTS["market_size"]
                + industry * WEIGHTS["industry_depth"]
                + energy_trade * WEIGHTS["energy_trade_position"]
                + logistics * WEIGHTS["logistics"]
                + stability * WEIGHTS["macro_stability"]
                + risk * WEIGHTS["risk_penalty"]
            )
            rows.append({
                "country": f["country"],
                "scenario_id": s["scenario_id"],
                "scenario": s["scenario"],
                "eirm_score_0_100": round(float(total), 2),
                "recommendation": "INVEST" if total >= 70 else "WAIT" if total >= 45 else "AVOID",
            })
    out = pd.DataFrame(rows).sort_values(["scenario_id", "eirm_score_0_100"], ascending=[True, False])
    Path(output_file).parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(output_file, index=False)
    return out

if __name__ == "__main__":
    print(score())
