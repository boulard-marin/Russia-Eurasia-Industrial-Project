# 📖 PLAYBOOK TECHNIQUE — SCORE EIII (EASTERN INDUSTRIAL INVESTMENT INDEX)
## Guide de Calcul & Diagnostic des 85 Régions de Russie pour les Gaz Industriels

**Version :** 2.5 (Édition Rosstat 2025)  
**Système :** Euroasia Industrial Investment System | Air Liquide BD  
**Base NocoDB liée :** `p0ygj6vufqhhhsc` (Table `eiii_regional_scores_2025`)  

---

### 1. FORMULE DÉTAILLÉE DU SCORE EIII (0-100)

L'**Eastern Industrial Investment Index (EIII)** mesure l'attractivité industrielle et commerciale d'une région pour l'implantation d'infrastructures de gaz industriels (ASU, SMR, VPSA, Réseaux de pipelines).

$$\text{Score EIII} = S_{\text{Éco}} \times 0.25 + S_{\text{Ind}} \times 0.20 + S_{\text{Éner}} \times 0.20 + S_{\text{Log}} \times 0.15 + S_{\text{Dyn}} \times 0.20$$

---

### 2. DÉCOMPOSITION DES 5 PILIERS

#### 1. Pilier Économie (25%)
- **Produit Régional Brut (GRP) :** Poids de la richesse produite (en Mrd ₽).
- **Investissements en Capital Fixe :** Volume d'investissements productifs (en Mrd ₽).
- *Formule de calcul :*
  $$S_{\text{Éco}} = \text{Clamp}_{0}^{100} \left( \frac{\text{GRP}}{310} + \frac{\text{Investissements}}{65} \right) \times 50$$

#### 2. Pilier Industrie Lourde (20%)
- **Proxy Métallurgie & Sidérurgie (40% demand O₂/N₂/Ar) :** Production minière + 35% de la production manufacturière.
- **Proxy Chimie & Pétrochimie (30% demand H₂/CO₂/N₂) :** 25% de la production manufacturière.
- *Formule de calcul :*
  $$S_{\text{Ind}} = \text{Clamp}_{0}^{100} \left( \frac{0.6 \cdot \text{Mining} + 0.35 \cdot \text{Manufacturing}}{18} \right) \times 100$$

#### 3. Pilier Énergie & Services Utilitaires (20%)
- Production d'électricité, de gaz naturel et approvisionnement en eau (Table 1.1 Rosstat p.20).
- *Formule de calcul :*
  $$S_{\text{Éner}} = \text{Clamp}_{0}^{100} \left( \frac{\text{Energy\_Gas\_Water}}{6.2} \right) \times 100$$

#### 4. Pilier Logistique & Infrastructures (15%)
- Volume de construction (en milliers de m²) et taille du bassin de population.
- *Formule de calcul :*
  $$S_{\text{Log}} = \text{Clamp}_{0}^{100} \left( \frac{0.3 \cdot \text{Construction} + 0.01 \cdot \text{Population}}{38} \right) \times 100$$

#### 5. Pilier Dynamisme Industrial (20%)
- Indice de Production Industrielle 2024 vs 2023 (Table 1.2 Rosstat p.21).
- *Formule de calcul :*
  $$S_{\text{Dyn}} = \text{Clamp}_{0}^{100} \left( (\text{IndProdIndex} - 95.0) \times 10.0 \right)$$

---

### 3. CLASSIFICATION DES 85 RÉGIONS & RÈGLES DE DÉPLOIEMENT COMMERCIAL

```
  Score EIII       Signal             Mode de Déploiement Commercial
 ─────────────────────────────────────────────────────────────────────────────
   ≥ 65.0       🟢 BUY             Contrats Long-Terme Over-The-Fence (OTF), 
                                   Unités Séparation Air (ASU) > 500 t/j
   40.0 - 64.9  🟡 WATCH           Ventes Liquides (Bulk), Unités Modulaires 
                                   VPSA / PSA sur site
   25.0 - 39.9  🟠 CAUTION         Conditionné à des projets ciblés, 
                                   Conditionnement Bouteilles (Cylinders)
   < 25.0       🔴 AVOID           Hors périmètre d'investissement
```

---

### 4. MATRICE DE DEMANDE PAR TYPE DE GAZ (0-10)

- **Oxygène ($O_2$) :** $(\text{Métallurgie} / 100 + \text{Mfg} / 50 \times 0.35) \times 3$
- **Azote ($N_2$) :** $(\text{Métallurgie} / 80 + \text{Mfg} / 200) \times 2.5$
- **Hydrogène ($H_2$) :** $(\text{Mfg} / 60 + \text{Énergie} / 80) \times 2$
- **Dioxyde de Carbone ($CO_2$) :** $(\text{Agriculture} / 80 + \text{Mfg} / 400) \times 3$
- **Argon ($Ar$) :** $(\text{Mfg} / 300 + \text{Métallurgie} / 200) \times 2$
