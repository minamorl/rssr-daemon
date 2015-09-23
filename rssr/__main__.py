import daemon
import sched
import argparse
import time
import rssr.rss
import datetime


def _argparse():
    parser = argparse.ArgumentParser()
    parser.add_argument('--daemonize', action='store_true')
    parser.add_argument('url', nargs='+')
    parser.add_argument('--delta', default=5)
    return parser


def task(urls):
    for url in urls:
        rssr.rss.fetch(url)


def _main(args):

    s = sched.scheduler(time.time, time.sleep)
    for t in exec_time(datetime.timedelta(minutes=int(args.delta))):
        s.enterabs(t, 1, task, argument=(args.url, ))
        s.run()


def exec_time(delta):
    while True:
        base_time = datetime.datetime.now()
        dt = base_time + delta
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
