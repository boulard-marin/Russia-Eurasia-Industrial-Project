# Power BI Analyse Russie : Strategic Market Assessment & Gas Demand Analysis (2025–2030)

---

## 🎯 Aperçu Executive (BD & Supply Chain)

Ce projet propose une analyse décisionnelle du marché des gaz industriels en Russie à l'horizon **2025–2030**. Conçu comme un outil d'arbitrage pour la **Direction Commerciale (Business Development)** et la Supply Chain, il couvre :

- Le chiffre d'affaires potentiel
- La demande régionale
- L'infrastructure logistique

L'analyse combine une modélisation **Power BI**, une base de données **Neo4j** (graphe), et une visualisation **Gephi** pour identifier les hubs critiques, les dépendances régionales, et les risques opérationnels.

---

## 📊 Analyse Synthétique des Scénarios & Impacts

L'analyse repose sur une baseline post-sanctions, projetée selon **quatre scénarios de reprise économique** :

| Scénario | CA Estimé | Impact Croissance | Directive Business Development | Recommandation Supply Chain |
|----------|-----------|-------------------|--------------------------------|----------------------------|
| **Baseline Sanctions 2025** | **2,59 M€** | *-15,08 %* | **Verrouillage :** Sécuriser les comptes clés du Top 5 (Tyumen, Moscou, Tatarstan). | **Ligne de défense :** Contrats de transport long terme et garanties de livraison. |
| **Partial Lift 2026** | **3,65 M€** | *+19,67 %* | **Pénétration :** Activer le pipeline sur le Tier 2 / Top 15 (Sverdlovsk, Krasnoïarsk). | **Flexibilité :** Ajustement des capacités de stockage et redéploiement logistique. |
| **Full Lift 2027** | **5,18 M€** | *+69,84 %* | **Expansion :** Couverture agressive des zones industrielles intermédiaires. | **Maillage :** Diversification des modes de transport et ajout de hubs régionaux. |
| **Recovery 2028** | **7,26 M€** | *+138,03 %* | **Conquête de l'Est :** Déploiement sur la Sibérie orientale (Irkoutsk, Yakoutie). | **Dimensionnement :** Augmentation des surfaces d'entrepôts et capacités de distribution. |
| **Boom 2030** | **10,87 M€** | *+256,39 %* | **Domination :** Capture maximale des parts de marché (Demande : 19,11K Mrd RUB). | **Refonte :** Transition vers un réseau distribution à haute capacité. |

---

## 🗺️ Cartographie & Matrice de Priorisation Régionale

### 1. Vision Business Development : Ciblage & Part de Marché

#### **Top 5 priorités absolues (Volume & Capitation) :**

1. **Tyumen (12,66 % du marché)** : Épicentre gazier national, priorité N°1 pour les contrats majeurs.
2. **Moscou & Oblast de Moscou (8,79 % cumulés)** : Concentrent les sièges décisionnels et la distribution.
3. **République du Tatarstan (3,22 %)** : Core target pour les gaz de synthèse et la chimie lourde.
4. **Saint-Pétersbourg (2,75 %)** : Hub portuaire et complexe industriel stratégique.

#### **Bassin de croissance Tier 2 :**
Les régions de **Sverdlovsk (3,12 %)**, **Krasnoïarsk (3,91 %)** et **Kemerovo (2,88 %)** constituent le relais de croissance prioritaire dès le scénario *Partial Lift*.

---

### 2. Vision Supply Chain : Contraintes & Maillage Réseau

- **Densification à l'Ouest :** La cartographie démontre une concentration critique du marché dans la partie européenne et l'Oural. Risk management impératif sur les goulots d'étranglement logistiques.
- **Passage à l'échelle (+256 % à horizon 2030) :** La hausse progressive des volumes nécessite l'ouverture anticipée de sous-hubs logistiques dans l'Oural (Sverdlovsk) et en Sibérie (Irkoutsk) ainsi qu'une diversification des itinéraires.

---

### 3. Structure des coûts par région (Mrd RUB)

- Le graphique de gauche classe la facture gazière régionale en **milliards de roubles**.
- Cela montre les puits financiers du marché intérieur russe : les régions comptant de gros complexes de transformation (raffinage, pétrochimie) et de grandes métropoles consomment du gaz pour des usages industriels intensifs.

---

## 📈 Analyse de Corrélation : Score EIII vs Chiffre d'Affaires

### Structure de la corrélation

Le nuage de points croise deux variables par **Region_Oblast** :

- **Axe X** : Score EIII Moyen Pondéré (de ~20 à 100)
- **Axe Y** : Chiffre d'Affaires Estimé en M€ (de 0,0 M€ à 0,5 M€)

### Tendances observées

- **Plancher massif (faible CA)** : La grande majorité des points se concentrent en bas du graphique (CA < 0,1 M€) avec des scores EIII étalés entre 25 et 50. Cela correspond aux régions à faible activité industrielle.
- **Tendance centrale croissante** : On observe une corrélation positive modérée au centre : lorsque le **Score EIII** augmente de 40 à 55, le **Chiffre d'Affaires** monte progressivement.
- **Anomalies / Valeurs extrêmes (*Outliers*)** :
  1. **Le point très haut (~60 en EIII / ~0,48 M€ de CA)** : Représente la région avec la valeur économique la plus critique (probablement Tyumen).
  2. **Le point à l'extrême droite (~92 en EIII / ~0,19 M€ de CA)** : Région avec une criticité industrielle/infrastructurelle maximale (score EIII élevé) mais CA intermédiaire.
  3. **Le point isolé en haut à gauche (~37 en EIII / ~0,27 M€ de CA)** : Région à fort chiffre d'affaires mais au score EIII relativement modéré (probablement Moscou ou Saint-Pétersbourg).

---

### Croisement avec les données du tableau

| Catégorie | Régions clés du tableau | Poids gazier (Gas Demand Share) | Impact sur la corrélation |
|-----------|--------------------------|--------------------------------|---------------------------|
| **TOP 5 (Super-hubs)** | *Tyumen*, *Moscou*, *Oblast de Moscou*, *Tatarstan*, *Saint-Pétersbourg* | **27,42 %** à elles seules (dont 12,66 % pour Tyumen) | Ce sont les points isolés en haut du graphe |
| **TOP 15 (Hubs secondaires)** | *Kemerovo*, *Krasnoïarsk*, *Sverdlovsk*, *Yamalo-Nenets*, etc. | **1,8 % à 3,9 %** par région | Ce sont les points formant le cluster intermédiaire |
| **Régions marginales** | *Kaliningrad*, *Kalouga*, *Bryansk*, *Sébastopol*, etc. | **< 1 %** par région | Forme le socle dense tout en bas du graphique (CA < 0,1 M€). |

---

### Conclusion stratégique

- **Asymétrie majeure :** Le marché est ultra-concentré. Un tout petit nombre de régions (le TOP 5) génère l'essentiel du chiffre d'affaires et contrôle plus d'un quart de la demande de gaz.
- **Score EIII vs CA :** Un Score EIII élevé ne garantit pas un CA massif, mais **les régions combinant un Score EIII > 50 et un fort pourcentage de demande gazière représentent les points névralgiques pour la stratégie commerciale.**

---

*Document généré pour usage interne — reproduire ou redistribuer uniquement selon les règles de gouvernance du projet.*
