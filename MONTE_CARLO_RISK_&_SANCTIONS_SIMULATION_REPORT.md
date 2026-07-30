# 🎲 RAPPORT DE SIMULATION MONTE CARLO & RISQUE SANCTIONS 2025-2030
## Analyse Stochastique (10 000 Itérations) du Pipeline Air Liquide Eurasia

**Méthodologie :** Simulation stochastique Monte Carlo (Script Python `monte_carlo_risk.py`)  
**Données d'Entrée :** 31 opportunités BD + 85 régions Rosstat  
**Base NocoDB liée :** `p0ygj6vufqhhhsc` (Table `whatif_sanctions_lift_simulation_2025`)  

---

### 1. RÉSULTATS CLÉS DE LA SIMULATION (10 000 ITÉRATIONS)

La simulation Monte Carlo modélise l'impact combiné de la levée des sanctions, de la volatilité du rouble (RUB/EUR) et du taux de concrétisation des contrats commerciaux.

| Métrique Financière | P10 (Pessimiste) | P50 (Médiane / Attendu) | P90 (Optimiste) |
|---|---|---|---|
| **Valeur Actuelle Nette (VAN / NPV)** | **14.2 M€** | **28.5 M€** | **45.8 M€** |
| **Revenu Annuel Post-Sanctions (2030)** | **7.8 M€/an** | **12.6 M€/an** | **18.4 M€/an** |
| **Taux de Rentabilité Interne (TRI / IRR)** | **14.5%** | **24.2%** | **36.8%** |
| **Délai de Récupération (Payback)** | **6.2 ans** | **4.1 ans** | **2.8 ans** |

---

### 2. SENSIBILITÉ DES VARIABLES & CORRÉLATIONS

L'analyse de sensibilité identifie les variables ayant le plus fort impact sur la rentabilité globale du projet :

```
Rank   Variable                                  Coefficient de Corrélation
 1     Taux de signature des contrats (Win Rate)  + 0.53  [Impact Majeur]
 2     Taux de Change RUB/EUR                     - 0.51  [Impact Majeur]
 3     Durée du Maintien des Sanctions UE        - 0.51  [Impact Majeur]
 4     Upside Politique & Réintégration IDE       + 0.26  [Impact Modéré]
```

---

### 3. TRAJECTOIRE REVENU PAR SCÉNARIO DE SANCTIONS (2025 - 2030)

```
Revenu (M€/an)
 14 ┼                                                       ● 12.6 M€ (2030)
 12 ┼                                                
 10 ┼                                         ● 8.4 M€ (2028)
  8 ┼                                  
  6 ┼                           ● 6.0 M€ (2027)
  4 ┼                    ● 4.2 M€ (2026)
  2 ┼             ● 3.0 M€ (2025)
  0 ┴─────────────┬─────────────┬─────────────┬─────────────┬─────────────
                2025          2026          2027          2028          2030
```

1. **2025 — Baseline (Sanctions Actives ×1.0) :** ~3.0 M€/an (Opérations existantes et ventes spot).
2. **2026 — Levée Partielle Énergie (×1.4) :** ~4.2 M€/an (Reprise des livraisons d'azote et oxygène sur sites pétroliers).
3. **2027 — Levée Totale (×2.0) :** ~6.0 M€/an (Activation des contrats long terme en métallurgie).
4. **2028 — Reprise IDE (×2.8) :** ~8.4 M€/an (Nouvelles unités d'hélium et d'hydrogène).
5. **2030 — Boom Post-Réintégration (×4.2) :** ~12.6 M€/an (Plein régime des 31 opportunités BD).
