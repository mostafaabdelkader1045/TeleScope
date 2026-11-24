-- Create the silver layer tables here
CREATE SCHEMA IF NOT EXISTS silver;

-- Create the silver_reviews table
CREATE TABLE IF NOT EXISTS silver.silver_reviews (
    review_id TEXT,
    content TEXT,
    score INTEGER,
    thumbs_up_count INTEGER,
    review_created_version TEXT,
    at TIMESTAMP,
    reply_content TEXT,
    replied_at TIMESTAMP,
    app_version TEXT,
    provider_name TEXT,
    review_date DATE,
    clean_text TEXT,
    word_count INTEGER,
    char_count INTEGER,
    exclam_count INTEGER,
    year INTEGER,
    month INTEGER,
    has_reply BOOLEAN,
    sentiment TEXT,
    label TEXT,
    filtered_text TEXT
);

-- Create the silver_offers table
CREATE TABLE IF NOT EXISTS silver.silver_offers (
    provider_name TEXT,
    offer_title TEXT,
    offer_type TEXT,
    price_egp NUMERIC(10,2),
    quota_amount NUMERIC(10,2),
    quota_unit TEXT,
    speed_limit NUMERIC(10,2),
    speed_unit TEXT,
    validity_days INTEGER,
    offer_description TEXT,
    target_customer TEXT,
    source_url TEXT,
    offer_category TEXT
);

-- create the silver_survey_responses
CREATE TABLE IF NOT EXISTS silver.silver_survey_responses (
    response_id TEXT,
    submitted_at TIMESTAMP,
    submission_date DATE,
    company_name TEXT,
    tenure_category TEXT,
    spending_category TEXT,
    comment_original TEXT,
    is_nlp_eligible BOOLEAN
);

-- create the silver_survey_ratings
CREATE TABLE IF NOT EXISTS silver.silver_survey_ratings (
    response_id TEXT,
    rating_category TEXT,
    rating_score INTEGER
);

-- create the silver_survey_preferences
CREATE TABLE IF NOT EXISTS silver.silver_survey_preferences (
    response_id TEXT,
    preference_factor TEXT,
    importance_rank INTEGER
);



