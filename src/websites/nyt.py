import logging
from bs4 import BeautifulSoup
from datetime import date
import newspaper

import src.util.constants as c
from src.util.functions import send_request, has_all_components

"""
    title: Title of article
    caption: NYT-given summary of article
    url: page url
    source: website story was retrieved from, nyt
    image: url to story image, optional
    text: story text
"""

NYT_LINK = ["https://www.nytimes.com/section/us", "https://www.nytimes.com/section/politics"]
NYT_WEBSITE = "https://www.nytimes.com"
NYT = 'NYT'
TODAY = date.today()
INTERACTIVE = '/interactive/'

def scrape_nyt():
    stories = []
    story_list = []
    logging.info("Starting web-scraping")

    for site in NYT_LINK:
        request = send_request(site, NYT)
        if not request:
            logging.critical("Unable to request NYT site")
        
        regex = '/' + str(TODAY.year) + '/'
        soup = BeautifulSoup(request.text, c.PARSER)
        for link in soup.find_all(c.ANCHOR_TAG):
            if regex in link.get(c.HREF_TAG) and INTERACTIVE not in link.get(c.HREF_TAG) and NYT_WEBSITE + link.get(c.HREF_TAG) not in stories:
                stories.append(NYT_WEBSITE + link.get(c.HREF_TAG))
        
        for story_url in stories:
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
            story_dict[c.STORY_CAPTION] = html_response.find(property=c.CAPTION_PROPERTY).get(c.CONTENT_PROPERTY)

            if (has_all_components(story_dict)):
                story_list.append(story_dict)
            else:
                logging.warning("Story missing some components, not added")
                

    return story_list
