import logging
from bs4 import BeautifulSoup
from datetime import date

import src.util.constants as c
from src.util.functions import send_request, has_all_components

"""
Would be nice to get rid of this at end of some articles:
Reporting was contributed by <!-- -->Eric Adelson<!-- --> from Lakeland, Fla.; <!-- -->Benjamin Guggenheim<!-- --> 
from Santa Monica, Calif.; <!-- -->Patricia Mazzei<!-- --> from Miami; Will Sennott from New Bedford, Mass.; and 
<!-- -->Deena Winter<!-- --> from St. Clou!-- -->Deena Winter<!-- --> from St. Cloud, Minn.
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

            story_request = send_request('https://www.nytimes.com/2021/08/16/us/covid-delta-variant-us.html', NYT)
            if not story_request:
                logging.error("Unable to get response for story")
                continue
            html_response = BeautifulSoup(story_request.text, c.PARSER)

            story_dict[c.STORY_TITLE] = html_response.title.string[:-21] #gets rid of - The New York Times
            logging.info("Scraping article %s", story_dict[c.STORY_TITLE])
            story_dict[c.STORY_CAPTION] = html_response.find(property=c.CAPTION_PROPERTY).get(c.CONTENT_PROPERTY)

            html_text= html_response.find("section", {"name":"articleBody"}).find_all(c.PARAGRAPH_TAG)
            text = ''.join([sentence.text for sentence in html_text])
            story_dict[c.STORY_TEXT] = text
            image = html_response.find(property=c.IMAGE_PROPERTY)
            if image:
                story_dict[c.STORY_IMAGE] = image.get(c.CONTENT_PROPERTY)
            if (has_all_components(story_dict)):
                story_list.append(story_dict)
            else:
                logging.warning("Story missing some components, not added")
                
    return story_list
