import os
import shutil
import csv
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
SOURCE_DIR = os.path.join(PROJECT_DIR, "Région de Russie", "_backup_pre_fix")
TARGET_DIR = os.path.join(PROJECT_DIR, "NocoDB_CRM_Import")

os.makedirs(TARGET_DIR, exist_ok=True)

files_to_copy = [
    "airliquide_bd_pipeline_russia_2025.csv",
    "master_regional_russia_2025.csv",
    "eiii_regional_scores_2025.csv",
    "whatif_sanctions_lift_simulation_2025.csv",
    "sector_focus_gaz_industriels.csv"
]

print("==================================================")
print(" PREPARING NOCODB CRM DIRECT IMPORT FILES")
print("==================================================")

for fname in files_to_copy:
    src = os.path.join(SOURCE_DIR, fname)
    dst = os.path.join(TARGET_DIR, fname)
    if os.path.exists(src):
        shutil.copy2(src, dst)
        with open(dst, 'r', encoding='utf-8-sig') as f:
            reader = csv.reader(f)
            header = next(reader, None)
            row_count = sum(1 for _ in reader)
        print(f"  [READY] {fname}")
        print(f"          -> Columns ({len(header or [])}): {', '.join((header or [])[:5])}...")
        print(f"          -> Rows: {row_count}")
        print(f"          -> Path: {dst}")

print("\n[COMPLETE] All CRM CSV files are ready in folder: NocoDB_CRM_Import")
