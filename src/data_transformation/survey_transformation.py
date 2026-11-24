import pandas as pd
import re

# 1. Load raw survey CSV exported from Google Forms
file_path = "استبيان تجربة عملاء شركات الاتصالات في مصر- Telescope (الردود) - ردود النموذج 1.csv"
df = pd.read_csv(file_path, encoding="utf-8")

# Rename raw Arabic column headers to clean snake_case identifiers
df.columns = [
    "raw_timestamp", "raw_company", "raw_tenure",
    "rate_Network Quality", "rate_Internet Quality", "rate_Price",
    "rate_Customer Service", "rate_Mobile Application", "rate_Overall Satisfaction",
    "pref_Network", "pref_Price", "pref_Customer Service",
    "pref_Application", "pref_Offers",
    "raw_spending", "comment_original"
]

# Generate sequential natural primary key (1 to 129)
df.insert(0, "survey_response_id", range(1, len(df) + 1))

# 2. Standardize Arabic timestamps into ISO format and extract calendar date
def parse_arabic_timestamp(ts):
    ts = str(ts).strip().replace("ص", "AM").replace("م", "PM")
    return pd.to_datetime(ts, format="%I:%M:%S %p %Y/%m/%d")

df["submitted_at"] = df["raw_timestamp"].apply(parse_arabic_timestamp)
df["submission_date"] = df["submitted_at"].dt.date

# 3. Standardize telecom provider names to match shared DimCompany
company_map = {
    "Vodafone Egypt — فودافون مصر": "Vodafone",
    "Orange Egypt — أورنج مصر": "Orange",
    "WE — وي": "WE",
    "e& Egypt — إي آند مصر": "Etisalat"
}
df["company_name"] = df["raw_company"].str.strip().map(company_map)

# 4. Standardize usage duration (DimTenure) and monthly spending (DimSpending)
tenure_map = {
    "أقل من 6 أشهر": "Less than 6 months",
    "من 6 أشهر إلى سنتين": "6 months to 2 years",
    "أكثر من سنتين": "More than 2 years"
}
spending_map = {
    "أقل من 100 جنيه": "Less than 100 EGP",
    "من 100 إلى أقل من 250 جنيه": "100 to less than 250 EGP",
    "من 250 إلى أقل من 500 جنيه": "250 to less than 500 EGP",
    "من 500 إلى أقل من 800 جنيه": "500 to less than 800 EGP",
    "أكثر من 800 جنيه": "More than 800 EGP"
}
df["tenure_category"] = df["raw_tenure"].str.strip().map(tenure_map)
df["spending_category"] = df["raw_spending"].str.strip().map(spending_map)

# 5. Extract integer scores (1-5) for satisfaction ratings and preference ranks
rating_cols = [c for c in df.columns if c.startswith("rate_")]
pref_cols = [c for c in df.columns if c.startswith("pref_")]

for col in rating_cols + pref_cols:
    df[col] = df[col].astype(str).str.extract(r"(\d+)").astype(int)

# 6. Flag customer comments for downstream NLP eligibility without deleting rows
placeholder_text = "شاركنا رأيك وتجربتك بحرية"

def check_nlp_eligibility(text):
    if pd.isna(text):
        return False
    clean = str(text).strip()
    # Exclude copied survey instruction prompt
    if placeholder_text in clean:
        return False
    # Retain only Arabic and English alphabetical characters
    letters_only = re.sub(r"[^a-zA-Z\u0600-\u06FF]", "", clean)
    # Exclude punctuation-only strings or fragments shorter than 4 letters
    if len(letters_only) < 4:
        return False
    return True

df["comment_original"] = df["comment_original"].fillna("").astype(str).str.strip()
df["is_nlp_eligible"] = df["comment_original"].apply(check_nlp_eligibility)

# 7. Construct the three normalized output datasets
# Table 1: Master survey responses (129 rows)
survey_responses = df[[
    "survey_response_id", "submitted_at", "submission_date",
    "company_name", "tenure_category", "spending_category",
    "comment_original", "is_nlp_eligible"
]]

# Table 2: Unpivoted satisfaction ratings (774 rows)
survey_ratings = df.melt(
    id_vars=["survey_response_id"],
    value_vars=rating_cols,
    var_name="rating_category",
    value_name="rating_score"
)
survey_ratings["rating_category"] = survey_ratings["rating_category"].str.replace("rate_", "")

# Table 3: Unpivoted customer preferences (645 rows)
survey_preferences = df.melt(
    id_vars=["survey_response_id"],
    value_vars=pref_cols,
    var_name="preference_factor",
    value_name="importance_rank"
)
survey_preferences["preference_factor"] = survey_preferences["preference_factor"].str.replace("pref_", "")

# Export final CSV deliverables using UTF-8-SIG encoding
survey_responses.to_csv("survey_responses.csv", index=False, encoding="utf-8-sig")
survey_ratings.to_csv("survey_ratings.csv", index=False, encoding="utf-8-sig")
survey_preferences.to_csv("survey_preferences.csv", index=False, encoding="utf-8-sig")

# 8. Post-transformation data quality validation checks
print("Survey Responses count:", len(survey_responses))       # Expected: 129
print("Survey Ratings count:", len(survey_ratings))           # Expected: 774
print("Survey Preferences count:", len(survey_preferences))   # Expected: 645
print("NLP Eligible comments:", survey_responses["is_nlp_eligible"].sum())
print("Null values check:\n", survey_responses.isnull().sum())