import redis
import pickle
import datetime
import feedparser
from rssr.utils import _logger

logger = _logger(__name__)


def save_parsed_value(url, data, redis_key=None):
    r = redis.StrictRedis()
    
    d = feedparser.parse(data).entries
    for item in d:
        redis_key = redis_key or "rssr:feed:{feed_url}:{item}".format(feed_url=url, item=item.link )
        print(item)
        r.hmset(redis_key, item) 


def save_raw_feed(data, fp):
    with fp:
        fp.write(data)
    logger.info("file {} was generated.".format(fp.name))


def get_url_lists(redis_key=None):
    r = redis.StrictRedis(decode_responses=True)
    redis_key = redis_key or "rssr:urls"
    return r.lrange(redis_key, 0, -1)

