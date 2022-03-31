import pytest

import pyhvr
from pyhvr.pyhvr_exceptions import (ConnectionError, LoginError, PyhvrError,
                                    RestError)

hvr_client = pyhvr.client(
    username="admin", password="Kiwi1234Kiwi1234", uri="http://localhost:4340"
)


def test_invalid_uri():
    with pytest.raises(ConnectionError):
        pyhvr.client(
            username="admin", password="Kiwi1234Kiwi1234", uri="xxx://localhost:4340"
        ).get_hubserver_clock()


def test_nonexistent_uri():
    with pytest.raises(ConnectionError):
        pyhvr.client(
            username="admin",
            password="Kiwi1234Kiwi1234",
            uri="http://nodomain.com:4340",
        ).get_hubserver_clock()


def test_wrong_login():
    with pytest.raises(LoginError):
        pyhvr.client(
            username="admin", password="wrong", uri="http://localhost:4340"
        ).get_hubserver_clock()


def test_post_hubs_definition_channels():
    ch = hvr_client.post_hubs_definition_channels(
        channel="ch2",
        hub="hvrhub",
        description="desc2",
        # loc_groups={"LOCGROUP1": {"members": ["loc1", "loc2"]}},
        tables={"t1": {"base_name": "bn1", "table_group": "TG1"}},
    )
    assert ch is None
    ch = hvr_client.post_hubs_definition_channels(
        channel="ch1", hub="hvrhub", description="desc1"
    )
    assert ch is None

    channels = hvr_client.get_hubs_definition_channels(hub="hvrhub", channel="ch2")
    assert channels["ch2"] is not None
    channels = hvr_client.get_hubs_definition_channels(hub="hvrhub", channel="ch1")
    assert channels.get("ch2") is None
    channels = hvr_client.get_hubs_definition_channels(
        hub="hvrhub", channel=["ch1", "ch2"]
    )
    assert channels["ch1"] is not None
    assert channels["ch2"] is not None
    channels = hvr_client.get_hubs_definition_channels(hub="hvrhub")
    assert channels["ch1"] is not None
    assert channels["ch2"] is not None

    ch = hvr_client.delete_hubs_definition_channels(channel="ch2", hub="hvrhub")
    ch = hvr_client.delete_hubs_definition_channels(channel="ch1", hub="hvrhub")
    assert ch is None


def test_hubs_definition_locs():

    loc = hvr_client.post_hubs_definition_locs(
        hub="hvrhub",
        loc="loc1",
        props={
            "Database_Host": "postgres-source",
            "Database_Port": 5432,
            "Database_Name": "tpcc",
            "Database_User": "postgres",
            "Database_Password": "Kiwi1234",
            "Class": "postgresql",
            "Capture_Method": "SQL",
            # "Agent_Host": agent,
            # "Agent_Port": "4343"
        },
    )

    assert loc is None

    locs = hvr_client.get_hubs_definition_locs(hub="hvrhub")

    assert locs["loc1"] is not None

    test_conn = hvr_client.post_hubs_locs_test(hub="hvrhub", loc="loc1")

    assert test_conn["discovered_props"] is not None

    loc = hvr_client.delete_hubs_definition_locs(hub="hvrhub", loc="loc1")

    assert loc is None


def test_conn_without_creating():
    t = hvr_client.post_hubs_new_loc_test(
        hub="hvrhub",
        props={
            "Database_Host": "postgres-source",
            "Database_Port": 5432,
            "Database_Name": "tpcc",
            "Database_User": "postgres",
            "Database_Password": "Kiwi1234",
            "Class": "postgresql",
            "Capture_Method": "SQL",
            # "Agent_Host": agent,
            # "Agent_Port": "4343"
        },
    )
    assert t["discovered_props"]["Class_Flavor"] == "vanilla"


def test_delete_exception():

    with pytest.raises(RestError):
        hvr_client.delete_hubs_definition_channels(channel="doesnotexist", hub="hvrhub")


def test_exception_components():
    try:
        hvr_client.delete_hubs_definition_channels(channel="doesnotexist", hub="hvrhub")
    except RestError as e:
        # test access to the fields
        print(e.status_code)
        print(e.message)
        print(e.error_code)


def test_exception_error_code():
    try:
        hvr_client.post_hubs_definition_channels(channel="duplicate", hub="hvrhub")
        hvr_client.post_hubs_definition_channels(channel="duplicate", hub="hvrhub")
    except PyhvrError as e:
        assert e.error_code == "F_JR171C"


def test_login():
    """Force client to login"""
    hvr_client.login()


def test_hubs_definition_locs_put():

    loc = hvr_client.put_hubs_definition_locs(
        hub="hvrhub",
        loc="loc3",
        props={
            "Database_Host": "postgres-source",
            "Database_Port": 5432,
            "Database_Name": "tpcc",
            "Database_User": "postgres",
            "Database_Password": "Kiwi1234",
            "Class": "postgresql",
            "Capture_Method": "SQL",
            # "Agent_Host": agent,
            # "Agent_Port": "4343"
        },
    )

    assert loc is None

    locs = hvr_client.get_hubs_definition_locs(hub="hvrhub")

    assert locs["loc3"] is not None


def test_hubs_definition_patch():

    loc = hvr_client.post_hubs_definition_locs(
        hub="hvrhub",
        loc="loc4",
        props={
            "Database_Host": "postgres-source",
            "Database_Port": 5432,
            "Database_Name": "tpcc",
            "Database_User": "postgres",
            "Database_Password": "Kiwi1234",
            "Class": "postgresql",
            "Capture_Method": "SQL",
            # "Agent_Host": agent,
            # "Agent_Port": "4343"``
        },
    )

    assert loc is None

    loc = hvr_client.patch_hubs_definition_locs_props(
        hub="hvrhub",
        loc="loc4",
        Database_Host="postgres-source",
        Database_Port=5432,
        Database_Name="tpcc",
        Database_User="postgres2",
        Database_Password="Kiwi12342",
        Class="postgresql",
        Capture_Method="SQL",
    )

    assert loc is None

    # Test how to pass props dict
    props = {
        "Database_Host": "postgres-source",
        "Database_Port": 5432,
        "Database_Name": "tpcc",
        "Database_User": "postgres",
        "Database_Password": "Kiwi1234",
        "Class": "postgresql",
        "Capture_Method": "SQL",
        "Agent_Host": "agent",
        "Agent_Port": "4343",
    }

    loc = hvr_client.patch_hubs_definition_locs_props(hub="hvrhub", loc="loc4", **props)

    assert loc is None


def test_event_status():
    # just to test bool type
    result_pattern = "Table_State|Table_Start_Time|Source_Rows_Used|Subtasks_Done|Subtasks_Total|Subtasks_Busy|Rows_Only_On_Target|Rows_Only_On_Source|Rows_Which_Differ"
    hvr_client.get_hubs_events(
        hub="hvrhub",
        ev_id="123",
        fetch_results=True,
        result_pattern=result_pattern,
        max_events=1,
    )


def test_api_version():
    api = hvr_client.get_api()

    assert "v0" in api
    assert "v6.1.0.3" in api
