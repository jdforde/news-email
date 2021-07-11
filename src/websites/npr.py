import re
import json
import logging

import src.util.constants as c
from src.util.functions import send_request, has_all_components

"""
NPR website request gives a feeds json file. The final digit changes often, varying between
0 and 9. There's a section of feeds called "items" which contains all stories. The json stories
can be read as dictionaries. 

    title: Title of article
    caption: NPR-given summary of article
    url: page url
    source: website story was retrieved from, npr
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
            story_dict[c.STORY_SOURCE] = NPR
        else:
            logging.warning("NPR: Story missing some components, not added")
            continue

        if (has_all_components(story_dict)):
            story_list.append(story_dict)
        else:
            logging.warning("NPR: Story missing some components, not added")

    
    return story_list
