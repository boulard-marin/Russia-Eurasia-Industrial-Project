# 🏢 AIR LIQUIDE EURASIA — MÉMORANDUM STRATÉGIQUE BD 2025-2030
## Plan d'Investissement Industriel & Scoring Régional (85 Régions de Russie)

**Date :** Juillet 2026  
**Auteur :** Direction du Business Development & Intelligence Économique Air Liquide Eurasia  
**Base NocoDB du Projet :** `p0ygj6vufqhhhsc` (NocoDB MCP Remote Connected)  

---

### 1. SYNTHÈSE EXÉCUTIVE (EXECUTIVE SUMMARY)

Le présent mémorandum établit la feuille de route stratégique pour le déploiement des gaz industriels (**O₂ / N₂ / H₂ / CO₂ / Ar**) en Russie et dans la zone Eurasie à l'horizon 2025-2030.

L'étude s'appuie sur la modélisation exhaustive des **85 régions russes** à partir des données statistiques officielles Rosstat 2025 (*Регионы России: Социально-экономические показатели 2025*, 1037 pages).

#### Chiffres Clés du Pipeline BD :
- **31 Opportunités Qualifiées (Tiers 1 à 4)**.
- **CAPEX Global Potentiel :** **21.8 M€**.
- **Revenu Baseline (Sanctions Actives - 2025) :** **3.0 M€/an**.
- **Revenu Post-Sanctions (Scénario Boom 2030) :** **12.6 M€/an** (Facteur multiplicateur ×4.2).
- **Nombre de Régions "BUY" (Score EIII ≥ 65) :** 2 (Moscou Ville & Moscou Oblast).
- **Nombre de Régions "WATCH" (Score EIII 40-64) :** 18 (Tioumen, Tatarstan, St-Pétersbourg, Sverdlovsk, Krasnoïarsk, etc.).

---

### 2. TOP 10 DES OPPORTUNITÉS COMMERCIALES STRATÉGIQUES (TIER 1 - CRITIQUE)

| # | Code Opportunité | Région | District Fédéral | Score EIII | CAPEX (M€) | Gaz Cible | Client Cible | Revenu 2030 (M€/an) |
|---|---|---|---|---|---|---|---|---|
| 1 | **AL-RU-ТЮМЕ-2025** | Тюменская область | Urals | 59.5 | **3.2 M€** | H₂ + CO₂ | Gazprom / Sibur | **1.20 M€** |
| 2 | **AL-RU-ХАНТ-2025** | Ханты-Мансийский АО | Urals | 37.2 | **1.8 M€** | H₂ + CO₂ | Surgutneftegas | **0.67 M€** |
| 3 | **AL-RU-Г.М-2025** | г. Москва | Central | **92.3** | **1.3 M€** | H₂ + CO₂ | Pharma / Chimie | **0.47 M€** |
| 4 | **AL-RU-КРАС-2025** | Красноярский край | Sibérie | 48.6 | **1.0 M€** | H₂ + CO₂ | Norilsk Nickel / Rusal | **0.37 M€** |
| 5 | **AL-RU-ЯМАЛ-2025** | Ямало-Ненецкий АО | Urals | 49.5 | **1.0 M€** | O₂ + N₂ | Novatek / Yamal LNG | **0.36 M€** |
| 6 | **AL-RU-МОСК-2025** | Московская область | Central | **71.1** | **1.0 M€** | H₂ + CO₂ | Mfg Diversifiée | **0.36 M€** |
| 7 | **AL-RU-РЕСП-2025** | Республика Татарстан | Volga | 53.0 | **0.8 M€** | H₂ + CO₂ | Tatneft / Nizhnekamskneftekhim | **0.30 M€** |
| 8 | **AL-RU-СВЕР-2025** | Свердловская область | Urals | 51.0 | **0.8 M€** | H₂ + CO₂ | NLMK / EVRAZ | **0.29 M€** |
| 9 | **AL-RU-КЕМЕ-2025** | Кемеровская область | Sibérie | 45.4 | **0.7 M€** | H₂ + CO₂ | Métallurgie / Acier | **0.27 M€** |
| 10 | **AL-RU-Г.С-2025** | г. Санкт-Петербург | Nord-Ouest | 52.4 | **0.7 M€** | H₂ + CO₂ | Construction Navale / Port | **0.26 M€** |

---

### 3. FONDEMENTS DU SCORING EIII (EASTERN INDUSTRIAL INVESTMENT INDEX)

L'EIII est un indice composite propriétaire (0 à 100) calculé selon la pondération suivante :

$$EIII = 25\% \cdot \text{Économie} + 20\% \cdot \text{Industrie Lourde} + 20\% \cdot \text{Énergie} + 15\% \cdot \text{Logistique} + 20\% \cdot \text{Dynamisme}$$

#### Grille de Décision d'Investissement :
- 🟢 **BUY (≥ 65)** : Déploiement d'unités de séparation d'air (ASU) prioritaires et contrats Over-The-Fence (OTF) long terme (15-20 ans).
- 🟡 **WATCH (40-64)** : Négociations conditionnelles, unités modulaires VPSA/PSA et ventes liquides (Bulk).
- 🟠 **CAUTION (25-39)** : Fourniture bouteilles (Cylinder Gas) et contrats spot.
- 🔴 **AVOID (< 25)** : Hors périmètre d'investissement direct.

---

### 4. ARCHITECTURE DES SYSTÈMES & CRM NOCODB

Toutes les opportunités et analyses régionales sont interconnectées en temps réel au CRM **NocoDB** (Base ID: `p0ygj6vufqhhhsc`) :
- **Table 1 (`airliquide_bd_pipeline_russia_2025`) :** Suivi des 31 opportunités BD.
- **Table 2 (`master_regional_russia_2025`) :** Indicateurs Rosstat des 85 régions.
- **Table 3 (`eiii_regional_scores_2025`) :** Benchmark et scoring EIII.
- **Table 4 (`sector_focus_gaz_industriels`) :** Consommation O₂/N₂/H₂/CO₂/Ar par région.
- **Table 5 (`whatif_sanctions_lift_simulation_2025`) :** Modèle prévisionnel 100 scénarios.
