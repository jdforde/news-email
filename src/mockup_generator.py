import itertools
import logging
import time
import re
from concurrent.futures import ThreadPoolExecutor
from inspect import getmembers, isfunction
from pathlib import Path

import numpy as np
import tensorflow_hub as hub
from sumy.nlp.tokenizers import Tokenizer
from sumy.parsers.plaintext import PlaintextParser
from sumy.summarizers.text_rank import TextRankSummarizer

import src.util.constants as c
from src.util.functions import cache
import src.websites as websites

WEBSITES = [website[1] for website in getmembers(websites, isfunction)]
MOCKUP_LEN = 10
WEBSITE_REGEX = r"_(.*?)\(\)"
CACHED_MOCKUP = "mockup.txt"
UNDER_THRESHOLD = len(WEBSITES)/24

SIMILARITY_CONSTANT = .2
MODEL = hub.load("USE/")

TOKENIZER = Tokenizer("english")
tr_summarizer = TextRankSummarizer()

SUMMARY_MAX_LENGTH = 40

def conflict(mockup, old_stories, toadd):
    toadd_embed = MODEL([toadd[c.STORY_TITLE]])
    story_count = 1
    for story in mockup:
        story_embed = MODEL([story[c.STORY_TITLE]])
        if (np.inner(toadd_embed, story_embed) > SIMILARITY_CONSTANT):
            return True
        
        if story[c.STORY_SOURCE] == toadd[c.STORY_SOURCE]:
            story_count+=1
    
    if toadd[c.STORY_TITLE] in old_stories:
        logging.info("Can't add story. Was in a previous mockup this week")
        return True

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

    if Path(c.CACHED_STORIES).exists():
        logging.info("Reading cached stories to use for conflict resolution")
        with open(c.CACHED_STORIES, "r") as f:
            old_stories = f.read().split('\n')
    else:
        logging.info("cached_stories.txt is unavailable")

    for story in sorted_stories:
        if not(conflict(mockup, old_stories, story)):
            mockup.append(story)
        if(len(mockup) == MOCKUP_LEN):
            break

    if (len(mockup) < MOCKUP_LEN):
        logging.critical("Unable to add at least {} stories to mockup".format(MOCKUP_LEN))

    for story in mockup:
        parser = PlaintextParser.from_string(story[c.STORY_TEXT], TOKENIZER)
        summary = tr_summarizer(parser.document, 3)
        summary_list = [str(sentence) for sentence in summary if len(str(sentence).split()) < SUMMARY_MAX_LENGTH]

        if not summary_list:
            logging.info("Sumy summary is too long. Taking 1 sumy point and turning it into several bullet points")
            summary = tr_summarizer(parser.document, 1)
            summary_list = re.sub(r'([a-z]{4,}\.((’|”)*)?)', r'\1**|**', str(summary[0]))
            summary_list = list(filter(None, summary_list.split("**|**")))
            if len(summary_list) > 3:
                summary_list = summary_list[:3]

        story[c.STORY_SUMMARY] = summary_list
            
    logging.info("Caching the mockup stories")
    with open(c.CACHED_STORIES, "a") as f:
        for story in mockup:
            f.write(story[c.STORY_TITLE] + '\n')

    #temporary, for testing, remove in production
    cache(mockup, "mockup.txt")

    logging.info("Finished generating complete mockup in {:.2f} seconds".format(time.time() - activity_time))
    return mockup
