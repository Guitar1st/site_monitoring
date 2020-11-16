import argparse
import daemon
import logging

from src.monitor import monitor
from src.store import store


def main():
    main_parser = argparse.ArgumentParser(description='Monitor sites')
    main_parser.add_argument('--daemon', action='store_true')

    subparsers = main_parser.add_subparsers()

    monitor_parser = subparsers.add_parser('monitor')
    monitor_parser.add_argument('--kafka-server')
    monitor_parser.add_argument('--kafka-topic')
    monitor_parser.add_argument('--ssl')
    monitor_parser.add_argument('--sites-file')
    monitor_parser.add_argument('--site-url')
    monitor_parser.set_defaults(func=monitor)

    store_parser = subparsers.add_parser('store')
    store_parser.add_argument('--postgres-config')
    store_parser.add_argument('--kafka-server')
    store_parser.add_argument('--kafka-topic')
    store_parser.add_argument('--ssl')
    store_parser.set_defaults(func=store)

    a = main_parser.parse_args()
    if a.daemon:
        logging.info('Running in daemon mode')
        print('Running in daemon mode')
        with daemon.daemon.DaemonContext():
            a.func(a)
    else:
        print('Running in script mode')
        logging.info('Running in script mode')
        a.func(a)
