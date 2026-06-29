import pandas as pd
import numpy as np
import os
import random
from datetime import datetime, timedelta

# Configurations
COUNTRIES = ['Russia', 'China', 'India', 'Kazakhstan', 'Turkmenistan', 'Georgia']
YEARS = [2020, 2021, 2022, 2023, 2024, 2025]

# Base directories
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIRS = {
    'data': os.path.join(BASE_DIR, 'data'),
    'sap': os.path.join(BASE_DIR, 'sap_simulation'),
    'crm': os.path.join(BASE_DIR, 'crm_simulation'),
    'excel': os.path.join(BASE_DIR, 'excel'),
    'sql': os.path.join(BASE_DIR, 'sql')
}
for d in DIRS.values():
    os.makedirs(d, exist_ok=True)

# Helper function to generate normalized data between min and max
def generate_norm_data(n, min_val=0, max_val=100):
    return np.clip(np.random.normal((min_val+max_val)/2, (max_val-min_val)/4, n), min_val, max_val).round(2)

# --- 1. EIII DATA GENERATION ---
def generate_eiii_data():
    records = []
    for year in YEARS:
        for country in COUNTRIES:
            records.append({
                'country': country,
                'year': year,
                
                # Economy (25%)
                'gdp_score': random.uniform(20, 100) if country in ['China', 'India'] else random.uniform(10, 60),
                'gdp_growth_score': random.uniform(40, 90),
                'inflation_inv_score': random.uniform(30, 80),
                'industrial_output_score': random.uniform(30, 95),
                'fdi_inflows_score': random.uniform(20, 90),
                
                # Energy (20%)
                'gas_prod_score': random.uniform(70, 100) if country in ['Russia', 'Turkmenistan'] else random.uniform(10, 50),
                'oil_prod_score': random.uniform(70, 100) if country in ['Russia', 'Kazakhstan'] else random.uniform(10, 60),
                'electricity_price_inv_score': random.uniform(40, 90),
                'energy_export_cap_score': random.uniform(20, 95),
                
                # Industrial (20%)
                'chemical_output_score': random.uniform(30, 95),
                'metallurgy_index_score': random.uniform(30, 95),
                'heavy_industry_score': random.uniform(30, 90),
                
                # Logistics (15%)
                'rail_density_score': random.uniform(20, 80),
                'port_score': random.uniform(60, 95) if country in ['China', 'India', 'Russia', 'Georgia'] else random.uniform(5, 30),
                'corridor_score': random.uniform(30, 85),
                'trade_conn_score': random.uniform(40, 90),
                
                # Risk (20% - Inverse: High score = Low Risk)
                # SCENARIO: Lift of EU sanctions for Russia in 2025
                'sanctions_inv_score': random.uniform(85, 100) if (country == 'Russia' and year == 2025) else (random.uniform(5, 20) if country == 'Russia' else random.uniform(60, 95)),
                'currency_vol_inv_score': random.uniform(30, 80),
                'payment_risk_inv_score': random.uniform(40, 90),
                'legal_risk_inv_score': random.uniform(40, 90),
                'insurance_cost_inv_score': random.uniform(30, 85)
            })
            
    df = pd.DataFrame(records)
    
    # Calculate weighted scores
    df['economy_score'] = (df['gdp_score']*0.2 + df['gdp_growth_score']*0.2 + df['inflation_inv_score']*0.2 + df['industrial_output_score']*0.2 + df['fdi_inflows_score']*0.2).round(2)
    df['energy_score'] = (df['gas_prod_score']*0.25 + df['oil_prod_score']*0.25 + df['electricity_price_inv_score']*0.25 + df['energy_export_cap_score']*0.25).round(2)
    df['industry_score'] = (df['chemical_output_score']*0.35 + df['metallurgy_index_score']*0.35 + df['heavy_industry_score']*0.30).round(2)
    df['logistics_score'] = (df['rail_density_score']*0.25 + df['port_score']*0.25 + df['corridor_score']*0.25 + df['trade_conn_score']*0.25).round(2)
    df['risk_score'] = (df['sanctions_inv_score']*0.3 + df['currency_vol_inv_score']*0.2 + df['payment_risk_inv_score']*0.2 + df['legal_risk_inv_score']*0.15 + df['insurance_cost_inv_score']*0.15).round(2)
    
    # EIII = Sum of weighted components
    df['EIII_score'] = (df['economy_score']*0.25 + df['energy_score']*0.20 + df['industry_score']*0.20 + df['logistics_score']*0.15 + df['risk_score']*0.20).round(2)
    
    # Save partial CSVs
    df[['country', 'year', 'gdp_score', 'inflation_inv_score', 'industrial_output_score', 'fdi_inflows_score', 'economy_score']].to_csv(os.path.join(DIRS['data'], 'macro_indicators.csv'), index=False)
    df[['country', 'year', 'chemical_output_score', 'metallurgy_index_score', 'heavy_industry_score', 'industry_score']].to_csv(os.path.join(DIRS['data'], 'industry.csv'), index=False)
    df[['country', 'year', 'gas_prod_score', 'oil_prod_score', 'electricity_price_inv_score', 'energy_export_cap_score', 'energy_score']].to_csv(os.path.join(DIRS['data'], 'energy.csv'), index=False)
    df[['country', 'year', 'rail_density_score', 'port_score', 'corridor_score', 'trade_conn_score', 'logistics_score']].to_csv(os.path.join(DIRS['data'], 'logistics.csv'), index=False)
    df[['country', 'year', 'sanctions_inv_score', 'currency_vol_inv_score', 'legal_risk_inv_score', 'payment_risk_inv_score', 'insurance_cost_inv_score', 'risk_score']].to_csv(os.path.join(DIRS['data'], 'risk.csv'), index=False)
    
    # Save Final Score
    df[['country', 'year', 'EIII_score', 'economy_score', 'energy_score', 'industry_score', 'logistics_score', 'risk_score']].to_csv(os.path.join(DIRS['data'], 'final_eiii_score.csv'), index=False)
    return df

# --- 2. AIR LIQUIDE SIMULATION ---
def generate_air_liquide(df_eiii):
    al_data = []
    # Filter on year 2025 for future decision
    df_2025 = df_eiii[df_eiii['year'] == 2025]
    for _, row in df_2025.iterrows():
        capex = round(random.uniform(50, 200), 2) # in M EUR
        opex = round(capex * random.uniform(0.05, 0.15) * (200 - row['energy_score'])/100, 2)
        rev = round(capex * random.uniform(0.15, 0.35) * (row['industry_score']/50), 2)
        roi_base = round((rev - opex) / capex * 100, 2)
        roi_risk_adj = round(roi_base * (row['risk_score'] / 100), 2)
        break_even = round(capex / (rev - opex), 1) if rev > opex else 99.9
        
        if roi_risk_adj > 15 and break_even < 7:
            decision = 'INVEST'
        elif roi_risk_adj > 8 and break_even < 12:
            decision = 'WAIT'
        else:
            decision = 'AVOID'
            
        al_data.append({
            'country': row['country'],
            'plant_location': f"{row['country']}_Industrial_Zone_A",
            'CAPEX_estimate_M': capex,
            'OPEX_energy_M': opex,
            'logistics_cost_M': round(opex * (200 - row['logistics_score'])/1000, 2),
            'expected_revenue_M': rev,
            'ROI_base_pct': roi_base,
            'ROI_risk_adjusted_pct': roi_risk_adj,
            'break_even_years': break_even,
            'investment_decision': decision
        })
    pd.DataFrame(al_data).to_csv(os.path.join(DIRS['excel'], 'air_liquide_simulation.csv'), index=False)

# --- 3. SAP MM/SD EXTENDED SIMULATION ---
def generate_sap_data():
    materials = ['Industrial Gas', 'Chemical Reagents', 'Piping parts', 'Compressors']
    plants = ['PL01', 'PL02', 'PL03']
    
    # SAP MM
    mm_data = []
    for i in range(1, 201):
        country = random.choice(COUNTRIES)
        qty = random.randint(10, 1000)
        price = round(random.uniform(10, 5000), 2)
        val = qty * price
        pr = f"PR{1000000+i}"
        po = f"450000{1000+i}" if random.random() > 0.1 else ""
        migo = f"500000{1000+i}" if po and random.random() > 0.15 else ""
        miro = f"510000{1000+i}" if migo and random.random() > 0.2 else ""
        
        mm_data.append({
            'Purchase_Requisition_PR': pr,
            'Purchase_Order_PO': po,
            'Goods_Receipt_MIGO': migo,
            'Invoice_Receipt_MIRO': miro,
            'Vendor': f"Vendor_{country}_{random.randint(1,10)}",
            'Country': country,
            'Material': random.choice(materials),
            'Plant': random.choice(plants),
            'Quantity': qty,
            'Unit_Price_EUR': price,
            'Total_Value_EUR': val,
            'Creation_Date': (datetime.today() - timedelta(days=random.randint(10, 365))).strftime('%Y-%m-%d')
        })
    pd.DataFrame(mm_data).to_csv(os.path.join(DIRS['sap'], 'sap_mm_comprehensive.csv'), index=False)

    # SAP SD
    sd_data = []
    customers = ['HeavyInd Corp', 'ChemWorks', 'AutoMotive Inc', 'TechSteel']
    for i in range(1, 201):
        country = random.choice(COUNTRIES)
        qty = random.randint(50, 500)
        price = round(random.uniform(50, 8000), 2)
        val = qty * price
        so = f"SO{2000000+i}"
        deliv = f"800000{1000+i}" if random.random() > 0.1 else ""
        gi = f"490000{1000+i}" if deliv and random.random() > 0.15 else ""
        billing = f"900000{1000+i}" if gi and random.random() > 0.2 else ""
        
        sd_data.append({
            'Sales_Order_SO': so,
            'Delivery_Document': deliv,
            'Goods_Issue_Document': gi,
            'Billing_Invoice_VF01': billing,
            'Customer': random.choice(customers),
            'Country': country,
            'Material': random.choice(materials),
            'Plant': random.choice(plants),
            'Quantity': qty,
            'Unit_Price_EUR': price,
            'Total_Value_EUR': val,
            'Incoterms': random.choice(['FOB', 'EXW', 'CIF', 'DDP']),
            'Creation_Date': (datetime.today() - timedelta(days=random.randint(10, 365))).strftime('%Y-%m-%d')
        })
    pd.DataFrame(sd_data).to_csv(os.path.join(DIRS['sap'], 'sap_sd_comprehensive.csv'), index=False)


# --- 4. SALESFORCE CRM SIMULATION ---
def generate_salesforce_data():
    sf_data = []
    stages = ['Lead', 'Qualified', 'Proposal', 'Negotiation', 'Closed Won', 'Closed Lost']
    accounts = ['Eurasia Corp', 'Global Dynamics', 'Future Industries', 'Acme Ind.', 'Stark Mining']
    sources = ['Webinar', 'Trade Show', 'Cold Call', 'Referral', 'LinkedIn']
    
    for i in range(1, 151):
        stage = random.choice(stages)
        prob = {'Lead': 10, 'Qualified': 30, 'Proposal': 50, 'Negotiation': 70, 'Closed Won': 100, 'Closed Lost': 0}[stage]
        amount = round(random.uniform(100000, 5000000), 2)
        
        sf_data.append({
            'Opportunity_ID': f"OPP-{10000+i}",
            'Account_Name': random.choice(accounts),
            'Opportunity_Name': f"Gas Supply / {random.choice(COUNTRIES)}",
            'Lead_Source': random.choice(sources),
            'Stage': stage,
            'Amount_EUR': amount,
            'Expected_Close_Date': (datetime.today() + timedelta(days=random.randint(-100, 180))).strftime('%Y-%m-%d'),
            'Probability_pct': prob,
            'Risk_Level': random.choice(['Low', 'Medium', 'High']) if prob < 100 else 'None',
            'Country': random.choice(COUNTRIES),
            'Decision_Maker': f"CxO_{random.randint(1,100)}"
        })
    pd.DataFrame(sf_data).to_csv(os.path.join(DIRS['crm'], 'salesforce_pipeline_extended.csv'), index=False)

if __name__ == '__main__':
    print("Generating EIII Model Data...")
    df_eiii = generate_eiii_data()
    print("Generating Air Liquide Simulation Data...")
    generate_air_liquide(df_eiii)
    print("Generating SAP MM/SD Data...")
    generate_sap_data()
    print("Generating Salesforce CRM Data...")
    generate_salesforce_data()
    print("All datasets successfully generated!")
