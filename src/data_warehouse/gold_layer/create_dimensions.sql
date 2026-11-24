-- create gold schema
CREATE SCHEMA IF NOT EXISTS gold;

-- Create Company Dimension View
CREATE OR REPLACE VIEW gold.dim_company AS

SELECT
    ROW_NUMBER() OVER (ORDER BY company_name)::INTEGER AS company_key,
    UPPER(company_name) AS company_code,
    company_name

FROM (
    SELECT DISTINCT TRIM(company_name) AS company_name
    FROM silver.silver_survey_responses
    WHERE company_name IS NOT NULL

    UNION

    SELECT DISTINCT TRIM(provider_name) AS company_name
    FROM silver.silver_offers
    WHERE provider_name IS NOT NULL
) AS companies;


-- create date dimension view 
DROP VIEW IF EXISTS gold.dim_date;

CREATE VIEW gold.dim_date AS

SELECT
    TO_CHAR(d.date_value, 'YYYYMMDD')::INTEGER AS date_key,
    d.date_value::DATE AS full_date,
    TO_CHAR(d.date_value, 'Month') AS month_name,
    EXTRACT(QUARTER FROM d.date_value)::INTEGER AS quarter,
    EXTRACT(ISODOW FROM d.date_value)::INTEGER AS day_of_week,
    TO_CHAR(d.date_value, 'Day') AS day_name,
    CASE
        WHEN EXTRACT(ISODOW FROM d.date_value) IN (5, 6)
        THEN TRUE
        ELSE FALSE
    END AS is_weekend
FROM GENERATE_SERIES(
    (SELECT MIN(submission_date)
     FROM silver.silver_survey_responses),
    (SELECT MAX(submission_date)
     FROM silver.silver_survey_responses),
    INTERVAL '1 day'
) AS d(date_value);


-- create gold.dim_app_version view
CREATE OR REPLACE VIEW gold.dim_app_version AS

SELECT
    ROW_NUMBER() OVER (ORDER BY app_version)::INTEGER AS app_version_key,
    app_version
FROM (
    SELECT DISTINCT app_version
    FROM silver.silver_reviews
    WHERE app_version IS NOT NULL
) AS versions;

-- create gold.dim_tenure view
CREATE OR REPLACE VIEW gold.dim_tenure AS

SELECT
    ROW_NUMBER() OVER (ORDER BY tenure_category)::INTEGER AS tenure_key,
    tenure_category
FROM (
    SELECT DISTINCT tenure_category
    FROM silver.silver_survey_responses
    WHERE tenure_category IS NOT NULL
) AS tenures;

-- create gold.dim_spending view 
CREATE OR REPLACE VIEW gold.dim_spending AS

SELECT
    ROW_NUMBER() OVER (ORDER BY spending_category)::INTEGER AS spending_key,
    spending_category
FROM (
    SELECT DISTINCT spending_category
    FROM silver.silver_survey_responses
    WHERE spending_category IS NOT NULL
) AS spending;

-- create gold.dim_rating_type view
CREATE OR REPLACE VIEW gold.dim_rating_type AS

SELECT
    ROW_NUMBER() OVER (ORDER BY rating_category)::INTEGER AS rating_type_key,
    rating_category AS rating_type_name
FROM (
    SELECT DISTINCT rating_category
    FROM silver.silver_survey_ratings
    WHERE rating_category IS NOT NULL
) AS rating_types;

-- create gold.dim_preference_factor view
CREATE OR REPLACE VIEW gold.dim_preference_factor AS

SELECT
    ROW_NUMBER() OVER (ORDER BY preference_factor)::INTEGER AS preference_factor_key,
    preference_factor AS factor_name
FROM (
    SELECT DISTINCT preference_factor
    FROM silver.silver_survey_preferences
    WHERE preference_factor IS NOT NULL
) AS factors;

-- create gold.dim_offer_type view
CREATE OR REPLACE VIEW gold.dim_offer_type AS

SELECT
    ROW_NUMBER() OVER (ORDER BY offer_type)::INTEGER AS offer_type_key,
    offer_type AS offer_type_name
FROM (
    SELECT DISTINCT offer_type
    FROM silver.silver_offers
    WHERE offer_type IS NOT NULL
) AS offer_types;

-- create gold.dim_target_customer view
CREATE OR REPLACE VIEW gold.dim_target_customer AS

SELECT
    ROW_NUMBER() OVER (ORDER BY target_customer)::INTEGER AS target_customer_key,
    target_customer AS target_customer_name
FROM (
    SELECT DISTINCT target_customer
    FROM silver.silver_offers
    WHERE target_customer IS NOT NULL
) AS customers;

-- create gold.dim_offer view
CREATE OR REPLACE VIEW gold.dim_offer AS

SELECT
    ROW_NUMBER() OVER (ORDER BY o.provider_name, o.offer_title, o.offer_type, o.target_customer)::INTEGER AS offer_key,
    CONCAT_WS('|', o.provider_name, o.offer_title, o.offer_type, o.target_customer) AS offer_natural_key,
    o.offer_title,
    o.offer_description,
    ot.offer_type_key,
    tc.target_customer_key,
    o.source_url
FROM (SELECT DISTINCT
        provider_name,
        offer_title,
        offer_type,
        target_customer,
        offer_description,
        source_url
    FROM silver.silver_offers
) AS o
LEFT JOIN gold.dim_offer_type AS ot
    ON o.offer_type = ot.offer_type_name
LEFT JOIN gold.dim_target_customer AS tc
    ON o.target_customer = tc.target_customer_name;