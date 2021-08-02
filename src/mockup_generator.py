import itertools
import logging
import re
import time
from concurrent.futures import ThreadPoolExecutor
from inspect import getmembers, isfunction

import numpy as np
import tensorflow_hub as hub
from newspaper import Article
from sumy.nlp.tokenizers import Tokenizer
from sumy.parsers.plaintext import PlaintextParser
from sumy.summarizers.text_rank import TextRankSummarizer

import src.util.constants as c
from src.util.functions import cache, read_cache
import src.websites as websites

logger = logging.getLogger()
logger.propagate = False
logger.setLevel(logging.INFO) 
log = logging.StreamHandler()
formatter = logging.Formatter('%(levelname)s %(asctime)s : %(filename)s : %(funcName)s :: %(message)s', "%Y-%m-%d %H:%M:%S")
log.setFormatter(formatter)
logger.addHandler(log)

WEBSITES = [website[1] for website in getmembers(websites, isfunction)]
MOCKUP_LEN = 10
WEBSITE_REGEX = r"_(.*?)\(\)"
CACHED_MOCKUP = "mockup.txt"
UNDER_THRESHOLD = len(WEBSITES)/24

SIMILARITY_CONSTANT = .2
MODEL = hub.load("USE/")

TOKENIZER = Tokenizer("english")
tr_summarizer = TextRankSummarizer()

def len_summary(article_text):
    num_words = len(re.findall(r'\w+', article_text))
    len_summary = round(num_words/400) 
    if (len_summary == 0):
        len_summary = 1
    return len_summary

def conflict(mockup, yesterday_mockup, toadd):
    toadd_embed = MODEL([toadd[c.STORY_TITLE]])
    story_count = 1
    for story in mockup:
        story_embed = MODEL([story[c.STORY_TITLE]])
        if (np.inner(toadd_embed, story_embed) > SIMILARITY_CONSTANT):
            return True
        
        if story[c.STORY_SOURCE] == toadd[c.STORY_SOURCE]:
            story_count+=1
    
    for story in yesterday_mockup:
        if toadd[c.STORY_TITLE] == story[c.STORY_TITLE]:
            return False

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

    logging.info("Finished scraping all {} stories in {:.2f}".format(len(all_stories), time.time() - activity_time))
    logging.info("Scoring all stories")

    activity_time = time.time()
    for story in all_stories:
        story[c.STORY_SCORE] = 0

    for story1, story2 in itertools.combinations(all_stories, 2):
        if not story1[c.STORY_SOURCE] == story2[c.STORY_SOURCE]:
            if not c.STORY_EMBED in story1.keys():
                story1[c.STORY_EMBED] = MODEL([story1[c.STORY_TITLE]])
            if not c.STORY_EMBED in story2.keys():
                story2[c.STORY_EMBED] = MODEL([story2[c.STORY_TITLE]])
            inner_product = np.inner(story1[c.STORY_EMBED], story2[c.STORY_EMBED])[0][0].astype(float)
            story1[c.STORY_SCORE] += inner_product
            story2[c.STORY_SCORE] += inner_product 
    
    for story in all_stories:
        story.pop(c.STORY_EMBED)
  
    logging.info("Finished scoring stories in {:.2f} seconds".format(time.time() - activity_time))
    logging.info("Generating mockup")

    activity_time = time.time()
    sorted_stories = sorted(all_stories, key = lambda i: i[c.STORY_SCORE], reverse=True)

    for story in sorted_stories:
        if not(conflict(mockup, read_cache(CACHED_MOCKUP), story)):
            mockup.append(story)
        if(len(mockup) == MOCKUP_LEN):
            break

    if (len(mockup) < MOCKUP_LEN):
        logging.critical("Unable to add at least {} stories to mockup".format(MOCKUP_LEN))

    headline = mockup[0]
    for story in mockup:
        article = Article(story[c.STORY_URL])
        article.build()
        story[c.STORY_TEXT] = article.text
        if article.has_top_image:
            story[c.STORY_IMAGE] = article.top_image
        parser = PlaintextParser.from_string(story[c.STORY_TEXT], TOKENIZER)
        summary = tr_summarizer(parser.document, 2 if story != headline else 3)
        story[c.STORY_SUMMARY] = [str(sentence) for sentence in summary]
    
    cache(mockup, CACHED_MOCKUP)
    logging.info("Finished generating mockup in {:.2f} seconds".format(time.time() - activity_time))
    return mockup
