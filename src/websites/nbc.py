from bs4 import BeautifulSoup
import logging
import re

import src.util.constants as c
from src.util.functions import send_request, has_all_components, in_category

NBC_LINK = "https://www.nbcnews.com/"
CATEGORIES = ["/sports/", "/pop-culture/", "/science/", "/opinion/", "/video/", "/shopping/", "/slideshow/", "/specials/"]
STORY_CLASS = "layout-container zone-a-margin lead-type--threeUp"
REGEX = "-.*[1-9]+$"
NBC = 'NBC'
AFFILIATES = "-affiliates-"

def scrape_nbc():
    stories = []
    story_list = []
    logging.info("Starting web-scraping")
    
    request = send_request(NBC_LINK, NBC)
    if not request:
        logging.critical("Unable to request NBC site")
        return

    html_response = BeautifulSoup(request.text, c.PARSER)
    for link in html_response.find_all(c.ANCHOR_TAG):
        if link.get(c.HREF_TAG).startswith(NBC_LINK) and not in_category(link.get(c.HREF_TAG), CATEGORIES):
            if re.search(REGEX, link.get(c.HREF_TAG)) and link.get(c.HREF_TAG) not in stories:
                stories.append(link.get(c.HREF_TAG))
    
    for story_url in stories:
        if AFFILIATES in story_url:
            logging.info("Skipping affiliates page")
            continue

        story_dict = {}
        story_dict[c.STORY_URL] = story_url
        story_dict[c.STORY_SOURCE] = NBC    

        story_request = send_request(story_url, NBC)
        if not story_request:
            logging.error("Unable to get response for story")
            continue
        
        html_response = BeautifulSoup(story_request.text, c.PARSER)
        story_dict[c.STORY_TITLE] = html_response.title.string
        logging.info("Scraping article %s", story_dict[c.STORY_TITLE])
        if ("<p>" not in html_response.find(property=c.CAPTION_PROPERTY).get(c.CONTENT_PROPERTY)):
            story_dict[c.STORY_CAPTION] = html_response.find(property=c.CAPTION_PROPERTY).get(c.CONTENT_PROPERTY)
        else:
            logging.warning("Story is malformed, skipping %s", story_url)
            continue
            
        if not html_response.find(class_="article-body__content"):
            logging.warning("Unable to find article text for %s", story_url)
            continue
        
        html_text = html_response.find(class_="article-body__content").find_all(c.PARAGRAPH_TAG, class_="")
        text = ''.join([sentence.text for sentence in html_text]).replace("Download the NBC News app for breaking news and politics", "")
        story_dict[c.STORY_TEXT] = text

        image = html_response.find(property=c.IMAGE_PROPERTY)
        if image:
            story_dict[c.STORY_IMAGE] = image.get(c.CONTENT_PROPERTY)
        
        if (has_all_components(story_dict)):
            story_list.append(story_dict)
        else:
            logging.warning("Story missing some components, not added")

    return story_list
