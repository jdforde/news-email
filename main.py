import logging
from websites.npr import scrape_npr
from websites.nbc import scrape_nbc
import time

logging.basicConfig(level=logging.INFO)
start_time = time.time()
npr = scrape_npr()
if not npr == "":
    logging.info("Finished scraping NPR of %d articles in %f seconds", len(npr), time.time() - start_time)


start_time = time.time()
nbc = scrape_nbc()
logging.info("Finished scraping NPR of %d articles in %f seconds", len(nbc), time.time() - start_time)