from bs4 import BeautifulSoup
import logging

from src.util.functions import has_all_components, send_request, send_selenium_request
import src.util.constants as c

"""
AP news does not have json/xml file with stories. Instead, we have to scrape the homepage
directly with selenium. Most of the page content is loaded with JS, so we can't just use
requests. From this, we can grab all the URLs. The URLs are sometimes repeated more than once
so there needs to be a check for this.

    title: Title of article
    caption: NPR-given summary of article
    url: page url
    source: website story was retrieved from, npr
"""

AP_LINK = "https://apnews.com/"
AP = "ap"
ARTICLE = "/article/"
CAPTION_PROPERTY = "og:description"
CONTENT = "content"

def scrape_ap():
    story_list = []
    args = ['--ignore-certificate-errors-spki-list', '--ignore-certificate-errors', '--ignore-ssl-errors']
    page_source = send_selenium_request(AP_LINK, AP, args)
    if not page_source:
        logging.critical("Unable to request AP site")
        return
    soup = BeautifulSoup(page_source, c.PARSER)

    stories = []
    for link in soup.find_all(c.ANCHOR_TAG):
        if link.get(c.HREF_TAG).startswith(ARTICLE):
            stories.append(AP_LINK[:-1] + link.get(c.HREF_TAG))

    for story_url in stories:
        skip = False
        for story in story_list:
            if story[c.STORY_URL] == story_url:
                skip = True
                logging.info("Skipping repeated article.")

        if not skip:
            story_dict = {}
            story_request = send_request(story_url, AP)
            html_response = BeautifulSoup(story_request.text, c.PARSER)

            story_dict[c.STORY_TITLE] = html_response.title.string
            logging.info("Scraping article %s", story_dict[c.STORY_TITLE])
            story_dict[c.STORY_CAPTION] = html_response.find(property=CAPTION_PROPERTY).get(CONTENT)
            story_dict[c.STORY_SOURCE] = AP
            story_dict[c.STORY_URL] = story_url


            if (has_all_components(story_dict)):
                story_list.append(story_dict)
            else:
                logging.warning("Story missing some components, not added")
            
    return story_list
