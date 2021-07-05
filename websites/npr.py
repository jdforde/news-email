from newspaper import Article
import requests
import re
import json
import logging

#comb through sumy and newspape to make sure no cool features were missed
#look into what TR summarizer does, and if there is a better one

"""
Scrapes the front page of NPR and turns each article into an article dictionary, storing
it in a list. Each dictionary has key/value pairs:

    title: Title of article
    caption: NPR-given summary of article
    url: page url
    tags: NPR-given tags + newspaper-given tags
    source: website story was retrieved from, npr
    img: header image, optional
"""

NPR_LINK = "https://www.npr.org/"
FEEDS_REGEX = "https://feeds.npr.org/feeds/100[0-9]/feed.json" #this is a guess

ITEMS = "items"
VIDEO_ARTICLE = "VIDEO"

STORY_URL = "url"
STORY_TITLE = "title"
STORY_SUMMARY = "summary"
STORY_TAGS = "tags"
STORY_SOURCE = "npr"

WORDS_PER_BULLET = 400 #Could probably use some fine tuning, maybe isn't linear

def scrape_npr():
    logging.info("NPR:Starting web-scraping")
    try:
        npr_request = requests.get(NPR_LINK)
        np_result = re.search(FEEDS_REGEX, npr_request.text)
        json_request = requests.get(np_result.group(0))

    except requests.exceptions.ConnectionError as e:
        logging.error("ERROR: Connection error raised while trying to request NPR: %s", e)
        return
    except requests.exceptions.HTTPError as e:
        logging.error("ERROR: HTTP error has occured while trying to request NPR: %s", e)
        return
    except requests.exceptions.Timeout as e:
        logging.error("ERORR: Request to NPR timed out: %s", e)
        return
    except requests.exceptions.TooManyRedirects as e:
        logging.error("ERROR: Too many requests made to NPR: %s", e)
        return
    except Exception as e:
        logging.error("ERROR: Unknown exception occured while trying to access NPR: %s", e)
        return

    stories = json.loads(json_request.text).get(ITEMS)

    story_list = []

    for story in stories:
        if VIDEO_ARTICLE in story[STORY_TITLE]:
            logging.info("NPR: Skipping video article")
            continue

        story_dict = {}
        if ({STORY_TITLE, STORY_SUMMARY, STORY_URL} <= story.keys()):
            logging.info("NPR: Scraping article %s", story[STORY_TITLE])
            story_dict['title'] = story[STORY_TITLE]
            story_dict['caption'] = story[STORY_SUMMARY]
            story_dict['url'] = story[STORY_URL]
        else:
            logging.warning("NPR: Story missing title, caption, or url. Skipping")
            continue

        try: 
            article = Article(story[STORY_URL])
            article.build()

        except Article.ArticleException as e: 
            logging.error("NPR: Error in trying to create Article for story %s:\n%s", story[STORY_TITLE], e)
            continue

        tags = []
        if STORY_TAGS in story.keys():
            tags.extend(story[STORY_TAGS])
        tags.extend(article.keywords)
        story_dict['tags'] = tags

        story_dict['source'] = STORY_SOURCE
        if (article.has_top_image):
            story_dict['img'] = article.top_image

        story_list.append(story_dict)

    
    return story_list
