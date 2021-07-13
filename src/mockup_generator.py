import logging
from src.websites.yahoo import scrape_yahoo
from websites.npr import scrape_npr
from websites.nbc import scrape_nbc
from websites.nyt import scrape_nyt
from websites.ap import scrape_ap
import time
import json

"""
Work to do:
Scrape another site
Create test cases for utils
Figure out what __init__.py is
Implement sorting algorithm
 https://datascience.stackexchange.com/questions/30513/are-there-any-good-nlp-apis-for-comparing-strings-in-terms-of-semantic-similarit
 Naive idea: From "top stories", pick the stories that have the highest "similarity score" to ALL other stories. Add them 
 one at a time and make sure the similarity score between stories is very small. If a story is too similar to other stories in
 the mockup, DO NOT ADD. From there, randomly pick 10 stories from all_stories making sure they're not the same story that's
 already in the mockup but also that their similarity score is small with regards to all stories. 
 COSINE SIMILARITY DOES NOT WORK FOR SEMANTICS 
Multithreading to speed this process up
Fix NYT bug... make sure ALL urls processed are starting with https://nyt or whatever the link is
"""
logger = logging.getLogger()
logger.setLevel(logging.INFO)

log = logging.StreamHandler()
formatter = logging.Formatter('%(levelname)s %(asctime)s : %(filename)s : %(funcName)s :: %(message)s', "%Y-%m-%d %H:%M:%S")
log.setFormatter(formatter)
logger.addHandler(log)

total_time = time.time()
all_stories = []
top_stories = []

start_time = time.time()
npr = scrape_npr()
if npr:
    logger.info("Finished scraping NPR of %d articles in %f seconds", len(npr), time.time() - start_time)
    all_stories.extend(npr)
    if len(npr) > 4:
        top_stories.extend(npr[0:4])
else:
    logger.critical("Unable to add NPR to all_stories")

start_time = time.time()
nbc = scrape_nbc()
if nbc:
    logger.info("Finished scraping NBC of %d articles in %f seconds", len(nbc), time.time() - start_time)
    all_stories.extend(nbc)
    if len(nbc) > 4:
        top_stories.extend(nbc[0:4])
else:
    logger.critical("Unable to add NBC to all_stories")


start_time = time.time()
nyt = scrape_nyt()
if nyt: 
    logger.info("Finished scraping NYT of %d articles in %f seconds", len(nyt), time.time() - start_time)
    all_stories.extend(nyt)
    if len(nyt) > 4:
        top_stories.extend(nyt[0:4])
else:
    logger.critical("Unable to add NYT to all_stories")

start_time = time.time()
ap = scrape_ap()
if ap:
    logger.info("Finished scraping AP of %d articles in %f seconds", len(ap), time.time() - start_time)
    all_stories.extend(ap)
    if len(ap) > 4:
        top_stories.extend(ap[0:4])
else:
    logger.critical("Unable to add NPR to all_stories")


start_time = time.time()
yahoo = scrape_yahoo()
if yahoo:
    logger.info("Finished scraping Yahoo of %d articles in %f seconds", len(yahoo), time.time() - start_time)
    all_stories.extend(yahoo)
    #Yahoo's stories aren't ordered by importance
else:
    logger.critical("Unable to add NPR to all_stories")
    
logger.info("Finished scraping all sites in %f seconds", time.time() - total_time)

with open("all_stories.txt", "w") as f:
    json.dump(json.dumps(all_stories), f)

with open("top_stories.txt", "w") as f:
    json.dump(json.dumps(top_stories), f)

# Creating temporary text files so each time I try this I don't have to scrape all sites
# with open("all_stories.txt", "r") as f:
#     all_list = json.load(f)

# with open("top_stories.txt", "r") as f:
#     top_list = json.load(f)

# all_stories = json.loads(all_list)
# top_stories = json.loads(top_list)
