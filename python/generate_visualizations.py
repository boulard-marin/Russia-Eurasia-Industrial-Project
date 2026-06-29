import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Set style
sns.set_theme(style="whitegrid")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
EXCEL_DIR = os.path.join(BASE_DIR, 'excel')
VISUALS_DIR = os.path.join(BASE_DIR, 'report', 'visuals')
os.makedirs(VISUALS_DIR, exist_ok=True)

print("Generating Strategic Data Visualizations...")

# 1. EIII Score Evolution (Showing the 2025 Russia Sanction Lift Scenario)
df_eiii = pd.read_csv(os.path.join(DATA_DIR, 'final_eiii_score.csv'))
plt.figure(figsize=(10, 6))
sns.lineplot(data=df_eiii, x='year', y='EIII_score', hue='country', marker='o', linewidth=2)
plt.title('Evolution of EIII Score (2020-2025)\nScenario: EU Lifts Sanctions on Russia in 2025', fontsize=14, fontweight='bold')
plt.xlabel('Year')
plt.ylabel('EIII Score (0-100)')
plt.legend(title='Country', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig(os.path.join(VISUALS_DIR, 'eiii_evolution_scenario.png'))
plt.close()

# 2. Air Liquide Investment Matrix 2025 (ROI vs Risk)
df_al = pd.read_csv(os.path.join(EXCEL_DIR, 'air_liquide_simulation.csv'))
plt.figure(figsize=(10, 6))
scatter = sns.scatterplot(
    data=df_al, 
    x='ROI_risk_adjusted_pct', 
    y='break_even_years', 
    hue='investment_decision',
    size='CAPEX_estimate_M',
    sizes=(100, 500),
    palette={'INVEST': 'green', 'WAIT': 'orange', 'AVOID': 'red'},
    alpha=0.7
)
# Add country labels
for i, row in df_al.iterrows():
    plt.annotate(row['country'], (row['ROI_risk_adjusted_pct'] + 0.5, row['break_even_years']))

plt.title('Air Liquide: Investment Decision Matrix (2025)', fontsize=14, fontweight='bold')
plt.xlabel('Risk-Adjusted ROI (%) - Higher is better')
plt.ylabel('Break Even (Years) - Lower is better')
plt.axvline(x=15, color='gray', linestyle='--')
plt.axhline(y=7, color='gray', linestyle='--')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig(os.path.join(VISUALS_DIR, 'air_liquide_matrix_2025.png'))
plt.close()

# 3. Energy Advantage vs Risk Score in 2025
df_2025 = df_eiii[df_eiii['year'] == 2025]
plt.figure(figsize=(10, 6))
sns.scatterplot(
    data=df_2025, 
    x='energy_score', 
    y='risk_score', 
    hue='country',
    s=200
)
for i, row in df_2025.iterrows():
    plt.annotate(row['country'], (row['energy_score'] + 1, row['risk_score'] + 1))

plt.title('Energy Advantage vs Geopolitical Risk (2025 Sanction Lift Scenario)', fontsize=14, fontweight='bold')
plt.xlabel('Energy Score (Cheap & Abundant = High Score)')
plt.ylabel('Risk Score (Inverse: High Score = Low Risk)')
plt.axvline(x=50, color='gray', linestyle=':')
plt.axhline(y=50, color='gray', linestyle=':')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig(os.path.join(VISUALS_DIR, 'energy_vs_risk_2025.png'))
plt.close()

print(f"Visualizations saved in {VISUALS_DIR}")
