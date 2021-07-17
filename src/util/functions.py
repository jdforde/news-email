from selenium import webdriver
from selenium.common import exceptions
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
def send_selenium_request(link, source, options=''):
    opts = webdriver.ChromeOptions()
    opts.add_argument("--headless")
    if options:
        for arg in options:
            opts.add_argument(arg)
    
    try:
        driver = webdriver.Chrome(c.PATH_TO_CHROMEDRIVER, options=opts)
        driver.get(link)
        response = driver.page_source
        driver.quit()
    except exceptions.WebDriverException as e:
        logging.error("Web driver error occured to %s: %s", source, e)
        return
    except exceptions.ErrorInResponseException as e:
        logging.error("Some error in response from %s: %s", source, e)
        return
    except exceptions.InvalidSessionIdException as e:
        logging.error("Invalid session id for %s: %s", source, e)
        return
    except exceptions.TimeoutException as e:
        logging.error("Website %s did not return a response in requested time: %s", source, e)
        return
    
    return response

def has_all_components(story_dict):
    if (story_dict[c.STORY_URL] and story_dict[c.STORY_TITLE] and story_dict[c.STORY_CAPTION] and story_dict[c.STORY_SOURCE]):
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
        logging.error("File \"all_stories\" cannot be found")
        return []
