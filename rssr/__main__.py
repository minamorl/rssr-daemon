import daemon
import sched
import time
import datetime
import os
import rssr.crawler
import sys
from rssr.utils import _argparse, exec_time, _logger
from rssr.models import save, get_url_lists


logger = _logger(__name__)


def task(args):
    for url in get_url_lists():
        logger.info("Start parsing {}".format(url))
        fetched = rssr.crawler.fetch(url)
        save(url, fetched.text) 
        logger.info("task end.")


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
