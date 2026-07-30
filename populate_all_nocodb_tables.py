import requests
import json
import csv
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

NOCODB_MCP_URL = "https://app.nocodb.com/mcp/ncvlottre3sgvvvs"
NOCODB_TOKEN = "HeFPyX-Pwh9Tdpx3UDdHxJZ9bcTwNw-E"

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
        r = requests.post(NOCODB_MCP_URL, headers=HEADERS, json=payload, timeout=20)
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
        return []
    data = []
    with open(filepath, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(row)
    return data

def main():
    print("==================================================")
    print(" 🚀 INGESTING FULL EUROASIA BD DATA INTO NOCODB ")
    print("==================================================")
    
    pipeline_data = load_csv("airliquide_bd_pipeline_russia_2025.csv")
    regional_data = load_csv("master_regional_russia_2025.csv")
    whatif_data = load_csv("whatif_sanctions_lift_simulation_2025.csv")

    # -------------------------------------------------------------
    # 1. POPULATE PIPELINE BD (31 Records) INTO TABLE 1 (mt8ep8jts6jwaak)
    # -------------------------------------------------------------
    print(f"\n[Table 1: BD Pipeline] Ingesting {len(pipeline_data)} opportunities into NocoDB...")
    t1_records = []
    for r in pipeline_data:
        record = {
            "fields": {
                "Album": f"[{r.get('Opportunity_ID')}] {r.get('Region_Oblast')} — {r.get('BD_Priority')}",
                "Notes": f"EIII Score: {r.get('EIII_Score')} | CAPEX Potential: {r.get('Est_CAPEX_Potential_M_EUR')} M€ | Gas Proxy: {r.get('Gas_Demand_Proxy_bln_rub')} Mrd RUB | Gas Target: {r.get('Top_Gas_Product')} | Target Clients: {r.get('Key_Clients_Target')} | Est Rev: {r.get('Est_Revenue_M_EUR_yr')} M€/yr | Rev Post-Sanctions: {r.get('Revenue_Post_Sanctions_M_EUR_yr')} M€/yr"
            }
        }
        t1_records.append(record)

    # Insert in batches of 10
    batch_size = 10
    for i in range(0, len(t1_records), batch_size):
        batch = t1_records[i:i+batch_size]
        res = call_mcp("tools/call", {
            "name": "createRecords",
            "arguments": {
                "tableId": "mt8ep8jts6jwaak",
                "records": batch
            }
        }, req_id=100+i)
        print(f"  -> Batch {i//batch_size + 1}: Inserted {len(batch)} records into Table 1. Status: {res.get('jsonrpc') == '2.0'}")

    # -------------------------------------------------------------
    # 2. POPULATE REGIONAL EIII MASTER (85 Records) INTO TABLE 2 (m1x72acim62kdon)
    # -------------------------------------------------------------
    print(f"\n[Table 2: Regional Master] Ingesting {len(regional_data)} Russia regions into NocoDB...")
    t2_records = []
    for idx, r in enumerate(regional_data):
        score = float(r.get('EIII_Regional_Score', 0) or 0)
        signal = "General"
        
        title = f"#{idx+1} {r.get('Region_Oblast')} (Score EIII: {score:.1f})"
        desc = (
            f"District: {r.get('Federal_District')}\n"
            f"GRP 2023: {r.get('GRP_PRB_2023_bln_rub')} Mrd RUB\n"
            f"Investments: {r.get('Investment_Fixed_Capital_bln_rub')} Mrd RUB\n"
            f"Metallurgy Output: {r.get('Metallurgy_Mining_Output_bln_rub')} Mrd RUB\n"
            f"Chemical Output: {r.get('Chemical_Petrochemical_Output_bln_rub')} Mrd RUB\n"
            f"Gas Demand Proxy: {r.get('Gas_Industrial_Demand_Proxy_bln_rub')} Mrd RUB\n"
            f"Top Sector for Gas: {r.get('Top_Opportunity_Sector_For_Gases')}\n"
            f"Rosstat Source: {r.get('Source_Rosstat_Page')}"
        )
        t2_records.append({
            "fields": {
                "Title": title,
                "Description": desc,
                "Category": signal
            }
        })

    for i in range(0, len(t2_records), batch_size):
        batch = t2_records[i:i+batch_size]
        res = call_mcp("tools/call", {
            "name": "createRecords",
            "arguments": {
                "tableId": "m1x72acim62kdon",
                "records": batch
            }
        }, req_id=200+i)
        print(f"  -> Batch {i//batch_size + 1}: Inserted {len(batch)} records into Table 2. Status: {res.get('jsonrpc') == '2.0'}")

    # -------------------------------------------------------------
    # 3. POPULATE WHAT-IF SIMULATION & LINKS INTO TABLE 3 (meodo332szf1zlj)
    # -------------------------------------------------------------
    print(f"\n[Table 3: What-If Simulation] Ingesting Sanctions scenarios & dashboard links into NocoDB...")
    scenarios = [
        {"Title": "Scénario 2025: Baseline (Sanctions Actives ×1.0) — Revenu ~3 M€/an", "Category": "1. Building Base", "Quick link": "http://localhost:8080/#2025"},
        {"Title": "Scénario 2026: Levée Partielle Énergie (Multiplier ×1.4) — Revenu ~4.2 M€/an", "Category": "2. Working with Views", "Quick link": "http://localhost:8080/#2026"},
        {"Title": "Scénario 2027: Levée Totale Sanctions (Multiplier ×2.0) — Revenu ~6.0 M€/an", "Category": "3. Table operations", "Quick link": "http://localhost:8080/#2027"},
        {"Title": "Scénario 2028: Reprise des Investissements Directs Étrangers (×2.8) — Revenu ~8.4 M€/an", "Category": "4. Field Types", "Quick link": "http://localhost:8080/#2028"},
        {"Title": "Scénario 2030: Boom Post-Réintégration Marché (Multiplier ×4.2) — Revenu ~12.6 M€/an", "Category": "5. Collaboration", "Quick link": "http://localhost:8080/#2030"},
        {"Title": "Dashboard BI & BD Analytics Interactif Complete App", "Category": "6. Automation", "Quick link": "http://localhost:8080"}
    ]
    t3_records = [{"fields": s} for s in scenarios]
    res3 = call_mcp("tools/call", {
        "name": "createRecords",
        "arguments": {
            "tableId": "meodo332szf1zlj",
            "records": t3_records
        }
    }, req_id=300)
    print(f"  -> Inserted {len(t3_records)} scenarios into Table 3. Status: {res3.get('jsonrpc') == '2.0'}")

    print("\n==================================================")
    print(" ✅ ALL EUROASIA DATA SUCCESSFULLY POPULATED IN NOCODB! ")
    print("==================================================")

if __name__ == "__main__":
    main()
