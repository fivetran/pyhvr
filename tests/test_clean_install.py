# from pyhvr.pyhvr_exceptions import ConnectionError, LoginError, RestError, PyhvrError
from pprint import pprint

import pyhvr


def test_init():
    hvr_sm_client = pyhvr.client_setup_mode(uri="http://localhost:4340")

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

    for agent_id in [1, 2]:

        agent_info = hvr_client.post_hubs_new_loc_agent_get(
            hub="hvrhub",
            loc_props={
                "Class": "postgresql",
                "Agent_Host": f"rtdsagent-{agent_id}",
                "Agent_Port": 4343,
            },
        )

        pprint("agent_info")
        pprint(agent_info)

        agent_test = hvr_client.post_hubs_new_loc_agent_test(
            hub="hvrhub",
            loc_props={
                "Class": "postgresql",
                "Agent_Host": f"rtdsagent-{agent_id}",
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
                "Agent_Host": f"rtdsagent-{agent_id}",
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

    # Just to test
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
            "Agent_Host": "rtdsagent-1",
            "Agent_Port": "4343",
        },
    )
    assert t["discovered_props"]["Class_Flavor"] == "vanilla"
    t = hvr_client.post_hubs_new_loc_test(
        hub="hvrhub",
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
    assert t["discovered_props"]["Class_Flavor"] == "vanilla"
