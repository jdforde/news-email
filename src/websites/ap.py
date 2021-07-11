from selenium import webdriver
from bs4 import BeautifulSoup
import logging

from src.util.functions import has_all_components, send_request
import src.util.constants as c

#TODO: Add error checking for driver. Maybe abstract to util? Also get rid of hanshake failed message
#TODO: Need to clean up scraping logic, there are some blank lines in logger + triple scrapes the title article

"""
AP news does not have json/xml file with stories. Instead, we have to scrape the homepage
directly with selenium. Most of the page content is loaded with JS, so we can't just use
requests. From this, we can grab all the URLs.

    title: Title of article
    caption: NPR-given summary of article
    url: page url
    source: website story was retrieved from, npr
"""

AP_LINK = "https://apnews.com/"
AP = "ap"
PATH_TO_CHROMEDRIVER = "C:\\Users\\Jakob\\Downloads\\chromedriver.exe"
ARTICLE = "/article/"
CAPTION_PROPERTY = "og:description"
CONTENT = "content"

def scrape_ap():
    story_list = []
    logging.info("AP:Starting web-scraping")
    opts = webdriver.ChromeOptions()
    opts.add_argument("--headless")

    driver = webdriver.Chrome(PATH_TO_CHROMEDRIVER, options=opts)
    driver.get(AP_LINK)
    soup = BeautifulSoup(driver.page_source, c.PARSER)
    driver.close()

    stories = []
    for link in soup.find_all(c.ANCHOR_TAG):
        if link.get(c.HREF_TAG).startswith(ARTICLE):
            stories.append(AP_LINK[:-1] + link.get(c.HREF_TAG))

    
    for story_url in stories:
        story_dict = {}
        story_request = send_request(story_url, AP)
        html_response = BeautifulSoup(story_request.text, c.PARSER)

        story_dict[c.STORY_TITLE] = html_response.title.string
        logging.info("AP: Scraping article %s", story_dict[c.STORY_TITLE])
        story_dict[c.STORY_CAPTION] = html_response.find(property=CAPTION_PROPERTY).get(CONTENT)
        story_dict[c.STORY_SOURCE] = AP
        story_dict[c.STORY_URL] = story_url


        if (has_all_components(story_dict)):
            story_list.append(story_dict)
        else:
           logging.warning("AP: Story missing some components, not added")
        
    return story_list
