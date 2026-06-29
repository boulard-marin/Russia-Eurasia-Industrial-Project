# Guide des Dossiers et des Données (CSV & Structure)

Ce document décrit l'organisation du dossier `contexte/` ainsi que le rôle et l'utilité de chaque fichier CSV pour vous aider à naviguer facilement dans le projet.

---

## 📂 Structure du Répertoire `contexte/`

Le dossier `contexte/` rassemble tous les éléments de base de données, de traitement de données et d'analyses stratégiques :

*   `contexte/data/` : Contient l'ensemble des bases de données sources (CSV) et les fichiers finaux consolidés.
*   `contexte/excel/` : Contient les simulations financières Excel interactives et les tableaux de bord décisionnels.
*   `contexte/python/` : Contient les scripts d'ingénierie de données (nettoyage, calcul des scores EIII, modélisation de ROI et génération de graphiques).
*   `contexte/report/` : Contient les rapports d'analyse stratégique rédigés en français ainsi que le dossier `visuals/` regroupant les graphiques exportés.
*   `contexte/slack_simulation/` : Contient des fichiers simulant les communications internes (échanges Slack) sur le projet eurasien.

---

## 📊 Utilité des Fichiers CSV du Dossier `contexte/data/`

Voici le détail de chaque fichier CSV présent dans le dossier [contexte/data/](file:///c:/Users/marin/OneDrive/Documents/MARIN%20école/Alternance/Projet%20Github/Projet%203/Russia-Eurasia-Industrial-Project/contexte/data/) :

### 1. `merged_eurasia_analytics.csv` (Jeu de données principal)
*   **Utilité** : C'est le fichier central consolidé. Il fusionne toutes les données économiques, énergétiques, industrielles, logistiques et de risque.
*   **Contenu** : Pour chaque pays d'Eurasie (Russie, Chine, Inde, Kazakhstan, Turkménistan, Géorgie) et chaque année (2020 à 2025), il fournit l'ensemble des scores intermédiaires et le score final EIII (*Eastern Industrial Investment Index*). C'est ce fichier qui sert de source pour les dashboards Power BI.

### 2. `air_liquide_financials.csv`
*   **Utilité** : Modélise les données financières d'une entité fictive de gaz industriels (style Air Liquide) implantée en Russie.
*   **Contenu** : CAPEX de construction des usines, OPEX annuels (électricité, maintenance, personnel), revenus des ventes de gaz (oxygène, azote, hydrogène) et cash-flows nets.

### 3. `energy.csv`
*   **Utilité** : Fournit les indicateurs liés au secteur de l'énergie.
*   **Contenu** : Volumes de production de gaz et de pétrole, capacités d'exportation énergétique et prix de l'électricité (inversés pour le scoring).

### 4. `industry.csv`
*   **Utilité** : Évalue le tissu industriel de chaque pays.
*   **Contenu** : Production chimique nationale, indice métallurgique et poids de l'industrie lourde locale.

### 5. `logistics.csv`
*   **Utilité** : Analyse les capacités de transport pour l'import/export de matériel lourd.
*   **Contenu** : Densité du réseau ferroviaire, connectivité portuaire et indice de développement des corridors de transport régionaux.

### 6. `macro_indicators.csv`
*   **Utilité** : Regroupe les données de cadrage économique global.
*   **Contenu** : PIB des pays, taux d'inflation (inversé pour le scoring) et flux d'investissements directs étrangers (IDE).

### 7. `risk.csv`
*   **Utilité** : Évalue la stabilité générale nécessaire à l'investissement.
*   **Contenu** : Volatilité des devises locales, risques juridiques/réglementaires, coûts d'assurance et indice d'exposition aux sanctions.

### 8. `sanctions_index.csv`
*   **Utilité** : Modélise l'historique et la simulation future de la sévérité des sanctions.
*   **Contenu** : Un index numérique traduisant l'impact des sanctions sur les transactions financières et les importations technologiques.

### 9. `source_registry.csv`
*   **Utilité** : Assure la traçabilité des données du projet.
*   **Contenu** : Liens et références vers les bases de données institutionnelles (Banque Mondiale, Banque Centrale de Russie) pour chaque indicateur utilisé.

### 10. `trade_flows.csv`
*   **Utilité** : Décrit les échanges commerciaux du secteur.
*   **Contenu** : Volumes d'importations et d'exportations de marchandises lourdes et de produits chimiques manufacturés.

---

## 📈 Utilité des Fichiers CSV du Dossier `contexte/excel/`

### 1. `air_liquide_simulation.csv`
*   **Utilité** : Utilisé pour alimenter les calculs de sensibilité de rentabilité dans le tableau de bord Excel.
*   **Contenu** : Scénarios comparatifs de ROI et de délai de récupération (Break-Even) selon le coût de l'énergie locale et la prime de risque géopolitique appliquée.
