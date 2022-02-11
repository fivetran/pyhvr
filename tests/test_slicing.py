import pyhvr

hvr_client = pyhvr.client(
    username="admin", password="Kiwi1234", uri="http://localhost:4340"
)


def test_setup_slicing():
    loc_source = hvr_client.post_hubs_definition_locs(
        hub="hvrhub",
        loc="test_slice_s",
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
        loc="test_slice_t",
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
        channel="t_slice_c",
        hub="hvrhub",
        description="Test channel ",
        loc_groups={
            "SOURCE": {"members": ["test_slice_s"]},
            "TARGET": {"members": ["test_slice_t"]},
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
        hub="hvrhub", channel="t_slice_c", loc_group="TEST_SLICE_G"
    )
    assert lg is None

    add = hvr_client.post_hubs_channels_locs_adapt_apply(
        hub="hvrhub",
        channel="t_slice_c",
        loc="test_slice_s",
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
        "start_immediate": True,
        "source_loc": "test_slice_s",
        "target_loc": "test_slice_t",
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
        "parallel_sessions": 4,
        "slicing": {
            "customer": {
                "slices": 4,
                "col": "c_id",
                "type": "modulo",
            }
        },
    }

    refresh = hvr_client.post_hubs_channels_refresh(
        hub="hvrhub", channel="t_slice_c", **refresh_data
    )

    assert refresh["job"] == "t_slice_c-refr-test_slice_s-test_slice_t"

    activate_data = {
        "parallel_locs": 2,
        "replace_enroll": False,
    }

    activate = hvr_client.post_hubs_channels_activate(
        hub="hvrhub", channel="t_slice_c", **activate_data
    )

    assert activate["job"] == "t_slice_c-activate"


def test_slicing_boundary():
    refresh_data = {
        "start_immediate": True,
        "source_loc": "test_slice_s",
        "target_loc": "test_slice_t",
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
        "parallel_sessions": 4,
        "slicing": {
            "customer": {"col": "c_id", "type": "boundary", "int_boundaries": [100]}
        },
    }

    refresh = hvr_client.post_hubs_channels_refresh(
        hub="hvrhub", channel="t_slice_c", **refresh_data
    )

    assert refresh["job"] == "t_slice_c-refr-test_slice_s-test_slice_t"

    activate_data = {
        "parallel_locs": 2,
        "replace_enroll": False,
    }

    activate = hvr_client.post_hubs_channels_activate(
        hub="hvrhub", channel="t_slice_c", **activate_data
    )

    assert activate["job"] == "t_slice_c-activate"


def test_slicing_compare():
    result = hvr_client.post_hubs_channels_compare(
        hub="hvrhub",
        channel="t_slice_c",
        start_immediate="true",
        source_loc="test_slice_s",
        target_loc="test_slice_t",
        online_compare="diff_diff",
        online_compare_sleep=0,
        granularity="rowwise",
        tables=["customer"],
        slicing={"customer": {"slices": 4, "col": "c_payment_cnt", "type": "modulo"}},
    )

    assert result["job"] == "t_slice_c-cmp-test_slice_s-test_slice_t"
    assert result["posted_ev_id"]
