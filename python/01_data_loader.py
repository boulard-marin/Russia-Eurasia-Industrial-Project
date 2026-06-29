"""Download public source data used by the project.

The loader intentionally avoids invented values. Missing API values remain blank and are handled downstream.
"""
from __future__ import annotations

import json
import urllib.request
from pathlib import Path

import pandas as pd

COUNTRIES = {"RUS": "Russia", "CHN": "China", "IND": "India", "KAZ": "Kazakhstan", "TKM": "Turkmenistan"}
INDICATORS = {
    "NY.GDP.MKTP.CD": "gdp_current_usd",
    "FP.CPI.TOTL.ZG": "inflation_pct",
    "BX.KLT.DINV.CD.WD": "fdi_inflows_usd",
    "NV.IND.TOTL.ZS": "industry_value_added_pct_gdp",
    "NV.IND.MANF.ZS": "manufacturing_value_added_pct_gdp",
    "IS.RRS.TOTL.KM": "rail_lines_km",
    "LP.LPI.OVRL.XQ": "lpi_overall_score",
    "NE.EXP.GNFS.CD": "exports_goods_services_usd",
    "NE.IMP.GNFS.CD": "imports_goods_services_usd",
}

def fetch_json(url: str):
    request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(request, timeout=45) as response:
        return json.loads(response.read().decode("utf-8"))

def load_world_bank(output_dir: str | Path = "../data/raw") -> pd.DataFrame:
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    rows = []
    for indicator, field in INDICATORS.items():
        url = f"https://api.worldbank.org/v2/country/{';'.join(COUNTRIES)}/indicator/{indicator}?format=json&per_page=20000&date=2019:2024"
        payload = fetch_json(url)
        for record in payload[1]:
            if record.get("countryiso3code") in COUNTRIES:
                rows.append({
                    "country_code": record["countryiso3code"],
                    "country": COUNTRIES[record["countryiso3code"]],
                    "year": int(record["date"]),
                    "field": field,
                    "value": record.get("value"),
                    "indicator_code": indicator,
                    "source_url": url,
                })
    df = pd.DataFrame(rows)
    df.to_csv(output_dir / "world_bank_tidy.csv", index=False)
    return df

if __name__ == "__main__":
    print(load_world_bank().head())
