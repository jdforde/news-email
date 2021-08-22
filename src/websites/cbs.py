from bs4 import BeautifulSoup
import logging

from src.util.functions import send_request, has_all_components
import src.util.constants as c
"""
This type of story might have issues: https://www.cbsnews.com/news/this-week-on-sunday-morning-at-home-august-22-2021/
"""
CBS_LINK = "https://www.cbsnews.com/"
CBS = 'CBS'
CAPTION_PROPERTY = "og:description"
TITLE_PROPERTY = "content__title"

def scrape_cbs():
    logging.info("Starting web-scraping")
    story_list = []
    request = send_request(CBS_LINK, CBS)
    if not request:
        logging.critical("Unable to request CBS site")
        return
    
    stories = []
    soup = BeautifulSoup(request.text, c.PARSER)
    for link in soup.find_all(class_="item__anchor"):
        if "/news/" in link.get(c.HREF_TAG) and link.get(c.HREF_TAG) not in stories:
            stories.append(link.get(c.HREF_TAG))

    for story in stories:
        if not story.startswith(CBS_LINK):
            logging.warning("Skipping story with incorrect URL: %s", story)
            continue
        story_dict = {}
        story_dict[c.STORY_URL] = story
        story_dict[c.STORY_SOURCE] = CBS
    
        story_request = send_request(story, CBS)
        if not story_request:
            logging.error("Unable to get response for story")
            continue
        html_response = BeautifulSoup(story_request.text, c.PARSER)

        if (html_response.find(class_=TITLE_PROPERTY)):
            story_dict[c.STORY_TITLE] = html_response.find(class_=TITLE_PROPERTY).text
        else:
            logging.warning("Unable to scrape article %s", story)
            continue
        logging.info("Scraping article %s", story_dict[c.STORY_TITLE])

        if not html_response.find(class_="content__body"):
            logging.warning("Unable to find article text for %s", story)
            continue
        
        html_text= html_response.find(class_="content__body").find_all(c.PARAGRAPH_TAG)
        text = ''.join([sentence.text for sentence in html_text])
        story_dict[c.STORY_TEXT] = text

        image = html_response.find(property=c.IMAGE_PROPERTY)
        if image:
            story_dict[c.STORY_IMAGE] = image.get(c.CONTENT_PROPERTY)
        story_dict[c.STORY_CAPTION] = html_response.find(property=CAPTION_PROPERTY).get(c.CONTENT_PROPERTY)
        if (has_all_components(story_dict)):
            story_list.append(story_dict)
        else:
            logging.warning("Story missing some components, not added")
    
    return story_list
