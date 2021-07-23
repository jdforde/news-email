import xml.etree.ElementTree as ET
import logging
from bs4 import BeautifulSoup
from datetime import date

import src.util.constants as c
from src.util.functions import send_request, has_all_components


"""
A simple request to NYT reveals some of the many articles on the website.

    title: Title of article
    caption: NYT-given summary of article
    url: page url
    source: website story was retrieved from, nbc
"""

NYT_LINK = "https://www.nytimes.com/"
CATEGORIES = ["/opinion/", "/sports/", "/arts/"]
NYT = 'nyt'
DESCRIPTION = "og:description"
CONTENT = "content"
TODAY = date.today()

def in_category(tag):
    for category in CATEGORIES:
        if category in tag:
            return True

    return False

def scrape_nyt():
    stories = []
    story_list = []
    logging.info("Starting web-scraping")

    regex = NYT_LINK + str(TODAY.year) + "/" + "{:02}".format(TODAY.month) + "/" + "{:02}".format(TODAY.day) 

    request = send_request(NYT_LINK, NYT)
    if not request:
        logging.critical("Unable to request NYT site")
    
    soup = BeautifulSoup(request.text, c.PARSER)
    for link in soup.find_all(c.ANCHOR_TAG):
        if link.get(c.HREF_TAG).startswith(regex) and not in_category(link.get(c.HREF_TAG)) and link.get(c.HREF_TAG) not in stories:
            stories.append(link.get(c.HREF_TAG))
    
    for story_url in stories:
        if not story_url.startswith(NYT_LINK):
            logging.warning("Skipping story with incorrect URL: %s", story_url)
            continue

        story_dict = {}
        story_dict[c.STORY_URL] = story_url
        story_dict[c.STORY_SOURCE] = NYT

        story_request = send_request(story_url, NYT)
        if not story_request:
            logging.error("Unable to get response for story")
            continue
        html_response = BeautifulSoup(story_request.text, c.PARSER)

        story_dict[c.STORY_TITLE] = html_response.title.string[:-21] #gets rid of - The New York Times
        logging.info("Scraping article %s", story_dict[c.STORY_TITLE])
        story_dict[c.STORY_CAPTION] = html_response.find(property=DESCRIPTION).get(CONTENT)

        if (has_all_components(story_dict)):
            story_list.append(story_dict)
        else:
            logging.warning("Story missing some components, not added")
            

    return story_list
