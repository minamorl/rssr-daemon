import daemon
import sched
import time
import datetime

import rssr.crawler
from rssr.utils import _argparse, exec_time, _logger


logger = _logger(__name__)


def task(urls):
    for url in urls:
        logger.info("Start parsing {}".format(url))

        fetched = rssr.crawler.fetch(url)
        print(rssr.crawler.format(fetched.text))

        logger.info("ok.")


def _main(args):
    logger.info("Start processing..")
    s = sched.scheduler(time.time, time.sleep)
    for t in exec_time(datetime.timedelta(minutes=int(args.delta))):
        s.enterabs(t, 1, task, argument=(args.url, ))
        s.run()


def main():
    args = _argparse().parse_args()

    if args.daemonize:
        with daemon.DaemonContext(pidfile=args.pidfile):
            _main(args)

    _main(args)


if __name__ == '__main__':
    main()
