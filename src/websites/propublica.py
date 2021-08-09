from bs4 import BeautifulSoup
import logging

from src.util.functions import send_request, has_all_components
import src.util.constants as c

"""
    title: Title of article
    caption: Propublica-given summary of article
    url: page url
    source: website story was retrieved from, Propublica
"""
PROPUBLICA_LINK = "https://www.propublica.org/"
PROPUBLICA = 'ProPublica'
ARTICLE_ROUTE = "/article/"
H2 = 'h2'

def scrape_propublica():
    stories = []
    story_list = []
    request = send_request(PROPUBLICA_LINK, PROPUBLICA)
    soup = BeautifulSoup(request.text, c.PARSER)
    for link in soup.find_all(c.ANCHOR_TAG):
        if link.get(c.HREF_TAG).startswith(PROPUBLICA_LINK[0:-1] + ARTICLE_ROUTE) and link.get(c.HREF_TAG) not in stories:
            stories.append(link.get(c.HREF_TAG))

    for story in stories:
        if not story.startswith(PROPUBLICA_LINK):
            logging.warning("Skipping story with incorrect URL: %s", story)
            continue

        story_dict = {}
        story_dict[c.STORY_URL] = story
        story_dict[c.STORY_SOURCE] = PROPUBLICA

        story_request = send_request(story, PROPUBLICA)
        if not story_request:
            logging.error("Unable to get response for story")
            continue
        html_response = BeautifulSoup(story_request.text, c.PARSER)

        story_dict[c.STORY_TITLE] = html_response.title.string[:-13] #gets rid of " - ProPublica"
        logging.info("Scraping article %s", story_dict[c.STORY_TITLE])
        story_dict[c.STORY_CAPTION] = html_response.find(H2).text.lstrip().rstrip()

        if (has_all_components(story_dict)):
            story_list.append(story_dict)
        else:
            logging.warning("Story missing some components, not added")

    return story_list