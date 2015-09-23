import time
import feedparser
import requests


def fetch(self, url, max_retry=0, sleep=1000):
    for i in range(0, max_retry):
        response = requests.get(url)

        if response.status_code == requests.codes.ok
            return response
        if i < max_retry:
            time.sleep(sleep)

    raise CrawlException()


def format(self, text):
    return feedparser.parse(text)


class CrawlException(Exception):
    pass