"""Air Liquide industrial unit simulation for Russia.

Simulation figures are tagged ASSUMPTION when no public plant-level value exists.
"""
from pathlib import Path

import pandas as pd

BASE = {
    "capex_million_eur": 200.0,
    "annual_revenue_million_eur": 95.0,
    "ebitda_margin_pct": 27.0,
    "energy_opex_pct_revenue": 18.0,
    "logistics_cost_pct_revenue": 7.0,
}

SCENARIOS = {
    "SCENARIO 1": {"risk_haircut_pct": 55, "financing_cost_pct": 16, "revenue_access_pct": 65},
    "SCENARIO 2": {"risk_haircut_pct": 30, "financing_cost_pct": 11, "revenue_access_pct": 82},
    "SCENARIO 3": {"risk_haircut_pct": 12, "financing_cost_pct": 8, "revenue_access_pct": 100},
}

def simulate(output_file: str | Path = "../data/processed/air_liquide_russia_simulation.csv") -> pd.DataFrame:
    rows = []
    for scenario, params in SCENARIOS.items():
        effective_revenue = BASE["annual_revenue_million_eur"] * params["revenue_access_pct"] / 100
        ebitda = effective_revenue * BASE["ebitda_margin_pct"] / 100
        energy_opex = effective_revenue * BASE["energy_opex_pct_revenue"] / 100
        logistics = effective_revenue * BASE["logistics_cost_pct_revenue"] / 100
        operating_cashflow = ebitda - energy_opex - logistics
        risk_adjusted_cashflow = operating_cashflow * (1 - params["risk_haircut_pct"] / 100)
        roi_brut_pct = operating_cashflow / BASE["capex_million_eur"] * 100
        roi_adjusted_pct = risk_adjusted_cashflow / BASE["capex_million_eur"] * 100
        breakeven_years = BASE["capex_million_eur"] / risk_adjusted_cashflow if risk_adjusted_cashflow > 0 else None
        rows.append({
            "country": "Russia",
            "scenario_id": scenario,
            "capex_million_eur": BASE["capex_million_eur"],
            "annual_revenue_million_eur": round(effective_revenue, 2),
            "energy_opex_million_eur": round(energy_opex, 2),
            "logistics_cost_million_eur": round(logistics, 2),
            "operating_cashflow_million_eur": round(operating_cashflow, 2),
            "risk_adjusted_cashflow_million_eur": round(risk_adjusted_cashflow, 2),
            "roi_brut_pct": round(roi_brut_pct, 2),
            "roi_adjusted_pct": round(roi_adjusted_pct, 2),
            "break_even_years": round(breakeven_years, 2) if breakeven_years else None,
            "methodology_flag": "ASSUMPTION - plant-level revenue/cost inputs are not publicly available",
        })
    out = pd.DataFrame(rows)
    Path(output_file).parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(output_file, index=False)
    return out

if __name__ == "__main__":
    print(simulate())
