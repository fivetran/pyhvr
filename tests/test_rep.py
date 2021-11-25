import pyhvr

hvr_client = pyhvr.client(
    username="admin", password="Kiwi1234", uri="http://localhost:4340"
)


def test_setup_direct_rep():
    loc_source = hvr_client.post_hubs_definition_locs(
        hub="hvrhub",
        loc="test1_source",
        props={
            "Database_Host": "postgres-source",
            "Database_Port": 5432,
            "Database_Name": "tpcc",
            "Database_User": "postgres",
            "Database_Password": "Kiwi1234",
            "Class": "postgresql",
            "Capture_Method": "SQL",
            "Agent_Host": "rtdsagent-1",
            "Agent_Port": "4343",
        },
    )

    assert loc_source is None

    loc_target = hvr_client.post_hubs_definition_locs(
        hub="hvrhub",
        loc="test1_target",
        props={
            "Database_Host": "postgres-target",
            "Database_Port": 5432,
            "Database_Name": "tpcc",
            "Database_User": "postgres",
            "Database_Password": "Kiwi1234",
            "Class": "postgresql",
            "Capture_Method": "SQL",
            "Agent_Host": "rtdsagent-2",
            "Agent_Port": "4343",
        },
    )

    assert loc_target is None

    ch = hvr_client.post_hubs_definition_channels(
        channel="t1_channel",
        hub="hvrhub",
        description="Test channel ",
        loc_groups={
            "SOURCE": {"members": ["test1_source"]},
            "TARGET": {"members": ["test1_target"]},
        },
        actions=[
            {
                "loc_scope": "SOURCE",
                "params": {},
                "table_scope": "*",
                "type": "Capture",
            },
            {
                "loc_scope": "TARGET",
                "params": {},
                "table_scope": "*",
                "type": "Integrate",
            },
        ],
    )
    assert ch is None

    lg = hvr_client.post_hubs_definition_channels_loc_groups(
        hub="hvrhub",
        channel="t1_channel",
        loc_group="TEST_GROUP"
    )
    assert lg is None

    add = hvr_client.post_hubs_channels_locs_adapt_apply(
        hub="hvrhub",
        channel="t1_channel",
        loc="test1_source",
        add_table_group={"group": "GENERAL"},
        add_tables=True,
        mapspec={"tables": [{"schema": "public", "base_name": "customer"}]},
    )

    assert add == {
        "add_tables": [
            {
                "base_name": "customer",
                "schema": "public",
                "table": "customer",
                "type": "Table",
            }
        ]
    }

    refresh_data = {
        "start_immediate": False,
        "source_loc": "test1_source",
        "target_loc": "test1_target",
        "online_refresh": "read_write",
        "tables": ["customer"],
        "create_tables": {
            "keep_structure": False,
            "force_recreate": True,
            "index": True,
            "keep_existing_data": False,
            "recreate_if_mismatch": False,
        },
        "granularity": "bulk",
        "start_next_jobs": ["integ"],
    }
    refresh = hvr_client.post_hubs_channels_refresh(
        hub="hvrhub", channel="t1_channel", **refresh_data
    )

    assert refresh["job"] == "t1_channel-refr-test1_source-test1_target"

    activate_data = {
        "parallel_locs": 2,
        "replace_enroll": False,
    }

    activate = hvr_client.post_hubs_channels_activate(
        hub="hvrhub", channel="t1_channel", **activate_data
    )

    assert activate["job"] == "t1_channel-activate"
