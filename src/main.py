import logging
from websites.npr import scrape_npr
from websites.nbc import scrape_nbc
from websites.nyt import scrape_nyt
from websites.ap import scrape_ap
import time

"""
Work to do:
1. Create test cases for utils
2. Comb over and make sure formatting good
3. Get logger to be more advanced + update logger messages accordingly
4. Figure out what __init__.py is
5. Come up with simple sorting algorithm. Maybe involving link
    https://www.geeksforgeeks.org/python-measure-similarity-between-two-sentences-using-cosine-similarity/
6. TODO in ap.py
7. Multithreading to speed this process up
"""
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

start_time = time.time()
ap = scrape_ap()
logging.info("Finished scraping AP of %d articles in %f seconds", len(ap), time.time() - start_time)

logging.info("Finished scraping all sites in %f seconds", time.time() - total_time)