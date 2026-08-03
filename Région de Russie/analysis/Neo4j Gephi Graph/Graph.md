## 🔗 Analyse Graphe Neo4j & Gephi

### Modélisation et Visualisation

La modélisation sous forme de graphe (Neo4j) permet de visualiser clairement les dépendances (via les relations `BELONGS_TO`) entre :

- Les régions spécifiques
- Les districts fédéraux
- Les acteurs industriels ou ressources clés (comme EVRAZ, NLMK, et le gaz)

Les données extraites des fichiers `edges.csv` et `neo4j_query_table_data_2026-7-29.csv` ont permis de générer une analyse de réseau qui met en lumière des asymétries géographiques majeures en terme de centralité et d'interdépendance.

---

### Aperçu des Districts Fédéraux (Macro-régions)

| District Fédéral | Score EIII Moyen | Demande en Gaz Totale | Région Moteur |
|------------------|------------------|-----------------------|---------------|
| **Oural (Уральский)** | 39.7 | 5931.8 | Oblast de Tioumen |
| **Central (Центральный)** | 29.3 | 3338.2 | Moscou (Ville) |
| **Volga (Приволжский)** | 31.1 | 3115.1 | République du Tatarstan |
| **Sibérie (Сибирский)** | 30.6 | 2485.5 | Kraï de Krasnoïarsk |
| **Nord-Ouest (Северо-Западный)** | 26.1 | 1487.3 | Saint-Pétersbourg |

---

### Points d'ancrage du réseau

- **L'Oural est le cœur industriel et énergétique :** L'Oblast de Tioumen capte à elle seule une demande en gaz de 2419.4, ce qui montre une concentration massive de l'industrie lourde et de l'extraction.
- **Le Centre est le pôle financier et décisionnel :** Moscou domine de manière écrasante le score d'attractivité/investissement (EIII) avec 92.3, bien au-dessus de la moyenne nationale (25.4).
- **Les entités industrielles :** La présence de nœuds corporatifs comme NLMK et EVRAZ rappelle que l'économie repose lourdement sur la métallurgie, une industrie particulièrement gourmande en énergie.

---

### Centralité de Degré et d'Intermédiarité

L'étude des **centralités de degré** (nombre de connexions directes) et des **centralités d'intermédiarité** (capacité d'un nœud à faire "le pont" entre d'autres nœuds) révèle des failles structurelles importantes.

#### 1. Les Piliers Administratifs (Forte Centralité de Degré)

- **Le District Central (Центральный)** est le super-nœud absolu de votre graphe avec le score de centralité de degré le plus élevé (0.187). Il regroupe le plus grand nombre de sous-régions.
- **Vulnérabilité face aux chocs :** Ces macro-régions agissent comme des "goulots d'étranglement" administratifs. Si le centre (notamment Moscou avec son score EIII de 92.3) subit une crise de liquidité ou des sanctions, l'impact se répercute rapidement.

#### 2. Les Régions "Ponts" et le Risque Industriel (Centralité d'Intermédiarité)

Deux régions se détachent avec une centralité d'intermédiarité supérieure :

- **L'Oblast de Lipetsk** (associé à l'entreprise NLMK)
- **L'Oblast de Sverdlovsk** (associé à l'entreprise EVRAZ)

Ces régions sont les seules (avec leurs entreprises) à faire le pont vers les nœuds `GasProduct` (via la relation `CONSUMES`).

- **Vulnérabilité face aux chocs (Scénario de Sanctions) :** Lipetsk et Sverdlovsk sont des **points de défaillance uniques (Single Points of Failure)**. Si des sanctions ciblent spécifiquement leurs capacités industrielles, cela peut fragmenter les chaînes d'approvisionnement.
- **Résilience sans sanctions :** Dans un marché ouvert, cette intermédiarité est une force. Ces régions captent la rente énergétique et industrielle de manière autonome, les rendant moins dépendantes des flux externes.

#### 3. L'Hyper-Concentration de l'Oural

L'Oural présente une topologie dangereuse. Bien que le district fédère une immense demande de gaz (Proxy à 5931.8) tirée par l'Oblast de Tioumen (2419.4) et la présence d'EVRAZ à Sverdlovsk, son exposition simultanée aux chocs prix/volume est élevée.

- **Le Choc Holistique :** L'Oural subit un effet "ciseaux". Si les prix de l'énergie s'effondrent (ou si un embargo sur le gaz réussit), l'Oblast de Tioumen s'effondre. Simultanément, si l'industrie métallique décroche, la demande régionale s'effondre.

---

## 🔮 Scénarios Prospectifs

### Scénario 1 : L'Avenir SANS Sanctions Économiques

Dans un contexte où les sanctions seraient levées ou inexistantes, le graphe économique russe se développerait de manière organique et mondialisée :

- **Maximisation de la rente énergétique (Oural & Sibérie) :** La demande en gaz extrêmement élevée de l'Oural et la présence de géants métallurgiques se traduisent par une forte capacité d'exportation et d'investissement.
- **Moscou comme Hub Global :** Avec son score EIII de 92.3, Moscou attirerait massivement les capitaux étrangers, redistribuant les investissements vers des régions à fort potentiel mais sous-financées.
- **Transition énergétique et diversification :** Les revenus tirés des exportations de gaz sans friction permettent à l'État de financer une diversification technologique, réduisant lentement la dépendance aux matières premières.

---

### Scénario 2 : L'Avenir AVEC Sanctions Économiques

Dans ce scénario de maintien ou de durcissement des sanctions, l'analyse de votre graphe montre que la Russie est contrainte à une restructuration interne douloureuse mais stratégique :

- **Le défi des "Actifs Échoués" (Stranded Assets) :** La production de gaz ne trouvant plus d'acheteurs européens traditionnels, l'Oblast de Tioumen et le district de l'Oural doivent réorienter la production vers des marchés alternatifs ou la consommation domestique.
- **Pivot vers l'Est (Sibérie et Extrême-Orient) :** Les nœuds de l'Extrême-Orient (EIII à 24.6) et de la Sibérie nécessitent d'énormes injections de capitaux étatiques pour construire de nouvelles infrastructures de transport et d'export.
- **Résilience par l'oligarchie industrielle :** Les entreprises liées à la métallurgie et aux matières premières (EVRAZ, NLMK) deviennent les piliers de l'économie de guerre ou d'autarcie.

---

## 🧠 Synthèse Prospective

Votre graphe démontre que l'économie russe est un réseau **"en étoile"** (Hub-and-Spoke) hautement vulnérable. Le pouvoir financier est verrouillé à Moscou, l'extraction de rente est isolée à quelques régions nucléaires. Sous sanctions prolongées, la rupture de l'un de ces ponts industriels (ex: faillite d'un conglomérat) fragmentera le graphe, isolant des régions entières de l'économie nationale.

---

## 🛠️ Structure du Projet

- Power BI reports
- Neo4j graph models (edges.csv)
- Export tables (neo4j_query_table_data_2026-7-29.csv)
- Gephi visualization files

---

*Document généré pour usage interne — reproduire ou redistribuer uniquement selon les règles de gouvernance du projet.*
