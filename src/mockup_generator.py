import itertools
import logging
import time
import re
from concurrent.futures import ThreadPoolExecutor
from inspect import getmembers, isfunction
from pathlib import Path

import numpy as np
import tensorflow_hub as hub
from newspaper import Article
from sumy.nlp.tokenizers import Tokenizer
from sumy.parsers.plaintext import PlaintextParser
from sumy.summarizers.text_rank import TextRankSummarizer
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

import src.util.constants as c
from src.util.functions import cache, read_cache
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

ABSTRACTIVE_MODEL = AutoModelForSeq2SeqLM.from_pretrained("mrm8488/t5-base-finetuned-summarize-news")
ABSTRACTIVE_TOKENIZER = AutoTokenizer.from_pretrained("mrm8488/t5-base-finetuned-summarize-news")

def abstractive_summary(start_text):
    if len(start_text.split()) > 512:
        logging.info("Story is too long for abstractive summarizer. Summarizing a summary")
        parser = PlaintextParser.from_string(start_text, TOKENIZER)
        sentences = tr_summarizer(parser.document, 6)
        start_text = ''.join([str(sentence) for sentence in sentences])

    input_ids = ABSTRACTIVE_TOKENIZER.encode(start_text, return_tensors="pt", add_special_tokens=True)
    generated_ids = ABSTRACTIVE_MODEL.generate(input_ids=input_ids, num_beams=2, max_length=100,  repetition_penalty=2.5, length_penalty=1.0, early_stopping=True)
    preds = [ABSTRACTIVE_TOKENIZER.decode(g, skip_special_tokens=True, clean_up_tokenization_spaces=True) for g in generated_ids]
    
    chopped_string = preds[0][re.search('\w', preds[0]).start():preds[0].rfind('.')+1]
    sentence_list = re.split('([a-z]{4,}\. )', chopped_string)
    for i in range(0, len(sentence_list)-1):
        if i+1 < len(sentence_list)-1:
            sentence_list[i] = sentence_list[i] + sentence_list[i+1]
            sentence_list[i] = sentence_list[i].capitalize()
            sentence_list.remove(sentence_list[i+1])
    
    return sentence_list

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
        article = Article(story[c.STORY_URL])
        article.build()
        story[c.STORY_TEXT] = article.text
        if article.has_top_image:
            if not article.top_image == "https://apnews.com/images/ShareLogo2.png":
                story[c.STORY_IMAGE] = article.top_image
            else:
                logging.warning("AP site does not have proper image. Not adding image to mockup")
        parser = PlaintextParser.from_string(story[c.STORY_TEXT], TOKENIZER)
        summary = tr_summarizer(parser.document, 2)
        if len(' '.join([str(sentence) for sentence in summary]).split()) > 90:
            logging.info("Sumy summary too long. Creating abstractive summary")
            story[c.STORY_SUMMARY] = abstractive_summary(article.text)
        else:
            story[c.STORY_SUMMARY] = [str(sentence) for sentence in summary]
            
    logging.info("Caching the mockup stories")
    with open(c.CACHED_STORIES, "a") as f:
        for story in mockup:
            f.write(story[c.STORY_TITLE] + '\n')

    #temporary, for testing, remove in production
    cache(mockup, CACHED_MOCKUP)

    logging.info("Finished generating complete mockup in {:.2f} seconds".format(time.time() - activity_time))
    return mockup
