import redis
import pickle
import datetime
import feedparser
import datetime
from time import mktime
from rssr.utils import _logger
import sys

logger = _logger(__name__)


def get_redis():
    r = redis.StrictRedis(decode_responses=True)
    try:
        check_radis_health(r)
        return r
    except redis.exceptions.ConnectionError:
        print("Redis server is not available. Please confirm that redis-server are running.")
        sys.exit(1)


def format(item):
    formatted = {
        "id": item.id,
        "link": item.link,
        "published": datetime.datetime.fromtimestamp(mktime(item.published_parsed)).strftime('%Y-%m-%d %H:%M:%S'),
        "title": item.title,
        "author": item.author,
        "summary": item.summary, }
    if "content" in item:
        formatted.update({"content": item.content[0].value})

    return formatted


def save_parsed_value(url, data, redis_key=None):
    r = get_redis()

    d = feedparser.parse(data).entries
    for item in d:
        redis_key = "rssr:feed:{feed_url}:{item}".format(feed_url=url, item=item.link)
        formatted = format(item)
        r.hmset(redis_key, formatted)


def save_raw_feed(data, fp):
    with fp:
        fp.write(data)
    logger.info("file {} was generated.".format(fp.name))


def get_url_lists():
    r = get_redis()
    redis_key = "rssr:urls"
    return r.lrange(redis_key, 0, -1)


def check_radis_health(r):
    return r.ping()
