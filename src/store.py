import itertools
import json
import time

from src import kafka_helper
from src import postgres_helper


def store(args, test_mode=False):
    consumer = kafka_helper.get_consumer(args.kafka_topic, server=args.kafka_server, ssl_folder=args.ssl)
    for i in itertools.count(1):  # here could be something more smart, like celery beat
        print(f'start store loop #{i}')
        _loop_store(consumer, args.postgres_config)
        if test_mode:
            break
        print('wait')
        time.sleep(30)  # todo: make this period customizable


def _loop_store(consumer, pgconfig_file_path):
    raw_msgs = consumer.poll(timeout_ms=10000, max_records=50)
    batch = []
    for tp, msgs in raw_msgs.items():
        for msg in msgs:
            batch.append(json.loads(msg.value.decode('utf-8')))
    print(f'Got batch of {len(batch)} items')
    consumer.commit()
    if batch:
        postgres_helper.store_batch_data(pgconfig_file_path, batch)
