import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from math import pi

# Setup Directories
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
EXCEL_DIR = os.path.join(BASE_DIR, 'excel')
VISUALS_DIR = os.path.join(BASE_DIR, 'report', 'visuals')

print("1. Merging all Data Sources...")
# Load datasets
macro = pd.read_csv(os.path.join(DATA_DIR, 'macro_indicators.csv'))
energy = pd.read_csv(os.path.join(DATA_DIR, 'energy.csv'))
industry = pd.read_csv(os.path.join(DATA_DIR, 'industry.csv'))
logistics = pd.read_csv(os.path.join(DATA_DIR, 'logistics.csv'))
risk = pd.read_csv(os.path.join(DATA_DIR, 'risk.csv'))
final_eiii = pd.read_csv(os.path.join(DATA_DIR, 'final_eiii_score.csv'))

# Merge into one comprehensive master dataset
merged = macro.merge(energy, on=['country', 'year'])
merged = merged.merge(industry, on=['country', 'year'])
merged = merged.merge(logistics, on=['country', 'year'])
merged = merged.merge(risk, on=['country', 'year'])
merged = merged.merge(final_eiii[['country', 'year', 'EIII_score']], on=['country', 'year'])

# Save merged CSV
merged.to_csv(os.path.join(DATA_DIR, 'merged_eurasia_analytics.csv'), index=False)
print("Merged dataset saved.")

# ==========================================
# 2. ADVANCED EXCEL GENERATION (XLSXWRITER)
# ==========================================
print("2. Generating Beautiful Excel Dashboard...")
excel_path = os.path.join(EXCEL_DIR, 'Russia_Strategic_Analysis_Dashboard.xlsx')
writer = pd.ExcelWriter(excel_path, engine='xlsxwriter')
workbook = writer.book

# Sheet 1: Data 2025 Focus
df_2025 = merged[merged['year'] == 2025].copy()
df_2025 = df_2025.sort_values(by='EIII_score', ascending=False)
df_2025.to_excel(writer, sheet_name='2025_Strategic_View', index=False)
worksheet = writer.sheets['2025_Strategic_View']

# Formats
header_format = workbook.add_format({'bold': True, 'bg_color': '#1F497D', 'font_color': 'white', 'border': 1})
worksheet.set_row(0, 20, header_format)
worksheet.set_column('A:A', 15) # Country
worksheet.set_column('B:Z', 12)

# Add Data Bars to EIII_score (Column AB / 27 if 0-indexed... wait, let's just do it for key columns)
# Find column indices
cols = list(df_2025.columns)
eiii_col_idx = cols.index('EIII_score')
energy_col_idx = cols.index('energy_score')
risk_col_idx = cols.index('risk_score')
eco_col_idx = cols.index('economy_score')

import string
def get_col_letter(idx):
    if idx < 26:
        return string.ascii_uppercase[idx]
    else:
        return string.ascii_uppercase[(idx//26)-1] + string.ascii_uppercase[idx%26]

# Apply Conditional Formatting (Data bars and Color Scales)
last_row = len(df_2025) + 1
worksheet.conditional_format(f'{get_col_letter(eiii_col_idx)}2:{get_col_letter(eiii_col_idx)}{last_row}', {'type': 'data_bar', 'bar_color': '#63C384'})
worksheet.conditional_format(f'{get_col_letter(energy_col_idx)}2:{get_col_letter(energy_col_idx)}{last_row}', {'type': '3_color_scale'})
worksheet.conditional_format(f'{get_col_letter(risk_col_idx)}2:{get_col_letter(risk_col_idx)}{last_row}', {'type': '3_color_scale', 'min_color': '#F8696B', 'mid_color': '#FFEB84', 'max_color': '#63C384'})

# Sheet 2: Full Raw Data
merged.to_excel(writer, sheet_name='Raw_Merged_Data', index=False)
writer.close()
print("Excel Dashboard generated.")

# ==========================================
# 3. PYTHON PANDAS VISUALIZATIONS
# ==========================================
print("3. Generating Python Advanced Visualizations...")
sns.set_theme(style="whitegrid")

# A. Correlation Heatmap
plt.figure(figsize=(12, 10))
# Select only score columns for correlation
score_cols = [c for c in merged.columns if 'score' in c and c not in ['country', 'year']]
corr = merged[score_cols].corr()
sns.heatmap(corr, cmap='coolwarm', center=0, annot=False, linewidths=.5)
plt.title('Correlation Matrix of all EIII Variables', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig(os.path.join(VISUALS_DIR, 'heatmap_correlations.png'))
plt.close()

# B. Radar Chart (Russia vs China vs India in 2025)
def create_radar_chart():
    categories = ['Economy', 'Energy', 'Industry', 'Logistics', 'Risk (Inv)']
    N = len(categories)
    
    # What will be the angle of each axis in the plot? (divide the plot / number of variable)
    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]
    
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
    
    # Draw one axe per variable + add labels
    plt.xticks(angles[:-1], categories, color='grey', size=11)
    
    # Draw ylabels
    ax.set_rlabel_position(0)
    plt.yticks([20, 40, 60, 80], ["20", "40", "60", "80"], color="grey", size=7)
    plt.ylim(0, 100)
    
    colors = ['#1f77b4', '#d62728', '#2ca02c']
    targets = ['Russia', 'China', 'India']
    
    for idx, country in enumerate(targets):
        country_data = df_2025[df_2025['country'] == country].iloc[0]
        values = [
            country_data['economy_score'], 
            country_data['energy_score'], 
            country_data['industry_score'], 
            country_data['logistics_score'], 
            country_data['risk_score']
        ]
        values += values[:1] # Repeat first value to close the circle
        
        ax.plot(angles, values, linewidth=2, linestyle='solid', label=country, color=colors[idx])
        ax.fill(angles, values, colors[idx], alpha=0.1)

    plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))
    plt.title('Strategic Pillar Comparison 2025 (Sanction Lift Scenario)', size=15, fontweight='bold', y=1.1)
    plt.savefig(os.path.join(VISUALS_DIR, 'radar_chart_comparison.png'))
    plt.close()

create_radar_chart()
print("All advanced visuals generated successfully!")
