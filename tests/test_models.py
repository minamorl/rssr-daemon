from rssr.models import FeedItem, Feed
import feedparser
import os
import glob
import pytest
import redisorm.core
import redis


_dir = os.path.abspath(os.path.dirname(__file__))


@pytest.fixture
def test_redis():
    port = os.environ.get("TEST_REDIS_PORT")
    r = redis.StrictRedis(port=port, decode_responses=True)
    r.ping()
    r.flushdb()
    return r


def test_format_and_save(test_redis):
    p = redisorm.core.Persistent("rssr", r=test_redis)
    for filename in glob.glob(os.path.join(_dir, 'samples/sample_feed*')):

        with open(filename) as data:

            feed = Feed(url=filename)
            p.save(feed)

            for item in feedparser.parse(data.read()).entries:
                item = FeedItem.create_from(feed, item)
                p.save(item)
