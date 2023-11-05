import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11.6; rv:51.0.1) Gecko/20100101 Firefox/51.0.1',
    'Content-Type': 'charset=UTF-8',
      }


def get_holidays():
    r = requests.get('https://kakoysegodnyaprazdnik.ru/', headers=headers)
    r.encoding = 'utf8'
    soup = BeautifulSoup(r.text, 'lxml')
    listing = soup.find('div', class_='listing_wr')
    holidays = []
    for day in listing.find_all('span', itemprop='text')[:5]:
        holidays.append(day.getText())
    print("good_job")
    return holidays
