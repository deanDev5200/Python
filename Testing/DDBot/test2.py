
import requests, lxml
from bs4 import BeautifulSoup

headers = {
  'User-agent':
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582'
}

params = {
    'q': 'luke skywalker lightsaber color',
    'gl': 'us'
}

def get_organic_result_answerbox():
  html = requests.get('https://www.google.com/search', headers=headers, params=params)
  soup = BeautifulSoup(html.text, 'lxml')

  answer = soup.select_one('.XcVN5d').text
  title = soup.select_one('.DKV0Md').text
  link = soup.select_one('.yuRUbf a')['href']
  snippet = soup.select_one('.hgKElc').text
  print(f"{answer}\n{title}\n{link}\n{snippet}")

get_organic_result_answerbox()