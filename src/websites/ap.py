from bs4 import BeautifulSoup
import logging

from src.util.functions import has_all_components, send_request
import src.util.constants as c
"""
Does not need article dependency
"""

AP_LINK = "https://apnews.com/"
AP = "Associated Press"
ARTICLE = "/article/"
AP_BLANK_IMAGE = "https://apnews.com/images/ShareLogo2.png"

def scrape_ap():
    stories = []
    story_list = []
    logging.info("Starting web-scraping")

    request = send_request(AP_LINK, AP)
    if not request:
        logging.critical("Unable to request AP site")
        return

    html_response = BeautifulSoup(request.text, c.PARSER)
    for link in html_response.find_all(c.ANCHOR_TAG):
        if link.get(c.HREF_TAG).startswith(ARTICLE) and AP_LINK[:-1] + link.get(c.HREF_TAG) not in stories:
            stories.append(AP_LINK[:-1] + link.get(c.HREF_TAG))
    
    for story_url in stories:
        story_dict = {}
        story_dict[c.STORY_URL] = story_url
        story_dict[c.STORY_SOURCE] = AP

        story_request = send_request(story_url, AP)
        if not story_request:
            logging.error("Unable to get response for story")
            continue
        
        html_response = BeautifulSoup(story_request.text, c.PARSER)
        story_dict[c.STORY_TITLE] = html_response.title.string
        logging.info("Scraping article %s", story_dict[c.STORY_TITLE])
       
        caption = html_response.find(property=c.CAPTION_PROPERTY).get(c.CONTENT_PROPERTY)
        if "(AP) —" in caption:
            story_dict[c.STORY_CAPTION] = caption[caption.index("(AP) —")+7:]
        else: 
            story_dict[c.STORY_CAPTION] = caption
       
        html_text = html_response.find(class_="Article").find_all(c.PARAGRAPH_TAG)
        text = ''.join([sentence.text for sentence in html_text])
        if "(AP) —" in text and "___" in text:
            text = text[text.index("(AP) —") + 7:text.index("___")]
        elif "(AP) —" in text:
            text = text[text.index("(AP) —") + 7:]
        elif "___" in text:
            text = text[:text.index("___")]

        story_dict[c.STORY_TEXT] = text

        image = html_response.find(property=c.IMAGE_PROPERTY).get(c.CONTENT_PROPERTY)
        if not image == AP_BLANK_IMAGE:
            story_dict[c.STORY_IMAGE] = image


        if (has_all_components(story_dict)):
            story_list.append(story_dict)
        else:
            logging.warning("Story missing some components, not added")

    return story_list
