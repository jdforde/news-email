import logging
from websites.npr import scrape_npr
from websites.nbc import scrape_nbc
from websites.nyt import scrape_nyt
import time



logging.basicConfig(level=logging.INFO)
total_time = time.time()
start_time = time.time()
npr = scrape_npr()
logging.info("Finished scraping NPR of %d articles in %f seconds", len(npr), time.time() - start_time)


start_time = time.time()
nbc = scrape_nbc()
logging.info("Finished scraping NBC of %d articles in %f seconds", len(nbc), time.time() - start_time)

start_time = time.time()
nyt = scrape_nyt()
logging.info("Finished scraping NYT of %d articles in %f seconds", len(nyt), time.time() - start_time)

logging.info("Finished scraping all sites in %f seconds", time.time() - total_time)