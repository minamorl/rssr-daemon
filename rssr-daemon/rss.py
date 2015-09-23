import time
import feedparser
import requests


class ScheduledCrawler():

    def __init__(self, url=None, dbo=None, response=None):
        self.url = url
        self.dbo = dbo
        self.reposnse = None

    def fetch(self, retry=0, sleep=1000):
        for i in range(0, retry):
            self.response = requests.get(self.url)

            if self.response.status_code == 200:
                return

            time.sleep(1000)

        if self.response.status_code != 200:
            raise CrawlException()

    def format(self):
        pass

    def save(self):
        pass


class CrawlException(Exception):
    pass
