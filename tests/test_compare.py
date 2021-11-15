import pytest
import pyhvr
from pyhvr.pyhvr_exceptions import (ConnectionError, LoginError, PyhvrError,
                                    RestError)
import test_activate

hvr_client = pyhvr.client(
    username="admin", password="Kiwi1234", uri="http://localhost:4340"
)


def test_get_active():
    print("Check activation Status of channels ")
    hvr_client.post_hubs_channels_activate(hub="hvrhub", channel="chanat")


def test_channel_activation():
    print("Check replication activation status of channel")
    hvr_client.get_hubs_channels_activate(hub="hvrhub",
                                          channel="chanat"
                                          )


def test_activate_post():
    print("ACTIVE the channel")
    hvr_client.post_hubs_channels_activate(hub="hvrhub", channel="chanat")


def test_hub_compare_Channel1():
    print("Running Compare")
    hvr_client.post_hubs_channels_compare(
        hub="hvrhub",
        channel="chanat",
        start_immediate="true",
        source_loc="sourceat",
        target_loc="targetat",
        online_compare="diff_diff",
        online_compare_sleep=0,
        granularity="rowwise",
        tables=["customer"]
    )


def test_hub_compare_Channel2():
    hvr_client.post_hubs_channels_compare(
        hub="hvrhub",
        channel="chanrl",
        source_loc="sourcerl",
        target_loc="targetrl",
        start_immediate="true",
        granularity="bulk",
        tables=["customer"]
    )


def test_hub_compare_invalid_param():
    try:
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
    except RestError as Er:
        print(Er.status_code)
        print(Er.message)
        print(Er.error_code)


def test_table_evenID():
    print("Get event ids for tables results of recent Compare ")
    hvr_client.get_hubs_channels_refresh_tables_results_ids(hub="hvrhub", channel="chanat")


def test_context():
    print("Show contexts and context variables ")
    hvr_client.get_hubs_channels_contexts(hub="hvrhub", channel="chanat")


def test_deactivate():
    hvr_client.post_hubs_channels_deactivate(hub="hvrhub", channel="chanrl")


def test_check_open_trans():
    hvr_client.get_hubs_channels_locs_capture_open_tx(
        hub="hvrhub",
        channel="chanat",
        loc="sourceat"
    )


def test_integrate_point():
    hvr_client.get_hubs_channels_locs_integrate_point(
        hub="hvrhub",
        channel="chanat",
        loc="sourceat"
    )


def test_refresh_table_result_ids():
    print("Get event ids for tables results of recent Refresh for all channels ")
    hvr_client.get_hubs_refresh_tables_results_ids(hub="hvrhub")


def test_get_tables():
    hvr_client.get_hubs_definition_channels_tables(hub="hvrhub", channel="chanst")


def test_definition_table():
    hvr_client.get_hubs_definition_channels_tables_table(hub="hvrhub", channel="chanst", table="customer")


def test_get_table_clos():
    hvr_client.get_hubs_definition_channels_tables_cols(
        hub="hvrhub",
        channel="chanst",
        table="customer"
    )


def test_rename_table():
    hvr_client.post_hubs_definition_channels_tables_rename(
        hub="hvrhub",
        channel="chanst",
        table="customer",
        new_name="new_cust"
    )


def test_table_delete_in_channel():
    hvr_client.delete_hubs_definition_channels_tables(
        hub="hvrhub",
        channel="chanst",
        table="new_cust"
    )


def test_delete_channel():
    hvr_client.delete_hubs_definition_channels(
        hub="hvrhub",
        channel="chanst"
    )


def test_channel_action():
    print(" Fetch channel actions from hub definition ")
    hvr_client.get_hubs_definition_channels_actions(
        hub="hvrhub",
        channel="chanjc"
    )


def test_add_loc_group():
    hvr_client.post_hubs_definition_channels_loc_groups(
        hub="hvrhub",
        channel="chanart",
        loc_group="TEST_LOC_G1")


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
