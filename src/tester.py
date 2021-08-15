import os
import src.util.constants as c
from pathlib import Path


with open(c.CACHED_STORIES, "r") as f:
    stories = f.read().split('\n')
with open(c.CACHED_STORIES, "w") as f:
    if len(stories) > 10:
        f.write('\n'.join(stories[-11:]))
    else:
        print('error')
