-- ==============================================
-- EUROASIA INDUSTRIAL INVESTMENT SIMULATION SYSTEM
-- STAR SCHEMA DEFINITION (SQL)
-- ==============================================

-- 1. DIMENSIONS
CREATE TABLE dim_country (
    country_id VARCHAR(50) PRIMARY KEY,
    region VARCHAR(100),
    currency VARCHAR(10)
);

CREATE TABLE dim_year (
    year INT PRIMARY KEY
);

CREATE TABLE dim_risk (
    risk_level VARCHAR(20) PRIMARY KEY,
    description TEXT
);

CREATE TABLE dim_vendor (
    vendor_id VARCHAR(100) PRIMARY KEY,
    country_id VARCHAR(50) REFERENCES dim_country(country_id),
    vendor_type VARCHAR(50)
);

CREATE TABLE dim_customer (
    customer_id VARCHAR(100) PRIMARY KEY,
    country_id VARCHAR(50) REFERENCES dim_country(country_id),
    customer_segment VARCHAR(50)
);


-- 2. FACT TABLES

-- Fact: EIII Scores
CREATE TABLE fact_eiii_scores (
    country_id VARCHAR(50) REFERENCES dim_country(country_id),
    year INT REFERENCES dim_year(year),
    eiii_score DECIMAL(5,2),
    economy_score DECIMAL(5,2),
    energy_score DECIMAL(5,2),
    industry_score DECIMAL(5,2),
    logistics_score DECIMAL(5,2),
    risk_score DECIMAL(5,2),
    PRIMARY KEY (country_id, year)
);

-- Fact: Air Liquide Investment Simulation
CREATE TABLE fact_air_liquide_investment (
    investment_id SERIAL PRIMARY KEY,
    country_id VARCHAR(50) REFERENCES dim_country(country_id),
    year INT REFERENCES dim_year(year),
    plant_location VARCHAR(100),
    capex_estimate_m DECIMAL(10,2),
    opex_energy_m DECIMAL(10,2),
    logistics_cost_m DECIMAL(10,2),
    expected_revenue_m DECIMAL(10,2),
    roi_base_pct DECIMAL(5,2),
    roi_risk_adjusted_pct DECIMAL(5,2),
    break_even_years DECIMAL(5,1),
    investment_decision VARCHAR(20)
);

-- Fact: Salesforce Pipeline
CREATE TABLE fact_salesforce_pipeline (
    opportunity_id VARCHAR(50) PRIMARY KEY,
    account_name VARCHAR(100),
    opportunity_name VARCHAR(150),
    lead_source VARCHAR(50),
    stage VARCHAR(50),
    amount_eur DECIMAL(15,2),
    expected_close_date DATE,
    probability_pct INT,
    risk_level VARCHAR(20) REFERENCES dim_risk(risk_level),
    country_id VARCHAR(50) REFERENCES dim_country(country_id),
    decision_maker VARCHAR(100)
);

-- Fact: SAP MM Procurement Cycle
CREATE TABLE fact_sap_mm (
    purchase_requisition_pr VARCHAR(50),
    purchase_order_po VARCHAR(50),
    goods_receipt_migo VARCHAR(50),
    invoice_receipt_miro VARCHAR(50),
    vendor_id VARCHAR(100) REFERENCES dim_vendor(vendor_id),
    country_id VARCHAR(50) REFERENCES dim_country(country_id),
    material VARCHAR(100),
    plant VARCHAR(20),
    quantity INT,
    unit_price_eur DECIMAL(10,2),
    total_value_eur DECIMAL(15,2),
    creation_date DATE,
    PRIMARY KEY (purchase_requisition_pr)
);

-- Fact: SAP SD Sales Cycle
CREATE TABLE fact_sap_sd (
    sales_order_so VARCHAR(50) PRIMARY KEY,
    delivery_document VARCHAR(50),
    goods_issue_document VARCHAR(50),
    billing_invoice_vf01 VARCHAR(50),
    customer_id VARCHAR(100) REFERENCES dim_customer(customer_id),
    country_id VARCHAR(50) REFERENCES dim_country(country_id),
    material VARCHAR(100),
    plant VARCHAR(20),
    quantity INT,
    unit_price_eur DECIMAL(10,2),
    total_value_eur DECIMAL(15,2),
    incoterms VARCHAR(10),
    creation_date DATE
);

-- 3. INDEXES
CREATE INDEX idx_eiii_score ON fact_eiii_scores(eiii_score DESC);
CREATE INDEX idx_sap_po ON fact_sap_mm(purchase_order_po);
CREATE INDEX idx_sap_so ON fact_sap_sd(sales_order_so);
CREATE INDEX idx_sf_stage ON fact_salesforce_pipeline(stage);
