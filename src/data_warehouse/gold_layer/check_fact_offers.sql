-- ==========================================
-- Gold Layer: Fact Offers Quality Checks
-- ==========================================


-- 1. Duplicate Offers
-- Check duplicate offers using main attributes
SELECT
provider_name,
offer_title,
offer_type,
target_customer,
COUNT(*) AS offer_count,
COUNT(DISTINCT price_egp) AS distinct_prices,
COUNT(DISTINCT quota_amount) AS distinct_quotas,
COUNT(DISTINCT speed_limit) AS distinct_speeds,
COUNT(DISTINCT validity_days) AS distinct_validities
FROM silver.silver_offers
GROUP BY
provider_name,
offer_title,
offer_type,
target_customer
HAVING COUNT(*) > 1
ORDER BY offer_count DESC;


-- 2. Exact Duplicate Offers
-- Check duplicates using all offer attributes
SELECT
provider_name,
offer_title,
offer_type,
target_customer,
price_egp,
quota_amount,
quota_unit,
speed_limit,
speed_unit,
validity_days,
COUNT(*) AS row_count
FROM silver.silver_offers
GROUP BY
provider_name,
offer_title,
offer_type,
target_customer,
price_egp,
quota_amount,
quota_unit,
speed_limit,
speed_unit,
validity_days
HAVING COUNT(*) > 1;


-- 3. Fact Offers Completeness and Uniqueness
SELECT
COUNT(*) AS total_rows,
COUNT(DISTINCT offer_fact_key) AS distinct_fact_keys,
COUNT(DISTINCT offer_key) AS distinct_offer_keys,
COUNT(*) FILTER (WHERE offer_key IS NULL) AS null_offer_keys,
COUNT(*) FILTER (WHERE company_key IS NULL) AS null_company_keys
FROM gold.fact_offers;


-- 4. Numeric Validity
-- Check negative and zero values
SELECT
COUNT(*) AS total_rows,
COUNT(*) FILTER (WHERE price_egp < 0) AS negative_prices,
COUNT(*) FILTER (WHERE quota_amount < 0) AS negative_quotas,
COUNT(*) FILTER (WHERE speed_limit < 0) AS negative_speeds,
COUNT(*) FILTER (WHERE validity_days < 0) AS negative_validity,
COUNT(*) FILTER (WHERE price_egp = 0) AS zero_prices,
COUNT(*) FILTER (WHERE validity_days = 0) AS zero_validity
FROM gold.fact_offers;


-- 5. Missing Values
-- Check NULL values in offer attributes
SELECT
COUNT(*) AS total_rows,
COUNT(*) FILTER (WHERE price_egp IS NULL) AS null_prices,
COUNT(*) FILTER (WHERE quota_amount IS NULL) AS null_quotas,
COUNT(*) FILTER (WHERE speed_limit IS NULL) AS null_speeds,
COUNT(*) FILTER (WHERE validity_days IS NULL) AS null_validities
FROM gold.fact_offers;