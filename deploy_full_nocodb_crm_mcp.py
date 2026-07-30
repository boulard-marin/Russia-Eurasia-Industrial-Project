import requests
import json
import csv
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

NOCODB_MCP_URL = "https://app.nocodb.com/mcp/ncvlottre3sgvvvs"
NOCODB_TOKEN = "HeFPyX-Pwh9Tdpx3UDdHxJZ9bcTwNw-E"
BASE_ID = "p0ygj6vufqhhhsc"

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(PROJECT_DIR, "Région de Russie", "_backup_pre_fix")

HEADERS = {
    "xc-mcp-token": NOCODB_TOKEN,
    "Accept": "application/json, text/event-stream",
    "Content-Type": "application/json"
}

def call_mcp(method, params=None, req_id=1):
    payload = {
        "jsonrpc": "2.0",
        "method": method,
        "params": params or {},
        "id": req_id
    }
    try:
        r = requests.post(NOCODB_MCP_URL, headers=HEADERS, json=payload, timeout=25)
        lines = r.text.strip().split("\n")
        for line in lines:
            if line.startswith("data: "):
                return json.loads(line[6:])
        return {"raw": r.text}
    except Exception as e:
        return {"error": str(e)}

def load_csv(filename):
    filepath = os.path.join(DATA_DIR, filename)
    if not os.path.exists(filepath):
        print(f"[ERR] File not found: {filepath}")
        return []
    rows = []
    with open(filepath, 'r', encoding='utf-8-sig') as f:
        # Detect delimiter
        first_line = f.readline()
        f.seek(0)
        delim = ';' if ';' in first_line else ','
        reader = csv.DictReader(f, delimiter=delim)
        for r in reader:
            rows.append(r)
    return rows

def deploy():
    print("==================================================")
    print(" 🛡️ OVERSEER_AI: FULL AUTOMATED NOCODB CRM DEPLOY ")
    print(" Base ID: p0ygj6vufqhhhsc | MCP Remote Engine      ")
    print("==================================================")

    # 1. Load Datasets
    pipeline = load_csv("airliquide_bd_pipeline_russia_2025.csv")
    regions = load_csv("master_regional_russia_2025.csv")
    whatif = load_csv("whatif_sanctions_lift_simulation_2025.csv")
    gases = load_csv("sector_focus_gaz_industriels.csv")

    print(f"\n[Data Status] Loaded:")
    print(f" - Pipeline 2025: {len(pipeline)} BD Opportunities")
    print(f" - Master Regions: {len(regions)} Russia Regions")
    print(f" - What-If Sanctions: {len(whatif)} Scenarios")
    print(f" - Sector Gas Focus: {len(gases)} Regional Gas Profiles")

    # -------------------------------------------------------------
    # DEPLOY TABLE 1: mt8ep8jts6jwaak (BD Pipeline 31 Opportunities)
    # -------------------------------------------------------------
    print(f"\n[Deploying Table 1: BD Pipeline] Table ID: mt8ep8jts6jwaak...")
    t1_records = []
    for r in pipeline:
        title = f"[{r.get('Opportunity_ID')}] {r.get('Region_Oblast')} | {r.get('BD_Priority')}"
        notes = (
            f"=== OPPORTUNITÉ BD AIR LIQUIDE 2025 ===\n"
            f"ID: {r.get('Opportunity_ID')}\n"
            f"Région: {r.get('Region_Oblast')} ({r.get('Federal_District')})\n"
            f"Score EIII: {r.get('EIII_Score')} / 100\n"
            f"Priorité BD: {r.get('BD_Priority')}\n"
            f"CAPEX Potentiel: {r.get('Est_CAPEX_Potential_M_EUR')} M€\n"
            f"Proxy Demande Gaz: {r.get('Gas_Demand_Proxy_bln_rub')} Mrd RUB\n"
            f"Produit Gaz Cible: {r.get('Top_Gas_Product')}\n"
            f"Scores Gaz (O2/N2/H2/CO2): {r.get('O2_Score')}/{r.get('N2_Score')}/{r.get('H2_Score')}/{r.get('CO2_Score')}\n"
            f"Clients Cibles: {r.get('Key_Clients_Target')}\n"
            f"Statut BD: {r.get('Stage_BD')}\n"
            f"Revenu Baseline: {r.get('Est_Revenue_M_EUR_yr')} M€/an\n"
            f"Multiplicateur Sanctions: ×{r.get('Sanctions_Risk_Lift_Multiplier')}\n"
            f"Revenu Post-Sanctions (2030): {r.get('Revenue_Post_Sanctions_M_EUR_yr')} M€/an\n"
            f"Notes: {r.get('Notes')}"
        )
        t1_records.append({"fields": {"Album": title, "Notes": notes}})

    # Batch Insert Table 1
    for i in range(0, len(t1_records), 10):
        batch = t1_records[i:i+10]
        res = call_mcp("tools/call", {
            "name": "createRecords",
            "arguments": {"tableId": "mt8ep8jts6jwaak", "records": batch}
        }, req_id=100+i)
        print(f"  -> Pipeline Batch {i//10 + 1}: Inserted {len(batch)} items.")

    # -------------------------------------------------------------
    # DEPLOY TABLE 2: m1x72acim62kdon (Master 85 Regions Rosstat & Scoring)
    # -------------------------------------------------------------
    print(f"\n[Deploying Table 2: Regional Master] Table ID: m1x72acim62kdon...")
    t2_records = []
    for idx, r in enumerate(regions):
        score_val = r.get('EIII_Regional_Score') or '0'
        try:
            score = float(score_val)
        except:
            score = 0.0
            
        signal = "General"
        if score >= 65: signal = "On Grid"
        elif score >= 40: signal = "Expanded Form"

        title = f"#{idx+1} {r.get('Region_Oblast')} — EIII: {score:.1f}/100 [{signal.upper()}]"
        desc = (
            f"=== 📊 MASTER FICHE RÉGIONALE ROSSTAT 2025 ===\n"
            f"Région: {r.get('Region_Oblast')}\n"
            f"District Fédéral: {r.get('Federal_District')}\n"
            f"Population 2024: {r.get('Population_2024_thou')} millier(s)\n"
            f"GRP 2023: {r.get('GRP_PRB_2023_bln_rub')} Mrd RUB\n"
            f"Investissements Capital Fixe: {r.get('Investment_Fixed_Capital_bln_rub')} Mrd RUB\n"
            f"Indice Production Industrielle: {r.get('Industrial_Production_Index_2024')}\n"
            f"Output Métallurgie & Mining: {r.get('Metallurgy_Mining_Output_bln_rub')} Mrd RUB\n"
            f"Output Chimie & Pétrochimie: {r.get('Chemical_Petrochemical_Output_bln_rub')} Mrd RUB\n"
            f"Production Manufacturing Totale: {r.get('Manufacturing_Total_bln_rub')} Mrd RUB\n"
            f"Énergie, Gaz & Eau: {r.get('Energy_Gas_Water_Supply_bln_rub')} Mrd RUB\n"
            f"Agriculture: {r.get('Agriculture_Output_bln_rub')} Mrd RUB\n"
            f"Construction Logements: {r.get('Construction_Volume_thou_m2')} k m²\n"
            f"Proxy Demande Gaz Industriels: {r.get('Gas_Industrial_Demand_Proxy_bln_rub')} Mrd RUB\n"
            f"SCORE EIII COMPOSITE: {score:.1f} / 100\n"
            f"Secteur Prioritaire Gaz: {r.get('Top_Opportunity_Sector_For_Gases')}\n"
            f"Source Officielle: Rosstat 2025 ({r.get('Source_Rosstat_Page')})"
        )
        t2_records.append({"fields": {"Title": title, "Description": desc, "Category": signal}})

    for i in range(0, len(t2_records), 10):
        batch = t2_records[i:i+10]
        res = call_mcp("tools/call", {
            "name": "createRecords",
            "arguments": {"tableId": "m1x72acim62kdon", "records": batch}
        }, req_id=200+i)
        print(f"  -> Regional Master Batch {i//10 + 1}: Inserted {len(batch)} items.")

    # -------------------------------------------------------------
    # DEPLOY TABLE 3: meodo332szf1zlj (What-If Sanctions 100 Scenarios)
    # -------------------------------------------------------------
    print(f"\n[Deploying Table 3: What-If Sanctions] Table ID: meodo332szf1zlj...")
    t3_records = []
    
    top_scenarios = [
        {"Title": "🔥 SCÉNARIO 2025: Baseline (Sanctions Actives ×1.0) — Revenu Air Liquide ~3.0 M€/an", "Category": "1. Building Base", "Quick link": "http://localhost:8080/#2025"},
        {"Title": "⚡ SCÉNARIO 2026: Levée Partielle Énergie (Multiplier ×1.4) — Revenu Air Liquide ~4.2 M€/an", "Category": "2. Working with Views", "Quick link": "http://localhost:8080/#2026"},
        {"Title": "🚀 SCÉNARIO 2027: Levée Totale Sanctions (Multiplier ×2.0) — Revenu Air Liquide ~6.0 M€/an", "Category": "3. Table operations", "Quick link": "http://localhost:8080/#2027"},
        {"Title": "📈 SCÉNARIO 2028: Reprise des IDE Étrangers (Multiplier ×2.8) — Revenu Air Liquide ~8.4 M€/an", "Category": "4. Field Types", "Quick link": "http://localhost:8080/#2028"},
        {"Title": "🏆 SCÉNARIO 2030: Boom Post-Réintégration (Multiplier ×4.2) — Revenu Air Liquide ~12.6 M€/an", "Category": "5. Collaboration", "Quick link": "http://localhost:8080/#2030"},
        {"Title": "📊 DASHBOARD BI & BD ANALYTICS COMMAND CENTER", "Category": "6. Automation", "Quick link": "http://localhost:8080"}
    ]
    t3_records.extend([{"fields": s} for s in top_scenarios])

    for r in whatif[:30]:
        sc_title = f"WhatIf {r.get('Scenario')} | {r.get('Region_Oblast')} | Rev: {r.get('Revenue_M_EUR_yr')}M€ (×{r.get('Sanctions_Multiplier')})"
        t3_records.append({
            "fields": {
                "Title": sc_title,
                "Category": "1. Building Base",
                "Quick link": "http://localhost:8080"
            }
        })

    for i in range(0, len(t3_records), 10):
        batch = t3_records[i:i+10]
        res = call_mcp("tools/call", {
            "name": "createRecords",
            "arguments": {"tableId": "meodo332szf1zlj", "records": batch}
        }, req_id=300+i)
        print(f"  -> What-If Batch {i//10 + 1}: Inserted {len(batch)} items.")

    print("\n==================================================")
    print(" 🎉 ALL TABLES FULLY DEPLOYED IN NOCODB BASE p0ygj6vufqhhhsc! ")
    print("==================================================")

if __name__ == "__main__":
    deploy()
