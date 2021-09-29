# PyHvr

A Python module to access the REST API of HVR (version 6).

This module is a wrapper of the API as described in https://www.hvr-software.com/docs/6/rest-api/rest-api-reference and thus the same documentation and the same workflow applies. This code is automatically generated and the function names are created from the API paths, too, although a few have been renamed to prevent duplicates.

## Usage

### Crate a client

The standard client needs username, password and the URI of the hub.

```python
import pyhvr
hvr_client = pyhvr.client(
    username="admin", password="password1234", uri="http://localhost:4340"
)
```

Creating a client does not establish a connection, it's a cheap operation that cannot fail. It is possible to call `hvr_client.login()` to force the login to happen and thus to check that the credentials and URI validity.

The explicit login call is optional - any further API operation will call login if necessary.

#### Setup mode

When the hub starts for the first time, there is no admin user created yet. It is possible to do the initial setup using PyHvr, too, using so called "setup mode client":

```python
import pyhvr
pyhvr.client_setup_mode(uri="http://localhost:4340")
```

See [tests/test_clean_install.py](tests/test_clean_install.py) for the required steps to set a valid license, create the admin user and hub repository database. The test also include steps to register new agents.

### Using the client

All error codes of the API (4xx, 5xx) are turned into Python exceptions. Generally, `ConnectionError` is for invalid URI or network issues, `LoginError` for invalid credentials and `RestError` for any error returned by the API. All of these derive from `PyhvrError`.

The returned value is a dictionary when the API returns JSON (vast majority of calls) or a string for text/plain.

The function parameters are either plain strings/numbers, or dictionaries. We understand that the use case for PyHvr is controlling or monitoring an HVR installation, not to do complex transformations on internal HVR objects. Thus we did not create bespoke classes for the different HVR objects like connections or locations; instead, we wanted to a simple-to-use module that makes day-to-day scripting easy.

```python
import pyhvr
hvr_client = pyhvr.client(
    username="admin", password="password1234", uri="http://localhost:4340"
)

try:
    hvr_client.put_hubs_definition_locs(
        hub="hvrhub",
        loc="sourceloc",
        props={
            "Database_Host": "postgres-source",
            "Database_Port": 5432,
            "Database_Name": "tpcc",
            "Database_User": "postgres",
            "Database_Password": "secret1234",
            "Class": "postgresql",
            "Capture_Method": "SQL",
            "Agent_Host": "agent-1",
            "Agent_Port": "4343",
        },
    )

    ...

    add = hvr_client.post_hubs_channels_locs_adapt_apply(
        hub="hvrhub",
        channel="channel",
        loc="sourceloc",
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
except when PyhvrError as e:
    print(e.message)
```

The `pytest` tests in [testing/](testing/) directory show more examples how to use this module.

## Generating PyHvr

The code used to generate the pyhvr module is a part of this repository, too. See [pyhvr-generate/](pyhvr-generate/). This code is tested by GitHub Workflow, too.

## Supported versions

Python versions 3.6, 3.7, 3.8 and 3.9 are tested and supported.

HVR 6.0.5 is the only support version at this time.
