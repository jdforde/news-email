from bs4 import BeautifulSoup
import logging

from src.util.functions import send_request, has_all_components
import src.util.constants as c
"""
    title: Title of article
    caption: Yahoo-given summary of article
    url: page url
    source: website story was retrieved from, yahoo

    A yahoo caption miss, it took too much:
    An upset in Ohio on Tuesday night is giving moderate, Biden-aligned Democrats momentum vs. the party's vocal left ahead of next year's midterms. 
    Driving the news: In a special primary for U.S. House in the Cleveland area, Cuyahoga County Council member Shontel Brown pulled out a surprise victory for the Democratic 
    establishment in Cleveland.Get market news worthy of your time with Axios Markets. Subscribe for free.The left's stars had come out for her leading opponent, progressive Nina Turner: F 
    https://news.yahoo.com/ohios-nina-turner-upset-flashes-113420698.html
"""
YAHOO_LINK = "https://news.yahoo.com/"
YAHOO = 'yahoo'
CAPTION_PROPERTY = "og:description"
CONTENT = "content"

def scrape_yahoo():
    logging.info("Starting web-scraping")
    story_list = []
    request = send_request(YAHOO_LINK, YAHOO)
    if not request:
        logging.critical("Unable to request Yahoo site")
        return
    
    stories = []
    soup = BeautifulSoup(request.text, c.PARSER)
    for link in soup.find_all(c.ANCHOR_TAG):
        if link.get(c.HREF_TAG).startswith('/') and link.get(c.HREF_TAG).endswith('.html'):
            stories.append(YAHOO_LINK[:-1] + link.get(c.HREF_TAG))
    
    for story in stories:
        if not story.startswith(YAHOO_LINK):
            logging.warning("Skipping story with incorrect URL: %s", story)
            continue
        story_dict = {}
        story_dict[c.STORY_URL] = story
        story_dict[c.STORY_SOURCE] = YAHOO
    
        story_request = send_request(story, YAHOO)
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
