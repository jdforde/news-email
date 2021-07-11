import logging
from src.websites.yahoo import scrape_yahoo
from websites.npr import scrape_npr
from websites.nbc import scrape_nbc
from websites.nyt import scrape_nyt
from websites.ap import scrape_ap
import time

"""
Work to do:
Scrape another site
Create test cases for utils
Figure out what __init__.py is
Come up with simple sorting algorithm. Maybe involving link
 https://www.geeksforgeeks.org/python-measure-similarity-between-two-sentences-using-cosine-similarity/
 Naive idea: for first four stories, pick one randomly from top 4 stories from random news source, compare
 each of them to make sure their titles are not too similar (low cosine similarity). Then randomly pick 10
 or so more articles from random sources. Order them form highest cosine similarity to ALL stories to lowest.
 Maybe, if one is too low, get rid of it and improve. Make sure low cosine similarity between stories currently
 present. Will have to do some experimenting
Multithreading to speed this process up
"""
logger = logging.getLogger()
logger.setLevel(logging.INFO)

log = logging.StreamHandler()
formatter = logging.Formatter('%(levelname)s %(asctime)s : %(filename)s : %(funcName) :: %(message)s', "%Y-%m-%d %H:%M:%S")
log.setFormatter(formatter)
logger.addHandler(log)

total_time = time.time()

start_time = time.time()
npr = scrape_npr()
logger.info("Finished scraping NPR of %d articles in %f seconds", len(npr), time.time() - start_time)

start_time = time.time()
nbc = scrape_nbc()
logger.info("Finished scraping NBC of %d articles in %f seconds", len(nbc), time.time() - start_time)

start_time = time.time()
nyt = scrape_nyt()
logger.info("Finished scraping NYT of %d articles in %f seconds", len(nyt), time.time() - start_time)

start_time = time.time()
ap = scrape_ap()
logger.info("Finished scraping AP of %d articles in %f seconds", len(ap), time.time() - start_time)

start_time = time.time()
yahoo = scrape_yahoo()
logger.info("Finished scraping Yahoo of %d articles in %f seconds", len(yahoo), time.time() - start_time)

logger.info("Finished scraping all sites in %f seconds", time.time() - total_time)