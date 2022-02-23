from pprint import pprint

import pyhvr

hvr_client = pyhvr.client(
    username="admin", password="Kiwi1234Kiwi1234", uri="http://localhost:4340"
)


def setup_replication(suffix):
    loc = hvr_client.put_hubs_definition_locs(
        hub="hvrhub",
        loc="source" + suffix,
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

    assert loc is None

    loc = hvr_client.put_hubs_definition_locs(
        hub="hvrhub",
        loc="target" + suffix,
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

    assert loc is None

    ch = hvr_client.post_hubs_definition_channels(
        channel="chan" + suffix,
        hub="hvrhub",
        description="channel " + suffix,
        loc_groups={
            "SOURCE": {"members": ["source" + suffix]},
            "TARGET": {"members": ["target" + suffix]},
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

    return ("hvrhub", "chan" + suffix, "source" + suffix, "target" + suffix)


def test_add_tables():
    (hub, channel, source, target) = setup_replication("at")

    add = hvr_client.post_hubs_channels_locs_adapt_apply(
        hub=hub,
        channel=channel,
        loc=source,
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


def test_add_remove_tables():
    (hub, channel, source, target) = setup_replication("art")

    add = hvr_client.post_hubs_channels_locs_adapt_apply(
        hub=hub,
        channel=channel,
        loc=source,
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

    add_not_exists = hvr_client.post_hubs_channels_locs_adapt_apply(
        hub=hub,
        channel=channel,
        loc=source,
        add_table_group={"group": "GENERAL"},
        add_tables=True,
        mapspec={"tables": [{"schema": "public", "base_name": "does_not_exist"}]},
    )

    assert add_not_exists == {"add_tables": []}

    add = hvr_client.post_hubs_channels_locs_adapt_apply(
        hub=hub,
        channel=channel,
        loc=source,
        add_table_group={"group": "GENERAL"},
        add_tables=True,
        mapspec={"tables": [{"schema": "public", "base_name": "district"}]},
    )

    assert add == {
        "add_tables": [
            {
                "base_name": "district",
                "schema": "public",
                "table": "district",
                "type": "Table",
            }
        ]
    }

    remove = hvr_client.post_hubs_definition_channels_tables_delete(
        hub=hub, channel=channel, tables=["district"]
    )

    assert remove is None

    tables = hvr_client.get_hubs_query_channels_tables(hub=hub, channel=channel)

    assert tables == {
        "customer": {
            "schema_bases": [
                {"base_name": "customer", "integ_locs": ["targetart"]},
                {
                    "base_name": "customer",
                    "cap_locs": ["sourceart"],
                    "schema": "public",
                    "schema_type": "discovered",
                },
            ]
        }
    }

    tables = hvr_client.get_hubs_query_channels_tables(
        hub=hub, channel=channel, table=["items"]
    )

    assert tables == {}

    tables = hvr_client.get_hubs_query_channels_tables(
        hub=hub, channel=channel, table=["customer"]
    )

    assert tables == {
        "customer": {
            "schema_bases": [
                {"base_name": "customer", "integ_locs": ["targetart"]},
                {
                    "base_name": "customer",
                    "cap_locs": ["sourceart"],
                    "schema": "public",
                    "schema_type": "discovered",
                },
            ]
        }
    }

    open_tx = hvr_client.get_hubs_channels_locs_capture_open_tx(
        hub=hub, channel=channel, loc=source
    )

    print(open_tx["num_open_tx"])


def test_open_tx():
    (hub, channel, source, target) = setup_replication("otx")

    add = hvr_client.post_hubs_channels_locs_adapt_apply(
        hub=hub,
        channel=channel,
        loc=source,
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

    open_tx = hvr_client.get_hubs_channels_locs_capture_open_tx(
        hub=hub, channel=channel, loc=source
    )

    print(open_tx["num_open_tx"])


def test_add_table_action():
    (hub, channel, source, target) = setup_replication("ata")

    add = hvr_client.post_hubs_channels_locs_adapt_apply(
        hub=hub,
        channel=channel,
        loc=source,
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

    action = hvr_client.patch_hubs_definition_channels_actions(
        hub=hub,
        channel=channel,
        actions=[
            {
                "params": {"BaseName": "renamed_customer", "Schema": "renamed_public"},
                "type": "TableProperties",
                "table_scope": "customer",
                "loc_scope": target,
            }
        ],
    )

    assert action is None


def test_start_repl1():
    _kickoff("sr1")


def _kickoff(prefix):
    (hub, channel, source, target) = setup_replication(prefix)

    add = hvr_client.post_hubs_channels_locs_adapt_apply(
        hub=hub,
        channel=channel,
        loc=source,
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
        "source_loc": source,
        "target_loc": target,
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
        hub=hub, channel=channel, **refresh_data
    )

    assert refresh["job"] == f"{channel}-refr-{source}-{target}"

    activate_data = {
        "start_next_jobs": ["cap"],
        "start_next_ev_ids": [refresh["posted_ev_id"]],
        "parallel_locs": 2,
        "replace_enroll": False,
    }

    activate = hvr_client.post_hubs_channels_activate(
        hub=hub, channel=channel, **activate_data
    )

    assert activate["job"] == f"{channel}-activate"

    jobs = hvr_client.get_hubs_jobs(hub=hub, channel=channel)

    assert jobs == {
        f"{channel}-activate": {"state": "RUNNING"},
        f"{channel}-refr-{source}-{target}": {"state": "SUSPEND"},
    }
    return (
        hub,
        channel,
        source,
        target,
        refresh["posted_ev_id"],
        activate["posted_ev_id"],
    )


def test_job_control():
    (hub, channel, source, target, refresh_ev_id, activate_ev_id) = _kickoff("jc")

    suspend = hvr_client.post_hubs_jobs_suspend(hub=hub, jobs=[f"{channel}-activate"])

    assert suspend is None

    unsuspend = hvr_client.post_hubs_jobs_unsuspend(
        hub=hub, jobs=[f"{channel}-activate"]
    )

    assert unsuspend is None

    suspend = hvr_client.post_hubs_jobs_suspend(hub=hub, jobs=[f"{channel}-activate"])

    assert suspend is None

    start = hvr_client.post_hubs_jobs_start(hub=hub, jobs=[f"{channel}-activate"])

    assert start == {f"{channel}-activate": {"not_started": "Job in state 'SUSPEND'"}}


def test_read_logs():
    (hub, channel, source, target, refresh_ev_id, activate_ev_id) = _kickoff("rl")

    logs = hvr_client.get_hubs_logs_search(
        hub=hub, file=f"{channel}-activate.out", search_tstamp="now-1m"
    )

    uri_parts = logs["path"].split("/")  # -> /api/v0/hubs/{hub}/logs/{file}
    file_name = uri_parts[6]
    pprint(uri_parts)

    log_lines = hvr_client.get_hubs_logs(
        hub=hub, file=file_name, max_lines=100, offset_begin=logs["offset"]
    )

    assert isinstance(log_lines, str)


def test_events():
    (hub, channel, source, target, refresh_ev_id, activate_ev_id) = _kickoff("e")

    result_pattern = "Table_State|Table_Start_Time|Source_Rows_Used|Subtasks_Done|Subtasks_Total|Subtasks_Busy|Rows_Only_On_Target|Rows_Only_On_Source|Rows_Which_Differ"
    ev_data_list = hvr_client.get_hubs_events(
        hub=hub,
        channel=channel,
        fetch_results=True,
        result_pattern=result_pattern,
        type="Refresh",
        ev_id=refresh_ev_id,
    )

    pprint(ev_data_list)
    assert ev_data_list[refresh_ev_id]["state"] == "ACTIVE"

    cancel = hvr_client.post_hubs_events_cancel(hub=hub, ev_ids=[refresh_ev_id])

    assert cancel is None

    ev_data_list = hvr_client.get_hubs_events(
        hub=hub,
        channel=channel,
        fetch_results=True,
        result_pattern=result_pattern,
        type="Refresh",
        ev_id=refresh_ev_id,
    )

    assert ev_data_list[refresh_ev_id]["state"] == "CANCELED"


def test_refresh_result_ids():
    (hub, channel, source, target, refresh_ev_id, activate_ev_id) = _kickoff("rri")

    results_ids = hvr_client.get_hubs_channels_refresh_tables_results_ids(
        hub=hub, channel=channel
    )

    assert results_ids is not None


def test_schemas_tables():
    (hub, channel, source, target, refresh_ev_id, activate_ev_id) = _kickoff("st")

    schemas = hvr_client.get_hubs_locs_db_schemas(hub=hub, channel=channel, loc=source)

    assert schemas == {
        "default_schema": "public",
        "schemas": ["nodata", "pgbench", "public"],
    }

    tables = hvr_client.post_hubs_channels_locs_adapt_check(
        hub=hub,
        channel=channel,
        loc=source,
        add_tables=True,
        show_views=False,
        tables_in_channel={},
        mapspec={"tables": [{"schema": "nodata", "pattern": "*"}]},
    )

    assert tables == {
        "tables_in_channel": {},
        "add_tables": [
            {"base_name": "anothertable", "schema": "nodata", "type": "Table"},
            {"base_name": "emptytable", "schema": "nodata", "type": "Table"},
        ],
    }


def test_schemas_tables_already_added():
    (hub, channel, source, target, refresh_ev_id, activate_ev_id) = _kickoff("staa")

    schemas = hvr_client.get_hubs_locs_db_schemas(hub=hub, channel=channel, loc=source)

    assert schemas == {
        "default_schema": "public",
        "schemas": ["nodata", "pgbench", "public"],
    }

    tables = hvr_client.post_hubs_channels_locs_adapt_check(
        hub=hub,
        channel=channel,
        loc=source,
        add_tables=True,
        show_views=False,
        tables_in_channel={},
        mapspec={"tables": [{"schema": "public", "pattern": "*"}]},
    )

    pprint(tables)

    assert tables["tables_in_channel"] == {
        "customer": {
            "base_name": "customer",
            "exists_in_db": True,
            "matched_by_mapspec": True,
            "schema": "public",
            "type": "Table",
        }
    }
