-- Top country attractiveness by latest data and scenario-adjusted risk.
WITH latest AS (
    SELECT m.*
    FROM macro_indicators m
    JOIN (
        SELECT country_code, MAX(year) AS max_year
        FROM macro_indicators
        GROUP BY country_code
    ) x ON x.country_code = m.country_code AND x.max_year = m.year
),
scored AS (
    SELECT
        latest.country,
        latest.year,
        latest.gdp_current_usd,
        latest.fdi_inflows_usd,
        latest.industry_value_added_pct_gdp,
        latest.lpi_overall_score,
        s.scenario_id,
        s.sanctions_intensity_index_0_100,
        (COALESCE(latest.industry_value_added_pct_gdp, 0) * 0.35)
        + (COALESCE(latest.lpi_overall_score, 0) * 10 * 0.20)
        + (CASE WHEN latest.fdi_inflows_usd > 0 THEN 20 ELSE 0 END)
        - (s.sanctions_intensity_index_0_100 * 0.45) AS eirm_score_raw
    FROM latest
    JOIN sanctions_index s ON s.country = latest.country
)
SELECT *
FROM scored
ORDER BY scenario_id, eirm_score_raw DESC;

-- Russia detail under current sanctions.
SELECT m.*, s.*
FROM macro_indicators m
JOIN sanctions_index s ON s.country = m.country
WHERE m.country = 'Russia' AND s.scenario_id = 'SCENARIO 1'
ORDER BY m.year DESC;
