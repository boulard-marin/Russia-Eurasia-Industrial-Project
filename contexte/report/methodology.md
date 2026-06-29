# Méthodologie (Methodology)

Le projet repose sur une hiérarchie de données vérifiable :

1. Valeurs officielles ou API directes lorsque disponibles : API de la Banque Mondiale et flux XML de la Banque Centrale de Russie (CBR).
2. Rapports institutionnels officiels ou registres sources lorsque l'extraction nécessite un travail manuel sur PDF/API.
3. Lignes d'HYPOTHÈSES explicites pour les paramètres de simulation lorsque les données au niveau des usines ne sont pas publiques.
4. Mentions `DONNÉES NON DISPONIBLES PUBLIQUEMENT` lorsqu'un détail requis ne peut être vérifié à partir de sources publiques ouvertes.

## Score EIII (ou EIRM)

L'EIII combine la taille du marché, la profondeur industrielle, la position énergétique/commerciale, la logistique, la stabilité macroéconomique et le risque lié aux sanctions.

Interprétation recommandée :
- `INVESTIR` (INVEST) : score >= 70 et ROI ajusté au risque acceptable.
- `ATTENDRE` (WAIT) : score >= 45 ou fondamentaux attrayants mais risques liés aux sanctions/paiements non résolus.
- `ÉVITER` (AVOID) : score < 45 ou risques juridiques/paiements/assurances actuels dominant l'économie du projet.

## Limites Importantes

L'indice des sanctions n'est pas un décompte officiel des sanctions. Il s'agit d'une hypothèse ordinale d'aide à la décision documentée dans `contexte/data/sanctions_index.csv`.
Le modèle d'unité Air Liquide Russie est un moteur de scénario. Les valeurs de CAPEX et d'OPEX sont des hypothèses basées sur des références de projets industriels publics, et non sur les états financiers réels des usines russes d'Air Liquide.
