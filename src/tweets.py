
from bs4 import BeautifulSoup
import requests

URL = 'https://twitter.com/search'


def get_html(q):
    params = {
        'lang': 'en',
        'q': q
    }
    response = requests.get(URL, params=params, timeout=3, verify=False)
    return response.text


def get_nodes(html):
    soup = BeautifulSoup(html, 'html.parser')
    return soup.find_all('p', class_='tweet-text')


def get_tweets(q):
    return [
        node.text
        for node in get_nodes(get_html(q))
    ]


if __name__ == '__main__':
    print get_tweets('bbc')
