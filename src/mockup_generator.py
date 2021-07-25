import logging
import re
import time

import numpy as np
import tensorflow_hub as hub
from newspaper import Article

from src.util.functions import cache
import src.util.constants as c
from websites import *

"""
Work to do:
- Scrape one more site
- Try to get tensor's summarizer to work so we have fewer dependencies
- Multithreading to speed this process up
- Read about tensor and what is actually going on 
- Improve scoring speed
- Consider scraping a different page of NYT to get more articles
"""
logger = logging.getLogger()
logger.propagate = False
logger.setLevel(logging.INFO)

log = logging.StreamHandler()
formatter = logging.Formatter('%(levelname)s %(asctime)s : %(filename)s : %(funcName)s :: %(message)s', "%Y-%m-%d %H:%M:%S")
log.setFormatter(formatter)
logger.addHandler(log)

MOCKUP_LEN = 16
WEBSITE_REGEX = r"_(.*?)\(\)"
WEBSITES = ["scrape_npr()", "scrape_nbc()", "scrape_nyt()", "scrape_ap()", "scrape_yahoo()", "scrape_propublica()"]
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

def conflict(mockup, toadd):
    toadd_embed = embed([toadd[c.STORY_TITLE]])
    story_count = 1
    names_to_add = []
    for story in mockup:
        story_embed = embed([story[c.STORY_TITLE]])
        if (np.inner(toadd_embed, story_embed) > SIMILARITY_CONSTANT):
            return True
        
        if story[c.STORY_SOURCE] == toadd[c.STORY_SOURCE]:
            story_count+=1
    
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
    print(UNDER_THRESHOLD)
    all_stories = []
    mockup = []

    activity_time = time.time()
    for website in WEBSITES:
        start_time = time.time()
        website_stories = eval(website)
        if website_stories:
            logging.info("Finished scraping %s of %d articles in %f seconds", re.search(WEBSITE_REGEX, website).group(1), 
                len(website_stories), time.time() - start_time)
            all_stories.extend(website_stories)
        else:
            logger.critical("Unable to add %s to all_stories", re.search(WEBSITE_REGEX, website).group(1))

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
    for story in sorted_stories:
        if not(conflict(mockup, story)):
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
