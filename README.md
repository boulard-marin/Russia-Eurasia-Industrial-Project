# 🇷🇺 EUROASIA INDUSTRIAL INVESTMENT SYSTEM
## Russia 85-Region Strategic Analysis | Air Liquide Gas Industrial BD

![Status](https://img.shields.io/badge/Status-Active-success?style=flat-square)
![Data](https://img.shields.io/badge/Source-Rosstat_2025-blue?style=flat-square)
![Regions](https://img.shields.io/badge/Regions-85-orange?style=flat-square)
![EIII](https://img.shields.io/badge/EIII_Score-0--100-purple?style=flat-square)
![Python](https://img.shields.io/badge/Python-3.11-yellow?style=flat-square&logo=python)
![NocoDB](https://img.shields.io/badge/NocoDB-MCP_Connected-10B981?style=flat-square)
![PowerBI](https://img.shields.io/badge/Power_BI-Connected-F2C811?style=flat-square&logo=powerbi)
![Tableau](https://img.shields.io/badge/Tableau-Public-E97627?style=flat-square&logo=tableau)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

---

> **TL;DR :** Système de Business Intelligence complet modélisant les **85 régions de Russie** comme marchés cibles pour les gaz industriels (O₂/N₂/H₂/CO₂/Ar). Score EIII propriétaire (0-100), pipeline BD 31 opportunités Tier 1-4, simulation Monte Carlo 10 000 itérations, what-if levée des sanctions. Stack : **Python + NocoDB MCP Remote + Power BI + ArcGIS/Kepler.gl + Neo4j + Tableau Public + Excel Power Query**.

---

## 🔥 Scénario Clé : What-If Sanctions 2025-2030

Le cœur du projet : *"Que se passe-t-il si l'UE lève les sanctions contre la Russie ?"*

| Scénario | Année | Multiplicateur | Revenue Air Liquide |
|---|---|---|---|
| Baseline (sanctions actives) | 2025 | ×1.0 | ~3 M€/an |
| Levée partielle (énergie) | 2026 | ×1.4 | ~4.2 M€/an |
| Levée totale | 2027 | ×2.0 | ~6 M€/an |
| Reprise IDE | 2028 | ×2.8 | ~8.4 M€/an |
| **Boom post-réintégration** | **2030** | **×4.2** | **~12.6 M€/an** |

**Variables déterminantes (Monte Carlo):** Taux win contrats (+0.53) > Taux RUB/EUR (-0.51) > Durée sanctions (-0.51) > Upside politique (+0.26)

---

## 📐 EIII — Eastern Industrial Investment Index

L'**EIII Régional** (0-100) est un indicateur composite d'aide à la décision :

```
EIII = 25% × Économie  (GRP + Investissements)
     + 20% × Industrie  (Mining + Manufacturing lourd)
     + 20% × Énergie    (Production électricité/gaz/eau)
     + 15% × Logistique (Construction + démographie)
     + 20% × Dynamisme  (Indice production industrielle 2024)
```

| Signal | EIII | Interprétation |
|---|---|---|
| 🟢 **BUY** | ≥ 65 | Investissement prioritaire — déploiement immédiat |
| 🟡 **WATCH** | 40-64 | Surveiller — opportunité conditionnelle |
| 🟠 **CAUTION** | 25-39 | Approche prudente — risques identifiés |
| 🔴 **AVOID** | < 25 | Hors périmètre — ROI insuffisant |

---

## 🏆 Top 10 Régions — EIII × Gas Demand

| # | Région | District | EIII | Gas Proxy (Mrd ₽) | Signal | Secteur |
|---|---|---|---|---|---|---|
| 1 | г. Москва | Central | **92.3** | 956 | 🟢 BUY | Pharma/Chimie |
| 2 | Московская область | Central | **71.1** | 725 | 🟢 BUY | Mfg diversifiée |
| 3 | Тюменская область | Oural | 59.5 | **2 419** 🔥 | 🟡 WATCH | Pétrole/Gaz |
| 4 | Республика Татарстан | Volga | 53.0 | 615 | 🟡 WATCH | Pétrochimie |
| 5 | г. Санкт-Петербург | Nord-Ouest | 52.4 | 526 | 🟡 WATCH | Industrie lourde |
| 6 | Свердловская область | Oural | 51.0 | 596 | 🟡 WATCH | Métallurgie 🏭 |
| 7 | Ямало-Ненецкий АО | Oural | 49.5 | 727 | 🟡 WATCH | Gaz naturel |
| 8 | Красноярский край | Sibérie | 48.6 | 747 | 🟡 WATCH | Norilsk Ni/Al |
| 9 | Кемеровская область | Sibérie | 45.4 | 550 | 🟡 WATCH | Charbon/Acier |
| 10 | Краснодарский край | Sud | 44.7 | 367 | 🟡 WATCH | Agro/Port |

> **Source :** Rosstat *«Регионы России — Социально-экономические показатели 2025»*, 1037 pages, Tables 1.1-1.2

---

## 🗂️ Architecture des Données

```
┌─────────────────────────────────────────────────────────────────┐
│              Region_Pokaz_2025.pdf (Rosstat, 1037p)             │
│              + Российский статистический ежегодник 2025.xls     │
└──────────────────────────┬──────────────────────────────────────┘
                           │  Python pdfplumber + pandas
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                      CSV LAYER (85 régions)                     │
│  master_regional (19 col) │ sector_gaz │ eiii_scores │ pipeline │
└──────────────────────────┬──────────────────────────────────────┘
          ┌────────────────┼────────────────┬──────────────┐
          ▼                ▼                ▼              ▼
   ┌────────────┐  ┌─────────────┐  ┌───────────┐  ┌──────────────┐
   │  Power BI  │  │ NocoDB MCP  │  │ Kepler.gl │  │  Tableau     │
   │  7 pages   │  │ Remote Engine│  │ Geo map   │  │  Public      │
   └────────────┘  └─────────────┘  └───────────┘  └──────────────┘
          │                                │
          ▼                                ▼
   ┌────────────┐                  ┌───────────────┐
   │  Neo4j /   │                  │  Monte Carlo  │
   │  Gephi     │                  │  10K iters    │
   │  Réseau    │                  │  Risk Sim     │
   └────────────┘                  └───────────────┘
```

---

## 📁 Structure du Repository

```
📦 Russia-Eurasia-Industrial-Project/
│
├── 📂 Région de Russie/              ← DONNÉES CORE
│   ├── 📄 Region_Pokaz_2025.pdf     ← Source Rosstat (1037 pages)
│   ├── 📊 master_regional_russia_2025.csv      (85 régions × 19 colonnes)
│   ├── 📊 sector_focus_gaz_industriels.csv     (scores O2/N2/H2/CO2/Ar)
│   ├── 📊 eiii_regional_scores_2025.csv        (5 piliers EIII)
│   ├── 📊 airliquide_bd_pipeline_russia_2025.csv (31 opportunités)
│   ├── 📊 whatif_sanctions_lift_simulation_2025.csv (5 scénarios)
│   ├── 📊 geo_coordinates.csv                  (lat/lng 85 régions)
│   ├── 📊 master_geo_regional_russia_2025.csv  (master + coordonnées)
│   ├── 🐍 consolidate_regional_data.py         (auto-consolidation)
│   ├── 📂 analysis/
│   │   ├── 🐍 monte_carlo_risk.py              (simulation 10K iter.)
│   │   ├── 🐍 generate_geo_coordinates.py      (Kepler.gl / ArcGIS)
│   │   └── 📂 outputs/
│   │       ├── 📊 monte_carlo_results.csv
│   │       ├── 📊 monte_carlo_summary.csv
│   │       └── 🖼️ monte_carlo_results.png
│   └── README.md
│
├── 📂 contexte/Russie/               ← ANALYSES QUALITATIVES
│   ├── Industry/ Agriculture/ Energy/ Transport/
│   ├── Finance/ Labor/ People/ Prices/
│   ├── External economic relation/ Environnement/
│   └── Sources Chiffres/
│       ├── analyse_brics_russie.xlsx
│       └── Российский статистический ежегодник 2025.xls
│
├── 📂 crm_simulation/                ← SALESFORCE
│   └── salesforce_pipeline.csv
│
└── README.md                         ← CE FICHIER
```

---

## 🚀 Quick Start

### 1. Installation
```bash
git clone https://github.com/[votre-profil]/Russia-Eurasia-Industrial-Project.git
cd Russia-Eurasia-Industrial-Project
pip install pandas numpy pdfplumber openpyxl matplotlib scipy
```

### 2. Générer tous les CSV
```bash
cd "Région de Russie"
python consolidate_regional_data.py
```

### 3. Lancer la simulation Monte Carlo
```bash
python analysis/monte_carlo_risk.py --iterations 10000 --export
# → outputs/monte_carlo_results.png + .csv
```

### 4. Préparer la carte Kepler.gl
```bash
python analysis/generate_geo_coordinates.py
# → master_geo_regional_russia_2025.csv (avec lat/lng)
```

### 5. Ajouter de nouvelles données régionales
```bash
# Déposer vos CSV/Excel dans input/
python consolidate_regional_data.py --input-dir ./input
# Colonnes reconnues automatiquement en Russe/Français/Anglais
```

---

## 🛠️ Tech Stack & Outils

### Data Engineering
| Outil | Usage | Fichier |
|---|---|---|
| Python 3.11 + pandas | ETL, calculs EIII, Monte Carlo | `*.py` |
| pdfplumber | Extraction PDF Rosstat (1037p) | `extract_*.py` |
| NumPy + SciPy | Simulation stochastique | `monte_carlo_risk.py` |
| Matplotlib | Graphiques tornado, distribution | `outputs/*.png` |

### Business Intelligence
| Outil | Usage | Données |
|---|---|---|
| **Power BI** ⭐ | Dashboard 7 pages, heatmap EIII | 5 CSV via Direct Query |
| **Tableau Public** | Story Points publics, bulles | master_geo CSV |
| Qlik Sense | Analyse associative, KPIs | Script Qlik custom |
| Excel + Power Query | TCD, Radar, Waterfall CFO | Dossier complet |

### Géospatial
| Outil | Usage | Config |
|---|---|---|
| **Kepler.gl** ⭐ | Carte bubbles EIII × Gas Demand | master_geo + JSON config |
| ArcGIS Online | Choroplèthe professionnel | Shapefile GADM + join |
| Folium / Plotly | Cartes interactives Python | `geo_map.py` [à créer] |

### CRM & Pipeline BD
| Outil | Usage | Import |
|---|---|---|
| **Salesforce** | Pipeline 31 opp, Kanban, Reports | `airliquide_bd_pipeline.csv` |
| HubSpot | Alternative free CRM | Même CSV |

### Graphe & Réseau
| Outil | Usage | Format |
|---|---|---|
| **Neo4j Aura** (free) | Graphe régions-entreprises-gaz | Cypher LOAD CSV |
| Gephi | Visualisation réseau industriel | Export NetworkX → GEXF |

### Documentation & KM
| Outil | Usage |
|---|---|
| **GitHub** ⭐ | Repository, versioning, Actions CI/CD |
| Obsidian | Knowledge base régions, acteurs, EIII |
| Notion | Dashboard projet, Kanban BD, Timeline |

---

## 📊 Résultats Pipeline BD Air Liquide

### Répartition des 31 Opportunités Tier 1+2

```
TIER 1 - CRITIQUE (Gas Proxy > 500 Mrd ₽) :  11 régions
████████████████████ 35% — CAPEX potentiel cumulé : ~12 M€

TIER 2 - HAUTE (Gas Proxy 150-500 Mrd ₽) :   20 régions
████████████████████████████████ 65% — CAPEX : ~5 M€

TIER 3 - MOYENNE (50-150 Mrd ₽) :             ~30 régions
TIER 4 - FAIBLE  (< 50 Mrd ₽) :               ~24 régions
```

### Top Acteurs Industriels Ciblés

| Acteur | Région | Secteur | Gaz Prioritaire |
|---|---|---|---|
| **Газпром / Novatek** | Ямало-НАО | Gaz naturel LNG | H₂, CO₂ |
| **Норильский Никель** | Красноярский | Ni/Cu/PGM | O₂, N₂ |
| **ЕВРАЗ / ММК / НЛМК** | Оural + Centrale | Acier | O₂ (masse) |
| **СИБУР / ТАИФ** | Татарстан + Пермь | Pétrochimie | H₂, N₂ |
| **РУСАЛ** | Красноярск + Иркутск | Aluminium | N₂ |
| **Роснефть / ЛУКОЙЛ** | Тюмень + Уфа | Raffinerie | H₂, CO₂ |
| **Северсталь** | Вологда | Acier | O₂, N₂, Ar |
| **ЕвроХим / Акрон** | Ставрополь + Новгород | Engrais | N₂, CO₂ |

---

## 🎯 Opportunités par Type de Gaz

| Gaz | Secteur Principal | Top Régions | Volume Estimé |
|---|---|---|---|
| **O₂** | Métallurgie (fours BOF) | Свердловская, Кемеровская, Челябинская | ~42% demande |
| **N₂** | Chimie, inertage, métallurgie | Татарстан, Пермь, Оренбург | ~28% demande |
| **H₂** | Raffinage, synthèse NH₃ | Тюмень, Башкирия, Самара | ~18% demande |
| **CO₂** | Serres, agro, food, pharma | Краснодар, Ставрополь, Moscou | ~8% demande |
| **Ar** | Soudure, électronique | Свердловская, Новосибирск | ~4% demande |

---

## 🌐 Intégrations Outils — Guides Rapides

### Power BI
```
1. Obtenir données > Texte/CSV > Sélectionner les 5 CSV du dossier
2. Relation : master[Region_Oblast] → eiii[Region_Oblast] (1:1)
3. Carte : Visuel Carte remplie > Russie > Champ = EIII_Regional_Score
4. DAX : EIII_Weighted = SUMX(master, [EIII]*[GRP]) / SUM([GRP])
5. What-If : Paramètre Slicer Scenario → Revenue_Scenario [DAX]
```

### Kepler.gl (Gratuit, immédiat)
```
1. https://kepler.gl/demo
2. Drag & drop : master_geo_regional_russia_2025.csv
3. Layer 1 : Point | lat=lat | lng=lng
   → Couleur : EIII_Regional_Score (gradient Rouge→Vert)
   → Taille : Gas_Industrial_Demand_Proxy_bln_rub
4. Layer 2 : Heatmap | même fichier
   → Intensité : Gas_Industrial_Demand_Proxy_bln_rub
5. Export screenshot → intégrer README
```

### Neo4j Aura Free
```cypher
-- Créer compte : console.neo4j.io (gratuit 1 instance)
-- Charger données :
LOAD CSV WITH HEADERS FROM
  'https://raw.githubusercontent.com/[profil]/[repo]/main/Région de Russie/master_regional_russia_2025.csv'
AS row FIELDTERMINATOR ';'
MERGE (r:Region {name: row.Region_Oblast})
SET r.eiii = toFloat(row.EIII_Regional_Score),
    r.gas = toFloat(row.Gas_Industrial_Demand_Proxy_bln_rub)
MERGE (d:District {name: row.Federal_District})
MERGE (r)-[:BELONGS_TO]->(d)
```

### Salesforce
```
Setup > Data Import Wizard > Opportunities
→ CSV : airliquide_bd_pipeline_russia_2025.csv
→ Champ Name = Opportunity_ID
→ Amount = Est_CAPEX_Potential_M_EUR
→ Expected_Revenue = Est_Revenue_M_EUR_yr
→ Stage = Stage_BD
→ Champs custom : EIII_Score__c, Gas_Demand__c, BD_Priority__c
```

---

## 📋 Méthodologie & Sources

### Sources de Données
| Source | Type | Couverture |
|---|---|---|
| Rosstat `Region_Pokaz_2025.pdf` | PDF officiel 1037p | 85 régions, 2024-2025 |
| `Российский статистический ежегодник 2025.xls` | XLS Rosstat | Séries longues 2000-2024 |
| `analyse_brics_russie.xlsx` | Analyse interne | Contexte BRICS |
| IEA Industrial Gas Demand Model 2024 | Référence sectorielle | Pondérations proxy gaz |

### Formules Proxy (Transparence Méthodologique)
```python
# Gas Industrial Demand Proxy
Gas_Proxy = (0.40 × (Mining×0.6 + Mfg×0.35)  # Métallurgie
           + 0.30 × (Mfg×0.25)                # Chimie/Pétrochimie
           + 0.20 × Energy_Gas_Water            # Énergie
           + 0.10 × Agriculture)               # Agro-industrie

# Proxy utilisé car les données de consommation gaz industrielle
# par région ne sont pas publiées par Rosstat.
# Calibré sur les ratios industrie-gaz de l'IEA 2024.
```

### Limites & Disclaimer
> ⚠️ Les données post-2022 sont partiellement restreintes (loi fédérale 282-FZ). Certaines valeurs sont estimées par proxy. Ce projet est académique et de simulation. Les estimations financières sont des ordres de grandeur indicatifs.

---

## 📈 Roadmap

```
✅ Phase 1 (Juillet 2025) — TERMINÉ
   ├── Extraction PDF Rosstat (1037 pages)
   ├── 5 CSV master (85 régions × 19 colonnes)
   ├── EIII Regional Score (0-100)
   ├── Monte Carlo 10 000 itérations
   └── Coordonnées géographiques 85 régions

🔄 Phase 2 (En cours)
   ├── Power BI Dashboard 7 pages
   ├── Kepler.gl carte interactive
   ├── Tableau Public Story Points
   └── Salesforce import pipeline

📅 Phase 3 (Prévu)
   ├── Neo4j graphe industriel
   ├── Gephi visualisation réseau
   ├── Obsidian Knowledge Base
   └── GitHub Actions CI/CD mensuel
```

---

## 🤝 Contribution

```bash
# Fork + Clone
git clone https://github.com/[votre-profil]/Russia-Eurasia-Industrial-Project
git checkout -b feature/[nom-feature]

# Ajouter données régionales
# Déposer dans : Région de Russie/input/
python consolidate_regional_data.py --input-dir ./input

# Commit
git add .
git commit -m "feat: add [description] regional data"
git push origin feature/[nom-feature]
```

---

## 👤 Auteur

**Marin** — Data Engineering & Business Development Industriel  
Projet de simulation académique — Alternance  
Stack : Python | Power BI | Salesforce | ArcGIS | Neo4j | Excel

---

*Données Rosstat 2024-2025 | EIII Methodology v1.0 | Mise à jour : Juillet 2025*
