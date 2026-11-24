-- ==========================================
-- Gold Layer: Fact Reviews Quality Checks
-- ==========================================

-- 1. Completeness and Uniqueness
-- Compare Silver and Gold row counts
SELECT
(SELECT COUNT(*)
FROM silver.silver_reviewsdata) AS silver_count,
(SELECT COUNT(*)
FROM gold.fact_reviews) AS fact_count,
(SELECT COUNT(DISTINCT review_id)
FROM gold.fact_reviews) AS distinct_reviews;


-- 2. Foreign Key Completeness
-- Check missing dimension keys
SELECT
COUNT(*) AS total_reviews,
COUNT(*) FILTER (WHERE company_key IS NULL) AS null_company_keys,
COUNT(*) FILTER (WHERE date_key IS NULL) AS null_date_keys,
COUNT(*) FILTER (WHERE app_version_key IS NULL) AS null_app_version_keys
FROM gold.fact_reviews;


-- 3. Rating Score Distribution
-- Check rating distribution
SELECT
rating_score,
COUNT(*) AS review_count,
ROUND(COUNT(*) * 100.0 /SUM(COUNT(*)) OVER (), 2) AS percentage
FROM gold.fact_reviews
GROUP BY rating_score
ORDER BY rating_score;


-- 4. Thumbs Up Count
-- Check validity and distribution
SELECT
COUNT(*) AS total_reviews,
COUNT(*) FILTER (WHERE thumbs_up_count IS NULL) AS null_count,
COUNT(*) FILTER (WHERE thumbs_up_count < 0) AS negative_count,
COUNT(*) FILTER (WHERE thumbs_up_count = 0) AS zero_count,
COUNT(*) FILTER (WHERE thumbs_up_count > 0) AS positive_count,
MIN(thumbs_up_count) AS min_value,
MAX(thumbs_up_count) AS max_value,
AVG(thumbs_up_count)::NUMERIC(10,2) AS avg_value
FROM gold.fact_reviews;


-- 5. Replies
-- Check reply distribution
SELECT
has_reply,
COUNT(*) AS review_count,
ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS percentage
FROM gold.fact_reviews
GROUP BY has_reply
ORDER BY has_reply;


-- 6. Word Count
-- Check validity of word count
SELECT
COUNT(*) AS total_reviews,
COUNT(*) FILTER (WHERE word_count IS NULL) AS null_word_count,
COUNT(*) FILTER (WHERE word_count < 0) AS negative_word_count,
MIN(word_count) AS min_word_count,
MAX(word_count) AS max_word_count,
AVG(word_count)::NUMERIC(10,2) AS avg_word_count
FROM gold.fact_reviews;


-- 7. Character Count
-- Check validity of character count
SELECT
COUNT(*) AS total_reviews,
COUNT(*) FILTER (WHERE char_count IS NULL) AS null_char_count,
COUNT(*) FILTER (WHERE char_count < 0) AS negative_char_count,
MIN(char_count) AS min_char_count,
MAX(char_count) AS max_char_count,
AVG(char_count)::NUMERIC(10,2) AS avg_char_count
FROM gold.fact_reviews;


-- 8. Exclamation Count
-- Check validity of exclamation count
SELECT
COUNT(*) AS total_reviews,
COUNT(*) FILTER (WHERE exclam_count IS NULL) AS null_exclam_count,
COUNT(*) FILTER (WHERE exclam_count < 0) AS negative_exclam_count,
MIN(exclam_count) AS min_value,
MAX(exclam_count) AS max_value,
AVG(exclam_count)::NUMERIC(10,2) AS avg_value
FROM gold.fact_reviews;


-- 9. Review Created Version
-- Check missing and distinct versions
SELECT
COUNT(*) AS total_reviews,
COUNT(*) FILTER (WHERE review_created_version IS NULL) AS null_versions,
COUNT(*) FILTER ( WHERE TRIM(review_created_version) = '') AS empty_versions,
COUNT(DISTINCT review_created_version) AS distinct_versions,
ROUND(COUNT(*) FILTER (WHERE review_created_version IS NULL OR TRIM(review_created_version) = '') * 100.0 / COUNT(*), 2) AS missing_percentage
FROM gold.fact_reviews;


-- 10. App Version Consistency
-- Compare app_version with review_created_version
SELECT
COUNT(*) AS total_reviews,
COUNT(*) FILTER (WHERE app_version = review_created_version) AS identical_versions,
COUNT(*) FILTER (WHERE app_version <> review_created_version) AS different_versions,
COUNT(*) FILTER (WHERE app_version IS NULL AND review_created_version IS NULL) AS both_null,
COUNT(*) FILTER (WHERE app_version IS NULL AND review_created_version IS NOT NULL) AS app_version_null_only,
COUNT(*) FILTER (WHERE app_version IS NOT NULL AND review_created_version IS NULL) AS created_version_null_only
FROM silver.silver_reviewsdata;