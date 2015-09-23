import daemon
import argparse 

def _argparse():
    parser = argparse.ArgumentParser()
    parser.add_argument('--daemonize', action='store_true')
    return parser

def _main():
    pass

def main():
    args = _argparse().parse_args()

    if args.daemonize:
        with daemon.DaemonContext():
            _main()
    else:
        _main()

if __name__ == '__main__':
    main()

