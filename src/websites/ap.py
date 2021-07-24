from bs4 import BeautifulSoup
import logging

from src.util.functions import has_all_components, send_request
import src.util.constants as c

"""
    title: Title of article
    caption: AP-given summary of article
    url: page url
    source: website story was retrieved from, ap
"""

AP_LINK = "https://apnews.com/"
AP = "ap"
ARTICLE = "/article/"

def scrape_ap():
    stories = []
    story_list = []
    logging.info("Starting web-scraping")

    request = send_request(AP_LINK, AP)
    if not request:
        logging.critical("Unable to request AP site")
        return

    html_response = BeautifulSoup(request.text, c.PARSER)
    for link in html_response.find_all(c.ANCHOR_TAG):
        if link.get(c.HREF_TAG).startswith(ARTICLE) and AP_LINK[:-1] + link.get(c.HREF_TAG) not in stories:
            stories.append(AP_LINK[:-1] + link.get(c.HREF_TAG))
    
    for story_url in stories:
        story_dict = {}
        story_dict[c.STORY_URL] = story_url
        story_dict[c.STORY_SOURCE] = AP

        story_request = send_request(story_url, AP)
        if not story_request:
            logging.error("Unable to get response for story")
            continue
        
        html_response = BeautifulSoup(story_request.text, c.PARSER)
        story_dict[c.STORY_TITLE] = html_response.title.string
        logging.info("Scraping article %s", story_dict[c.STORY_TITLE])
        story_dict[c.STORY_CAPTION] = html_response.find(property=c.CAPTION_PROPERTY).get(c.CONTENT_PROPERTY)
        
        if (has_all_components(story_dict)):
            story_list.append(story_dict)
        else:
            logging.warning("Story missing some components, not added")

    return story_list
