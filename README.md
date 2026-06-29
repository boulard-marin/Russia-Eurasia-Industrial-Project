# EUROASIA INDUSTRIAL INVESTMENT SIMULATION SYSTEM

![Project Status](https://img.shields.io/badge/Status-Active-success)
![Version](https://img.shields.io/badge/Version-1.0.0-blue)
![Architecture](https://img.shields.io/badge/Architecture-Data%20Engineering%20%26%20BI-orange)

## 📌 Vision Stratégique
Ce projet modélise un écosystème de **Business Intelligence (BI) et Data Engineering** pour la simulation d'investissements industriels massifs en Eurasie (Russie, Chine, Inde, Asie Centrale, Caucase).

Le cœur du système repose sur l'**EIII (Eastern Industrial Investment Index)**, un modèle mathématique exclusif de scoring pays.

🔥 **Le Scénario Clé (What-If 2025)** : Le projet intègre une simulation financière majeure : *"Que se passe-t-il si l'UE lève les sanctions économiques contre la Russie en 2025 ?"*. Nos algorithmes calculent instantanément la bascule du marché de l'énergie et prouvent, chiffres à l'appui, pourquoi la Russie redevient la destination d'investissement N°1 (Air Liquide) face à l'Inde ou la Chine.

---

## 📖 Qu'est-ce que l'EIII (Eastern Industrial Investment Index) ?

L'EIII est un **indicateur composite de stratégie d'investissement**. 
Il ne s'agit pas d'un simple classement économique. C'est un outil d'aide à la décision conçu pour répondre à la question : *"Doit-on implanter une usine de plusieurs millions d'euros (CAPEX) dans ce pays, sachant les risques actuels ?"*

Il est structuré autour de 5 piliers fondamentaux pour l'industrie lourde :
1. **Économie (25%)** : Dynamisme du marché local, IDE (Investissements Directs Étrangers), Croissance.
2. **Énergie (20%)** : Coût et disponibilité du Gaz/Pétrole/Électricité (crucial pour l'industrie chimique et métallurgique).
3. **Capacité Industrielle (20%)** : Présence d'un écosystème d'acheteurs B2B (Heavy Industry, Chimie).
4. **Logistique (15%)** : Accès aux ports, corridors ferroviaires, routes d'exportation.
5. **Risque (20%)** : Stabilité juridique, sanctions internationales, volatilité des devises.

**Comment le lire ?**
Un EIII de `85/100` signifie que le pays offre un environnement très favorable, énergétique et logistique, avec un risque maîtrisé. Un score de `30/100` déclenche un signal "AVOID" (risque trop élevé par rapport au ROI espéré).

---

## 🗂 Architecture du Repository (Plan GitHub)

Pour qu'un recruteur ou un directeur comprenne la portée de ce projet, le repository est structuré ainsi :

```text
📦 Russia-Eurasia-Industrial-Project
 ┣ 📂 crm_simulation/       # Données Salesforce (Pipeline, Opportunités B2B)
 ┣ 📂 contexte/             # Espace d'analyses géopolitiques et données de simulation
 ┃ ┣ 📂 data/               # Datasets EIII (Macro, Énergie, Industrie, Scores, CSV principal)
 ┃ ┣ 📂 excel/              # Simulation financière (CAPEX/OPEX type Air Liquide, Excel)
 ┃ ┣ 📂 python/             # Scripts et moteurs d'analyse de données (Pandas/Numpy)
 ┃ ┣ 📂 report/             # Rapports stratégiques traduits en français (Markdown) et visuels
 ┃ ┗ 📂 slack_simulation/   # Échanges de communications internes d'entreprise (TXT)
 ┣ 📂 powerbi/              # Fichiers sources pour dashboards analytiques
 ┣ 📂 sap_simulation/       # ERP : Cycles complets MM (Achat) & SD (Vente)
 ┗ 📂 sql/                  # Architecture Star Schema et requêtes analytiques BI
```

---

## 🚀 Ce que vous devez faire pour déployer ce projet

En tant que propriétaire du projet, voici les prochaines étapes de votre côté :

1. **GitHub : Valider et Commiter**
   - Ajoutez tous ces fichiers sur GitHub avec des messages clairs (ex: `feat: add EIII calculation engine`, `docs: add strategic business context`).
2. **BI : Connecter les Données**
   - Ouvrez Power BI.
   - Importez les fichiers SQL ou directement les fichiers CSV.
   - Liez les tables via le `Country` et l'`Year` (Le Star Schema est déjà pensé pour ça).
3. **Restitution : Présenter la Valeur**
   - Créez des visuels (Map de l'Eurasie avec les couleurs EIII, Funnel de conversion Salesforce, Spend Analysis SAP).
   - Préparez un "Executive Summary" pour prouver que vous maîtrisez la technique ET le business.
