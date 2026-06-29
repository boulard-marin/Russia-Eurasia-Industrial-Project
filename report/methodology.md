# Methodology

The project uses an auditable data hierarchy:

1. Direct official/API values when available: World Bank API and CBR XML.
2. Official institutional reports or source registries where extraction requires manual PDF/API work.
3. Explicit ASSUMPTION rows for simulation parameters where plant-level data is not publicly disclosed.
4. `DATA NOT AVAILABLE PUBLICLY` labels where a required detail cannot be verified from open public sources.

## EIRM Score

EIRM combines market size, industrial depth, energy/trade position, logistics, macro stability and sanctions risk.

Recommended interpretation:
- `INVEST`: score >= 70 and risk-adjusted ROI acceptable.
- `WAIT`: score >= 45 or attractive fundamentals but unresolved sanctions/payment risk.
- `AVOID`: score < 45 or current legal/payment/insurance risks dominate economics.

## Important Limits

The sanctions index is not an official sanctions count. It is an ordinal decision-support assumption documented in `data/sanctions_index.csv`.
The Air Liquide Russia unit model is a scenario engine. CAPEX and operating values are assumptions based on public industrial project benchmarks, not disclosed Russia plant economics.
