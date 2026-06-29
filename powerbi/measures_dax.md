# DAX Measures

```DAX
EIRM Score = AVERAGE(eirm_scores[eirm_score_0_100])

Recommendation =
SWITCH(
    TRUE(),
    [EIRM Score] >= 70, "INVEST",
    [EIRM Score] >= 45, "WAIT",
    "AVOID"
)

Trade Balance USD =
SUM(trade_flows[exports_goods_services_usd])
- SUM(trade_flows[imports_goods_services_usd])

Risk Adjusted ROI % =
AVERAGE(air_liquide_russia_simulation[roi_adjusted_pct])

Break Even Years =
AVERAGE(air_liquide_russia_simulation[break_even_years])
```
