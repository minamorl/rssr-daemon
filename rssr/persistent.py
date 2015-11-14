import redis
import pickle
import datetime
import feedparser
import datetime
from time import mktime
from rssr.utils import _logger
import redisorm.core
import redisorm.proxy
import sys

logger = _logger(__name__)


def get_redis():
    r = redis.StrictRedis(decode_responses=True)
    try:
        r.ping()
        return r
    except redis.exceptions.ConnectionError:
        print("Redis server is not available. Please confirm that redis-server are running.")
        sys.exit(1)



class Feed(redisorm.core.PersistentData):
    def __init__(self, id=None, url=None):
        self.id = id
        self.url = url

class FeedItem(redisorm.core.PersistentData):
    def __init__(self, id=None, feed=None, link=None, published=None, title=None, author=None, summary=None, content=None):
        self.id = id
        self.feed = redisorm.proxy.PersistentProxy(feed)
        self.link = link
        self.published = published
        self.title = title
        self.author = author
        self.summary = summary
        self.content = content

    @classmethod
    def create_from(cls, feed, item):
        obj = cls(feed=feed)
        obj.link = item.link
        obj.published = datetime.datetime.fromtimestamp(mktime(item.published_parsed)).strftime('%Y-%m-%d %H=%M=%S')
        obj.title = item.title
        obj.author = item.author
        obj.summary = item.summary
        if "content" in item:
            obj.content= item.content[0].value
        return obj

def save_parsed_value(url, data, r=get_redis()):
    p = redisorm.core.Persistent("rssr", r=r)
    d = feedparser.parse(data).entries

    feed = Feed(url)
    p.save(feed)
    for _item in d:
        item = FeedItem.create_from(feed, _item)
        p.save(item)


def save_raw_feed(data, fp):
    with fp:
        fp.write(data)
    logger.info("file {} was generated.".format(fp.name))


def get_url_lists(r=get_redis()):
    redis_key = "rssr:urls"
    return r.lrange(redis_key, 0, -1)
