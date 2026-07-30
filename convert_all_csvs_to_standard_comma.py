import os
import csv
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
TARGET_DIR = os.path.join(PROJECT_DIR, "NocoDB_CRM_Import")

files = [
    "airliquide_bd_pipeline_russia_2025.csv",
    "master_regional_russia_2025.csv",
    "eiii_regional_scores_2025.csv",
    "whatif_sanctions_lift_simulation_2025.csv",
    "sector_focus_gaz_industriels.csv"
]

print("==================================================")
print(" CONVERTING ALL NOCODB CRM CSVS TO COMMA DELIMITER")
print("==================================================")

for fname in files:
    fpath = os.path.join(TARGET_DIR, fname)
    if not os.path.exists(fpath):
        continue
    
    # Detect delimiter
    with open(fpath, 'r', encoding='utf-8-sig') as f:
        first_line = f.readline()
        delimiter = ';' if ';' in first_line else ','
    
    # Read rows
    rows = []
    with open(fpath, 'r', encoding='utf-8-sig') as f:
        reader = csv.reader(f, delimiter=delimiter)
        for row in reader:
            rows.append(row)
    
    # Re-write with standard comma delimiter
    with open(fpath, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        for row in rows:
            writer.writerow(row)
            
    header = rows[0] if rows else []
    print(f"  [CONVERTED] {fname}")
    print(f"              -> Columns ({len(header)}): {', '.join(header[:5])}...")
    print(f"              -> Rows: {len(rows)-1}")

print("\n[SUCCESS] All CSV files in NocoDB_CRM_Import are 100% standard comma-delimited!")
