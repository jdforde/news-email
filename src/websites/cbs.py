from bs4 import BeautifulSoup
import logging

from src.util.functions import send_request, has_all_components
import src.util.constants as c
"""
    title: Title of article
    caption: CBS-given summary of article
    url: page url
    source: website story was retrieved from, cbs
"""
CBS_LINK = "https://www.cbsnews.com/"
CBS = 'cbs'
CAPTION_PROPERTY = "og:description"
TITLE_PROPERTY = "content__title"
CONTENT = "content"

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
        if "/news/" in link.get(c.HREF_TAG) and link.get(c.HREF_TAG) not in stories and "48-hours/" not in link.get(c.HREF_TAG):
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

   
        story_dict[c.STORY_TITLE] = html_response.find(class_=TITLE_PROPERTY).text
        logging.info("Scraping article %s", story_dict[c.STORY_TITLE])
        story_dict[c.STORY_CAPTION] = html_response.find(property=CAPTION_PROPERTY).get(CONTENT)
        if (has_all_components(story_dict)):
            story_list.append(story_dict)
        else:
            logging.warning("Story missing some components, not added")
    
    return story_list

if __name__ == '__main__':
    stories = scrape_cbs()
    for story in stories:
        print(story[c.STORY_TITLE])
