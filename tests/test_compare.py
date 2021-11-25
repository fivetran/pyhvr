import pyhvr
import pytest
from pyhvr.pyhvr_exceptions import (RestError)

hvr_client = pyhvr.client(
    username="admin", password="Kiwi1234", uri="http://localhost:4340"
)


def test_activate_post():
    activate_data = {
        "start_next_jobs": ["cap"],
        "parallel_locs": 2,
        "replace_enroll": False,
    }

    activate = hvr_client.post_hubs_channels_activate(
        hub="hvrhub", channel="chanat", **activate_data
    )
    print("ACTIVE the channel")
    assert activate["job"] == f"chanat-activate"


def test_hub_compare_Channel1():
    result = hvr_client.post_hubs_channels_compare(
        hub="hvrhub",
        channel="chanat",
        start_immediate="true",
        source_loc="sourceat",
        target_loc="targetat",
        online_compare="diff_diff",
        online_compare_sleep=0,
        granularity="rowwise",
        tables=["customer"],
    )
    assert result["job"] == "chanat-cmp-sourceat-targetat"
    assert result["posted_ev_id"]


def test_hub_compare_Channel2():
    result = hvr_client.post_hubs_channels_compare(
        hub="hvrhub",
        channel="chanrl",
        source_loc="sourcerl",
        target_loc="targetrl",
        start_immediate="true",
        granularity="bulk",
        tables=["customer"]
    )
    assert result["job"] == "chanrl-cmp-sourcerl-targetrl"
    assert result["posted_ev_id"]


def test_hub_compare_invalid_param():
    with pytest.raises(RestError):
        hvr_client.post_hubs_channels_compare(
            hub="hvrhub",
            channel="chanat",
            start_immediate="true",
            source_loc="sourceat",
            target_loc="targetat",
            online_compare="diff_diff",
            online_compare_sleep=0,
            granularity="bulk",
            tables=["customer"]
        )


def test_deactivate():
    deactivate_data = {
        "start_immediate": "true",
        "components": ["state_tables"],
        "parallel_locs": 2,
    }

    deactivate = hvr_client.post_hubs_channels_deactivate(
        hub="hvrhub", channel="chanat", **deactivate_data
    )
    print("DeACTIVE the channel")
    assert deactivate["job"] == f"chanat-activate"


def test_get_tables():
    ht = hvr_client.get_hubs_definition_channels_tables(hub="hvrhub", channel="chanst")
    print(ht)
    assert ht["customer"]["base_name"] == "customer"


def test_definition_table():
    ht = hvr_client.get_hubs_definition_channels_tables_table(hub="hvrhub", channel="chanst", table="customer")
    print(ht)
    assert ht is not None


def test_get_table_clos():
    ht = hvr_client.get_hubs_definition_channels_tables_cols(
        hub="hvrhub",
        channel="chanst",
        table="customer"
    )
    print(ht)
    assert ht is not None


def test_rename_table():
    hvr_client.post_hubs_definition_channels_tables_rename(
        hub="hvrhub",
        channel="chanst",
        table="customer",
        new_name="new_cust"
    )


def test_table_delete_in_channel():
    tb1 =hvr_client.delete_hubs_definition_channels_tables(
        hub="hvrhub",
        channel="chanst",
        table="new_cust"
    )
    assert tb1 is None


def test_delete_channel():
    ch = hvr_client.delete_hubs_definition_channels(
        hub="hvrhub",
        channel="chane"
    )
    print(ch)
    assert ch is None


def test_delete_non_ext_channel():
    with pytest.raises(RestError):
        hvr_client.delete_hubs_definition_channels(channel="chane", hub="hvrhub")


def test_add_loc_group():
    lc = hvr_client.post_hubs_definition_channels_loc_groups(
        hub="hvrhub",
        channel="chanart",
        loc_group="TEST_LOC_G1"
    )
    print(lc)
    assert lc is None


def test_wrong_loc_group():
    try:
        hvr_client.post_hubs_definition_channels_loc_groups(
            hub="hvrhub",
            channel="testc",
            loc_group="wrong_loc_group"
        )
    except RestError as e:
        print(e.status_code)
        print(e.message)
        print(e.error_code)


def test_get_loc_group():
    hvr_client.get_hubs_definition_channels_loc_groups(hub="hvrhub", channel="chanart")


def test_get_loc():
    hvr_client.get_hubs_definition_channels_loc_groups_group(hub="hvrhub",
                                                             channel="chanart",
                                                             loc_group="TEST_LOC_G1")


def test_get_loc_gmembers():
    hvr_client.get_hubs_definition_channels_loc_groups_members(hub="hvrhub", channel="chanart", loc_group="TEST_LOC_G1")


def test_put_loc_group():
    hvr_client.put_hubs_definition_channels_loc_groups(hub="hvrhub", channel="chanart", loc_group="TEST_LOC_G1")


def test_rename_loc_group():
    hvr_client.post_hubs_definition_channels_loc_groups_rename(hub="hvrhub",
                                                               channel="chanart",
                                                               loc_group="TEST_LOC_G1",
                                                               new_name="TEST_LOC_G_NEW")


def test_channel_rename():
    hvr_client.post_hubs_definition_channels_rename(hub="hvrhub", channel="chanart", new_name="new_chan")


def test_channel_tables():
    hvr_client.get_hubs_definition_channels_tables(hub="hvrhub", channel="new_chan")


def test_delete_loc_group():
    hvr_client.delete_hubs_definition_channels_loc_groups(hub="hvrhub", channel="new_chan", loc_group="TEST_LOC_G_NEW")
