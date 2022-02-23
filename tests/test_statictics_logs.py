import pyhvr
from pyhvr.pyhvr_exceptions import PyhvrError, RestError

hvr_client = pyhvr.client(
    username="admin", password="Kiwi1234Kiwi1234", uri="http://localhost:4340"
)


def test_hubserver():
    test_h = hvr_client.post_hubserver_test()
    assert test_h is None


def test_conn_test():
    tc = hvr_client.post_hubs_locs_test(hub="hvrhub", loc="sourceat", channel="chanat")
    assert tc["discovered_props"]["Class_Flavor"] == "vanilla"


def test_wrong_ch_name():
    try:
        hvr_client.post_hubs_locs_test(hub="hvrhub", loc="sourceat", channel="chanat1")
    except PyhvrError as e:
        assert e.error_code == "F_JR071E"


def test_ch_exception_loc():
    try:
        hvr_client.post_hubs_locs_test(
            hub="hvrhub", loc="sourceat1123", channel="chanat"
        )
    except RestError as e:
        # test access to the fields
        print(e.status_code)
        print(e.message)
        print(e.error_code)


def test_metrics_oldest():
    om = hvr_client.get_hubs_stats_oldest(hub="hvrhub")
    assert om is not None


def test_export_metrics():
    data = {
        "channel": ["chanat"],
        "table": ["customer"],
        "loc": ["sourceat"],
        "metric": ["Captured Inserts"],
        "time_gran": ["1"],
        "scope": ["clt"],
        "tstamp_begin": "1643275080",
        "tstamp_end": "1643275731",
        "format": "json",
    }
    ct = hvr_client.post_hubs_stats_metrics_export(hub="hvrhub", **data)
    assert ct is not None


def test_metrics():
    m = hvr_client.get_hubs_stats_metrics(hub="hvrhub")
    assert m is not None
