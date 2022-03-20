# from pyhvr.pyhvr_exceptions import ConnectionError, LoginError, RestError, PyhvrError
from pprint import pprint
import time
import pyhvr
import os

schema_source = "TPCC"
schema_target = "target_tpcc"


def run_source_sql(sql):
    # very ugly, but gets the job done
    # os.system(
    #     f"docker exec oracle-source bash -c 'echo \"{sql}\" | sqlplus tpcc/Kiwi1234'"
    # )
    os.system(f"docker exec postgres-source psql --user=postgres -d tpcc -c '{sql}'")
    print(sql)
    pass


def run_target_sql(sql):
    # very ugly, but gets the job done
    os.system(f"docker exec postgres-target psql --user=postgres -d tpcc -c '{sql}'")
    print(sql)
    pass


def process_status(hvr_client, hub_name, channel, source, target):

    """
    Get process status:
        - activate, refresh, compare = event 'state'
        - capture, integrate = job 'state'
    """

    detail = process_detail(hvr_client, hub_name, channel, source, target)
    rt = {}
    for (k, v) in detail.items():
        rt[k] = v["state"]

    return rt


def process_detail(hvr_client, hub_name, channel, source, target):

    """
    Get all process details
    """

    rt = {}

    jobs = hvr_client.get_hubs_jobs(hub=hub_name)

    for job_name in jobs:
        if (
            job_name == f"{channel}-activate"
            or job_name == f"{channel}-refr-{source}-{target}"
            or job_name == f"{channel}-cmp-{source}-{target}"
        ):
            if job_name == f"{channel}-activate":
                short = "activate"
            elif job_name == f"{channel}-cmp-{source}-{target}":
                short = "compare"
            else:
                short = "refresh"
            result_pattern = "Table_State|Table_Start_Time|Source_Rows_Used|Subtasks_Done|Subtasks_Total|Subtasks_Busy|Rows_Only_On_Target|Rows_Only_On_Source|Rows_Which_Differ"
            event_status_rp = hvr_client.get_hubs_events(
                hub=hub_name,
                job=job_name,
                fetch_results=True,
                result_pattern=result_pattern,
                max_events=1,
            )
            for ev_id in event_status_rp:
                # there is one key, ev_id
                rt[short] = event_status_rp[ev_id]

        else:
            if job_name == f"{channel}-cap-{source}":
                rt["capture"] = jobs[job_name]
            elif job_name == f"{channel}-integ-{target}":
                rt["integrate"] = jobs[job_name]

    return rt


# -- wait for process to finish
def wait_for_status(
    process, target_state, hvr_client, hub_name, channel, source, target
):

    """
    Wait for a process to go into desired status
    """

    print(f"Wait for {process} to be {target_state}...")
    while True:
        pstatus = process_status(hvr_client, hub_name, channel, source, target)

        if pstatus.get(process) == target_state:
            break
        time.sleep(5)


def setup_replication(hvr_client, suffix):
    loc = hvr_client.post_hubs_definition_locs(
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
            # "Database_User": "tpcc",
            # "Database_Password": "Kiwi1234",
            # "Class": "oracle",
            # "Capture_Method": "DIRECT",
            # "Oracle_SID": "XE",
            # "Oracle_Home": "/u01/app/oracle/product/11.2.0/xe",
            # "Agent_Host": "oracle-source",
            "Agent_Host": "rtdsagent-1",
            "Agent_Port": "4343",
            "Case_Sensitive_Names": True,
        },
    )

    assert loc is None

    loc = hvr_client.post_hubs_definition_locs(
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
                "params": {"Method": "BURST"},
                "table_scope": "*",
                "type": "Integrate",
            },
            # {
            #     "type": "ColumnProperties",
            #     "loc_scope": "SOURCE",
            #     "table_scope": "*",
            #     "params": {"CaptureFromRowId": True, "Name": "_fivetran_id"},
            # }
        ],
    )
    assert ch is None

    return ("hvrhub", "chan" + suffix, "source" + suffix, "target" + suffix)


def test_init():
    hvr_sm_client = pyhvr.client_setup_mode(uri="http://localhost:4340")

    run_source_sql("create table testtable (i smallint);")

    run_target_sql(f"CREATE SCHEMA {schema_target}")
    run_target_sql(f"GRANT ALL ON SCHEMA {schema_target} TO postgres")
    run_target_sql(f"GRANT ALL ON ALL TABLES IN SCHEMA {schema_target} TO postgres")

    props = hvr_sm_client.patch_hubserver_props(
        HTTP_Port="4340",
        Database_Host="pghub",
        Database_Port=5432,
        Database_Name="pghub",
        Database_User="postgres",
        Database_Password="Kiwi1234",
        Repository_Class="postgresql",
        Setup_Mode=True,
    )

    pprint(props)

    create_repo = hvr_sm_client.post_repos()

    pprint(create_repo)

    license_file = "hvr.lic"
    with open("tests/" + license_file, "r") as fd:
        license_data = fd.read()

    lic = hvr_sm_client.post_licenses(license=license_file, raw=license_data)

    pprint(lic)

    wallet = hvr_sm_client.post_wallet(props={"Type": "SOFTWARE", "Auto_Open": True})

    pprint(wallet)

    user = hvr_sm_client.post_users(
        authentication="local",
        password="Kiwi1234Kiwi1234",
        props={"Full_Name": "Admin User"},
        user="admin",
    )

    pprint(user)

    repo_props = hvr_sm_client.patch_repos_props(
        Access_List=[{"user": "admin", "level": "SysAdmin"}]
    )

    pprint(repo_props)

    hvr_client = pyhvr.client(
        username="admin", password="Kiwi1234Kiwi1234", uri="http://localhost:4340"
    )

    hub_create = hvr_client.post_hubs(
        hub="hvrhub",
        props={
            "Description": "HubDesc",
            "Access_List": [
                {"user": "admin", "level": "HubOwner"},
                {"level": "ReadOnly"},
            ],
        },
    )

    pprint(hub_create)

    disable_sm = hvr_client.patch_hubserver_props(Setup_Mode=None)

    pprint(disable_sm)

    current_repo_props = hvr_client.get_repos_props()

    pprint("current_repo_props")
    pprint(current_repo_props)

    # for agent_id in ["oracle-source", "rtdsagent-2"]:
    for agent_id in ["rtdsagent-1", "rtdsagent-2"]:

        agent_info = hvr_client.post_hubs_new_loc_agent_get(
            hub="hvrhub",
            loc_props={
                "Class": "postgresql",
                "Agent_Host": agent_id,
                "Agent_Port": 4343,
            },
        )

        pprint("agent_info")
        pprint(agent_info)

        agent_test = hvr_client.post_hubs_new_loc_agent_test(
            hub="hvrhub",
            loc_props={
                "Class": "postgresql",
                "Agent_Host": agent_id,
                "Agent_Port": 4343,
            },
            setup_timed=agent_info["setup_timed"],
        )

        pprint("agent_info")
        pprint(agent_test)
        a_p = agent_test["discovered_props"]

        agent_setup = hvr_client.post_hubs_new_loc_agent_props_patch(
            hub="hvrhub",
            loc_props={
                "Agent_HVR_CONFIG": a_p["Agent_HVR_CONFIG"],
                "Agent_HVR_HOME": a_p["Agent_HVR_HOME"],
                "Agent_Operating_System": a_p["Agent_Operating_System"],
                "Agent_Platform": a_p["Agent_Platform"],
                "Agent_Server_Public_Certificate": a_p[
                    "Agent_Server_Public_Certificate"
                ],
                "Agent_Version": a_p["Agent_Version"],
                "Agent_Host": agent_id,
                "Agent_Port": 4343,
                "Class": "postgres",
            },
            agent_props={
                "Setup_Mode_Timed_Until": None,
                "Only_From_Client_Public_Certificates": {
                    "http://rtdshub:4340/": current_repo_props[
                        "Agent_Client_Public_Certificate"
                    ]
                },
                "Anonymous_Access": {"allow": True},
            },
            setup_timed=agent_info["setup_timed"],
        )

        pprint("agent_setup")
        pprint(agent_setup)

    suffix = "dup"
    (hub, channel, source, target) = setup_replication(hvr_client, suffix)

    old_name = "testtable"  # old tbl_name
    new_table_name = (
        "unique_prefix_testtable"  # new tbl_name, to make burst tables glovally unique
    )
    # base_name = "TESTTABLE"
    base_name = "testtable"
    new_table_base_name = "testtable"

    # adapt_ddl_action = {
    #     "type": "AdaptDDL",
    #     "loc_scope": source,
    #     "table_scope": "*",
    #     "params": {
    #         "AddTablePattern": "*",
    #         "CaptureSchema": "TPCC",
    #         "IntegrateSchema": "renamed_tpcc",
    #         "OnDropTable": "DROP_FROM_CHANNEL_ONLY",
    #         "OnEnrollBreak": "REFRESH",
    #     },
    # }

    # adapt_ddl_enroll_action_src = {
    #     "type": "AdaptDDL",
    #     "loc_scope": source,
    #     "table_scope": "*",
    #     "params": {
    #             "AddTablePattern": "*",
    #             "CaptureSchema": schema_source,
    #             "IntegrateSchema": schema_target,
    #             "OnDropTable": "DROP_FROM_CHANNEL_ONLY",
    #             "OnEnrollBreak": "REFRESH",
    #     },
    # }

    # adapt_ddl_enroll_action_tgt = {
    #     "type": "AdaptDDL",
    #     "loc_scope": target,
    #     "table_scope": "*",
    #     "params": {
    #         "KeepExistingStructure": True,
    #         "OnEnrollBreak": "REFRESH",
    #     },
    # }

    rename_target_action = {
        "params": {"BaseName": new_table_base_name, "Schema": schema_target},
        "type": "TableProperties",
        "table_scope": new_table_name,
        "loc_scope": target,
    }

    # # F_JR2D33: Action AdaptDDL with parameter AddTablePattern is defined for location 'sourcedup' with class 'postgresql' which does not support the required capability 'AdaptDdlCap'.
    # hvr_client.patch_hubs_definition_channels_actions(
    #     hub=hub, channel=channel, actions=[adapt_ddl_action]
    # )
    # hvr_client.patch_hubs_definition_channels_actions(
    #     hub=hub, channel=channel, actions=[adapt_ddl_enroll_action_src]
    # )
    # hvr_client.patch_hubs_definition_channels_actions(
    #     hub=hub, channel=channel, actions=[adapt_ddl_enroll_action_tgt]
    # )

    add = hvr_client.post_hubs_channels_locs_adapt_apply(
        hub=hub,
        channel=channel,
        loc=source,
        add_table_group={"group": "GENERAL"},
        add_tables=True,
        mapspec={"tables": [{"schema": "public", "base_name": "testtable"}]},
    )

    assert add == {
        "add_tables": [
            {
                "base_name": "testtable",
                "schema": "public",
                "table": old_name,
                "type": "Table",
            }
        ]
    }

    # hvr_client.post_hubs_definition_channels_actions_delete(
    #     hub=hub,
    #     channel=channel,
    #     actions = [{
    #         "type": "ColumnProperties",
    #         "loc_scope": "SOURCE",
    #         "table_scope": "*",
    #         "params": {"CaptureFromRowId": True, "Name": "_fivetran_id"},
    #     }]
    # )

    hvr_client.post_hubs_definition_channels_tables_rename(
        hub=hub,
        channel=channel,
        table=old_name,
        new_name=new_table_name,
    )
    hvr_client.patch_hubs_definition_channels_tables_table(
        hub=hub,
        channel=channel,
        table=new_table_name,
        base_name=base_name,
        table_group="GENERAL",
    )
    hvr_client.patch_hubs_definition_channels_actions(
        hub=hub, channel=channel, actions=[rename_target_action]
    )

    refresh_data = {
        "start_immediate": False,
        "source_loc": source,
        "target_loc": target,
        "online_refresh": "read_write",
        "tables": [new_table_name],
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

    # assert jobs == {
    #     f"{channel}-activate": {"state": "RUNNING"},
    #     f"{channel}-refr-{source}-{target}": {"state": "SUSPEND"},
    # }

    wait_for_status("refresh", "DONE", hvr_client, hub, channel, source, target)
    wait_for_status("capture", "RUNNING", hvr_client, hub, channel, source, target)

    run_source_sql("alter table testtable add j smallint;")

    time.sleep(60)

    actions = hvr_client.get_hubs_definition_channels_actions(hub=hub, channel=channel)

    pprint(actions)

    query_tables = hvr_client.get_hubs_query_channels_tables(hub=hub, channel=channel)

    pprint(query_tables)

    run_target_sql("\\d target_tpcc.*")

    assert actions == [
        {"loc_scope": "SOURCE", "table_scope": "*", "type": "Capture"},
        {
            "loc_scope": "TARGET",
            "params": {"Method": "BURST"},
            "table_scope": "*",
            "type": "Integrate",
        },
        {
            "loc_scope": "targetdup",
            "params": {"BaseName": "testtable", "Schema": "target_tpcc"},
            "table_scope": "unique_prefix_testtable",
            "type": "TableProperties",
        },
    ]
