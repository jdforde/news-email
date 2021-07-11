import xml.etree.ElementTree as ET
import logging

import src.util.constants as c
from src.util.functions import send_request, has_all_components


"""
NYT has an xml file which corresponds to their current homepage. Section "channel/item" has all
of the stories. Using ElementTree, relevant values are extracted and put into story_dict.

    title: Title of article
    caption: NYT-given summary of article
    url: page url
    source: website story was retrieved from, nbc
"""

NYT_LINK = "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml"
NYT = 'nyt'
XML_STORY_STRUCTURE = "channel/item"
STORY_DESCRIPTION = "description"
LINK_PROPERTY = "link"


def scrape_nyt():
    logging.info("NYT:Starting web-scraping")
    story_list = []

    request = send_request(NYT_LINK, NYT)
    if request == None:
        logging.critical("NYT: Unable to request NYT site")

    root = ET.fromstring(request.text)
    stories = root.findall(XML_STORY_STRUCTURE)

    for item in stories:
        story_dict = {}

        story_dict[c.STORY_TITLE] = item.find(c.STORY_TITLE).text
        logging.info("NYT: Scraping article %s", story_dict[c.STORY_TITLE])
        story_dict[c.STORY_CAPTION] = item.find(STORY_DESCRIPTION).text
        story_dict[c.STORY_URL] = item.find(LINK_PROPERTY).text
        story_dict[c.STORY_SOURCE] = NYT

        if (has_all_components(story_dict)):
            story_list.append(story_dict)
        else:
            logging.warning("NYT: Story missing some components, not added")

    return story_list




