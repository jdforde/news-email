from bs4 import BeautifulSoup
import logging

from src.util.functions import send_request, has_all_components
import src.util.constants as c
"""
A simple request from Yahoo reveals some of the many articles on the website. Note that the order
of stories is not by importance, so there is no "headline" story
    title: Title of article
    caption: Yahoo-given summary of article
    url: page url
    source: website story was retrieved from, yahoo
"""
YAHOO_LINK = "https://news.yahoo.com/"
YAHOO = 'yahoo'
CAPTION_PROPERTY = "og:description"
CONTENT = "content"

def scrape_yahoo():
    logging.info("Starting web-scraping")
    story_list = []
    request = send_request(YAHOO_LINK, YAHOO)
    if not request:
        logging.critical("Unable to request Yahoo site")
        return
    
    stories = []
    soup = BeautifulSoup(request.text, c.PARSER)
    for link in soup.find_all(c.ANCHOR_TAG):
        if link.get(c.HREF_TAG).startswith('/') and link.get(c.HREF_TAG).endswith('.html'):
            stories.append(YAHOO_LINK[:-1] + link.get(c.HREF_TAG))
    
    for story in stories:
        if not story.startswith(YAHOO_LINK):
            logging.warning("Skipping story with incorrect URL: %s", story)
            continue
        story_dict = {}
        story_dict[c.STORY_URL] = story
        story_dict[c.STORY_SOURCE] = YAHOO
    
        story_request = send_request(story, YAHOO)
        if not story_request:
            logging.error("Unable to get response for story")
            continue
        html_response = BeautifulSoup(story_request.text, c.PARSER)


        story_dict[c.STORY_TITLE] = html_response.title.string
        logging.info("Scraping article %s", story_dict[c.STORY_TITLE])
        story_dict[c.STORY_CAPTION] = html_response.find(property=CAPTION_PROPERTY).get(CONTENT)

        if (has_all_components(story_dict)):
            story_list.append(story_dict)
        else:
            logging.warning("Story missing some components, not added")
    
    return story_list
