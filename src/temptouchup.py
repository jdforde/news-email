from src.util.functions import read_cache
import src.util.constants as c
import tensorflow_hub as hub
import numpy as np
import re

SIMILARITY_CONSTANT = .2
MOCKUP_LEN = 14
UNDER_THRESHOLD = .25 #ie no website can be more than x of the mockup, change with number of stories
IMPORTANT_NAMES = ["pelosi", "trump", "kavanaugh"] #perhaps we can have a list of these and dynamically add to them or use a dataset
#combine three functions into one and then implement into mockup 

module_url = "https://tfhub.dev/google/universal-sentence-encoder/4"
model = hub.load(module_url)


def embed(input):
    return model(input)


def conflict(mockup, toadd):
    toadd_embed = embed([toadd[c.STORY_TITLE]])
    story_count = 1
    names_to_add = []
    for story in mockup:
        story_embed = embed([story[c.STORY_TITLE]])
        if (np.inner(toadd_embed, story_embed > SIMILARITY_CONSTANT)):
            return True
        
        if story[c.STORY_SOURCE] == toadd[c.STORY_SOURCE]:
            story_count+=1
    
    
#this is nice but has issues. Consider a story about Jill Biden being more popular than a Biden story
#thus, the Biden story would not get added
    for name in IMPORTANT_NAMES:
        if name.isupper() and re.search(name, toadd[c.STORY_TITLE], re.IGNORECASE):
            IMPORTANT_NAMES.extend(names_to_add)
            return True
        
        if name.islower() and re.search(name, toadd[c.STORY_TITLE], re.IGNORECASE):
            IMPORTANT_NAMES.remove(name)
            names_to_add.append(name.upper())
    
    IMPORTANT_NAMES.extend(names_to_add)
    return ((story_count)/MOCKUP_LEN) > UNDER_THRESHOLD
     



all_stories = read_cache("allstories.txt")
sorted_stories = sorted(all_stories, key = lambda i: i[c.STORY_SCORE], reverse=True)

mockup2 = []
for story in sorted_stories:
    if not(conflict(mockup2, story)):
        mockup2.append(story)
    
    if (len(mockup2) == 16):
        break
# for story in mockup1:
#     print(story[c.STORY_TITLE])

# print("\n\n\n")
# for story in mockup2:
#     print(story[c.STORY_TITLE])