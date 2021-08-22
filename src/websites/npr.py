from bs4 import BeautifulSoup
from datetime import date
import logging

import src.util.constants as c
from src.util.functions import send_request, has_all_components
"""
There might be an issue with NPR text, but this would be quite difficult to fix
"""

NPR_LINK = "https://www.npr.org/"
NPR = "NPR"
FEEDS_REGEX = "https://feeds.npr.org/feeds/100[0-9]/feed.json"
TODAY = date.today()
ITEMS = "items"
VIDEO_ARTICLE = "VIDEO"
STORY_SUMMARY = "summary"

def scrape_npr():
    stories = []
    story_list = []
    requests = send_request(NPR_LINK, NPR)
    soup = BeautifulSoup(requests.text, c.PARSER)
    for link in soup.find_all(c.ANCHOR_TAG):
        if (link.get(c.HREF_TAG) 
        and link.get(c.HREF_TAG).startswith(NPR_LINK + str(TODAY.year)) 
        and link.get(c.HREF_TAG) not in stories):
            stories.append(link.get(c.HREF_TAG))
    
    for story_url in stories:
        story_dict = {}
        story_dict[c.STORY_URL] = story_url
        story_dict[c.STORY_SOURCE] = NPR

        story_request = send_request(story_url, NPR)
        if not story_request:
            logging.error("Unable to get response for story")
            continue
        html_response = BeautifulSoup(story_request.text, c.PARSER)

        story_dict[c.STORY_TITLE] = html_response.title.string[:-6] #gets rid of  : NPR at the end
        logging.info("Scraping article %s", story_dict[c.STORY_TITLE])

        story_dict[c.STORY_CAPTION] = html_response.find(property=c.CAPTION_PROPERTY).get(c.CONTENT_PROPERTY)
        image = html_response.find(property=c.IMAGE_PROPERTY)

        if image:
            story_dict[c.STORY_IMAGE] = image.get(c.CONTENT_PROPERTY)

        if not html_response.find(id="storytext"):
            logging.warning("Unable to find article text for %s", story_url)
            continue

        html_text= html_response.find(id="storytext").find_all(c.PARAGRAPH_TAG, class_="")
        text = ''.join([sentence.text for sentence in html_text if "Getty Images" not in sentence.text and "/AP" not in sentence.text and not "WireImage" in sentence.text])
        story_dict[c.STORY_TEXT] = text.replace('\n', '')

        if (has_all_components(story_dict)):
            story_list.append(story_dict)
        else:
            logging.warning("Story missing some components, not added")

    return story_list
