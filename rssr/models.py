import redis
import pickle
import datetime
import feedparser
import datetime
from time import mktime
from rssr.utils import _logger
from redisorm.core import Column, PersistentData
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


class Feed(PersistentData):

    id = Column()
    url = Column()
    fulltext = Column()


class FeedItem(PersistentData):

    id = Column()
    feed = Column(redisorm.proxy.PersistentProxy)
    link = Column()
    published = Column()
    title = Column()
    author = Column()
    summary = Column()
    content = Column()

    @classmethod
    def create_from(cls, feed, item):
        obj = cls(feed=feed)
        obj.link = item.get("link")
        if item.get("published_parsed", None) is not None:
            obj.published = datetime.datetime.fromtimestamp(mktime(item.published_parsed)).strftime('%Y-%m-%d %H=%M=%S')
        obj.title = item.get("title")
        obj.author = item.get("author")
        obj.summary = item.get("summary")
        if "content" in item:
            obj.content = item.content[0].value
        return obj


def save(url, data, r=get_redis()):
    p = redisorm.core.Persistent("rssr", r=r)
    entries = feedparser.parse(data).entries

    feed = p.find(Feed, lambda feed: feed.url == url)
    if feed is None:
        feed = Feed(url=url ,fulltext=data)
        p.save(feed)
    for _item in entries:
        item = p.find(FeedItem, lambda feed: feed.link == _item.get("link"))
        if item is None:
            item = FeedItem.create_from(feed, _item)
            p.save(item)


def get_url_lists(r=get_redis()):
    redis_key = "rssr:urls"
    return r.lrange(redis_key, 0, -1)
