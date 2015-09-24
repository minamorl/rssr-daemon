import daemon
import redis
import sched
import time
import datetime
import os
import rssr.crawler
from rssr.utils import _argparse, exec_time, _logger, validate_filename
import pickle


logger = _logger(__name__)


def task(args):
    for url in args.url:
        logger.info("Start parsing {}".format(url))
        fetched = rssr.crawler.fetch(url)

        filename = validate_filename(url)
        filepath = os.path.join(args.dest, filename)

        with open(filepath, 'w') as f:
            f.write(fetched.text)

        logger.info("file {} was generated.".format(filepath))

        data = rssr.crawler.format(fetched.text)
        save_redis(url, data)

        logger.info("task end.")


def save_redis(url, data):
    r = redis.StrictRedis()
    redis_key = "rssr:feed:{title}@{date}".format(title=url, date=datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
    savable = pickle.dumps(data)
    r.append(redis_key, savable)

def _main(args):
    logger.info("Start processing..")
    s = sched.scheduler(time.time, time.sleep)
    for t in exec_time(datetime.timedelta(minutes=int(args.delta))):
        s.enterabs(t, 1, task, argument=(args, ))
        s.run()


def main():
    args = _argparse().parse_args()

    if args.daemonize:
        with daemon.DaemonContext(pidfile=args.pidfile):
            _main(args)

    _main(args)


if __name__ == '__main__':
    main()
