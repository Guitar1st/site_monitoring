import itertools

from src import file_utils


def list_sites(sites_file, site_url):
    return list(itertools.chain(_sites_from_file(sites_file), _site_from_url(site_url)))


def _sites_from_file(sites_file):
    if sites_file:
        for site in file_utils.load_json(sites_file):
            yield site


def _site_from_url(url):
    if url:
        yield {'url': url}
