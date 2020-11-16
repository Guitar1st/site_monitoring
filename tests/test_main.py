from src import postgres_helper
from src import monitor
from src import store


class TestArgs:
    kafka_server = "kafka-site-monitoring-kvasovdmitry-7cd9.aivencloud.com:19234"
    kafka_topic = "monitoring-results"
    ssl = "./ssl"
    sites_file = "./sites.json"
    site_url = ""
    postgres_config = './configs/pgconfig.json'


def test__no_exceptions():
    """Simple smoke test, just to make sure, that there are no obvious exceptions."""
    args = TestArgs()
    postgres_helper.prepare_db(args.postgres_config)
    monitor.monitor(args, test_mode=True)
    store.store(args, test_mode=True)
