from src import sites_iteration


def test__sites_iteration():
    assert {"url": "bing.com"} == sites_iteration.list_sites("", "bing.com")[0]
