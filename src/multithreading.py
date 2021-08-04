from websites import *
from threading import Thread
import logging
import time

class ThreadWithResult(Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs={}, *, daemon=None):
        def function():
            self.result = target(*args, **kwargs)
        super().__init__(group=group, target=function, name=name, daemon=daemon)

start = time.time()
logger = logging.getLogger()
logger.propagate = False
logger.setLevel(logging.INFO) 

log = logging.StreamHandler()
formatter = logging.Formatter('%(levelname)s %(asctime)s : %(filename)s : %(funcName)s :: %(message)s', "%Y-%m-%d %H:%M:%S")
log.setFormatter(formatter)
logger.addHandler(log)
WEBSITES = [scrape_yahoo, scrape_npr, scrape_nbc, scrape_ap, scrape_propublica, scrape_slate, scrape_nyt]


threads = []
for website in WEBSITES:
    thr = ThreadWithResult(target=website)
    thr.start()
    threads.append(thr)


for thread in threads:
    thread.join()

print(time.time() - start)
    