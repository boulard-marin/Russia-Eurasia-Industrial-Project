# Analyses Monte Carlo - Air Liquide Russia BD Pipeline

Ce dossier contient les résultats des simulations Monte Carlo effectuées pour l'analyse de risque des investissements régionaux en Russie.

## Analyse des Résultats (`monte_carlo_results.png`)

L'image d'analyse présente 4 graphiques essentiels pour la prise de décision :

### 1. Distribution Revenue Annuel (M€/an)
- **P10 (Pessimiste) :** 0.69 M€/an
- **P50 (Médian) :** 1.27 M€/an
- **P90 (Optimiste) :** 2.21 M€/an
- **Base (Théorique) :** 3.00 M€/an
*Analyse :* Le modèle montre une forte décote par rapport au cas de base théorique (3.00 M€). Le revenu médian estimé sous conditions de risque se situe à 1.27 M€.

### 2. Distribution VAN sur 15 ans — P(>0)=1%
- **VAN P50 :** -14 M€
- **Probabilité de VAN > 0 :** Seulement 1%
*Analyse :* Dans l'environnement actuel (modélisé avec les paramètres actuels de sanctions/taux), la Valeur Actuelle Nette (VAN) du pipeline est très majoritairement négative, démontrant l'aspect hautement risqué d'un investissement immédiat en capital (CAPEX) sans atténuation.

### 3. Tornado Chart — Sensibilité Revenue
Ce graphique met en évidence les facteurs les plus influents sur le revenu :
- **Taux de win des contrats** (Fort impact positif) : C'est le levier de performance principal.
- **Taux RUB/EUR** et **Durée des sanctions** (Fort impact négatif) : Ce sont les principaux destructeurs de valeur.
- Les facteurs de croissance industrielle et le prix du pétrole (Brent) ont un impact positif mais modéré en comparaison.

### 4. Revenue par Scénario Sanctions (M€/an)
Démontre le potentiel de croissance ("upside") en cas d'assouplissement géopolitique :
- **Baseline (Sanctions) :** 1.8 M€/an
- **Partial Lift 2026 :** 4.2 M€/an
- **Full Lift 2027 :** 6.0 M€/an
- **Recovery 2028 :** 8.4 M€/an
- **Boom 2030 :** 12.6 M€/an
*Analyse :* Le pipeline a une forte élasticité géopolitique. Une levée même partielle des sanctions en 2026 doublerait plus que les revenus (de 1.8 à 4.2 M€).
