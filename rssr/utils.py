import argparse
import time
import datetime
import logging
import base64


def _logger(name):
    logging.basicConfig(level=logging.INFO, filename='rssr-daemon.log', filemode='w')
    return logging.getLogger(name)

logger = _logger(__name__)


def validate_filename(filename):
    return base64.b64encode(filename.encode('utf-8')).decode('utf-8')


def _argparse():
    parser = argparse.ArgumentParser()
    parser.add_argument('--daemonize', action='store_true')
    parser.add_argument('url', nargs='+')
    parser.add_argument('--delta', default=5)
    parser.add_argument('--pidfile', default=None)
    parser.add_argument('--dest', default="./misc/")
    return parser


def exec_time(delta):
    yield datetime_to_time(datetime.datetime.now())
    while True:
        base_time = datetime.datetime.now()
        dt = base_time + delta
        logger.info("Next scheduled time: {}".format(dt))
        yield datetime_to_time(dt)


def datetime_to_time(dt):
    return time.mktime(dt.timetuple())
