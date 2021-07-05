from newspaper import Article
import re
import json
import logging

import util.constants as c
from util.functions import send_request, has_all_components

"""
Scrapes the front page of NPR and turns each article into an article dictionary, storing
it in a list. Each dictionary has key/value pairs:

    title: Title of article
    caption: NPR-given summary of article
    url: page url
    tags: NPR-given tags + newspaper-given tags
    source: website story was retrieved from, npr
    img: header image, optional

NPR website request gives a feeds json file. The final digit changes often, varying between
0 and 9. There's a section of feeds called "items" which contains all stories. The json stories
can be read as dictionaries. 
"""

NPR_LINK = "https://www.npr.org/"
NPR = "npr"
FEEDS_REGEX = "https://feeds.npr.org/feeds/100[0-9]/feed.json" #this is a guess

ITEMS = "items"
VIDEO_ARTICLE = "VIDEO"
STORY_SUMMARY = "summary"

def scrape_npr():
    logging.info("NPR:Starting web-scraping")

    npr_request = send_request(NPR_LINK, NPR)
    if npr_request == None:
        logging.critical("NPR: Unable to request NPR site")
        return

    np_result = re.search(FEEDS_REGEX, npr_request.text)
    json_request = send_request(np_result.group(0), NPR)
    if json_request == None:
        logging.critical("NPR: Unable to request NPR json")
        return

    stories = json.loads(json_request.text).get(ITEMS)

    story_list = []

    for story in stories:
        if VIDEO_ARTICLE in story[c.STORY_TITLE]:
            logging.info("NPR: Skipping video article")
            continue

        story_dict = {}
        if ({c.STORY_TITLE, STORY_SUMMARY, c.STORY_URL} <= story.keys()):
            logging.info("NPR: Scraping article %s", story[c.STORY_TITLE])
            story_dict[c.STORY_TITLE] = story[c.STORY_TITLE]
            story_dict[c.STORY_CAPTION] = story[STORY_SUMMARY]
            story_dict[c.STORY_URL] = story[c.STORY_URL]
        else:
            logging.warning("NPR: Story missing some components, not added")
            continue

        try: 
            article = Article(story[c.STORY_URL])
            article.build()

        except Article.ArticleException as e: 
            logging.error("NPR: Error in trying to create Article for story %s:\n%s", story[STORY_TITLE], e)
            continue

        tags = []
        if c.STORY_TAGS in story.keys():
            tags.extend(story[c.STORY_TAGS])
        tags.extend(article.keywords)
        story_dict[c.STORY_TAGS] = tags

        story_dict[c.STORY_SOURCE] = c.STORY_SOURCE
        if (article.has_top_image):
            story_dict[c.STORY_IMG] = article.top_image

        if (has_all_components(story_dict)):
            story_list.append(story_dict)
        else:
            logging.warning("NPR: Story missing some components, not added")

    
    return story_list
