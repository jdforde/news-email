import logging
from websites.npr import scrape_npr

logging.basicConfig(level=logging.INFO)
test = scrape_npr()
logging.info("Finished scraping NPR of %d articles", len(test))
