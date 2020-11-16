import os

from kafka import KafkaProducer, KafkaConsumer


def get_security(ssl_folder):
    return {
        'security_protocol': 'SSL',
        'ssl_cafile': os.path.join(ssl_folder, 'ca.pem'),
        'ssl_certfile': os.path.join(ssl_folder, 'service.cert'),
        'ssl_keyfile': os.path.join(ssl_folder, 'service.key'),
    }


def get_producer(server, ssl_folder='../ssl'):
    return KafkaProducer(
        bootstrap_servers=server,
        **get_security(ssl_folder)
    )


def get_consumer(topic, server, ssl_folder='../ssl'):
    return KafkaConsumer(
        topic,
        bootstrap_servers=server,
        client_id='demo-client-3',
        group_id='demo-group-3',
        **get_security(ssl_folder)
    )
