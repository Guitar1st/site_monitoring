import itertools
import json
import requests
import re
import time

from src import kafka_helper
from src import sites_iteration


def monitor(args, test_mode=False):
    assert args.sites_file or args.site_url, 'Sites file or site url must be provided'
    producer = kafka_helper.get_producer(server=args.kafka_server, ssl_folder=args.ssl)
    sites = sites_iteration.list_sites(args.sites_file, args.site_url)
    for i in itertools.count(1):  # here could be something more smart, like celery beat
        print(f'start monitoring loop #{i}')
        _loop_monitor(sites, producer, args.kafka_topic)
        if test_mode:
            break
        print('wait')
        time.sleep(10)  # todo: make this period customizable


def _loop_monitor(sites, kafka_producer, kafka_topic):
    for site in sites:  # this code could be easily modified to use with ThreadPoolExecutor
        site_data = _get_site_data(site)
        _send_site_data(kafka_producer, kafka_topic, site_data)


def _get_site_data(site):
    response = requests.get(site['url'])
    regexp = site.get('regexp')
    regexp_found = None
    if regexp:
        regexp_found = bool(re.match(regexp, response.text))
    return {
        'request_start_time': time.time(),
        'url': site['url'],
        'status_code': response.status_code,
        'response_time': response.elapsed.total_seconds(),
        'regexp': regexp,
        'regexp_found': regexp_found,
    }


def _send_site_data(producer, topic, site_data):
    producer.send(topic, json.dumps(site_data).encode('utf-8'))
