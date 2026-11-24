import logging

from .offers_loader import load_offers
from .reviews_loader import load_reviews
from .survey_loader import load_survey


logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)


def main():

    logger.info("Starting data loading pipeline.")

    try:
        # Load Offers
        logger.info("Loading Offers...")
        offers_count = load_offers()
        logger.info(f"Offers loaded successfully: {offers_count} records.")

        # Load Reviews
        logger.info("Loading Reviews...")
        reviews_results = load_reviews()
        logger.info("Reviews loaded successfully.")

        # Load Survey
        logger.info("Loading Survey...")
        survey_count = load_survey()
        logger.info(f"Survey loaded successfully: {survey_count} records.")
        logger.info(f"Offers Loaded: {offers_count}")
        total_reviews = 0

        for table_name, count in reviews_results.items():
            logger.info(f"{table_name}: {count}")
            total_reviews += count
        logger.info(f"Total Reviews: {total_reviews}")
        logger.info(f"Survey Responses: {survey_count}")

    except Exception:
        logger.exception("Data loading pipeline failed.")
        raise


if __name__ == "__main__":
    main()