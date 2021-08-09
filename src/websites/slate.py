from bs4 import BeautifulSoup
import logging

from src.util.functions import send_request, has_all_components
import src.util.constants as c
"""
    title: Title of article
    caption: Slate-given summary of article
    url: page url
    source: website story was retrieved from, slate
"""
SLATE_LINKS = ["https://slate.com/news-and-politics", "https://slate.com/business"]
SLATE = 'Slate'
CAPTION_PROPERTY = "og:description"
CONTENT = "content"
PODCAST = "/podcasts/"

def scrape_slate():
    logging.info("Starting web-scraping")
    stories = []
    story_list = []
    for slate_link in SLATE_LINKS:
        request = send_request(slate_link, SLATE)
        if not request:
            logging.critical("Unable to request slate site")
            continue
        
        html_response = BeautifulSoup(request.text, c.PARSER)
        for link in html_response.find_all(c.ANCHOR_TAG, class_="topic-story"):
            if not PODCAST in link.get(c.HREF_TAG):
                stories.append(link.get(c.HREF_TAG))

        for story in stories:
            story_dict = {}
            story_dict[c.STORY_URL] = story
            story_dict[c.STORY_SOURCE] = SLATE
        
            story_request = send_request(story, SLATE)
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
