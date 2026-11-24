from google_play_scraper import reviews, Sort
import boto3
import time
import pandas as pd

# =========================
# SETTINGS
# =========================

APP_ID = "com.ucare.we"
LANG = "ar" # Arabic
COUNTRY = "eg"

TARGET = 500000
BATCH_SIZE = 2000

# SeaweedFS
BUCKET = "telecom-data"
S3_ENDPOINT = "http://100.83.218.121:8333"

# Local file
OUTPUT_FILE = f"{APP_ID}_{LANG}_reviews.csv"

# SeaweedFS path
S3_KEY = f"raw/reviews/my_we/{LANG}/my_we_reviews_{LANG}.csv"


# CONNECT TO SEAWEEDFS
session = boto3.Session(
    profile_name="telecom-team"
)

s3 = session.client(
    "s3",
    endpoint_url=S3_ENDPOINT
)

# COLLECT REVIEWS
all_reviews = []
token = None

start = time.time()

print("Starting collection...\n")

while len(all_reviews) < TARGET:

    result, token = reviews(
        APP_ID,
        lang=LANG,
        country=COUNTRY,
        sort=Sort.NEWEST,
        count=BATCH_SIZE,
        continuation_token=token
    )

    if not result:
        print("No more reviews.")
        break

    all_reviews.extend(result)

    print(f"Collected: {len(all_reviews):,}")

    if token is None:
        print("No more pages.")
        break


# REMOVE DUPLICATES
unique_reviews = {
    review["reviewId"]: review
    for review in all_reviews
}

unique_reviews = list(unique_reviews.values())


# CREATE DATAFRAME
df = pd.DataFrame(unique_reviews)

# VALIDATION
if df.empty:
    raise ValueError("No reviews collected.")

if df["reviewId"].duplicated().any():
    raise ValueError("Duplicate review IDs found.")

print(f"\nUnique reviews: {len(df):,}")



# SAVE CSV LOCALLY
df.to_csv(
    OUTPUT_FILE,
    index=False,
    encoding="utf-8-sig"
)

print(f"Local file created: {OUTPUT_FILE}")


# UPLOAD TO SEAWEEDFS
print("\nUploading to SeaweedFS...")

s3.upload_file(
    OUTPUT_FILE,
    BUCKET,
    S3_KEY
)

print("Upload completed successfully.")

# RESULTS
elapsed = time.time() - start

print(f"App:            {APP_ID}")
print(f"Language:       {LANG}")
print(f"Raw reviews:    {len(all_reviews):,}")
print(f"Unique reviews: {len(unique_reviews):,}")
print(f"Time:            {elapsed:.2f} seconds")
print(f"Local file:     {OUTPUT_FILE}")
print(f"S3 location:    s3://{BUCKET}/{S3_KEY}")
