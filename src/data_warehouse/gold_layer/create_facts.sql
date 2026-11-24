-- create gold.fact_offers view
CREATE OR REPLACE VIEW gold.fact_offers AS

SELECT
    ROW_NUMBER() OVER (ORDER BY o.provider_name, o.offer_title)::INTEGER AS offer_fact_key,
    c.company_key,
    TO_CHAR(CURRENT_DATE, 'YYYYMMDD')::INTEGER AS date_key,
    d.offer_key,
    o.price_egp,
    o.quota_amount,
    o.quota_unit,
    o.speed_limit,
    o.speed_unit,
    o.validity_days,
    o.offer_category,
    o.offer_description,
    o.target_customer,
    o.source_url,
    CURRENT_TIMESTAMP AS load_timestamp
FROM silver.silver_offers AS o
LEFT JOIN gold.dim_company AS c
    ON o.provider_name = c.company_name
LEFT JOIN gold.dim_offer AS d
    ON CONCAT_WS('|', o.provider_name, o.offer_title, o.offer_type, o.target_customer) = d.offer_natural_key;


-- create gold.fact_reviews view
CREATE OR REPLACE VIEW gold.fact_reviews AS

SELECT
    ROW_NUMBER() OVER (ORDER BY r.review_id)::INTEGER AS review_key,
    r.review_id,
    c.company_key,
    TO_CHAR(r.at, 'YYYYMMDD')::INTEGER AS date_key,
    av.app_version_key,
    r.content AS review_text_original,
    r.score AS rating_score,
    r.thumbs_up_count,
    r.review_created_version,
    r.reply_content,
    r.replied_at,
    r.language,
    CURRENT_TIMESTAMP AS load_timestamp
FROM silver.silver_reviews AS r
LEFT JOIN gold.dim_company AS c
    ON r.provider_name = c.company_name
LEFT JOIN gold.dim_app_version AS av
    ON r.app_version = av.app_version;

-- create gold.fact_survey_response view
CREATE OR REPLACE VIEW gold.fact_survey_response AS

SELECT
    ROW_NUMBER() OVER (ORDER BY s.response_id)::INTEGER AS response_key,
    s.response_id,
    c.company_key,
    TO_CHAR(s.submission_date, 'YYYYMMDD')::INTEGER AS date_key,
    t.tenure_key,
    sp.spending_key,
    s.comment_original AS customer_comment,
    s.is_nlp_eligible AS comment_nlp_eligible,
    CURRENT_TIMESTAMP AS load_timestamp
FROM silver.silver_survey_responses AS s
LEFT JOIN gold.dim_company AS c
    ON s.company_name = c.company_name
LEFT JOIN gold.dim_tenure AS t
    ON s.tenure_category = t.tenure_category
LEFT JOIN gold.dim_spending AS sp
    ON s.spending_category = sp.spending_category; 

-- create gold.fact_survey_rating view
CREATE OR REPLACE VIEW gold.fact_survey_rating AS

SELECT
    ROW_NUMBER() OVER (ORDER BY r.response_id, r.rating_category)::INTEGER AS rating_key,
    fr.response_key,
    rt.rating_type_key,
    r.rating_score,
    CURRENT_TIMESTAMP AS load_timestamp
FROM silver.silver_survey_ratings AS r
LEFT JOIN gold.fact_survey_response AS fr
    ON r.response_id = fr.response_id
LEFT JOIN gold.dim_rating_type AS rt
    ON r.rating_category = rt.rating_type_name;

--create gold.fact_survey_preference view
CREATE OR REPLACE VIEW gold.fact_survey_preference AS

SELECT
    ROW_NUMBER() OVER (ORDER BY p.response_id, p.preference_factor)::INTEGER AS preference_key,
    fr.response_key,
    pf.preference_factor_key,
    p.importance_rank AS importance_score,
    CURRENT_TIMESTAMP AS load_timestamp
FROM silver.silver_survey_preferences AS p
LEFT JOIN gold.fact_survey_response AS fr
    ON p.response_id = fr.response_id
LEFT JOIN gold.dim_preference_factor AS pf
    ON p.preference_factor = pf.factor_name;