-- ==========================================
-- Gold Layer: Fact Survey Quality Checks
-- ==========================================

-- ==========================================
-- 1. Fact Survey Response
-- Completeness and Uniqueness
-- ==========================================
SELECT
(SELECT COUNT(*)
FROM silver.silver_survey_responses) AS silver_count,
(SELECT COUNT(*)
FROM gold.fact_survey_response) AS fact_count,
(SELECT COUNT(DISTINCT response_key)
FROM gold.fact_survey_response) AS distinct_response_keys,
(SELECT COUNT(DISTINCT response_id)
FROM gold.fact_survey_response) AS distinct_response_ids;


-- Check missing foreign keys
SELECT
COUNT(*) AS total_rows,
COUNT(*) FILTER (WHERE company_key IS NULL) AS null_company_keys,
COUNT(*) FILTER (WHERE date_key IS NULL) AS null_date_keys,
COUNT(*) FILTER (WHERE tenure_key IS NULL) AS null_tenure_keys,
COUNT(*) FILTER (WHERE spending_key IS NULL) AS null_spending_keys
FROM gold.fact_survey_response;


-- ==========================================
-- 2. Survey Comments
-- Check missing comments and NLP eligibility
-- ==========================================
SELECT
COUNT(*) AS total_rows,
COUNT(*) FILTER (WHERE customer_comment IS NULL) AS null_comments,
COUNT(*) FILTER (WHERE TRIM(customer_comment) = '') AS empty_comments,
COUNT(*) FILTER (WHERE comment_nlp_eligible = TRUE) AS eligible_comments,
COUNT(*) FILTER (WHERE comment_nlp_eligible = FALSE) AS ineligible_comments,
COUNT(*) FILTER (WHERE comment_nlp_eligible IS NULL) AS null_eligibility_flags
FROM gold.fact_survey_response;


-- ==========================================
-- 3. Fact Survey Rating
-- Completeness and Uniqueness
-- ==========================================
SELECT
(SELECT COUNT(*)
FROM silver.silver_survey_ratings) AS silver_count,
(SELECT COUNT(*)
FROM gold.fact_survey_rating) AS fact_count,
(SELECT COUNT(DISTINCT rating_key)
FROM gold.fact_survey_rating) AS distinct_rating_keys,
(SELECT COUNT(DISTINCT response_key, rating_type_key)
FROM gold.fact_survey_rating) AS distinct_rating_combinations;


-- Check missing foreign keys
SELECT
COUNT(*) AS total_rows,
COUNT(*) FILTER (WHERE response_key IS NULL) AS null_response_keys,
COUNT(*) FILTER (WHERE rating_type_key IS NULL) AS null_rating_type_keys
FROM gold.fact_survey_rating;


-- Check rating score validity
SELECT
COUNT(*) AS total_rows,
COUNT(*) FILTER (WHERE rating_score IS NULL) AS null_scores,
COUNT(*) FILTER (WHERE rating_score < 1 OR rating_score > 5) AS invalid_scores,
COUNT(DISTINCT rating_score) AS distinct_scores,
MIN(rating_score) AS min_score,
MAX(rating_score) AS max_score
FROM gold.fact_survey_rating;


-- ==========================================
-- 4. Fact Survey Preference
-- Completeness and Uniqueness
-- ==========================================
SELECT
(SELECT COUNT(*)
FROM silver.silver_survey_preferences) AS silver_count,
(SELECT COUNT(*)
FROM gold.fact_survey_preference) AS fact_count,
(SELECT COUNT(DISTINCT preference_key)
FROM gold.fact_survey_preference) AS distinct_preference_keys,
(SELECT COUNT(DISTINCT response_key, preference_factor_key)
FROM gold.fact_survey_preference) AS distinct_preference_combinations;


-- Check missing foreign keys
SELECT
COUNT(*) AS total_rows,
COUNT(*) FILTER (WHERE response_key IS NULL) AS null_response_keys,
COUNT(*) FILTER (WHERE preference_factor_key IS NULL) AS null_factor_keys
FROM gold.fact_survey_preference;


-- Check importance score validity
SELECT
COUNT(*) AS total_rows,
COUNT(*) FILTER (WHERE importance_score IS NULL) AS null_scores,
COUNT(*) FILTER (WHERE importance_score < 1 OR importance_score > 5) AS invalid_scores,
COUNT(DISTINCT importance_score) AS distinct_scores,
MIN(importance_score) AS min_score,
MAX(importance_score) AS max_score
FROM gold.fact_survey_preference;