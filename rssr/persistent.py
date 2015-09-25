import redis
import pickle
import datetime
from rssr.utils import _logger

logger = _logger(__name__)


def save_parsed_value(url, data, redis_key=None):
    r = redis.StrictRedis()
    redis_key = redis_key or "rssr:feed:{title}@{date}".format(title=url, date=datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
    savable = pickle.dumps(data)
    r.append(redis_key, savable)


def save_raw_feed(data, fp):
    with fp:
        fp.write(data)
    logger.info("file {} was generated.".format(fp.name))
