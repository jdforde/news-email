import requests
import logging

def send_request(link, source):
    try:
        request = requests.get(link)

    except requests.exceptions.ConnectionError as e:
        logging.error("ERROR: Connection error raised while trying to request %s: %s", source, e)
        return
    except requests.exceptions.HTTPError as e:
        logging.error("ERROR: HTTP error has occured while trying to request %s: %s", source, e)
        return
    except requests.exceptions.Timeout as e:
        logging.error("ERORR: Request to %s timed out: %s", source, e)
        return
    except requests.exceptions.TooManyRedirects as e:
        logging.error("ERROR: Too many requests made to %s: %s", source, e)
        return
    except Exception as e:
        logging.error("ERROR: Unknown exception occured while trying to access %s: %s", source, e)
        return
    
    return request