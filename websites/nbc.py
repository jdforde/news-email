from newspaper import Article
from bs4 import BeautifulSoup
import logging
import util.constants as c
from util.functions import send_request, has_all_components

"""
Scrapes the front page of nbc and turns each article into an article dictionary, storing
it in a list. Each dictionary has key/value pairs:

    title: Title of article
    caption: NBC-given summary of article
    url: page url
    tags: newspaper-given tags
    source: website story was retrieved from, nbc
    img: header image, optional

NBC request gives the actual homepage as html file. Section STORY_CLASS has all relevant story
information. Relevant attributes need to be extracted via BeautifulSoup html parsing.
"""

NBC_LINK = "https://www.nbcnews.com/"
NBC = 'nbc'

STORY_CLASS = "alacarte__image-wrapper"
CAPTION_PROPERTY = "og:description"
IMAGE_PROPERTY = "og:image"
CONTENT = "content"

def scrape_nbc():
    logging.info("NBC:Starting web-scraping")
    story_list = []
    request = send_request(NBC_LINK, NBC)
    if request == None:
        logging.critical("NBC: Unable to request NBC site")
        return

    html_response = BeautifulSoup(request.text, c.PARSER)
    stories = html_response.find_all(class_=STORY_CLASS)

    for story in stories:
        story_dict = {}

        story_dict[c.STORY_URL] = story.find(c.ANCHOR_TAG).get(c.HREF_TAG)
        story_request = send_request(story_dict[c.STORY_URL], NBC)

        html_response = BeautifulSoup(story_request.text, c.PARSER)

        story_dict[c.STORY_TITLE] = html_response.title.string
        logging.info("NBC: Scraping article %s", story_dict[c.STORY_TITLE])
        story_dict[c.STORY_CAPTION] = (html_response.find(property=CAPTION_PROPERTY)).get(CONTENT)
        story_dict[c.STORY_IMG] = (html_response.find(property=IMAGE_PROPERTY).get(CONTENT))

        article = Article(story_dict[c.STORY_URL])
        article.build()

        story_dict[c.STORY_TAGS] = article.keywords
        story_dict[c.STORY_SOURCE] = NBC

        if (has_all_components(story_dict)):
            story_list.append(story_dict)
        else:
            logging.warning("NBC: Story missing some components, not added")
    
    return story_list
