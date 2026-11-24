-- Create the schema of bronze layer
CREATE SCHEMA IF NOT EXISTS bronze;

-- Create the raw_reviews table
CREATE TABLE IF NOT EXISTS bronze.raw_reviews_we_ar (
    review_id TEXT,
    user_name TEXT,
    user_image TEXT,
    content TEXT,
    score TEXT,
    thumbs_up_count TEXT,
    review_created_version TEXT,
    at TEXT,
    reply_content TEXT,
    replied_at TEXT,
    app_version TEXT
);

CREATE TABLE IF NOT EXISTS bronze.raw_reviews_we_en (
    LIKE bronze.raw_reviews_we_ar INCLUDING ALL
);

CREATE TABLE IF NOT EXISTS bronze.raw_reviews_orange_ar (
    LIKE bronze.raw_reviews_we_ar INCLUDING ALL
);

CREATE TABLE IF NOT EXISTS bronze.raw_reviews_orange_en (
    LIKE bronze.raw_reviews_we_ar INCLUDING ALL
);

CREATE TABLE IF NOT EXISTS bronze.raw_reviews_vodafone_ar (
    LIKE bronze.raw_reviews_we_ar INCLUDING ALL
);

CREATE TABLE IF NOT EXISTS bronze.raw_reviews_vodafone_en (
    LIKE bronze.raw_reviews_we_ar INCLUDING ALL
);

CREATE TABLE IF NOT EXISTS bronze.raw_reviews_etisalat_ar (
    LIKE bronze.raw_reviews_we_ar INCLUDING ALL
);

CREATE TABLE IF NOT EXISTS bronze.raw_reviews_etisalat_en (
    LIKE bronze.raw_reviews_we_ar INCLUDING ALL
);

-- create raw_offers table
CREATE TABLE IF NOT EXISTS bronze.raw_offers (
    provider_name TEXT,
    offer_title TEXT,
    offer_type TEXT,
    price_egp TEXT,
    quota_amount TEXT,
    quota_unit TEXT,
    speed_limit TEXT,
    speed_unit TEXT,
    validity_days TEXT,
    offer_description TEXT,
    target_customer TEXT,
    scraped_at TEXT,
    source_url TEXT
);

-- Create the raw_surveys table
CREATE TABLE IF NOT EXISTS bronze.raw_surveys (
    response_timestamp TEXT,
    provider_name TEXT,
    tenure TEXT,

    network_coverage_rating TEXT,
    internet_speed_rating TEXT,
    value_for_money_rating TEXT,
    customer_service_rating TEXT,
    mobile_app_rating TEXT,
    overall_satisfaction_rating TEXT,

    network_importance TEXT,
    value_for_money_importance TEXT,
    customer_service_importance TEXT,
    app_experience_importance TEXT,
    offers_importance TEXT,

    monthly_spending TEXT,
    customer_comment TEXT
);