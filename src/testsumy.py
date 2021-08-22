from sumy.nlp.tokenizers import Tokenizer
from sumy.parsers.plaintext import PlaintextParser
from sumy.summarizers.text_rank import TextRankSummarizer
from src.util.functions import read_cache
import src.util.constants as c
import re
"""
Make usre to copy over code from mockup_generator
Look at latest email to see what the issue is
Not sure why we're lowercasing
Extra bonus bullet points :)

https://stackoverflow.com/questions/11475885/python-replace-regex/11475905
try replacing with something and thdfasdf35

"""
tr_summarizer = TextRankSummarizer()
SUMMARY_MAX_LENGTH = 40
mockup = read_cache("mockup.txt")
TOKENIZER = Tokenizer("english")
for story in mockup:
    parser = PlaintextParser.from_string(story[c.STORY_TEXT], TOKENIZER)
    summary = tr_summarizer(parser.document, 3)
    summary_list = [str(sentence) for sentence in summary if len(str(sentence).split()) < SUMMARY_MAX_LENGTH]

    if not summary_list:
        #logging.warning("Sumy summary is too long. Taking 1 sumy point and turning it into several bullet points")
        summary = tr_summarizer(parser.document, 1)
        summary_list = re.sub(r'([a-z]{4,}\.((’|”)*)?)', r'\1**|**', str(summary[0]))
        summary_list = list(filter(None, summary_list.split("**|**")))
        print(summary_list)


    
    story[c.STORY_SUMMARY] = summary_list

