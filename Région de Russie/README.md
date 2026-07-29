# 🇷🇺 Région de Russie — Données Rosstat 2025
## Business Development Air Liquide | EIII Regional Scoring

> **Source officielle :** Rosstat — *«Регионы России: Социально-экономические показатели 2025»* (1037 pages, `Region_Pokaz_2025.pdf`)

---

## 📁 Fichiers CSV Générés

| Fichier | Contenu | Lignes | Usage |
|---|---|---|---|
| [`master_regional_russia_2025.csv`](./master_regional_russia_2025.csv) | **Master principal** — tous indicateurs par région | 85 | Power BI heatmap, analyse macro |
| [`sector_focus_gaz_industriels.csv`](./sector_focus_gaz_industriels.csv) | Focus secteurs O₂/N₂/H₂/CO₂ | 85 | Ciblage commercial Air Liquide |
| [`eiii_regional_scores_2025.csv`](./eiii_regional_scores_2025.csv) | Scoring EIII détaillé par pilier | 85 | Benchmark investissement |
| [`airliquide_bd_pipeline_russia_2025.csv`](./airliquide_bd_pipeline_russia_2025.csv) | Pipeline BD Tier 1+2 | 31 | CRM Salesforce, pipeline |
| [`whatif_sanctions_lift_simulation_2025.csv`](./whatif_sanctions_lift_simulation_2025.csv) | Simulation ROI 5 scénarios sanctions | 100 | What-if CFO analysis |
| [`consolidate_regional_data.py`](./consolidate_regional_data.py) | Script Python consolidation auto | — | Mise à jour continue |

---

## 📊 Structure des CSV

### `master_regional_russia_2025.csv` — Colonnes

| Colonne | Type | Description | Source Rosstat |
|---|---|---|---|
| `Region_Oblast` | str | Nom officiel région | Table 1.1 p.19 |
| `Federal_District` | str | District fédéral (8) | Table 1.1 p.19 |
| `Population_2024_thou` | float | Population 1er jan 2024 (milliers) | Table 1.1 p.19 |
| `GRP_PRB_2023_bln_rub` | float | Produit Régional Brut 2023 (Mrd ₽) | Table 1.1 p.19 |
| `Investment_Fixed_Capital_bln_rub` | float | Investissements capital fixe (Mrd ₽) | Table 1.1 p.19 |
| `Industrial_Production_Index_2024` | float | Indice production industrielle 2024 vs 2023 | Table 1.2 p.21 |
| `Metallurgy_Mining_Output_bln_rub` | float | **Proxy métallurgie** (mining + 40% mfg) | Calculé |
| `Chemical_Petrochemical_Output_bln_rub` | float | **Proxy chimie** (25% manufacturing) | Calculé |
| `Manufacturing_Total_bln_rub` | float | Production mfg totale (Mrd ₽) | Table 1.1 p.20 |
| `Energy_Gas_Water_Supply_bln_rub` | float | Énergie+gaz+eau (Mrd ₽) | Table 1.1 p.20 |
| `Agriculture_Output_bln_rub` | float | Production agricole (Mrd ₽) | Table 1.1 p.20 |
| `Construction_Volume_thou_m2` | float | Construction logements (milliers m²) | Table 1.1 p.20 |
| `Gas_Industrial_Demand_Proxy_bln_rub` | float | **PROXY CLEF** demande gaz industriels | Calculé |
| `EIII_Regional_Score` | float | **Score EIII** régional (0-100) | Calculé |
| `Top_Opportunity_Sector_For_Gases` | str | Secteur prioritaire Air Liquide | Calculé |
| `Source_Rosstat_Page` | str | Référence Rosstat + acteurs clés | Documentation |

---

## 🧮 Formules de Calcul

### Gas_Industrial_Demand_Proxy
```
Gas_Proxy = 0.40 × Métallurgie_Proxy
           + 0.30 × Chimie_Proxy
           + 0.20 × Énergie
           + 0.10 × Agriculture

Métallurgie_Proxy = Mining_Output × 0.6 + Manufacturing × 0.35
Chimie_Proxy      = Manufacturing × 0.25
```

### EIII_Regional_Score (0-100)
```
EIII = 25% × Pilier_Économie
      + 20% × Pilier_Industrie_Lourde
      + 20% × Pilier_Énergie
      + 15% × Pilier_Logistique
      + 20% × Pilier_Dynamisme_Industriel
```

| Pilier | Formule | Normalisation |
|---|---|---|
| Économie | (GRP/310 + Investissements/65) / 2 | /100 |
| Industrie | (Mining×0.6 + Mfg×0.35) / 18 | /100 |
| Énergie | Energy_Gas_Water / 6.2 | /100 |
| Logistique | (Construction×0.3 + Pop×0.01) / 38 | /100 |
| Dynamisme | (IndProdIndex - 95) × 10 | clamped 0-100 |

### Scores Gaz par Type (0-10)
```
O₂  = (Metallurgy/100 + Mfg/50×0.35) × 3
N₂  = (Metallurgy/80 + Mfg/200) × 2.5
H₂  = (Mfg/60 + Energy/80) × 2
CO₂ = (Agriculture/80 + Mfg/400) × 3
Ar  = (Mfg/300 + Metallurgy/200) × 2
```

---

## 🏆 Top Régions Air Liquide (EIII Score)

| Rang | Région | EIII | Gaz Proxy (Mrd ₽) | Tier |
|---|---|---|---|---|
| 1 | г. Москва | 92.3 | 956 | TIER 2 |
| 2 | Московская область | 71.1 | 725 | TIER 1 |
| 3 | Тюменская область | 59.5 | 2419 | **TIER 1** |
| 4 | Республика Татарстан | 53.0 | 615 | TIER 1 |
| 5 | г. Санкт-Петербург | 52.4 | 526 | TIER 1 |
| 6 | Свердловская область | 51.0 | 596 | TIER 1 |
| 7 | Ямало-Ненецкий АО | 49.5 | 727 | TIER 1 |
| 8 | Красноярский край | 48.6 | 747 | TIER 1 |
| 9 | Кемеровская область | 45.4 | 550 | TIER 1 |
| 10 | Краснодарский край | 44.7 | 367 | TIER 2 |

---

## 📈 Intégration Power BI Dashboard

### Étapes de connexion
1. **Importer les données**
   - `Accueil > Obtenir des données > Texte/CSV`
   - Sélectionner tous les 5 CSV (séparateur `;`, encodage UTF-8)
   
2. **Modèle de données (Star Schema)**
   ```
   FAIT: master_regional_russia_2025
   ├── DIM: eiii_regional_scores_2025 (clé: Region_Oblast)
   ├── DIM: sector_focus_gaz_industriels (clé: Region_Oblast)
   └── FAIT: whatif_sanctions_lift_simulation (clé: Region_Oblast + Scenario)
   ```

3. **Visuels recommandés**

   | Visuel | Source | Champs |
   |---|---|---|
   | 🗺️ Heatmap Russie | master + eiii | Region_Oblast → EIII_Score (couleur) |
   | 📊 Barres EIII | eiii_regional | Top20 par EIII_Score |
   | 🔴🟡🟢 KPI Signals | eiii_regional | Investment_Signal (BUY/WATCH/AVOID) |
   | 💰 Scatter ROI | pipeline | CAPEX vs Revenue (bulles = Gas_Proxy) |
   | 📈 What-If Line | whatif | Scenario × Revenue_M_EUR_yr |
   | 🥧 Pie Gaz | sector | O2/N2/H2/CO2 Need Scores |

4. **Mesures DAX EIII**
   ```dax
   EIII_Avg = AVERAGE(eiii_regional_scores_2025[EIII_Regional_Score])
   
   Gas_Total_Demand_Mrd = 
       SUM(master_regional_russia_2025[Gas_Industrial_Demand_Proxy_bln_rub])
   
   Revenue_Post_Sanctions = 
       SUM(airliquide_bd_pipeline_russia_2025[Revenue_Post_Sanctions_M_EUR_yr])
   
   Multiplier_Sanctions = 
       DIVIDE([Revenue_Post_Sanctions], [Revenue_Baseline])
   ```

5. **Slicer recommandés**
   - `Federal_District` (dropdown multi-select)
   - `AirLiquide_BD_Priority` (TIER 1/2/3/4)
   - `Investment_Signal` (BUY / WATCH / CAUTION / AVOID)
   - `Scenario` (What-If sanctions)

---

## 🐍 Script Python — Consolidation Automatique

```bash
# Installation des dépendances
pip install pandas numpy pdfplumber openpyxl

# Usage basique (déposer vos CSV dans ./input/)
python consolidate_regional_data.py

# Usage avancé avec mise à jour du master existant
python consolidate_regional_data.py \
    --input-dir ./nouvelles_donnees \
    --output-dir ./output \
    --master-file ./master_regional_russia_2025.csv

# Résultat automatique :
# ✓ consolidated_master.csv
# ✓ sector_focus_gaz_industriels_consolidated.csv
# ✓ eiii_scores_consolidated.csv
```

### Ce que fait le script automatiquement :
- ✅ Détection du séparateur CSV (`;`, `,`, `\t`)
- ✅ Reconnaissance des colonnes en Russe/Français/Anglais
- ✅ Détection automatique du district fédéral depuis le nom de région
- ✅ Calcul Gas_Demand_Proxy, EIII, Top_Sector
- ✅ Déduplication intelligente (garde le GRP le plus élevé)
- ✅ Export UTF-8 BOM compatible Excel

---

## 🎯 Simulation What-If Sanctions

Le fichier `whatif_sanctions_lift_simulation_2025.csv` modélise 5 scénarios :

| Scénario | Multiplicateur | Interprétation |
|---|---|---|
| `Baseline_Sanctions_2025` | ×1.0 | Situation actuelle (sanctions UE/US en vigueur) |
| `Partial_Lift_2026` | ×1.4 | Levée partielle (énergie seulement) |
| `Full_Lift_2027` | ×2.0 | Levée complète des sanctions commerciales |
| `Recovery_2028` | ×2.8 | Reprise investissements étrangers |
| `Boom_2030` | ×4.2 | Boom post-réintégration (scénario optimiste) |

**Revenu Air Liquide estimé :**
- Baseline sanctions : ~3 M€/an (31 opportunités Tier 1+2)
- Post-levée totale : ~7.6 M€/an
- **Multiplicateur sanctions : ×2.5**

---

## 📋 Districts Fédéraux Couverts

| District | Nb Régions | Gas Proxy Total (Mrd ₽) | Secteur Dominant |
|---|---|---|---|
| Уральский (Oural) | 6 | 5 932 | Pétrole/Gaz/Métallurgie |
| Центральный (Central) | 19 | 3 338 | Manufacturing/Chimie |
| Приволжский (Volga) | 14 | 3 115 | Chimie/Pétrochimie/Auto |
| Сибирский (Sibérie) | 10 | 2 486 | Mining/Aluminium/Charbon |
| Северо-Западный (Nord-Ouest) | 11 | 1 487 | Métallurgie/Pétrochimie |
| Дальневосточный (Extrême-Orient) | 11 | 1 355 | Mining/LNG/Fisheries |
| Южный (Sud) | 8 | 1 095 | Agro/Pétrole/Ports |
| Северо-Кавказский (Caucase-Nord) | 7 | 305 | Agro/Construction |

---

## 🔗 Sources

- **Recueil principal :** `Region_Pokaz_2025.pdf` — Rosstat, 1037 pages
- **Tables utilisées :** 1.1 (p.19-20), 1.2 (p.21-28), sections industrie ch.12-14
- **Données croisées :** XLS Rosstat `Российский статистический ежегодник 2025.xls`
- **Référence proxy gaz :** IEA Industrial Gas Demand Model 2024
- **EIII Methodology :** EUROASIA INDUSTRIAL INVESTMENT INDEX — projet interne

---

*Dernière mise à jour : Juillet 2025 | Données Rosstat 2024-2025*
