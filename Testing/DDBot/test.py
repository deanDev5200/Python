import requests
from lxml import etree
from bs4 import BeautifulSoup

URL = "https://www.kompas.com/tren"

HEADERS = ({'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
            (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',\
            'Accept-Language': 'en-US, en;q=0.5'})

webpage = requests.get(URL, headers=HEADERS)
soup = BeautifulSoup(webpage.content, "html.parser")
dom = etree.HTML(str(soup)) # type: ignore
respond = dom.xpath('/html/body/div[1]/div[1]/div[4]/div[3]/div[1]/div[1]/div[2]/div/div[3]/a/div[1]/img')[0]

print(respond.items()[0][1])