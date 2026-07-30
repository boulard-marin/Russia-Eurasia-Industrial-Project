#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===========================================================================
CONSOLIDATEUR AUTOMATIQUE - DONNÉES RÉGIONALES RUSSIE ROSSTAT
===========================================================================
Usage:
    Déposez des fichiers CSV/Excel régionaux dans le répertoire 'input/'
    Ce script les consolide automatiquement dans les formats maîtres.

    python consolidate_regional_data.py [--input-dir ./input] [--output-dir ./]

Auteur: OVERSEER_AI / Projet Russia-Eurasia Industrial
Source: Rosstat "Régions de la Russie - Indicateurs socio-économiques 2025"
===========================================================================
"""

import pandas as pd
import numpy as np
import os
import glob
import argparse
import sys
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')


# ─────────────────────────────────────────────────────────────────────────────
# CONFIGURATION
# ─────────────────────────────────────────────────────────────────────────────

SEPARATOR = ";"
ENCODING = "utf-8-sig"

# Colonnes obligatoires dans les fichiers source
REQUIRED_COLUMNS_MAP = {
    # Colonnes source possibles → colonne cible normalisée
    "регион": "Region_Oblast",
    "region": "Region_Oblast",
    "oblast": "Region_Oblast",
    "федеральный округ": "Federal_District",
    "federal_district": "Federal_District",
    "валовой региональный продукт": "GRP_PRB_2023_bln_rub",
    "grp": "GRP_PRB_2023_bln_rub",
    "vrp": "GRP_PRB_2023_bln_rub",
    "население": "Population_2024_thou",
    "population": "Population_2024_thou",
    "численность": "Population_2024_thou",
    "промышленность": "Manufacturing_Total_bln_rub",
    "manufacturing": "Manufacturing_Total_bln_rub",
    "industrie": "Manufacturing_Total_bln_rub",
    "добыча": "Mining_Output_bln_rub",
    "mining": "Mining_Output_bln_rub",
    "сельское хозяйство": "Agriculture_Output_bln_rub",
    "agriculture": "Agriculture_Output_bln_rub",
    "строительство": "Construction_Volume_thou_m2",
    "construction": "Construction_Volume_thou_m2",
    "энергетика": "Energy_Gas_Water_Supply_bln_rub",
    "energy": "Energy_Gas_Water_Supply_bln_rub",
    "инвестиции": "Investment_Fixed_Capital_bln_rub",
    "investment": "Investment_Fixed_Capital_bln_rub",
    "заработная плата": "Avg_Monthly_Wage_RUB",
    "wage": "Avg_Monthly_Wage_RUB",
    "salaire": "Avg_Monthly_Wage_RUB",
}

FEDERAL_DISTRICTS = {
    "Белгородская": "Центральный", "Брянская": "Центральный",
    "Владимирская": "Центральный", "Воронежская": "Центральный",
    "Ивановская": "Центральный", "Калужская": "Центральный",
    "Костромская": "Центральный", "Курская": "Центральный",
    "Липецкая": "Центральный", "Московская": "Центральный",
    "Орловская": "Центральный", "Рязанская": "Центральный",
    "Смоленская": "Центральный", "Тамбовская": "Центральный",
    "Тверская": "Центральный", "Тульская": "Центральный",
    "Ярославская": "Центральный", "Москва": "Центральный",
    "Карелия": "Северо-Западный", "Коми": "Северо-Западный",
    "Архангельская": "Северо-Западный", "Вологодская": "Северо-Западный",
    "Калининградская": "Северо-Западный", "Ленинградская": "Северо-Западный",
    "Мурманская": "Северо-Западный", "Новгородская": "Северо-Западный",
    "Псковская": "Северо-Западный", "Санкт-Петербург": "Северо-Западный",
    "Адыгея": "Южный", "Калмыкия": "Южный", "Крым": "Южный",
    "Краснодарский": "Южный", "Астраханская": "Южный",
    "Волгоградская": "Южный", "Ростовская": "Южный", "Севастополь": "Южный",
    "Дагестан": "Северо-Кавказский", "Ингушетия": "Северо-Кавказский",
    "Кабардино": "Северо-Кавказский", "Карачаево": "Северо-Кавказский",
    "Осетия": "Северо-Кавказский", "Чеченская": "Северо-Кавказский",
    "Ставропольский": "Северо-Кавказский",
    "Башкортостан": "Приволжский", "Марий": "Приволжский",
    "Мордовия": "Приволжский", "Татарстан": "Приволжский",
    "Удмуртская": "Приволжский", "Чувашская": "Приволжский",
    "Пермский": "Приволжский", "Кировская": "Приволжский",
    "Нижегородская": "Приволжский", "Оренбургская": "Приволжский",
    "Пензенская": "Приволжский", "Самарская": "Приволжский",
    "Саратовская": "Приволжский", "Ульяновская": "Приволжский",
    "Курганская": "Уральский", "Свердловская": "Уральский",
    "Тюменская": "Уральский", "Ханты": "Уральский",
    "Ямало": "Уральский", "Челябинская": "Уральский",
    "Алтай": "Сибирский", "Тыва": "Сибирский", "Хакасия": "Сибирский",
    "Алтайский": "Сибирский", "Красноярский": "Сибирский",
    "Иркутская": "Сибирский", "Кемеровская": "Сибирский",
    "Новосибирская": "Сибирский", "Омская": "Сибирский",
    "Томская": "Сибирский",
    "Бурятия": "Дальневосточный", "Саха": "Дальневосточный",
    "Забайкальский": "Дальневосточный", "Камчатский": "Дальневосточный",
    "Приморский": "Дальневосточный", "Хабаровский": "Дальневосточный",
    "Амурская": "Дальневосточный", "Магаданская": "Дальневосточный",
    "Сахалинская": "Дальневосточный", "Еврейская": "Дальневосточный",
    "Чукотский": "Дальневосточный",
}


# ─────────────────────────────────────────────────────────────────────────────
# FONCTIONS UTILITAIRES
# ─────────────────────────────────────────────────────────────────────────────

def detect_federal_district(region_name: str) -> str:
    """Détecte automatiquement le district fédéral depuis le nom de la région."""
    for keyword, district in FEDERAL_DISTRICTS.items():
        if keyword.lower() in region_name.lower():
            return district
    return "Неизвестный"


def normalize_column_name(col: str) -> str:
    """Normalise les noms de colonnes (Russe/FR/EN → standard)."""
    col_lower = col.lower().strip()
    for key, value in REQUIRED_COLUMNS_MAP.items():
        if key in col_lower:
            return value
    return col


def calc_gas_demand_proxy(row: pd.Series) -> float:
    """
    Calcule le proxy de demande en gaz industriels.
    Formule : 0.40 * Métallurgie + 0.30 * Chimie + 0.20 * Énergie + 0.10 * Agro
    """
    metallurgy = (
        float(row.get("Mining_Output_bln_rub", 0) or 0) * 0.6 +
        float(row.get("Manufacturing_Total_bln_rub", 0) or 0) * 0.35
    )
    chemical = float(row.get("Manufacturing_Total_bln_rub", 0) or 0) * 0.25
    energy = float(row.get("Energy_Gas_Water_Supply_bln_rub", 0) or 0)
    agro = float(row.get("Agriculture_Output_bln_rub", 0) or 0)
    
    proxy = 0.40 * metallurgy + 0.30 * chemical + 0.20 * energy + 0.10 * agro
    return round(proxy, 2)


def calc_eiii_regional(row: pd.Series) -> float:
    """
    Calcule le score EIII Régional (0-100).
    Piliers : Économie 25% | Industrie 20% | Énergie 20% | Logistique 15% | Dynamisme 20%
    """
    grp = float(row.get("GRP_PRB_2023_bln_rub", 0) or 0)
    inv = float(row.get("Investment_Fixed_Capital_bln_rub", 0) or 0)
    mining = float(row.get("Mining_Output_bln_rub", 0) or 0)
    mfg = float(row.get("Manufacturing_Total_bln_rub", 0) or 0)
    nrj = float(row.get("Energy_Gas_Water_Supply_bln_rub", 0) or 0)
    constr = float(row.get("Construction_Volume_thou_m2", 0) or 0)
    pop = float(row.get("Population_2024_thou", 0) or 0)
    ind_idx = float(row.get("Industrial_Production_Index_2024", 100) or 100)
    
    pilier_eco = min((grp / 310.0 + inv / 65.0) / 2, 100)
    pilier_ind = min((mining * 0.6 + mfg * 0.35) / 18.0, 100)
    pilier_nrj = min(nrj / 6.2, 100)
    pilier_log = min((constr * 0.3 + pop * 0.01) / 38.0, 100)
    pilier_dyn = max(0, min((ind_idx - 95) * 10, 100))
    
    eiii = (0.25 * pilier_eco + 0.20 * pilier_ind +
            0.20 * pilier_nrj + 0.15 * pilier_log + 0.20 * pilier_dyn)
    return round(min(eiii, 100), 1)


def get_top_sector(row: pd.Series) -> str:
    """Identifie le secteur prioritaire pour Air Liquide."""
    mining = float(row.get("Mining_Output_bln_rub", 0) or 0)
    mfg = float(row.get("Manufacturing_Total_bln_rub", 0) or 0)
    nrj = float(row.get("Energy_Gas_Water_Supply_bln_rub", 0) or 0)
    agro = float(row.get("Agriculture_Output_bln_rub", 0) or 0)
    
    scores = {
        "Métallurgie": mining * 0.7 + mfg * 0.4,
        "Chimie/Pétrochimie": mfg * 0.35,
        "Énergie/Gaz": nrj * 2.0,
        "Agro-industrie": agro * 0.8,
    }
    return max(scores, key=scores.get)


def get_al_priority(gas_proxy: float) -> str:
    """Attribue la priorité Air Liquide BD."""
    if gas_proxy > 500:
        return "TIER 1 - CRITIQUE"
    elif gas_proxy > 150:
        return "TIER 2 - HAUTE"
    elif gas_proxy > 50:
        return "TIER 3 - MOYENNE"
    else:
        return "TIER 4 - FAIBLE"


def get_investment_signal(eiii: float) -> str:
    """Signal d'investissement basé sur l'EIII."""
    if eiii >= 65:
        return "BUY"
    elif eiii >= 40:
        return "WATCH"
    elif eiii >= 25:
        return "CAUTION"
    else:
        return "AVOID"


# ─────────────────────────────────────────────────────────────────────────────
# LECTURE DES FICHIERS SOURCE
# ─────────────────────────────────────────────────────────────────────────────

def load_csv_file(filepath: str) -> pd.DataFrame:
    """Charge un fichier CSV avec détection automatique du séparateur."""
    for sep in [";", ",", "\t", "|"]:
        try:
            df = pd.read_csv(filepath, sep=sep, encoding="utf-8-sig")
            if len(df.columns) > 2:
                return df
        except Exception:
            pass
    try:
        return pd.read_csv(filepath, encoding="utf-8")
    except Exception as e:
        print(f"  ⚠ Erreur lecture {filepath}: {e}")
        return pd.DataFrame()


def load_excel_file(filepath: str) -> pd.DataFrame:
    """Charge un fichier Excel (toutes feuilles)."""
    frames = []
    try:
        xl = pd.ExcelFile(filepath)
        for sheet in xl.sheet_names:
            df = xl.parse(sheet)
            if len(df) > 2:
                frames.append(df)
    except Exception as e:
        print(f"  ⚠ Erreur lecture Excel {filepath}: {e}")
    return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()


def normalize_dataframe(df: pd.DataFrame, source_file: str) -> pd.DataFrame:
    """
    Normalise un DataFrame quelconque vers le format maître.
    Renomme les colonnes, détecte les districts, calcule les proxies.
    """
    if df.empty:
        return df
    
    # Renommage des colonnes
    rename_map = {}
    for col in df.columns:
        normalized = normalize_column_name(str(col))
        if normalized != str(col):
            rename_map[col] = normalized
    df = df.rename(columns=rename_map)
    
    # Assurer Region_Oblast
    if "Region_Oblast" not in df.columns:
        # Chercher première colonne texte non-numérique
        for col in df.columns:
            if df[col].dtype == object and df[col].notna().sum() > 0:
                df = df.rename(columns={col: "Region_Oblast"})
                break
    
    # Détecter Federal_District si absent
    if "Federal_District" not in df.columns and "Region_Oblast" in df.columns:
        df["Federal_District"] = df["Region_Oblast"].apply(detect_federal_district)
    
    # Convertir colonnes numériques
    numeric_cols = [
        "Population_2024_thou", "GRP_PRB_2023_bln_rub",
        "Investment_Fixed_Capital_bln_rub", "Industrial_Production_Index_2024",
        "Mining_Output_bln_rub", "Manufacturing_Total_bln_rub",
        "Energy_Gas_Water_Supply_bln_rub", "Agriculture_Output_bln_rub",
        "Construction_Volume_thou_m2", "Retail_Trade_bln_rub",
        "Avg_Monthly_Wage_RUB", "Agriculture_Index_2024"
    ]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(
                df[col].astype(str).str.replace(",", ".").str.replace(" ", ""),
                errors="coerce"
            )
    
    # Calculer les proxies si pas déjà présents
    if "Gas_Industrial_Demand_Proxy_bln_rub" not in df.columns:
        df["Gas_Industrial_Demand_Proxy_bln_rub"] = df.apply(calc_gas_demand_proxy, axis=1)
    
    if "EIII_Regional_Score" not in df.columns:
        df["EIII_Regional_Score"] = df.apply(calc_eiii_regional, axis=1)
    
    if "Top_Opportunity_Sector_For_Gases" not in df.columns:
        df["Top_Opportunity_Sector_For_Gases"] = df.apply(get_top_sector, axis=1)
    
    if "AirLiquide_BD_Priority" not in df.columns:
        df["AirLiquide_BD_Priority"] = df["Gas_Industrial_Demand_Proxy_bln_rub"].apply(get_al_priority)
    
    if "Investment_Signal" not in df.columns:
        df["Investment_Signal"] = df["EIII_Regional_Score"].apply(get_investment_signal)
    
    # Ajouter traçabilité
    df["Source_File"] = os.path.basename(source_file)
    df["Loaded_At"] = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    return df


# ─────────────────────────────────────────────────────────────────────────────
# CONSOLIDATION PRINCIPALE
# ─────────────────────────────────────────────────────────────────────────────

def consolidate_regional_data(input_dir: str, output_dir: str, master_file: str = None) -> dict:
    """
    Consolide tous les fichiers CSV/Excel du répertoire input_dir.
    
    Args:
        input_dir: Répertoire contenant les fichiers source
        output_dir: Répertoire de sortie pour les CSV consolidés
        master_file: Fichier maître existant à mettre à jour (optionnel)
    
    Returns:
        dict avec les DataFrames générés
    """
    print(f"\n{'='*70}")
    print("CONSOLIDATEUR ROSSTAT - RÉGIONS DE RUSSIE 2025")
    print(f"{'='*70}")
    print(f"Input : {input_dir}")
    print(f"Output: {output_dir}")
    
    # Charger le fichier maître existant si disponible
    frames = []
    if master_file and os.path.exists(master_file):
        print(f"\nChargement master existant: {master_file}")
        df_master_existing = pd.read_csv(master_file, sep=";", encoding="utf-8-sig")
        frames.append(df_master_existing)
        print(f"  ✓ {len(df_master_existing)} régions chargées")
    
    # Scanner les fichiers source
    patterns = ["*.csv", "*.xlsx", "*.xls", "*.CSV"]
    source_files = []
    for pattern in patterns:
        source_files.extend(glob.glob(os.path.join(input_dir, "**", pattern), recursive=True))
    
    # Exclure les fichiers de sortie déjà générés
    output_files = {
        "master_regional_russia_2025.csv",
        "sector_focus_gaz_industriels.csv",
        "eiii_regional_scores_2025.csv",
        "airliquide_bd_pipeline_russia_2025.csv",
        "whatif_sanctions_lift_simulation_2025.csv",
        "consolidated_master.csv",
    }
    source_files = [f for f in source_files if os.path.basename(f) not in output_files]
    
    print(f"\nFichiers détectés: {len(source_files)}")
    
    for filepath in source_files:
        print(f"\n  📄 {os.path.basename(filepath)}")
        ext = os.path.splitext(filepath)[1].lower()
        
        if ext in [".csv"]:
            df = load_csv_file(filepath)
        elif ext in [".xlsx", ".xls"]:
            df = load_excel_file(filepath)
        else:
            print(f"    ⚠ Format non supporté: {ext}")
            continue
        
        if df.empty:
            print(f"    ⚠ Fichier vide ou illisible")
            continue
        
        print(f"    → {len(df)} lignes × {len(df.columns)} colonnes")
        df_norm = normalize_dataframe(df, filepath)
        
        if "Region_Oblast" in df_norm.columns and not df_norm.empty:
            frames.append(df_norm)
            print(f"    ✓ Normalisé et ajouté")
        else:
            print(f"    ⚠ Colonne Region_Oblast non trouvée, ignoré")
    
    if not frames:
        print("\n⚠ Aucune donnée à consolider.")
        return {}
    
    # Consolidation
    df_all = pd.concat(frames, ignore_index=True, sort=False)
    
    # Déduplication par région (garder la ligne avec le GRP le plus récent/élevé)
    if "Region_Oblast" in df_all.columns:
        df_all["GRP_PRB_2023_bln_rub"] = pd.to_numeric(
            df_all.get("GRP_PRB_2023_bln_rub", 0), errors="coerce"
        ).fillna(0)
        df_all = (df_all
                  .sort_values("GRP_PRB_2023_bln_rub", ascending=False)
                  .drop_duplicates(subset=["Region_Oblast"], keep="first"))
    
    # Recalculer les scores sur le dataset final
    df_all["Gas_Industrial_Demand_Proxy_bln_rub"] = df_all.apply(calc_gas_demand_proxy, axis=1)
    df_all["EIII_Regional_Score"] = df_all.apply(calc_eiii_regional, axis=1)
    df_all["Top_Opportunity_Sector_For_Gases"] = df_all.apply(get_top_sector, axis=1)
    df_all["AirLiquide_BD_Priority"] = df_all["Gas_Industrial_Demand_Proxy_bln_rub"].apply(get_al_priority)
    df_all["Investment_Signal"] = df_all["EIII_Regional_Score"].apply(get_investment_signal)
    
    # Tri EIII décroissant
    df_all = df_all.sort_values("EIII_Regional_Score", ascending=False)
    
    # ─── EXPORT DES FICHIERS ─────────────────────────────────────────────
    
    os.makedirs(output_dir, exist_ok=True)
    results = {}
    
    # 1. Master consolidé
    out_master = os.path.join(output_dir, "consolidated_master.csv")
    df_all.to_csv(out_master, sep=SEPARATOR, index=False, encoding=ENCODING)
    results["master"] = df_all
    print(f"\n✓ consolidated_master.csv ({len(df_all)} régions)")
    
    # 2. Focus secteurs gaz
    gas_cols = [
        "Region_Oblast", "Federal_District", "EIII_Regional_Score",
        "AirLiquide_BD_Priority", "Gas_Industrial_Demand_Proxy_bln_rub",
        "Mining_Output_bln_rub", "Manufacturing_Total_bln_rub",
        "Energy_Gas_Water_Supply_bln_rub", "Agriculture_Output_bln_rub",
        "Industrial_Production_Index_2024", "Top_Opportunity_Sector_For_Gases",
        "Source_File",
    ]
    df_gas = df_all[[c for c in gas_cols if c in df_all.columns]].copy()
    
    # Scores O2/N2/H2/CO2
    df_gas["O2_Need_Score"] = df_gas.apply(
        lambda r: round(min((float(r.get("Mining_Output_bln_rub", 0) or 0) / 100 + 
                             float(r.get("Manufacturing_Total_bln_rub", 0) or 0) / 50 * 0.35) * 3, 10), 2), axis=1)
    df_gas["N2_Need_Score"] = df_gas.apply(
        lambda r: round(min((float(r.get("Mining_Output_bln_rub", 0) or 0) / 80 + 
                             float(r.get("Manufacturing_Total_bln_rub", 0) or 0) / 200) * 2.5, 10), 2), axis=1)
    df_gas["H2_Need_Score"] = df_gas.apply(
        lambda r: round(min((float(r.get("Manufacturing_Total_bln_rub", 0) or 0) / 60 + 
                             float(r.get("Energy_Gas_Water_Supply_bln_rub", 0) or 0) / 80) * 2, 10), 2), axis=1)
    df_gas["CO2_Need_Score"] = df_gas.apply(
        lambda r: round(min((float(r.get("Agriculture_Output_bln_rub", 0) or 0) / 80 + 
                             float(r.get("Manufacturing_Total_bln_rub", 0) or 0) / 400) * 3, 10), 2), axis=1)
    
    df_gas = df_gas.sort_values("Gas_Industrial_Demand_Proxy_bln_rub", ascending=False)
    out_gas = os.path.join(output_dir, "sector_focus_gaz_industriels_consolidated.csv")
    df_gas.to_csv(out_gas, sep=SEPARATOR, index=False, encoding=ENCODING)
    results["sector_gaz"] = df_gas
    print(f"✓ sector_focus_gaz_industriels_consolidated.csv")
    
    # 3. Scores EIII
    eiii_cols = [
        "Region_Oblast", "Federal_District", "EIII_Regional_Score",
        "Investment_Signal", "GRP_PRB_2023_bln_rub",
        "Investment_Fixed_Capital_bln_rub", "Gas_Industrial_Demand_Proxy_bln_rub",
        "Industrial_Production_Index_2024", "Population_2024_thou",
        "AirLiquide_BD_Priority",
    ]
    df_eiii = df_all[[c for c in eiii_cols if c in df_all.columns]].copy()
    df_eiii = df_eiii.sort_values("EIII_Regional_Score", ascending=False)
    out_eiii = os.path.join(output_dir, "eiii_scores_consolidated.csv")
    df_eiii.to_csv(out_eiii, sep=SEPARATOR, index=False, encoding=ENCODING)
    results["eiii"] = df_eiii
    print(f"✓ eiii_scores_consolidated.csv")
    
    # ─── RAPPORT FINAL ───────────────────────────────────────────────────
    
    print(f"\n{'='*70}")
    print(f"RAPPORT DE CONSOLIDATION - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"{'='*70}")
    print(f"Total régions consolidées : {len(df_all)}")
    print(f"\nTop 10 EIII_Regional_Score :")
    top10_cols = ["Region_Oblast", "EIII_Regional_Score", "Investment_Signal",
                  "Gas_Industrial_Demand_Proxy_bln_rub", "AirLiquide_BD_Priority"]
    available_cols = [c for c in top10_cols if c in df_all.columns]
    print(df_all[available_cols].head(10).to_string(index=False))
    
    if "AirLiquide_BD_Priority" in df_all.columns:
        print(f"\nRépartition priorités Air Liquide :")
        print(df_all["AirLiquide_BD_Priority"].value_counts().to_string())
    
    print(f"\nFichiers générés dans: {output_dir}")
    for key, df in results.items():
        print(f"  ✓ {key}: {len(df)} entrées")
    
    return results


# ─────────────────────────────────────────────────────────────────────────────
# POINT D'ENTRÉE
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Consolidateur de données régionales Russie Rosstat → CSV Air Liquide"
    )
    parser.add_argument(
        "--input-dir", default="./input",
        help="Répertoire contenant les fichiers CSV/Excel source (default: ./input)"
    )
    parser.add_argument(
        "--output-dir", default=".",
        help="Répertoire de sortie des CSV (default: répertoire courant)"
    )
    parser.add_argument(
        "--master-file", default=None,
        help="Fichier master_regional_russia_2025.csv existant à mettre à jour"
    )
    args = parser.parse_args()
    
    # Créer le répertoire input si nécessaire
    os.makedirs(args.input_dir, exist_ok=True)
    
    results = consolidate_regional_data(
        input_dir=args.input_dir,
        output_dir=args.output_dir,
        master_file=args.master_file
    )
    
    if results:
        print("\n✅ Consolidation terminée avec succès!")
    else:
        print("\n⚠ Aucun fichier traité. Déposez des CSV/Excel dans le répertoire input/")
        print("  Exemple: python consolidate_regional_data.py --input-dir ./mes_donnees")
