import requests
from bs4 import BeautifulSoup

r = requests.get("https://www.nbcnews.com/")
write_me = BeautifulSoup(r.text, 'html')
f = open("nbc_text.txt", "w")
#We will need to beautifulsoup this html and extract the titles + summaries since
#that's all they provide. No JSON or XML -- directly from website
f.write(write_me.prettify())
f.close()