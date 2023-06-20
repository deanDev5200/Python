
from bs4 import BeautifulSoup
from lxml import etree
import requests
  
  
URL = "https://poltracking.com/rilis-temuan-survei-nasional-poltracking-indonesia-tendensi-peta-politik-pilpres-2024/"
  
HEADERS = ({'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
            (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',\
            'Accept-Language': 'en-US, en;q=0.5'})
  
webpage = requests.get(URL, headers=HEADERS)
soup = BeautifulSoup(webpage.content, "html.parser")
dom = etree.HTML(str(soup)) # type: ignore
print(dom.xpath('//*[@id="post-29188"]/div/div[3]/div[1]/p[2]/text()[2]'))