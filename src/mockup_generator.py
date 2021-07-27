import logging
import re
import time

import numpy as np
import tensorflow_hub as hub
from newspaper import Article
from concurrent.futures import ThreadPoolExecutor

from src.util.functions import cache, read_cache
import src.util.constants as c
from websites import *

"""
Work to do:
- Implement tensor's summarizer
- Read about tensor and what is actually going on 
- Improve scoring speed
"""
logger = logging.getLogger()
logger.propagate = False
logger.setLevel(logging.INFO) 

log = logging.StreamHandler()
formatter = logging.Formatter('%(levelname)s %(asctime)s : %(filename)s : %(funcName)s :: %(message)s', "%Y-%m-%d %H:%M:%S")
log.setFormatter(formatter)
logger.addHandler(log)
WEBSITES = [scrape_yahoo, scrape_npr, scrape_nbc, scrape_ap, scrape_propublica, scrape_slate, scrape_nyt]
MOCKUP_LEN = 16
WEBSITE_REGEX = r"_(.*?)\(\)"

SIMILARITY_CONSTANT = .2
UNDER_THRESHOLD = len(WEBSITES)/24
MODULE_URL = "https://tfhub.dev/google/universal-sentence-encoder/4"
MODEL = hub.load(MODULE_URL)

def embed(input):
    return MODEL(input)

def len_summary(article_text):
    num_words = len(re.findall(r'\w+', article_text))
    len_summary = round(num_words/400) #a guess
    if (len_summary == 0):
        len_summary = 1
    return len_summary

def conflict(mockup, yesterday_mockup, toadd):
    toadd_embed = embed([toadd[c.STORY_TITLE]])
    story_count = 1
    names_to_add = []
    for story in mockup:
        story_embed = embed([story[c.STORY_TITLE]])
        if (np.inner(toadd_embed, story_embed) > SIMILARITY_CONSTANT):
            return True
        
        if story[c.STORY_SOURCE] == toadd[c.STORY_SOURCE]:
            story_count+=1
    
    for story in yesterday_mockup:
        if toadd[c.STORY_TITLE] == story[c.STORY_TITLE]:
            return False
    
    #this is nice but has issues. Consider a story about Jill Biden being more popular than a Biden story
    #thus, the Biden story would not get added
    for name in c.IMPORTANT_NAMES:
        if name.isupper() and re.search(name, toadd[c.STORY_TITLE], re.IGNORECASE):
            c.IMPORTANT_NAMES.extend(names_to_add)
            return True
        
        if name.islower() and re.search(name, toadd[c.STORY_TITLE], re.IGNORECASE):
            c.IMPORTANT_NAMES.remove(name)
            names_to_add.append(name.upper())
    
    c.IMPORTANT_NAMES.extend(names_to_add)
    return ((story_count)/MOCKUP_LEN) > UNDER_THRESHOLD

def mockup_generator():
    all_stories = []
    mockup = []

    activity_time = time.time()
    futures = []
    with ThreadPoolExecutor(max_workers=len(WEBSITES)) as executor:
        for website in WEBSITES:
            future = executor.submit(website)
            futures.append(future)
    
    for future in futures:
        if future.result():
            all_stories.extend(future.result())
        else:
            logging.critical("Error with one of the futures. Unable to add stories")

    logging.info("Finished scraping all %d stories in %f seconds", len(all_stories), time.time() - activity_time)
    logging.info("Scoring all stories")

    activity_time = time.time()
    for story1 in all_stories:
        story1_embed = embed([story1[c.STORY_TITLE]])
        score = 0
        for story2 in all_stories:
            story2_embed = embed([story2[c.STORY_TITLE]])
            score += np.inner(story1_embed, story2_embed)

        story1[c.STORY_SCORE] = score[0][0].astype(float)

    logging.info("Finished scoring stories in %f seconds", time.time() - activity_time)
    logging.info("Generating mockup")

    activity_time = time.time()
    sorted_stories = sorted(all_stories, key = lambda i: i[c.STORY_SCORE], reverse=True)

    yesterday_mockup = read_cache("mockup.txt")
    for story in sorted_stories:
        if not(conflict(mockup, yesterday_mockup, story)):
            mockup.append(story)
        if(len(mockup) == MOCKUP_LEN):
            break

    if (len(mockup) < MOCKUP_LEN):
        logging.critical("Unable to add at least %s stories to mockup", MOCKUP_LEN)

    
    for story in mockup:
        article = Article(story[c.STORY_URL])
        article.build()
        story[c.STORY_TEXT] = article.text
        if article.has_top_image:
            story[c.STORY_IMAGE] = article.top_image
    
    cache(mockup, "mockup.txt")
    logging.info("Finished generating mockup in %f seconds", time.time() - activity_time)

if __name__ == '__main__':
    mockup_generator()
