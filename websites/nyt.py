import requests
from newspaper import Article
import re
import xml.etree.ElementTree as ET

from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer


#Add how long the scrape takes to each news website thing logger
#Clean up code, extract constants
#Add logger capabilities
#The search for image url is slow, try to clean it up 
url = "https://www.nytimes.com/"
request = requests.get("https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml")

WORDS_PER_BULLET = 400 
tr_summarizer = TextRankSummarizer()
def get_len_summary(article_text):
    num_words = len(re.findall(r'\w+', article_text))
    len_summary = round(num_words/WORDS_PER_BULLET)
    if (len_summary == 0):
        len_summary = 1
    return len_summary

root = ET.fromstring(request.text)
story_list = []
for item in root.findall("channel/item"):

    story_dict = {}

    story_dict['title'] = item.find('title').text
    story_dict['caption'] = item.find('description').text
    story_dict['url'] = item.find('link').text

    article = Article(story_dict['url'])
    article.build()
    
    parser = PlaintextParser.from_string(article.text, Tokenizer("english"))
    story_dict['summary'] = tr_summarizer(parser.document, get_len_summary(article.text))
    story_dict['tags'] = article.keywords
    story_dict['source'] = 'nyt'

    for component in item:
        if 'url' in component.keys():
            story_dict['img'] = component.attrib['url']

    story_list.append(story_dict)

for item in story_list:
    print(item)




