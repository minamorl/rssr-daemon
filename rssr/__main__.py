import daemon
import sched
import argparse
import time
import rssr.rss
import datetime
import logging


logging.basicConfig(level=logging.INFO, filename='rssr-daemon.log', filemode='w')
logger = logging.getLogger(__name__)

def _argparse():
    parser = argparse.ArgumentParser()
    parser.add_argument('--daemonize', action='store_true')
    parser.add_argument('url', nargs='+')
    parser.add_argument('--delta', default=5)
    return parser


def task(urls):
    for url in urls:
        logger.info("Start parsing {}".format(url))

        fetched = rssr.rss.fetch(url)
        print(rssr.rss.format(fetched.text))

        logger.info("ok.")

def _main(args):

    logger.info("Start processing..")
    s = sched.scheduler(time.time, time.sleep)
    for t in exec_time(datetime.timedelta(minutes=int(args.delta))):
        s.enterabs(t, 1, task, argument=(args.url, ))
        s.run()


def exec_time(delta):
    while True:
        base_time = datetime.datetime.now()
        dt = base_time + delta
        logger.info("Next scheduled time: {}".format(dt))
        yield time.mktime(dt.timetuple())


def main():
    args = _argparse().parse_args()

    if args.daemonize:
        with daemon.DaemonContext():
            _main(args)
    else:
        _main(args)

if __name__ == '__main__':
    main()
