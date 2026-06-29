-- ==============================================
-- EUROASIA INDUSTRIAL INVESTMENT SIMULATION SYSTEM
-- SQL ANALYTICAL QUERIES
-- ==============================================

-- 1. Top Countries by EIII Score in 2025
SELECT 
    country_id, 
    eiii_score, 
    risk_score, 
    economy_score 
FROM 
    fact_eiii_scores 
WHERE 
    year = 2025 
ORDER BY 
    eiii_score DESC;

-- 2. Russia vs China Comparison (Energy & Risk)
SELECT 
    country_id, 
    year, 
    energy_score, 
    risk_score, 
    eiii_score 
FROM 
    fact_eiii_scores 
WHERE 
    country_id IN ('Russia', 'China') 
ORDER BY 
    year, country_id;

-- 3. Air Liquide Investment Recommendation Filter
SELECT 
    country_id, 
    plant_location, 
    capex_estimate_m, 
    roi_risk_adjusted_pct, 
    investment_decision 
FROM 
    fact_air_liquide_investment 
WHERE 
    investment_decision = 'INVEST' 
    AND roi_risk_adjusted_pct > 15;

-- 4. Salesforce Pipeline Risk Analysis
SELECT 
    country_id, 
    stage, 
    COUNT(opportunity_id) AS nb_opportunities, 
    SUM(amount_eur) AS total_pipeline, 
    risk_level 
FROM 
    fact_salesforce_pipeline 
GROUP BY 
    country_id, stage, risk_level 
ORDER BY 
    total_pipeline DESC;

-- 5. SAP MM Procurement Spend by Country and Material
SELECT 
    country_id, 
    material, 
    COUNT(purchase_order_po) AS nb_pos, 
    SUM(total_value_eur) AS total_spend_eur 
FROM 
    fact_sap_mm 
WHERE 
    purchase_order_po != '' 
GROUP BY 
    country_id, material 
ORDER BY 
    total_spend_eur DESC;

-- 6. SAP SD Order-to-Cash Completion Rate
SELECT
    COUNT(sales_order_so) AS total_orders,
    SUM(CASE WHEN billing_invoice_vf01 != '' THEN 1 ELSE 0 END) AS fully_invoiced_orders,
    SUM(total_value_eur) AS total_booked_revenue
FROM
    fact_sap_sd;
