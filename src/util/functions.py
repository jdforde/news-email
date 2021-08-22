import requests
import logging
import json


import src.util.constants as c

def send_request(link, source):
    try:
        request = requests.get(link)

    except requests.exceptions.ConnectionError as e:
        logging.error("Connection error raised while trying to request %s: %s", source, e)
        return
    except requests.exceptions.HTTPError as e:
        logging.error("HTTP error has occured while trying to request %s: %s", source, e)
        return
    except requests.exceptions.Timeout as e:
        logging.error("Request to %s timed out: %s", source, e)
        return
    except requests.exceptions.TooManyRedirects as e:
        logging.error("Too many requests made to %s: %s", source, e)
        return
    except Exception as e:
        logging.error("Unknown exception occured while trying to access %s: %s", source, e)
        return
    
    return request

def has_all_components(story_dict):
    if not type(story_dict) is dict:
        return False

    components = [c.STORY_CAPTION, c.STORY_SOURCE, c.STORY_TEXT, c.STORY_TITLE, c.STORY_URL]
    if (all(x in list(story_dict.keys()) for x in components)):
        return True
    else:
        return False

def cache(all_stories, filename):
    with open(filename, "w") as f:
        json.dump(json.dumps(all_stories), f)


def read_cache(filename):
    try:
        with open(filename, "r") as f:
            all_list = json.load(f)
        return json.loads(all_list)
    except FileNotFoundError:
        logging.error("File %s cannot be found. No mockup will be used", filename)
        return []

def in_category(tag, CATEGORIES):
    for category in CATEGORIES:
        if category in tag:
            return True

    return False
