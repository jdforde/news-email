from newspaper import Article
import xml.etree.ElementTree as ET
import logging
import util.constants as c
from util.functions import send_request, has_all_components


"""
Scrapes the front page of NYT and turns each article into an article dictionary, storing
it in a list. Each dictionary has key/value pairs:

    title: Title of article
    caption: NYT-given summary of article
    url: page url
    tags: newspaper-given tags
    source: website story was retrieved from, nbc
    img: header image, optional

NYT has an xml file which corresponds to their current homepage. Section "channel/item" has all
of the stories. Using ElementTree, relevant values are extracted and put into story_dict.
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

        article = Article(story_dict[c.STORY_URL])
        article.build()
        
        story_dict[c.STORY_TAGS] = article.keywords
        story_dict[c.STORY_SOURCE] = NYT

        for component in item:
            if c.STORY_URL in component.keys():
                story_dict[c.STORY_IMG] = component.attrib[c.STORY_URL]

        if (has_all_components(story_dict)):
            story_list.append(story_dict)
        else:
            logging.warning("NYT: Story missing some components, not added")

    return story_list




