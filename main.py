import logging
from websites.npr import scrape_npr
import time

logging.basicConfig(level=logging.INFO)
npr_time = time.time()
test = scrape_npr()
logging.info("Finished scraping NPR of %d articles in %f seconds", len(test), time.time() - npr_time)
