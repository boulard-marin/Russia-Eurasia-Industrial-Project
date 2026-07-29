"""
Monte Carlo Risk Simulation — Air Liquide Russia BD
Simulation quantitative des risques sur le pipeline de 31 opportunités

Usage:
    python analysis/monte_carlo_risk.py
    python analysis/monte_carlo_risk.py --iterations 50000 --export
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import argparse
import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

# ─────────────────────────────────────────────────────────────────────────────
# CONFIGURATION
# ─────────────────────────────────────────────────────────────────────────────

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "Région de Russie")
OUTPUT_DIR = os.path.join(BASE_DIR, "analysis", "outputs")
os.makedirs(OUTPUT_DIR, exist_ok=True)


def run_monte_carlo(n_iterations: int = 10_000, export: bool = False):
    """
    Simulation Monte Carlo — 10 variables stochastiques
    Sortie : distribution Revenue, ROI, VAN
    """
    np.random.seed(42)
    N = n_iterations

    print(f"🎲 Monte Carlo Risk Simulation — {N:,} itérations")
    print("=" * 60)

    # ─── CHARGEMENT DONNÉES DE BASE ───────────────────────────────────────
    try:
        pipeline = pd.read_csv(
            os.path.join(DATA_DIR, "airliquide_bd_pipeline_russia_2025.csv"),
            sep=";", encoding="utf-8-sig"
        )
        base_capex = pipeline["Est_CAPEX_Potential_M_EUR"].sum()
        base_revenue = pipeline["Est_Revenue_M_EUR_yr"].sum()
        n_opportunities = len(pipeline)
        print(f"Pipeline chargé : {n_opportunities} opportunités")
        print(f"CAPEX base : {base_capex:.2f} M€ | Revenue base : {base_revenue:.2f} M€/an")
    except FileNotFoundError:
        print("⚠ Fichier pipeline non trouvé, utilisation valeurs par défaut")
        base_capex = 15.0
        base_revenue = 3.0
        n_opportunities = 31

    print()

    # ─── VARIABLES STOCHASTIQUES ──────────────────────────────────────────

    # 1. Prix du pétrole Brent (USD/bbl)
    #    Impact : corrèle avec demande gaz industriels russie
    oil_price = np.random.normal(70, 18, N)  # Normal(mean=70, std=18)
    oil_price = np.clip(oil_price, 30, 150)

    # 2. Durée résiduelle des sanctions (années)
    #    Distribution triangulaire : min=0.5, mode=3, max=10
    sanctions_years = np.random.triangular(0.5, 3.0, 10.0, N)

    # 3. Taux de change RUB/EUR
    #    LogNormal autour de 100 RUB/EUR, volatilité 25%
    rub_eur = np.random.lognormal(np.log(100), 0.25, N)
    rub_eur = np.clip(rub_eur, 60, 200)

    # 4. Taux de croissance industrielle annuel Russie
    #    Actuellement ~4.6% (Rosstat 2024) avec incertitude
    industrial_growth = np.random.normal(0.046, 0.015, N)
    industrial_growth = np.clip(industrial_growth, -0.05, 0.15)

    # 5. Probabilité d'obtenir le contrat par région TIER 1
    #    50-80% en conditions normales
    win_rate_tier1 = np.random.beta(6, 4, N)  # Beta(6,4) → mode ~0.6

    # 6. CAPEX overrun multiplier (risque projet)
    #    LogNormal : 10% des projets dépassent de 40%
    capex_overrun = np.random.lognormal(0, 0.2, N)  # median=1.0, P90=1.28
    capex_overrun = np.clip(capex_overrun, 0.8, 2.5)

    # 7. Délai de mise en œuvre (années avant premier revenu)
    #    Uniforme 1.5 à 4 ans (construction ASU)
    implementation_delay = np.random.uniform(1.5, 4.0, N)

    # 8. Inflation énergétique (coût opérationnel)
    inflation_energy = np.random.normal(0.08, 0.03, N)  # ~8% inflation énergie
    inflation_energy = np.clip(inflation_energy, 0.02, 0.20)

    # 9. Dépréciation marché (pression concurrentielle)
    #    0% à 15% de perte de pricing power
    price_erosion = np.random.beta(2, 8, N) * 0.15  # P90 = 10%

    # 10. Upside politique (normalisation relations commerciales)
    #     0 à +60% si levée sanctions accélérée
    political_upside = np.random.exponential(0.15, N)
    political_upside = np.clip(political_upside, 0, 0.60)

    # ─── CALCUL DES OUTPUTS ───────────────────────────────────────────────

    # Facteur demande gaz (lié pétrole + croissance industrielle)
    gas_demand_factor = (1 + (oil_price - 70) / 200 +
                         industrial_growth * 3 +
                         political_upside)

    # Facteur sanctions (discount sur marché adressable)
    sanctions_factor = np.exp(-0.12 * sanctions_years)  # déclin exponentiel

    # Revenue annuel simulé (M€)
    revenue_annual = (base_revenue *
                      gas_demand_factor *
                      sanctions_factor *
                      win_rate_tier1 *
                      (1 - price_erosion) *
                      100 / rub_eur)  # normalisation change

    revenue_annual = np.clip(revenue_annual, 0, base_revenue * 20)

    # CAPEX total simulé (M€)
    capex_total = base_capex * capex_overrun

    # Actualisation (WACC = 12% pour marché émergent à risque)
    WACC = 0.12
    PROJECT_LIFE = 15  # années

    # VAN (Valeur Actuelle Nette)
    annual_cf = revenue_annual * (1 - inflation_energy) - capex_total / PROJECT_LIFE
    npv = np.sum(
        [annual_cf / (1 + WACC) ** t for t in range(1, PROJECT_LIFE + 1)],
        axis=0
    ) - capex_total

    # ROI sur 5 ans (%)
    roi_5yr = (revenue_annual * 5 - capex_total) / capex_total * 100

    # Payback period (années)
    payback = np.where(revenue_annual > 0, capex_total / revenue_annual, 999)
    payback = np.clip(payback, 0, 50)

    # ─── STATISTIQUES ─────────────────────────────────────────────────────

    def percentile_summary(name, data, unit=""):
        p10, p25, p50, p75, p90 = np.percentile(data, [10, 25, 50, 75, 90])
        print(f"\n  {name} {unit}:")
        print(f"    P10={p10:.2f} | P25={p25:.2f} | P50={p50:.2f} | P75={p75:.2f} | P90={p90:.2f}")
        return p10, p50, p90

    print("📊 RÉSULTATS SIMULATION MONTE CARLO")
    print("-" * 60)

    p10_rev, p50_rev, p90_rev = percentile_summary("Revenue Annuel", revenue_annual, "(M€/an)")
    p10_npv, p50_npv, p90_npv = percentile_summary("VAN 15 ans", npv, "(M€)")
    p10_roi, p50_roi, p90_roi = percentile_summary("ROI 5 ans", roi_5yr, "(%)")
    p10_pay, p50_pay, p90_pay = percentile_summary("Payback", payback, "(ans)")

    # Probabilités clés
    print(f"\n📌 PROBABILITÉS CLÉS :")
    print(f"  P(Revenue > baseline {base_revenue:.1f} M€/an) = {(revenue_annual > base_revenue).mean():.1%}")
    print(f"  P(VAN > 0) = {(npv > 0).mean():.1%}")
    print(f"  P(ROI > 15%) = {(roi_5yr > 15).mean():.1%}")
    print(f"  P(ROI > 30%) = {(roi_5yr > 30).mean():.1%}")
    print(f"  P(Payback < 5 ans) = {(payback < 5).mean():.1%}")
    print(f"  P(Payback < 10 ans) = {(payback < 10).mean():.1%}")

    # ─── ANALYSE DE SENSIBILITÉ (TORNADO CHART) ───────────────────────────

    correlations = {
        "Prix pétrole (Brent)": np.corrcoef(oil_price, revenue_annual)[0, 1],
        "Durée sanctions (ans)": np.corrcoef(sanctions_years, revenue_annual)[0, 1],
        "Taux RUB/EUR": np.corrcoef(rub_eur, revenue_annual)[0, 1],
        "Croissance industrielle": np.corrcoef(industrial_growth, revenue_annual)[0, 1],
        "Taux win contrats": np.corrcoef(win_rate_tier1, revenue_annual)[0, 1],
        "Overrun CAPEX": np.corrcoef(capex_overrun, revenue_annual)[0, 1],
        "Délai implémentation": np.corrcoef(implementation_delay, revenue_annual)[0, 1],
        "Inflation énergie": np.corrcoef(inflation_energy, revenue_annual)[0, 1],
        "Érosion prix": np.corrcoef(price_erosion, revenue_annual)[0, 1],
        "Upside politique": np.corrcoef(political_upside, revenue_annual)[0, 1],
    }

    print(f"\n🌪️ ANALYSE DE SENSIBILITÉ (corrélation avec Revenue) :")
    sorted_corr = dict(sorted(correlations.items(), key=lambda x: abs(x[1]), reverse=True))
    for var, corr in sorted_corr.items():
        bar = "█" * int(abs(corr) * 20)
        sign = "+" if corr >= 0 else "-"
        print(f"  {sign}{bar:<20} {corr:+.3f}  {var}")

    # ─── EXPORT GRAPHIQUES ────────────────────────────────────────────────

    if export:
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle("Monte Carlo Risk Analysis — Air Liquide Russia BD Pipeline",
                     fontsize=14, fontweight='bold', y=0.98)

        # 1. Distribution Revenue
        ax1 = axes[0, 0]
        ax1.hist(revenue_annual, bins=100, color='steelblue', alpha=0.7, edgecolor='none')
        ax1.axvline(p10_rev, color='red', linestyle='--', label=f'P10: {p10_rev:.2f}')
        ax1.axvline(p50_rev, color='green', linestyle='-', linewidth=2, label=f'P50: {p50_rev:.2f}')
        ax1.axvline(p90_rev, color='orange', linestyle='--', label=f'P90: {p90_rev:.2f}')
        ax1.axvline(base_revenue, color='purple', linestyle=':', label=f'Base: {base_revenue:.2f}')
        ax1.set_title('Distribution Revenue Annuel (M€/an)')
        ax1.set_xlabel('Revenue M€/an')
        ax1.legend(fontsize=8)
        ax1.grid(alpha=0.3)

        # 2. Distribution VAN
        ax2 = axes[0, 1]
        npv_clipped = np.clip(npv, -200, 500)
        ax2.hist(npv_clipped, bins=100, color='mediumseagreen', alpha=0.7, edgecolor='none')
        ax2.axvline(0, color='red', linewidth=2, label='VAN = 0 (seuil)')
        ax2.axvline(p50_npv, color='green', linestyle='-', linewidth=2, label=f'P50: {p50_npv:.0f} M€')
        profitable_pct = (npv > 0).mean()
        ax2.set_title(f'Distribution VAN 15 ans — P(>0)={profitable_pct:.0%}')
        ax2.set_xlabel('VAN M€')
        ax2.legend(fontsize=8)
        ax2.grid(alpha=0.3)

        # 3. Tornado Chart
        ax3 = axes[1, 0]
        vars_names = list(sorted_corr.keys())[:8]
        corr_vals = [sorted_corr[v] for v in vars_names]
        colors = ['#00C853' if c > 0 else '#D50000' for c in corr_vals]
        bars = ax3.barh(vars_names, corr_vals, color=colors, alpha=0.8)
        ax3.axvline(0, color='black', linewidth=0.8)
        ax3.set_title('Tornado Chart — Sensibilité Revenue')
        ax3.set_xlabel('Corrélation avec Revenue')
        ax3.set_xlim(-1, 1)
        ax3.grid(alpha=0.3, axis='x')

        # 4. Scénarios What-If
        ax4 = axes[1, 1]
        scenarios = {
            'Baseline\n(Sanctions)': base_revenue * sanctions_factor.mean(),
            'Partial\nLift 2026': base_revenue * 1.4,
            'Full\nLift 2027': base_revenue * 2.0,
            'Recovery\n2028': base_revenue * 2.8,
            'Boom\n2030': base_revenue * 4.2,
        }
        sc_colors = ['#B71C1C', '#F57F17', '#1B5E20', '#0D47A1', '#4A148C']
        bars4 = ax4.bar(scenarios.keys(), scenarios.values(), color=sc_colors, alpha=0.85)
        for bar, val in zip(bars4, scenarios.values()):
            ax4.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05,
                     f'{val:.1f} M€', ha='center', va='bottom', fontsize=9, fontweight='bold')
        ax4.set_title('Revenue par Scénario Sanctions (M€/an)')
        ax4.set_ylabel('Revenue M€/an')
        ax4.grid(alpha=0.3, axis='y')

        plt.tight_layout()
        output_path = os.path.join(OUTPUT_DIR, "monte_carlo_results.png")
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        print(f"\n✓ Graphiques exportés : {output_path}")
        plt.close()

    # ─── EXPORT CSV RÉSULTATS ─────────────────────────────────────────────

    if export:
        results_df = pd.DataFrame({
            "Iteration": range(1, N + 1),
            "Oil_Price_USD": oil_price,
            "Sanctions_Years": sanctions_years,
            "RUB_EUR": rub_eur,
            "Industrial_Growth_pct": industrial_growth * 100,
            "Win_Rate_pct": win_rate_tier1 * 100,
            "CAPEX_Overrun": capex_overrun,
            "Revenue_M_EUR_yr": revenue_annual,
            "NPV_M_EUR": npv,
            "ROI_5yr_pct": roi_5yr,
            "Payback_Years": payback,
        }).round(4)

        csv_path = os.path.join(OUTPUT_DIR, "monte_carlo_results.csv")
        results_df.to_csv(csv_path, sep=";", index=False, encoding="utf-8-sig")
        print(f"✓ Données exportées : {csv_path}")

        # Summary statistics
        summary = pd.DataFrame({
            "Metric": ["Revenue_M_EUR_yr", "NPV_M_EUR", "ROI_5yr_pct", "Payback_Years"],
            "P10": [p10_rev, p10_npv, p10_roi, p10_pay],
            "P50": [p50_rev, p50_npv, p50_roi, p50_pay],
            "P90": [p90_rev, p90_npv, p90_roi, p90_pay],
            "P(positive)": [
                (revenue_annual > 0).mean(),
                (npv > 0).mean(),
                (roi_5yr > 0).mean(),
                (payback < PROJECT_LIFE).mean()
            ]
        })
        summary_path = os.path.join(OUTPUT_DIR, "monte_carlo_summary.csv")
        summary.to_csv(summary_path, sep=";", index=False, encoding="utf-8-sig")
        print(f"✓ Résumé exporté : {summary_path}")

    print(f"\n✅ Simulation terminée — {N:,} itérations")
    return {
        "revenue": revenue_annual,
        "npv": npv,
        "roi": roi_5yr,
        "payback": payback,
        "correlations": correlations
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Monte Carlo Risk Simulation — Air Liquide Russia BD"
    )
    parser.add_argument("--iterations", type=int, default=10_000,
                        help="Nombre d'itérations (default: 10000)")
    parser.add_argument("--export", action="store_true",
                        help="Exporter graphiques PNG et CSV résultats")
    args = parser.parse_args()

    run_monte_carlo(n_iterations=args.iterations, export=args.export)
