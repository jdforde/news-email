import logging
import time
import re

from newspaper import Article

from websites.yahoo import scrape_yahoo
from websites.npr import scrape_npr
from websites.nbc import scrape_nbc
from websites.nyt import scrape_nyt
from websites.ap import scrape_ap
from websites.propublica import scrape_propublica
import src.util.constants as c

import tensorflow_hub as hub
import numpy as np

from sumy.nlp.tokenizers import Tokenizer
from sumy.parsers.plaintext import PlaintextParser
from sumy.summarizers.text_rank import TextRankSummarizer

"""
Work to do:
- Scrape another site
- Create test cases for utils
- Figure out what __init__.py is
- Improve story-selecting algorithm, introduce some balancing of story sources
- Try to get tensor's summarizer to work so we have fewer dependencies
- Think about changing structure of mockup_generator, seems like a lot for one file and it's not
    very well organized
- Multithreading to speed this process up
- Read about tensor and what is actually going on 
- Get rid of or understand what the tensor stuff at the beginning is
- Code cleanup
"""
logger = logging.getLogger()
logger.propagate = False
logger.setLevel(logging.INFO)

log = logging.StreamHandler()
formatter = logging.Formatter('%(levelname)s %(asctime)s : %(filename)s : %(funcName)s :: %(message)s', "%Y-%m-%d %H:%M:%S")
log.setFormatter(formatter)
logger.addHandler(log)

all_stories = []
mockup = []
WEBSITE_REGEX = "_(.*?)\(\)"
websites = ["scrape_npr()", "scrape_nbc()", "scrape_nyt()", "scrape_ap()", "scrape_yahoo()", "scrape_propublica()"]
SIMILARITY_CONSTANT = .35 #This is a guess
module_url = "https://tfhub.dev/google/universal-sentence-encoder/4"
model = hub.load(module_url)
tokenizer = Tokenizer("english")
tr_summarizer = TextRankSummarizer()

def embed(input):
    return model(input)

def too_similar(mockup, story):
    to_add = embed([story[c.STORY_TITLE]])
    for finalized_story in mockup:
        story_embed = embed([finalized_story[c.STORY_TITLE]])
        if (np.inner(to_add, story_embed > SIMILARITY_CONSTANT)):
            return True
    
    return False

def len_summary(article_text):
    num_words = len(re.findall(r'\w+', article_text))
    len_summary = round(num_words/400) #a guess
    if (len_summary == 0):
        len_summary = 1
    return len_summary

total_time = time.time()

for website in websites:
    start_time = time.time()
    website_stories = eval(website)
    if website_stories:
        logging.info("Finished scraping %s of %d articles in %f seconds", re.search(WEBSITE_REGEX, website).group(1), 
            len(website_stories), time.time() - start_time)
        all_stories.extend(website_stories)
    else:
        logger.critical("Unable to add %s to all_stories", re.search(WEBSITE_REGEX, website).group(1))

logging.info("Finished scraping all %d stories in %f seconds", len(all_stories), time.time() - total_time)

logging.info("Scoring all stories")
total_time = time.time()
for story1 in all_stories:
    story1_embed = embed([story1[c.STORY_TITLE]])
    score = 0
    for story2 in all_stories:
        story2_embed = embed([story2[c.STORY_TITLE]])
        score += np.inner(story1_embed, story2_embed)

    story1[c.STORY_SCORE] = score[0][0].astype(float)

logging.info("Finished scoring stories in %f seconds", time.time() - total_time)
logging.info("Generating mockup")

sorted_stories = sorted(all_stories, key = lambda i: i[c.STORY_SCORE], reverse=True)
for story in sorted_stories:
    if not(too_similar(mockup, story)):
        mockup.append(story)
        if(len(mockup) >=16 ):
            break

if (len(mockup) < 12):
    logging.critical("Unable to add more than 12 stories to mockup")

total_time = time.time()
headline = mockup[0]
for story in mockup:
    article = Article(story[c.STORY_URL])
    article.build()
    story[c.STORY_TEXT] = article.text
    parser = PlaintextParser.from_string(article.text, tokenizer)
    summary = tr_summarizer(parser.document, len_summary(article.text) if story != headline 
        else len_summary(article.text)+2)
    print(story[c.STORY_SOURCE])

logging.info("Finished mockup summaries in %f seconds", time.time() - total_time)
