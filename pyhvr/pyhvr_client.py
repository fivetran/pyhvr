import json
import time

import requests

import pyhvr.pyhvr_exceptions

# from pprint import pprint


class Client:
    username: str
    password: str
    uri: str
    bearer_token: str = None
    bearer_token_valid_until: int = 0
    setup_mode: bool = False

    def __init__(self, uri, setup_mode, username=None, password=None):
        self.username = username
        self.password = password
        self.uri = uri
        self.setup_mode = setup_mode

    def login(self):
        self.login_token()
        return None  # do not leak the token

    def header_nonauth(self):
        return {"Content-type": "application/json", "Accept": "application/json"}

    def header_auth(self, bearer_token):
        return {
            "Content-type": "application/json",
            "Accept": "application/json",
            "Authorization": "bearer " + bearer_token,
        }

    def login_token(self):
        # ToDo - use refresh token if possible
        if self.bearer_token_valid_until < time.time():
            try:
                if self.setup_mode:
                    rq = requests.post(
                        self.uri + "/auth/v1/setup",
                        headers=self.header_nonauth(),
                    )
                else:
                    rq = requests.post(
                        self.uri + "/auth/v1/password",
                        data=json.dumps(
                            {
                                "username": self.username,
                                "password": self.password,
                                "refresh": "token",
                            }
                        ),
                        headers=self.header_nonauth(),
                    )
                if rq.ok:
                    self.bearer_token = rq.json()["access_token"]
                    # Force renew 60 seconds before expiry
                    self.bearer_token_valid_until = time.time() + (
                        rq.json()["expires_in"] - 60
                    )
                    return self.bearer_token

            except Exception as e:
                raise pyhvr.pyhvr_exceptions.ConnectionError(
                    message="Cannot login: " + str(e)
                )

            raise pyhvr.pyhvr_exceptions.LoginError(
                status_code=rq.status_code, message=rq.text
            )

        else:
            return self.bearer_token

    def get(self, path, query, headers, payload, is_json):
        headers.update(self.header_auth(self.login_token()))
        rq = requests.get(
            self.uri + path,
            params=query,
            data=json.dumps(payload),
            headers=headers,
        )

        if rq.ok:
            if rq.text and is_json:
                return rq.json()
            elif rq.text:
                return rq.text
            else:
                return None

        raise pyhvr.pyhvr_exceptions.RestError(
            status_code=rq.status_code, message=rq.text
        )

    def post(self, path, query, headers, payload, is_json):
        headers.update(self.header_auth(self.login_token()))
        rq = requests.post(
            self.uri + path,
            params=query,
            data=json.dumps(payload),
            headers=headers,
        )

        if rq.ok:
            if rq.text and is_json:
                return rq.json()
            elif rq.text:
                return rq.text
            else:
                return None

        raise pyhvr.pyhvr_exceptions.RestError(
            status_code=rq.status_code, message=rq.text
        )

    def put(self, path, query, headers, payload, is_json):
        headers.update(self.header_auth(self.login_token()))
        rq = requests.put(
            self.uri + path,
            params=query,
            data=json.dumps(payload),
            headers=headers,
        )

        if rq.ok:
            if rq.text and is_json:
                return rq.json()
            elif rq.text:
                return rq.text
            else:
                return None

        raise pyhvr.pyhvr_exceptions.RestError(
            status_code=rq.status_code, message=rq.text
        )

    def delete(self, path, query, headers, payload, is_json):
        headers.update(self.header_auth(self.login_token()))
        rq = requests.delete(
            self.uri + path,
            params=query,
            data=json.dumps(payload),
            headers=headers,
        )

        if rq.ok:
            if rq.text and is_json:
                return rq.json()
            elif rq.text:
                return rq.text
            else:
                return None

        raise pyhvr.pyhvr_exceptions.RestError(
            status_code=rq.status_code, message=rq.text
        )

    def patch(self, path, query, headers, payload, is_json):
        headers.update(self.header_auth(self.login_token()))
        rq = requests.patch(
            self.uri + path,
            params=query,
            data=json.dumps(payload),
            headers=headers,
        )

        if rq.ok:
            if rq.text and is_json:
                return rq.json()
            elif rq.text:
                return rq.text
            else:
                return None

        raise pyhvr.pyhvr_exceptions.RestError(
            status_code=rq.status_code, message=rq.text
        )

    def from_bool(self, b):
        if b:
            return "true"
        else:
            return "false"

    def delete_hubs(self, hub):

        return self.delete(f"/api/v6.1.0.3/hubs/{hub}", None, {}, None, True)

    def delete_hubs_alerts(self, hub, alert):

        return self.delete(
            f"/api/v6.1.0.3/hubs/{hub}/alerts/{alert}", None, {}, None, True
        )

    def delete_hubs_definition_channels(self, hub, channel):

        return self.delete(
            f"/api/v6.1.0.3/hubs/{hub}/definition/channels/{channel}",
            None,
            {},
            None,
            True,
        )

    def delete_hubs_definition_channels_loc_groups(self, hub, channel, loc_group):

        return self.delete(
            f"/api/v6.1.0.3/hubs/{hub}/definition/channels/{channel}/loc_groups/{loc_group}",
            None,
            {},
            None,
            True,
        )

    def delete_hubs_definition_channels_loc_groups_members(
        self, hub, channel, loc_group, member
    ):

        return self.delete(
            f"/api/v6.1.0.3/hubs/{hub}/definition/channels/{channel}/loc_groups/{loc_group}/members/{member}",
            None,
            {},
            None,
            True,
        )

    def delete_hubs_definition_channels_tables(self, hub, channel, table):

        return self.delete(
            f"/api/v6.1.0.3/hubs/{hub}/definition/channels/{channel}/tables/{table}",
            None,
            {},
            None,
            True,
        )

    def delete_hubs_definition_locs(self, hub, loc):

        return self.delete(
            f"/api/v6.1.0.3/hubs/{hub}/definition/locs/{loc}", None, {}, None, True
        )

    def delete_hubs_definition_locs_props(self, hub, loc, prop):

        return self.delete(
            f"/api/v6.1.0.3/hubs/{hub}/definition/locs/{loc}/props/{prop}",
            None,
            {},
            None,
            True,
        )

    def delete_hubs_job_system_attributes(self, hub, attr):

        return self.delete(
            f"/api/v6.1.0.3/hubs/{hub}/job_system/attributes/{attr}",
            None,
            {},
            None,
            True,
        )

    def delete_hubs_job_system_env_vars(self, hub, var):

        return self.delete(
            f"/api/v6.1.0.3/hubs/{hub}/job_system/env_vars/{var}", None, {}, None, True
        )

    def delete_hubs_jobs(self, hub, job):

        return self.delete(f"/api/v6.1.0.3/hubs/{hub}/jobs/{job}", None, {}, None, True)

    def delete_hubs_jobs_attributes(self, hub, job, attr):

        return self.delete(
            f"/api/v6.1.0.3/hubs/{hub}/jobs/{job}/attributes/{attr}",
            None,
            {},
            None,
            True,
        )

    def delete_hubs_jobs_env_vars(self, hub, job, var):

        return self.delete(
            f"/api/v6.1.0.3/hubs/{hub}/jobs/{job}/env_vars/{var}", None, {}, None, True
        )

    def delete_licenses(self, license):

        return self.delete(f"/api/v6.1.0.3/licenses/{license}", None, {}, None, True)

    def delete_repos(self):

        return self.delete("/api/v6.1.0.3/repos", None, {}, None, True)

    def delete_users(self, user):

        return self.delete(f"/api/v6.1.0.3/users/{user}", None, {}, None, True)

    def get_api(self):

        return self.get("/api", None, {}, None, True)

    def get_hubs(self):

        return self.get("/api/v6.1.0.3/hubs", None, {}, None, True)

    def get_hubs_activate(self, hub, channels=None, locs=None):
        query = {}
        if channels:
            query["channels"] = channels
        if locs:
            query["locs"] = locs

        return self.get(f"/api/v6.1.0.3/hubs/{hub}/activate", query, {}, None, True)

    def get_hubs_alerts(self, hub):

        return self.get(f"/api/v6.1.0.3/hubs/{hub}/alerts", None, {}, None, True)

    def get_hubs_alerts_props(
        self, hub, alert, fetch=None, x_hvr_classified_access=None
    ):
        query = {}
        if fetch:
            query["fetch"] = fetch
        headers = {}
        if x_hvr_classified_access:
            headers["X-Hvr-Classified-Access"] = x_hvr_classified_access

        return self.get(
            f"/api/v6.1.0.3/hubs/{hub}/alerts/{alert}/props", query, headers, None, True
        )

    def get_hubs_channels_activate(self, hub, channel, locs=None):
        query = {}
        if locs:
            query["locs"] = locs

        return self.get(
            f"/api/v6.1.0.3/hubs/{hub}/channels/{channel}/activate",
            query,
            {},
            None,
            True,
        )

    def get_hubs_channels_compare_tables_results_ids(
        self,
        hub,
        channel,
        result_pattern=None,
        source_loc=None,
        target_loc=None,
        table=None,
        ev_tstamp_begin=None,
        ev_tstamp_end=None,
    ):
        query = {}
        if result_pattern:
            query["result_pattern"] = result_pattern
        if source_loc:
            query["source_loc"] = source_loc
        if target_loc:
            query["target_loc"] = target_loc
        if table:
            query["table"] = table
        if ev_tstamp_begin:
            query["ev_tstamp_begin"] = ev_tstamp_begin
        if ev_tstamp_end:
            query["ev_tstamp_end"] = ev_tstamp_end

        return self.get(
            f"/api/v6.1.0.3/hubs/{hub}/channels/{channel}/compare/tables_results_ids",
            query,
            {},
            None,
            True,
        )

    def get_hubs_channels_contexts(self, hub, channel):

        return self.get(
            f"/api/v6.1.0.3/hubs/{hub}/channels/{channel}/contexts",
            None,
            {},
            None,
            True,
        )

    def get_hubs_channels_controls(
        self, hub, channel, task_name=None, loc_name=None, ctrl_name=None, ctrl_id=None
    ):
        query = {}
        if task_name:
            query["task_name"] = task_name
        if loc_name:
            query["loc_name"] = loc_name
        if ctrl_name:
            query["ctrl_name"] = ctrl_name
        if ctrl_id:
            query["ctrl_id"] = ctrl_id

        return self.get(
            f"/api/v6.1.0.3/hubs/{hub}/channels/{channel}/controls",
            query,
            {},
            None,
            True,
        )

    def get_hubs_channels_controls_ctrl_id(self, hub, channel, ctrl_id):

        return self.get(
            f"/api/v6.1.0.3/hubs/{hub}/channels/{channel}/controls/{ctrl_id}",
            None,
            {},
            None,
            True,
        )

    def get_hubs_channels_locs_capture_open_tx(self, hub, channel, loc):

        return self.get(
            f"/api/v6.1.0.3/hubs/{hub}/channels/{channel}/locs/{loc}/capture_open_tx",
            None,
            {},
            None,
            True,
        )

    def get_hubs_channels_locs_integrate_point(
        self, hub, channel, loc, orig_channel=None, orig_integ_loc=None
    ):
        query = {}
        if orig_channel:
            query["orig_channel"] = orig_channel
        if orig_integ_loc:
            query["orig_integ_loc"] = orig_integ_loc

        return self.get(
            f"/api/v6.1.0.3/hubs/{hub}/channels/{channel}/locs/{loc}/integrate_point",
            query,
            {},
            None,
            True,
        )

    def get_hubs_channels_refresh_tables_results_ids(
        self,
        hub,
        channel,
        result_pattern=None,
        source_loc=None,
        target_loc=None,
        table=None,
        ev_tstamp_begin=None,
        ev_tstamp_end=None,
    ):
        query = {}
        if result_pattern:
            query["result_pattern"] = result_pattern
        if source_loc:
            query["source_loc"] = source_loc
        if target_loc:
            query["target_loc"] = target_loc
        if table:
            query["table"] = table
        if ev_tstamp_begin:
            query["ev_tstamp_begin"] = ev_tstamp_begin
        if ev_tstamp_end:
            query["ev_tstamp_end"] = ev_tstamp_end

        return self.get(
            f"/api/v6.1.0.3/hubs/{hub}/channels/{channel}/refresh/tables_results_ids",
            query,
            {},
            None,
            True,
        )

    def get_hubs_compare_tables_results_ids(
        self,
        hub,
        channel=None,
        result_pattern=None,
        source_loc=None,
        target_loc=None,
        table=None,
        ev_tstamp_begin=None,
        ev_tstamp_end=None,
    ):
        query = {}
        if channel:
            query["channel"] = channel
        if result_pattern:
            query["result_pattern"] = result_pattern
        if source_loc:
            query["source_loc"] = source_loc
        if target_loc:
            query["target_loc"] = target_loc
        if table:
            query["table"] = table
        if ev_tstamp_begin:
            query["ev_tstamp_begin"] = ev_tstamp_begin
        if ev_tstamp_end:
            query["ev_tstamp_end"] = ev_tstamp_end

        return self.get(
            f"/api/v6.1.0.3/hubs/{hub}/compare/tables_results_ids",
            query,
            {},
            None,
            True,
        )

    def get_hubs_definition(
        self,
        hub,
        fetch=None,
        channel=None,
        loc=None,
        table=None,
        action_type=None,
        cache_view_tstamp=None,
        x_hvr_classified_access=None,
    ):
        query = {}
        if fetch:
            query["fetch"] = fetch
        if channel:
            query["channel"] = channel
        if loc:
            query["loc"] = loc
        if table:
            query["table"] = table
        if action_type:
            query["action_type"] = action_type
        if cache_view_tstamp:
            query["cache_view_tstamp"] = cache_view_tstamp
        headers = {}
        if x_hvr_classified_access:
            headers["X-Hvr-Classified-Access"] = x_hvr_classified_access

        return self.get(
            f"/api/v6.1.0.3/hubs/{hub}/definition", query, headers, None, True
        )

    def get_hubs_definition_change_events(
        self,
        hub,
        direction=None,
        channel=None,
        loc=None,
        ev_tstamp_begin=None,
        ev_tstamp_end=None,
        ev_id=None,
        x_hvr_classified_access=None,
    ):
        query = {}
        if direction:
            query["direction"] = direction
        if channel:
            query["channel"] = channel
        if loc:
            query["loc"] = loc
        if ev_tstamp_begin:
            query["ev_tstamp_begin"] = ev_tstamp_begin
        if ev_tstamp_end:
            query["ev_tstamp_end"] = ev_tstamp_end
        if ev_id:
            query["ev_id"] = ev_id
        headers = {}
        if x_hvr_classified_access:
            headers["X-Hvr-Classified-Access"] = x_hvr_classified_access

        return self.get(
            f"/api/v6.1.0.3/hubs/{hub}/definition/change/events",
            query,
            headers,
            None,
            True,
        )

    def get_hubs_definition_channels(
        self,
        hub,
        fetch=None,
        channel=None,
        table=None,
        action_type=None,
        cache_view_tstamp=None,
    ):
        query = {}
        if fetch:
            query["fetch"] = fetch
        if channel:
            query["channel"] = channel
        if table:
            query["table"] = table
        if action_type:
            query["action_type"] = action_type
        if cache_view_tstamp:
            query["cache_view_tstamp"] = cache_view_tstamp

        return self.get(
            f"/api/v6.1.0.3/hubs/{hub}/definition/channels", query, {}, None, True
        )

    def get_hubs_definition_channels_actions(
        self, hub, channel, action_type=None, cache_view_tstamp=None
    ):
        query = {}
        if action_type:
            query["action_type"] = action_type
        if cache_view_tstamp:
            query["cache_view_tstamp"] = cache_view_tstamp

        return self.get(
            f"/api/v6.1.0.3/hubs/{hub}/definition/channels/{channel}/actions",
            query,
            {},
            None,
            True,
        )

    def get_hubs_definition_channels_channel(
        self,
        hub,
        channel,
        fetch=None,
        table=None,
        action_type=None,
        cache_view_tstamp=None,
    ):
        query = {}
        if fetch:
            query["fetch"] = fetch
        if table:
            query["table"] = table
        if action_type:
            query["action_type"] = action_type
        if cache_view_tstamp:
            query["cache_view_tstamp"] = cache_view_tstamp

        return self.get(
            f"/api/v6.1.0.3/hubs/{hub}/definition/channels/{channel}",
            query,
            {},
            None,
            True,
        )

    def get_hubs_definition_channels_loc_groups(
        self, hub, channel, fetch=None, cache_view_tstamp=None
    ):
        query = {}
        if fetch:
            query["fetch"] = fetch
        if cache_view_tstamp:
            query["cache_view_tstamp"] = cache_view_tstamp

        return self.get(
            f"/api/v6.1.0.3/hubs/{hub}/definition/channels/{channel}/loc_groups",
            query,
            {},
            None,
            True,
        )

    def get_hubs_definition_channels_loc_groups_group(
        self, hub, channel, loc_group, fetch=None, cache_view_tstamp=None
    ):
        query = {}
        if fetch:
            query["fetch"] = fetch
        if cache_view_tstamp:
            query["cache_view_tstamp"] = cache_view_tstamp

        return self.get(
            f"/api/v6.1.0.3/hubs/{hub}/definition/channels/{channel}/loc_groups/{loc_group}",
            query,
            {},
            None,
            True,
        )

    def get_hubs_definition_channels_loc_groups_members(self, hub, channel, loc_group):

        return self.get(
            f"/api/v6.1.0.3/hubs/{hub}/definition/channels/{channel}/loc_groups/{loc_group}/members",
            None,
            {},
            None,
            True,
        )

    def get_hubs_definition_channels_tables(
        self, hub, channel, fetch=None, table=None, cache_view_tstamp=None
    ):
        query = {}
        if fetch:
            query["fetch"] = fetch
        if table:
            query["table"] = table
        if cache_view_tstamp:
            query["cache_view_tstamp"] = cache_view_tstamp

        return self.get(
            f"/api/v6.1.0.3/hubs/{hub}/definition/channels/{channel}/tables",
            query,
            {},
            None,
            True,
        )

    def get_hubs_definition_channels_tables_cols(self, hub, channel, table):

        return self.get(
            f"/api/v6.1.0.3/hubs/{hub}/definition/channels/{channel}/tables/{table}/cols",
            None,
            {},
            None,
            True,
        )

    def get_hubs_definition_channels_tables_table(
        self, hub, channel, table, fetch=None, cache_view_tstamp=None
    ):
        query = {}
        if fetch:
            query["fetch"] = fetch
        if cache_view_tstamp:
            query["cache_view_tstamp"] = cache_view_tstamp

        return self.get(
            f"/api/v6.1.0.3/hubs/{hub}/definition/channels/{channel}/tables/{table}",
            query,
            {},
            None,
            True,
        )

    def get_hubs_definition_hub_actions(
        self, hub, action_type=None, cache_view_tstamp=None
    ):
        query = {}
        if action_type:
            query["action_type"] = action_type
        if cache_view_tstamp:
            query["cache_view_tstamp"] = cache_view_tstamp

        return self.get(
            f"/api/v6.1.0.3/hubs/{hub}/definition/hub_actions", query, {}, None, True
        )

    def get_hubs_definition_locs(
        self,
        hub,
        fetch=None,
        loc=None,
        action_type=None,
        cache_view_tstamp=None,
        x_hvr_classified_access=None,
    ):
        query = {}
        if fetch:
            query["fetch"] = fetch
        if loc:
            query["loc"] = loc
        if action_type:
            query["action_type"] = action_type
        if cache_view_tstamp:
            query["cache_view_tstamp"] = cache_view_tstamp
        headers = {}
        if x_hvr_classified_access:
            headers["X-Hvr-Classified-Access"] = x_hvr_classified_access

        return self.get(
            f"/api/v6.1.0.3/hubs/{hub}/definition/locs", query, headers, None, True
        )

    def get_hubs_definition_locs_actions(
        self, hub, loc, action_type=None, cache_view_tstamp=None
    ):
        query = {}
        if action_type:
            query["action_type"] = action_type
        if cache_view_tstamp:
            query["cache_view_tstamp"] = cache_view_tstamp

        return self.get(
            f"/api/v6.1.0.3/hubs/{hub}/definition/locs/{loc}/actions",
            query,
            {},
            None,
            True,
        )

    def get_hubs_definition_locs_loc(
        self,
        hub,
        loc,
        fetch=None,
        action_type=None,
        cache_view_tstamp=None,
        x_hvr_classified_access=None,
    ):
        query = {}
        if fetch:
            query["fetch"] = fetch
        if action_type:
            query["action_type"] = action_type
        if cache_view_tstamp:
            query["cache_view_tstamp"] = cache_view_tstamp
        headers = {}
        if x_hvr_classified_access:
            headers["X-Hvr-Classified-Access"] = x_hvr_classified_access

        return self.get(
            f"/api/v6.1.0.3/hubs/{hub}/definition/locs/{loc}",
            query,
            headers,
            None,
            True,
        )

    def get_hubs_definition_locs_props(self, hub, loc, x_hvr_classified_access=None):

        headers = {}
        if x_hvr_classified_access:
            headers["X-Hvr-Classified-Access"] = x_hvr_classified_access

        return self.get(
            f"/api/v6.1.0.3/hubs/{hub}/definition/locs/{loc}/props",
            None,
            headers,
            None,
            True,
        )

    def get_hubs_dirs(self, hub, path=None, pattern=None):
        query = {}
        if path:
            query["path"] = path
        if pattern:
            query["pattern"] = pattern

        return self.get(f"/api/v6.1.0.3/hubs/{hub}/dirs", query, {}, None, True)

    def get_hubs_event_channels(
        self,
        hub,
        type=None,
        state=None,
        loc=None,
        fetch_repos_events=None,
        ev_tstamp_begin=None,
        ev_tstamp_end=None,
    ):
        query = {}
        if type:
            query["type"] = type
        if state:
            query["state"] = state
        if loc:
            query["loc"] = loc
        if fetch_repos_events:
            query["fetch_repos_events"] = self.from_bool(fetch_repos_events)
        if ev_tstamp_begin:
            query["ev_tstamp_begin"] = ev_tstamp_begin
        if ev_tstamp_end:
            query["ev_tstamp_end"] = ev_tstamp_end

        return self.get(
            f"/api/v6.1.0.3/hubs/{hub}/event_channels", query, {}, None, True
        )

    def get_hubs_event_locs(
        self,
        hub,
        channel=None,
        type=None,
        state=None,
        fetch_repos_events=None,
        ev_tstamp_begin=None,
        ev_tstamp_end=None,
    ):
        query = {}
        if channel:
            query["channel"] = channel
        if type:
            query["type"] = type
        if state:
            query["state"] = state
        if fetch_repos_events:
            query["fetch_repos_events"] = self.from_bool(fetch_repos_events)
        if ev_tstamp_begin:
            query["ev_tstamp_begin"] = ev_tstamp_begin
        if ev_tstamp_end:
            query["ev_tstamp_end"] = ev_tstamp_end

        return self.get(f"/api/v6.1.0.3/hubs/{hub}/event_locs", query, {}, None, True)

    def get_hubs_event_types(
        self,
        hub,
        channel=None,
        state=None,
        loc=None,
        fetch_repos_events=None,
        ev_tstamp_begin=None,
        ev_tstamp_end=None,
    ):
        query = {}
        if channel:
            query["channel"] = channel
        if state:
            query["state"] = state
        if loc:
            query["loc"] = loc
        if fetch_repos_events:
            query["fetch_repos_events"] = self.from_bool(fetch_repos_events)
        if ev_tstamp_begin:
            query["ev_tstamp_begin"] = ev_tstamp_begin
        if ev_tstamp_end:
            query["ev_tstamp_end"] = ev_tstamp_end

        return self.get(f"/api/v6.1.0.3/hubs/{hub}/event_types", query, {}, None, True)

    def get_hubs_events(
        self,
        hub,
        channel=None,
        ev_id=None,
        type=None,
        state=None,
        current_only=None,
        loc=None,
        job=None,
        body_pattern=None,
        fetch_results=None,
        fetch_repos_events=None,
        result_pattern=None,
        result_table=None,
        ev_tstamp_begin=None,
        ev_tstamp_end=None,
        updated_begin=None,
        updated_end=None,
        max_events=None,
    ):
        query = {}
        if channel:
            query["channel"] = channel
        if ev_id:
            query["ev_id"] = ev_id
        if type:
            query["type"] = type
        if state:
            query["state"] = state
        if current_only:
            query["current_only"] = self.from_bool(current_only)
        if loc:
            query["loc"] = loc
        if job:
            query["job"] = job
        if body_pattern:
            query["body_pattern"] = body_pattern
        if fetch_results:
            query["fetch_results"] = self.from_bool(fetch_results)
        if fetch_repos_events:
            query["fetch_repos_events"] = self.from_bool(fetch_repos_events)
        if result_pattern:
            query["result_pattern"] = result_pattern
        if result_table:
            query["result_table"] = result_table
        if ev_tstamp_begin:
            query["ev_tstamp_begin"] = ev_tstamp_begin
        if ev_tstamp_end:
            query["ev_tstamp_end"] = ev_tstamp_end
        if updated_begin:
            query["updated_begin"] = updated_begin
        if updated_end:
            query["updated_end"] = updated_end
        if max_events:
            query["max_events"] = max_events

        return self.get(f"/api/v6.1.0.3/hubs/{hub}/events", query, {}, None, True)

    def get_hubs_events_log(
        self, hub, ev_id, max_lines=None, head_crc=None, offset_begin=None, archive=None
    ):
        query = {}
        if max_lines:
            query["max_lines"] = max_lines
        if head_crc:
            query["head_crc"] = head_crc
        if offset_begin:
            query["offset_begin"] = offset_begin
        if archive:
            query["archive"] = archive

        return self.get(
            f"/api/v6.1.0.3/hubs/{hub}/events/{ev_id}/log", query, {}, None, False
        )

    def get_hubs_hub(self, hub):

        return self.get(f"/api/v6.1.0.3/hubs/{hub}", None, {}, None, True)

    def get_hubs_job_system_attributes(self, hub):

        return self.get(
            f"/api/v6.1.0.3/hubs/{hub}/job_system/attributes", None, {}, None, True
        )

    def get_hubs_job_system_env_vars(self, hub):

        return self.get(
            f"/api/v6.1.0.3/hubs/{hub}/job_system/env_vars", None, {}, None, True
        )

    def get_hubs_jobs(
        self,
        hub,
        channel=None,
        job=None,
        updated_jobs_since=None,
        updated_err_since=None,
        fetch=None,
    ):
        query = {}
        if channel:
            query["channel"] = channel
        if job:
            query["job"] = job
        if updated_jobs_since:
            query["updated_jobs_since"] = updated_jobs_since
        if updated_err_since:
            query["updated_err_since"] = updated_err_since
        if fetch:
            query["fetch"] = fetch

        return self.get(f"/api/v6.1.0.3/hubs/{hub}/jobs", query, {}, None, True)

    def get_hubs_jobs_attributes(self, hub, job):

        return self.get(
            f"/api/v6.1.0.3/hubs/{hub}/jobs/{job}/attributes", None, {}, None, True
        )

    def get_hubs_jobs_controls_log(
        self,
        hub,
        job,
        ctrl_id,
        max_lines=None,
        head_crc=None,
        offset_begin=None,
        archive=None,
    ):
        query = {}
        if max_lines:
            query["max_lines"] = max_lines
        if head_crc:
            query["head_crc"] = head_crc
        if offset_begin:
            query["offset_begin"] = offset_begin
        if archive:
            query["archive"] = archive

        return self.get(
            f"/api/v6.1.0.3/hubs/{hub}/jobs/{job}/controls/{ctrl_id}/log",
            query,
            {},
            None,
            False,
        )

    def get_hubs_jobs_env_vars(self, hub, job):

        return self.get(
            f"/api/v6.1.0.3/hubs/{hub}/jobs/{job}/env_vars", None, {}, None, True
        )

    def get_hubs_locs_activate(self, hub, loc):

        return self.get(
            f"/api/v6.1.0.3/hubs/{hub}/locs/{loc}/activate", None, {}, None, True
        )

    def get_hubs_locs_agent(self, hub, loc):

        return self.get(
            f"/api/v6.1.0.3/hubs/{hub}/locs/{loc}/agent", None, {}, None, True
        )

    def get_hubs_locs_db_schemas(self, hub, loc, channel=None):
        query = {}
        if channel:
            query["channel"] = channel

        return self.get(
            f"/api/v6.1.0.3/hubs/{hub}/locs/{loc}/db/schemas", query, {}, None, True
        )

    def get_hubs_locs_dirs(
        self, hub, loc, path=None, pattern=None, local=None, channel=None
    ):
        query = {}
        if path:
            query["path"] = path
        if pattern:
            query["pattern"] = pattern
        if local:
            query["local"] = self.from_bool(local)
        if channel:
            query["channel"] = channel

        return self.get(
            f"/api/v6.1.0.3/hubs/{hub}/locs/{loc}/dirs", query, {}, None, True
        )

    def get_hubs_locs_env_odbc_drivers(
        self, hub, loc, odbcinst=None, odbcsysini=None, channel=None
    ):
        query = {}
        if odbcinst:
            query["odbcinst"] = odbcinst
        if odbcsysini:
            query["odbcsysini"] = odbcsysini
        if channel:
            query["channel"] = channel

        return self.get(
            f"/api/v6.1.0.3/hubs/{hub}/locs/{loc}/env/odbc_drivers",
            query,
            {},
            None,
            True,
        )

    def get_hubs_locs_env_oratab(self, hub, loc, channel=None):
        query = {}
        if channel:
            query["channel"] = channel

        return self.get(
            f"/api/v6.1.0.3/hubs/{hub}/locs/{loc}/env/oratab", query, {}, None, True
        )

    def get_hubs_locs_env_vars(self, hub, loc, vars=None, channel=None):
        query = {}
        if vars:
            query["vars"] = vars
        if channel:
            query["channel"] = channel

        return self.get(
            f"/api/v6.1.0.3/hubs/{hub}/locs/{loc}/env/vars", query, {}, None, True
        )

    def get_hubs_logs(
        self,
        hub,
        file,
        max_lines=None,
        head_crc=None,
        offset_begin=None,
        offset_begin_limit=None,
        offset_end=None,
        search_eof=None,
    ):
        query = {}
        if max_lines:
            query["max_lines"] = max_lines
        if head_crc:
            query["head_crc"] = head_crc
        if offset_begin:
            query["offset_begin"] = offset_begin
        if offset_begin_limit:
            query["offset_begin_limit"] = offset_begin_limit
        if offset_end:
            query["offset_end"] = offset_end
        if search_eof:
            query["search_eof"] = self.from_bool(search_eof)

        return self.get(f"/api/v6.1.0.3/hubs/{hub}/logs/{file}", query, {}, None, False)

    def get_hubs_logs_archive(
        self,
        hub,
        file,
        archive,
        max_lines=None,
        offset_begin=None,
        offset_end=None,
        search_eof=None,
    ):
        query = {}
        if max_lines:
            query["max_lines"] = max_lines
        if offset_begin:
            query["offset_begin"] = offset_begin
        if offset_end:
            query["offset_end"] = offset_end
        if search_eof:
            query["search_eof"] = self.from_bool(search_eof)

        return self.get(
            f"/api/v6.1.0.3/hubs/{hub}/logs/{file}/archive/{archive}",
            query,
            {},
            None,
            False,
        )

    def get_hubs_logs_search(self, hub, file, search_tstamp=None):
        query = {}
        if search_tstamp:
            query["search_tstamp"] = search_tstamp

        return self.get(
            f"/api/v6.1.0.3/hubs/{hub}/logs/{file}/search", query, {}, None, True
        )

    def get_hubs_props(self, hub, fetch=None):
        query = {}
        if fetch:
            query["fetch"] = fetch

        return self.get(f"/api/v6.1.0.3/hubs/{hub}/props", query, {}, None, True)

    def get_hubs_query_channels(
        self, hub, channel=None, loc=None, fetch=None, table=None
    ):
        query = {}
        if channel:
            query["channel"] = channel
        if loc:
            query["loc"] = loc
        if fetch:
            query["fetch"] = fetch
        if table:
            query["table"] = table

        return self.get(
            f"/api/v6.1.0.3/hubs/{hub}/query/channels", query, {}, None, True
        )

    def get_hubs_query_channels_locs(
        self, hub, channel, loc=None, fetch=None, table=None
    ):
        query = {}
        if loc:
            query["loc"] = loc
        if fetch:
            query["fetch"] = fetch
        if table:
            query["table"] = table

        return self.get(
            f"/api/v6.1.0.3/hubs/{hub}/query/channels/{channel}/locs",
            query,
            {},
            None,
            True,
        )

    def get_hubs_query_channels_locs_tables(
        self, hub, channel, loc, table, context=None
    ):
        query = {}
        if context:
            query["context"] = context

        return self.get(
            f"/api/v6.1.0.3/hubs/{hub}/query/channels/{channel}/locs/{loc}/tables/{table}",
            query,
            {},
            None,
            True,
        )

    def get_hubs_query_channels_tables(self, hub, channel, table=None):
        query = {}
        if table:
            query["table"] = table

        return self.get(
            f"/api/v6.1.0.3/hubs/{hub}/query/channels/{channel}/tables",
            query,
            {},
            None,
            True,
        )

    def get_hubs_query_status(self, hub):

        return self.get(f"/api/v6.1.0.3/hubs/{hub}/query/status", None, {}, None, True)

    def get_hubs_refresh_tables_results_ids(
        self,
        hub,
        channel=None,
        result_pattern=None,
        source_loc=None,
        target_loc=None,
        table=None,
        ev_tstamp_begin=None,
        ev_tstamp_end=None,
    ):
        query = {}
        if channel:
            query["channel"] = channel
        if result_pattern:
            query["result_pattern"] = result_pattern
        if source_loc:
            query["source_loc"] = source_loc
        if target_loc:
            query["target_loc"] = target_loc
        if table:
            query["table"] = table
        if ev_tstamp_begin:
            query["ev_tstamp_begin"] = ev_tstamp_begin
        if ev_tstamp_end:
            query["ev_tstamp_end"] = ev_tstamp_end

        return self.get(
            f"/api/v6.1.0.3/hubs/{hub}/refresh/tables_results_ids",
            query,
            {},
            None,
            True,
        )

    def get_hubs_stats_metrics(
        self,
        hub,
        fetch_values=None,
        channel=None,
        loc=None,
        table=None,
        metric=None,
        time_gran=None,
        scope=None,
        tstamp_begin=None,
        tstamp_end=None,
        updated_logs_since=None,
        updated_glob_since=None,
    ):
        query = {}
        if fetch_values:
            query["fetch_values"] = self.from_bool(fetch_values)
        if channel:
            query["channel"] = channel
        if loc:
            query["loc"] = loc
        if table:
            query["table"] = table
        if metric:
            query["metric"] = metric
        if time_gran:
            query["time_gran"] = time_gran
        if scope:
            query["scope"] = scope
        if tstamp_begin:
            query["tstamp_begin"] = tstamp_begin
        if tstamp_end:
            query["tstamp_end"] = tstamp_end
        if updated_logs_since:
            query["updated_logs_since"] = updated_logs_since
        if updated_glob_since:
            query["updated_glob_since"] = updated_glob_since

        return self.get(
            f"/api/v6.1.0.3/hubs/{hub}/stats/metrics", query, {}, None, True
        )

    def get_hubs_stats_oldest(self, hub, time_gran=None, scope=None):
        query = {}
        if time_gran:
            query["time_gran"] = time_gran
        if scope:
            query["scope"] = scope

        return self.get(f"/api/v6.1.0.3/hubs/{hub}/stats/oldest", query, {}, None, True)

    def get_hubs_users_props(self, hub, user, fetch=None):
        query = {}
        if fetch:
            query["fetch"] = fetch

        return self.get(
            f"/api/v6.1.0.3/hubs/{hub}/users/{user}/props", query, {}, None, True
        )

    def get_hubserver_clock(self):

        return self.get("/api/v6.1.0.3/hubserver/clock", None, {}, None, True)

    def get_hubserver_dirs(self, path=None, pattern=None):
        query = {}
        if path:
            query["path"] = path
        if pattern:
            query["pattern"] = pattern

        return self.get("/api/v6.1.0.3/hubserver/dirs", query, {}, None, True)

    def get_hubserver_env_odbc_drivers(self, odbcinst=None, odbcsysini=None):
        query = {}
        if odbcinst:
            query["odbcinst"] = odbcinst
        if odbcsysini:
            query["odbcsysini"] = odbcsysini

        return self.get(
            "/api/v6.1.0.3/hubserver/env/odbc_drivers", query, {}, None, True
        )

    def get_hubserver_env_oratab(self):

        return self.get("/api/v6.1.0.3/hubserver/env/oratab", None, {}, None, True)

    def get_hubserver_env_vars(self, vars=None):
        query = {}
        if vars:
            query["vars"] = vars

        return self.get("/api/v6.1.0.3/hubserver/env/vars", query, {}, None, True)

    def get_hubserver_props(self, fetch=None, x_hvr_classified_access=None):
        query = {}
        if fetch:
            query["fetch"] = fetch
        headers = {}
        if x_hvr_classified_access:
            headers["X-Hvr-Classified-Access"] = x_hvr_classified_access

        return self.get("/api/v6.1.0.3/hubserver/props", query, headers, None, True)

    def get_licenses(self, license=None):
        query = {}
        if license:
            query["license"] = license

        return self.get("/api/v6.1.0.3/licenses", query, {}, None, True)

    def get_licenses_license(self, license):

        return self.get(f"/api/v6.1.0.3/licenses/{license}", None, {}, None, False)

    def get_licensing(self):

        return self.get("/api/v6.1.0.3/licensing", None, {}, None, True)

    def get_logs(
        self,
        file,
        max_lines=None,
        head_crc=None,
        offset_begin=None,
        offset_begin_limit=None,
        offset_end=None,
        search_eof=None,
    ):
        query = {}
        if max_lines:
            query["max_lines"] = max_lines
        if head_crc:
            query["head_crc"] = head_crc
        if offset_begin:
            query["offset_begin"] = offset_begin
        if offset_begin_limit:
            query["offset_begin_limit"] = offset_begin_limit
        if offset_end:
            query["offset_end"] = offset_end
        if search_eof:
            query["search_eof"] = self.from_bool(search_eof)

        return self.get(f"/api/v6.1.0.3/logs/{file}", query, {}, None, False)

    def get_logs_archive(
        self,
        file,
        archive,
        max_lines=None,
        offset_begin=None,
        offset_end=None,
        search_eof=None,
    ):
        query = {}
        if max_lines:
            query["max_lines"] = max_lines
        if offset_begin:
            query["offset_begin"] = offset_begin
        if offset_end:
            query["offset_end"] = offset_end
        if search_eof:
            query["search_eof"] = self.from_bool(search_eof)

        return self.get(
            f"/api/v6.1.0.3/logs/{file}/archive/{archive}", query, {}, None, False
        )

    def get_metering_download(self, period_begin=None, period_end=None):
        query = {}
        if period_begin:
            query["period_begin"] = period_begin
        if period_end:
            query["period_end"] = period_end

        return self.get("/api/v6.1.0.3/metering/download", query, {}, None, True)

    def get_repos(self):

        return self.get("/api/v6.1.0.3/repos", None, {}, None, True)

    def get_repos_event_types(
        self, state=None, ev_tstamp_begin=None, ev_tstamp_end=None
    ):
        query = {}
        if state:
            query["state"] = state
        if ev_tstamp_begin:
            query["ev_tstamp_begin"] = ev_tstamp_begin
        if ev_tstamp_end:
            query["ev_tstamp_end"] = ev_tstamp_end

        return self.get("/api/v6.1.0.3/repos/event_types", query, {}, None, True)

    def get_repos_events(
        self,
        ev_id=None,
        type=None,
        state=None,
        body_pattern=None,
        ev_tstamp_begin=None,
        ev_tstamp_end=None,
        updated_begin=None,
        updated_end=None,
        max_events=None,
    ):
        query = {}
        if ev_id:
            query["ev_id"] = ev_id
        if type:
            query["type"] = type
        if state:
            query["state"] = state
        if body_pattern:
            query["body_pattern"] = body_pattern
        if ev_tstamp_begin:
            query["ev_tstamp_begin"] = ev_tstamp_begin
        if ev_tstamp_end:
            query["ev_tstamp_end"] = ev_tstamp_end
        if updated_begin:
            query["updated_begin"] = updated_begin
        if updated_end:
            query["updated_end"] = updated_end
        if max_events:
            query["max_events"] = max_events

        return self.get("/api/v6.1.0.3/repos/events", query, {}, None, True)

    def get_repos_props(self, fetch=None, x_hvr_classified_access=None):
        query = {}
        if fetch:
            query["fetch"] = fetch
        headers = {}
        if x_hvr_classified_access:
            headers["X-Hvr-Classified-Access"] = x_hvr_classified_access

        return self.get("/api/v6.1.0.3/repos/props", query, headers, None, True)

    def get_users(self, fetch=None):
        query = {}
        if fetch:
            query["fetch"] = fetch

        return self.get("/api/v6.1.0.3/users", query, {}, None, True)

    def get_users_props(self, user, fetch=None):
        query = {}
        if fetch:
            query["fetch"] = fetch

        return self.get(f"/api/v6.1.0.3/users/{user}/props", query, {}, None, True)

    def get_users_user(self, user, fetch=None):
        query = {}
        if fetch:
            query["fetch"] = fetch

        return self.get(f"/api/v6.1.0.3/users/{user}", query, {}, None, True)

    def get_wallet_props(self, fetch=None, x_hvr_classified_access=None):
        query = {}
        if fetch:
            query["fetch"] = fetch
        headers = {}
        if x_hvr_classified_access:
            headers["X-Hvr-Classified-Access"] = x_hvr_classified_access

        return self.get("/api/v6.1.0.3/wallet/props", query, headers, None, True)

    def patch_hubs_alerts_props(
        self, hub, alert, x_hvr_classified_transport_key=None, **payload
    ):

        headers = {}
        if x_hvr_classified_transport_key:
            headers["X-Hvr-Classified-Transport-Key"] = x_hvr_classified_transport_key

        return self.patch(
            f"/api/v6.1.0.3/hubs/{hub}/alerts/{alert}/props",
            None,
            headers,
            payload,
            True,
        )

    def patch_hubs_definition_channels(self, hub, channel, description):

        payload = {}
        payload["description"] = description
        return self.patch(
            f"/api/v6.1.0.3/hubs/{hub}/definition/channels/{channel}",
            None,
            {},
            payload,
            True,
        )

    def patch_hubs_definition_channels_actions(self, hub, channel, actions):

        payload = {}
        payload["actions"] = actions
        return self.patch(
            f"/api/v6.1.0.3/hubs/{hub}/definition/channels/{channel}/actions",
            None,
            {},
            payload,
            True,
        )

    def patch_hubs_definition_channels_loc_groups_members(
        self, hub, channel, loc_group, members
    ):

        payload = {}
        payload["members"] = members
        return self.patch(
            f"/api/v6.1.0.3/hubs/{hub}/definition/channels/{channel}/loc_groups/{loc_group}/members",
            None,
            {},
            payload,
            True,
        )

    def patch_hubs_definition_channels_tables(self, hub, channel, **payload):

        return self.patch(
            f"/api/v6.1.0.3/hubs/{hub}/definition/channels/{channel}/tables",
            None,
            {},
            payload,
            True,
        )

    def patch_hubs_definition_channels_tables_cols(
        self, hub, channel, table, **payload
    ):

        return self.patch(
            f"/api/v6.1.0.3/hubs/{hub}/definition/channels/{channel}/tables/{table}/cols",
            None,
            {},
            payload,
            True,
        )

    def patch_hubs_definition_channels_tables_table(
        self, hub, channel, table, base_name=None, table_group=None
    ):

        payload = {}
        if base_name is not None:
            payload["base_name"] = base_name
        if table_group is not None:
            payload["table_group"] = table_group
        return self.patch(
            f"/api/v6.1.0.3/hubs/{hub}/definition/channels/{channel}/tables/{table}",
            None,
            {},
            payload,
            True,
        )

    def patch_hubs_definition_hub_actions(self, hub, actions):

        payload = {}
        payload["actions"] = actions
        return self.patch(
            f"/api/v6.1.0.3/hubs/{hub}/definition/hub_actions", None, {}, payload, True
        )

    def patch_hubs_definition_locs_actions(self, hub, loc, actions):

        payload = {}
        payload["actions"] = actions
        return self.patch(
            f"/api/v6.1.0.3/hubs/{hub}/definition/locs/{loc}/actions",
            None,
            {},
            payload,
            True,
        )

    def patch_hubs_definition_locs_props(
        self, hub, loc, x_hvr_classified_transport_key=None, **payload
    ):

        headers = {}
        if x_hvr_classified_transport_key:
            headers["X-Hvr-Classified-Transport-Key"] = x_hvr_classified_transport_key

        return self.patch(
            f"/api/v6.1.0.3/hubs/{hub}/definition/locs/{loc}/props",
            None,
            headers,
            payload,
            True,
        )

    def patch_hubs_props(self, hub, **payload):

        return self.patch(f"/api/v6.1.0.3/hubs/{hub}/props", None, {}, payload, True)

    def patch_hubs_users_props(self, hub, user, **payload):

        return self.patch(
            f"/api/v6.1.0.3/hubs/{hub}/users/{user}/props", None, {}, payload, True
        )

    def patch_hubserver_props(self, x_hvr_classified_transport_key=None, **payload):

        headers = {}
        if x_hvr_classified_transport_key:
            headers["X-Hvr-Classified-Transport-Key"] = x_hvr_classified_transport_key

        return self.patch("/api/v6.1.0.3/hubserver/props", None, headers, payload, True)

    def patch_repos_props(self, x_hvr_classified_transport_key=None, **payload):

        headers = {}
        if x_hvr_classified_transport_key:
            headers["X-Hvr-Classified-Transport-Key"] = x_hvr_classified_transport_key

        return self.patch("/api/v6.1.0.3/repos/props", None, headers, payload, True)

    def patch_users_props(self, user, **payload):

        return self.patch(f"/api/v6.1.0.3/users/{user}/props", None, {}, payload, True)

    def post_hubs(self, hub, props=None):

        payload = {}
        payload["hub"] = hub
        if props is not None:
            payload["props"] = props
        return self.post("/api/v6.1.0.3/hubs", None, {}, payload, True)

    def post_hubs_alerts(self, hub, alert, props, x_hvr_classified_transport_key=None):

        headers = {}
        if x_hvr_classified_transport_key:
            headers["X-Hvr-Classified-Transport-Key"] = x_hvr_classified_transport_key
        payload = {}
        payload["alert"] = alert
        payload["props"] = props
        return self.post(
            f"/api/v6.1.0.3/hubs/{hub}/alerts", None, headers, payload, True
        )

    def post_hubs_alerts_clear(self, hub, alert):

        return self.post(
            f"/api/v6.1.0.3/hubs/{hub}/alerts/{alert}/clear", None, {}, None, True
        )

    def post_hubs_alerts_disable(self, hub, alert):

        return self.post(
            f"/api/v6.1.0.3/hubs/{hub}/alerts/{alert}/disable", None, {}, None, True
        )

    def post_hubs_alerts_execute(self, hub, alert):

        return self.post(
            f"/api/v6.1.0.3/hubs/{hub}/alerts/{alert}/execute", None, {}, None, False
        )

    def post_hubs_alerts_props_delete(self, hub, alert, props):

        payload = {}
        payload["props"] = props
        return self.post(
            f"/api/v6.1.0.3/hubs/{hub}/alerts/{alert}/props_delete",
            None,
            {},
            payload,
            True,
        )

    def post_hubs_alerts_test(self, hub, alert):

        return self.post(
            f"/api/v6.1.0.3/hubs/{hub}/alerts/{alert}/test", None, {}, None, False
        )

    def post_hubs_channels_activate(
        self,
        hub,
        channel,
        locs=None,
        tables=None,
        parallel_locs=None,
        components=None,
        start_immediate=None,
        replace_enroll=None,
        rewind_scan_start=None,
        rewind_emit=None,
        start_next_jobs=None,
        start_next_ev_ids=None,
    ):

        payload = {}
        if locs is not None:
            payload["locs"] = locs
        if tables is not None:
            payload["tables"] = tables
        if parallel_locs is not None:
            payload["parallel_locs"] = parallel_locs
        if components is not None:
            payload["components"] = components
        if start_immediate is not None:
            payload["start_immediate"] = self.from_bool(start_immediate)
        if replace_enroll is not None:
            payload["replace_enroll"] = self.from_bool(replace_enroll)
        if rewind_scan_start is not None:
            payload["rewind_scan_start"] = rewind_scan_start
        if rewind_emit is not None:
            payload["rewind_emit"] = rewind_emit
        if start_next_jobs is not None:
            payload["start_next_jobs"] = start_next_jobs
        if start_next_ev_ids is not None:
            payload["start_next_ev_ids"] = start_next_ev_ids
        return self.post(
            f"/api/v6.1.0.3/hubs/{hub}/channels/{channel}/activate",
            None,
            {},
            payload,
            True,
        )

    def post_hubs_channels_compare(
        self,
        hub,
        channel,
        source_loc,
        target_loc,
        contexts=None,
        granularity=None,
        difference_filter=None,
        quota_run=None,
        parallel_sessions=None,
        db_sequences=None,
        slicing=None,
        tables=None,
        task=None,
        context_variables=None,
        file_preread_subtasks=None,
        start_immediate=None,
        online_compare=None,
        online_compare_sleep=None,
        select_moment=None,
        save_diff_file=None,
        prereader_intermediate_files=None,
    ):

        payload = {}
        payload["source_loc"] = source_loc
        payload["target_loc"] = target_loc
        if contexts is not None:
            payload["contexts"] = contexts
        if granularity is not None:
            payload["granularity"] = granularity
        if difference_filter is not None:
            payload["difference_filter"] = difference_filter
        if quota_run is not None:
            payload["quota_run"] = quota_run
        if parallel_sessions is not None:
            payload["parallel_sessions"] = parallel_sessions
        if db_sequences is not None:
            payload["db_sequences"] = self.from_bool(db_sequences)
        if slicing is not None:
            payload["slicing"] = slicing
        if tables is not None:
            payload["tables"] = tables
        if task is not None:
            payload["task"] = task
        if context_variables is not None:
            payload["context_variables"] = context_variables
        if file_preread_subtasks is not None:
            payload["file_preread_subtasks"] = file_preread_subtasks
        if start_immediate is not None:
            payload["start_immediate"] = self.from_bool(start_immediate)
        if online_compare is not None:
            payload["online_compare"] = online_compare
        if online_compare_sleep is not None:
            payload["online_compare_sleep"] = online_compare_sleep
        if select_moment is not None:
            payload["select_moment"] = select_moment
        if save_diff_file is not None:
            payload["save_diff_file"] = self.from_bool(save_diff_file)
        if prereader_intermediate_files is not None:
            payload["prereader_intermediate_files"] = prereader_intermediate_files
        return self.post(
            f"/api/v6.1.0.3/hubs/{hub}/channels/{channel}/compare",
            None,
            {},
            payload,
            True,
        )

    def post_hubs_channels_controls_delete(self, hub, channel, ctrl_ids):

        payload = {}
        payload["ctrl_ids"] = ctrl_ids
        return self.post(
            f"/api/v6.1.0.3/hubs/{hub}/channels/{channel}/controls_delete",
            None,
            {},
            payload,
            True,
        )

    def post_hubs_channels_deactivate(
        self,
        hub,
        channel,
        locs=None,
        tables=None,
        parallel_locs=None,
        components=None,
        start_immediate=None,
    ):

        payload = {}
        if locs is not None:
            payload["locs"] = locs
        if tables is not None:
            payload["tables"] = tables
        if parallel_locs is not None:
            payload["parallel_locs"] = parallel_locs
        if components is not None:
            payload["components"] = components
        if start_immediate is not None:
            payload["start_immediate"] = self.from_bool(start_immediate)
        return self.post(
            f"/api/v6.1.0.3/hubs/{hub}/channels/{channel}/deactivate",
            None,
            {},
            payload,
            True,
        )

    def post_hubs_channels_locs_adapt_apply(
        self,
        hub,
        channel,
        loc,
        tables_in_channel=None,
        add_tables=None,
        add_table_group=None,
        show_views=None,
        mapspec=None,
    ):

        payload = {}
        if tables_in_channel is not None:
            payload["tables_in_channel"] = tables_in_channel
        if add_tables is not None:
            payload["add_tables"] = self.from_bool(add_tables)
        if add_table_group is not None:
            payload["add_table_group"] = add_table_group
        if show_views is not None:
            payload["show_views"] = self.from_bool(show_views)
        if mapspec is not None:
            payload["mapspec"] = mapspec
        return self.post(
            f"/api/v6.1.0.3/hubs/{hub}/channels/{channel}/locs/{loc}/adapt/apply",
            None,
            {},
            payload,
            True,
        )

    def post_hubs_channels_locs_adapt_check(
        self,
        hub,
        channel,
        loc,
        tables_in_channel=None,
        add_tables=None,
        show_views=None,
        fetch_extra=None,
        mapspec=None,
        mapspec_table_not_in_db_error=None,
    ):

        payload = {}
        if tables_in_channel is not None:
            payload["tables_in_channel"] = tables_in_channel
        if add_tables is not None:
            payload["add_tables"] = self.from_bool(add_tables)
        if show_views is not None:
            payload["show_views"] = self.from_bool(show_views)
        if fetch_extra is not None:
            payload["fetch_extra"] = fetch_extra
        if mapspec is not None:
            payload["mapspec"] = mapspec
        if mapspec_table_not_in_db_error is not None:
            payload["mapspec_table_not_in_db_error"] = self.from_bool(
                mapspec_table_not_in_db_error
            )
        return self.post(
            f"/api/v6.1.0.3/hubs/{hub}/channels/{channel}/locs/{loc}/adapt/check",
            None,
            {},
            payload,
            True,
        )

    def post_hubs_channels_locs_adapt_check_table(
        self,
        hub,
        channel,
        loc,
        table,
        contexts=None,
        localize_datatypes=None,
        fetch_extra=None,
    ):

        payload = {}
        if contexts is not None:
            payload["contexts"] = contexts
        if localize_datatypes is not None:
            payload["localize_datatypes"] = self.from_bool(localize_datatypes)
        if fetch_extra is not None:
            payload["fetch_extra"] = fetch_extra
        return self.post(
            f"/api/v6.1.0.3/hubs/{hub}/channels/{channel}/locs/{loc}/adapt/check/{table}",
            None,
            {},
            payload,
            True,
        )

    def post_hubs_channels_locs_adapt_other_channels(self, hub, channel, loc):

        return self.post(
            f"/api/v6.1.0.3/hubs/{hub}/channels/{channel}/locs/{loc}/adapt/other_channels",
            None,
            {},
            None,
            True,
        )

    def post_hubs_channels_locs_slicing_suggest(
        self,
        hub,
        channel,
        loc,
        rows_per_slice=None,
        max_slices_per_table=None,
        repeat_last_refresh_slicing=None,
        repeat_last_compare_slicing=None,
        suggest_from_last_refresh_rows=None,
        suggest_from_last_compare_rows=None,
        suggest_from_db_stats=None,
        tables=None,
    ):

        payload = {}
        if rows_per_slice is not None:
            payload["rows_per_slice"] = rows_per_slice
        if max_slices_per_table is not None:
            payload["max_slices_per_table"] = max_slices_per_table
        if repeat_last_refresh_slicing is not None:
            payload["repeat_last_refresh_slicing"] = self.from_bool(
                repeat_last_refresh_slicing
            )
        if repeat_last_compare_slicing is not None:
            payload["repeat_last_compare_slicing"] = self.from_bool(
                repeat_last_compare_slicing
            )
        if suggest_from_last_refresh_rows is not None:
            payload["suggest_from_last_refresh_rows"] = self.from_bool(
                suggest_from_last_refresh_rows
            )
        if suggest_from_last_compare_rows is not None:
            payload["suggest_from_last_compare_rows"] = self.from_bool(
                suggest_from_last_compare_rows
            )
        if suggest_from_db_stats is not None:
            payload["suggest_from_db_stats"] = self.from_bool(suggest_from_db_stats)
        if tables is not None:
            payload["tables"] = tables
        return self.post(
            f"/api/v6.1.0.3/hubs/{hub}/channels/{channel}/locs/{loc}/slicing_suggest",
            None,
            {},
            payload,
            True,
        )

    def post_hubs_channels_locs_tables_slicing_boundaries(
        self, hub, channel, loc, table, col, slices
    ):

        payload = {}
        payload["col"] = col
        payload["slices"] = slices
        return self.post(
            f"/api/v6.1.0.3/hubs/{hub}/channels/{channel}/locs/{loc}/tables/{table}/slicing_boundaries",
            None,
            {},
            payload,
            True,
        )

    def post_hubs_channels_locs_tasks_controls(
        self,
        hub,
        channel,
        loc,
        task,
        ctrl_name=None,
        filters=None,
        set_env=None,
        journaling=None,
        finish_after_cycle=None,
        expiry_date=None,
        recv_expiry=None,
    ):

        payload = {}
        if ctrl_name is not None:
            payload["ctrl_name"] = ctrl_name
        if filters is not None:
            payload["filters"] = filters
        if set_env is not None:
            payload["set_env"] = set_env
        if journaling is not None:
            payload["journaling"] = self.from_bool(journaling)
        if finish_after_cycle is not None:
            payload["finish_after_cycle"] = self.from_bool(finish_after_cycle)
        if expiry_date is not None:
            payload["expiry_date"] = expiry_date
        if recv_expiry is not None:
            payload["recv_expiry"] = recv_expiry
        return self.post(
            f"/api/v6.1.0.3/hubs/{hub}/channels/{channel}/locs/{loc}/tasks/{task}/controls",
            None,
            {},
            payload,
            True,
        )

    def post_hubs_channels_refresh(
        self,
        hub,
        channel,
        source_loc,
        target_loc,
        contexts=None,
        granularity=None,
        difference_filter=None,
        quota_run=None,
        parallel_sessions=None,
        db_sequences=None,
        slicing=None,
        tables=None,
        task=None,
        context_variables=None,
        file_preread_subtasks=None,
        start_immediate=None,
        create_tables=None,
        data_refresh=None,
        fire_db_triggers=None,
        foreign_keys=None,
        select_moment=None,
        online_refresh=None,
        start_next_jobs=None,
    ):

        payload = {}
        payload["source_loc"] = source_loc
        payload["target_loc"] = target_loc
        if contexts is not None:
            payload["contexts"] = contexts
        if granularity is not None:
            payload["granularity"] = granularity
        if difference_filter is not None:
            payload["difference_filter"] = difference_filter
        if quota_run is not None:
            payload["quota_run"] = quota_run
        if parallel_sessions is not None:
            payload["parallel_sessions"] = parallel_sessions
        if db_sequences is not None:
            payload["db_sequences"] = self.from_bool(db_sequences)
        if slicing is not None:
            payload["slicing"] = slicing
        if tables is not None:
            payload["tables"] = tables
        if task is not None:
            payload["task"] = task
        if context_variables is not None:
            payload["context_variables"] = context_variables
        if file_preread_subtasks is not None:
            payload["file_preread_subtasks"] = file_preread_subtasks
        if start_immediate is not None:
            payload["start_immediate"] = self.from_bool(start_immediate)
        if create_tables is not None:
            payload["create_tables"] = create_tables
        if data_refresh is not None:
            payload["data_refresh"] = self.from_bool(data_refresh)
        if fire_db_triggers is not None:
            payload["fire_db_triggers"] = self.from_bool(fire_db_triggers)
        if foreign_keys is not None:
            payload["foreign_keys"] = foreign_keys
        if select_moment is not None:
            payload["select_moment"] = select_moment
        if online_refresh is not None:
            payload["online_refresh"] = online_refresh
        if start_next_jobs is not None:
            payload["start_next_jobs"] = start_next_jobs
        return self.post(
            f"/api/v6.1.0.3/hubs/{hub}/channels/{channel}/refresh",
            None,
            {},
            payload,
            True,
        )

    def post_hubs_definition_action_modify(self, hub, type, old, new):

        payload = {}
        payload["type"] = type
        payload["old"] = old
        payload["new"] = new
        return self.post(
            f"/api/v6.1.0.3/hubs/{hub}/definition/action_modify",
            None,
            {},
            payload,
            True,
        )

    def post_hubs_definition_action_replace(self, hub, type, old, new):

        payload = {}
        payload["type"] = type
        payload["old"] = old
        payload["new"] = new
        return self.post(
            f"/api/v6.1.0.3/hubs/{hub}/definition/action_replace",
            None,
            {},
            payload,
            True,
        )

    def post_hubs_definition_channels(
        self, hub, channel, description=None, loc_groups=None, tables=None, actions=None
    ):

        payload = {}
        payload["channel"] = channel
        if description is not None:
            payload["description"] = description
        if loc_groups is not None:
            payload["loc_groups"] = loc_groups
        if tables is not None:
            payload["tables"] = tables
        if actions is not None:
            payload["actions"] = actions
        return self.post(
            f"/api/v6.1.0.3/hubs/{hub}/definition/channels", None, {}, payload, True
        )

    def post_hubs_definition_channels_actions_delete(self, hub, channel, actions):

        payload = {}
        payload["actions"] = actions
        return self.post(
            f"/api/v6.1.0.3/hubs/{hub}/definition/channels/{channel}/actions_delete",
            None,
            {},
            payload,
            True,
        )

    def post_hubs_definition_channels_loc_groups(
        self, hub, channel, loc_group, members=None
    ):

        payload = {}
        payload["loc_group"] = loc_group
        if members is not None:
            payload["members"] = members
        return self.post(
            f"/api/v6.1.0.3/hubs/{hub}/definition/channels/{channel}/loc_groups",
            None,
            {},
            payload,
            True,
        )

    def post_hubs_definition_channels_loc_groups_members_delete(
        self, hub, channel, loc_group, members
    ):

        payload = {}
        payload["members"] = members
        return self.post(
            f"/api/v6.1.0.3/hubs/{hub}/definition/channels/{channel}/loc_groups/{loc_group}/members_delete",
            None,
            {},
            payload,
            True,
        )

    def post_hubs_definition_channels_loc_groups_rename(
        self, hub, channel, loc_group, new_name
    ):

        payload = {}
        payload["new_name"] = new_name
        return self.post(
            f"/api/v6.1.0.3/hubs/{hub}/definition/channels/{channel}/loc_groups/{loc_group}/rename",
            None,
            {},
            payload,
            True,
        )

    def post_hubs_definition_channels_rename(self, hub, channel, new_name):

        payload = {}
        payload["new_name"] = new_name
        return self.post(
            f"/api/v6.1.0.3/hubs/{hub}/definition/channels/{channel}/rename",
            None,
            {},
            payload,
            True,
        )

    def post_hubs_definition_channels_tables(
        self, hub, channel, table, base_name=None, table_group=None, cols=None
    ):

        payload = {}
        payload["table"] = table
        if base_name is not None:
            payload["base_name"] = base_name
        if table_group is not None:
            payload["table_group"] = table_group
        if cols is not None:
            payload["cols"] = cols
        return self.post(
            f"/api/v6.1.0.3/hubs/{hub}/definition/channels/{channel}/tables",
            None,
            {},
            payload,
            True,
        )

    def post_hubs_definition_channels_tables_cols_delete(
        self, hub, channel, table, cols
    ):

        payload = {}
        payload["cols"] = cols
        return self.post(
            f"/api/v6.1.0.3/hubs/{hub}/definition/channels/{channel}/tables/{table}/cols_delete",
            None,
            {},
            payload,
            True,
        )

    def post_hubs_definition_channels_tables_delete(self, hub, channel, tables):

        payload = {}
        payload["tables"] = tables
        return self.post(
            f"/api/v6.1.0.3/hubs/{hub}/definition/channels/{channel}/tables_delete",
            None,
            {},
            payload,
            True,
        )

    def post_hubs_definition_channels_tables_rename(
        self, hub, channel, table, new_name
    ):

        payload = {}
        payload["new_name"] = new_name
        return self.post(
            f"/api/v6.1.0.3/hubs/{hub}/definition/channels/{channel}/tables/{table}/rename",
            None,
            {},
            payload,
            True,
        )

    def post_hubs_definition_hub_actions_delete(self, hub, actions):

        payload = {}
        payload["actions"] = actions
        return self.post(
            f"/api/v6.1.0.3/hubs/{hub}/definition/hub_actions_delete",
            None,
            {},
            payload,
            True,
        )

    def post_hubs_definition_import(
        self,
        hub,
        changes,
        x_hvr_classified_transport_key=None,
        export_header=None,
        allowed_changes=None,
        loc_context=None,
        channel_context=None,
        table_context=None,
        on_add_exists=None,
        on_action_absent_loc=None,
        on_old_group_members=None,
        on_member_absent_loc=None,
        on_absent=None,
    ):

        headers = {}
        if x_hvr_classified_transport_key:
            headers["X-Hvr-Classified-Transport-Key"] = x_hvr_classified_transport_key
        payload = {}
        if export_header is not None:
            payload["export_header"] = export_header
        if allowed_changes is not None:
            payload["allowed_changes"] = allowed_changes
        if loc_context is not None:
            payload["loc_context"] = loc_context
        if channel_context is not None:
            payload["channel_context"] = channel_context
        if table_context is not None:
            payload["table_context"] = table_context
        if on_add_exists is not None:
            payload["on_add_exists"] = on_add_exists
        if on_action_absent_loc is not None:
            payload["on_action_absent_loc"] = on_action_absent_loc
        if on_old_group_members is not None:
            payload["on_old_group_members"] = on_old_group_members
        if on_member_absent_loc is not None:
            payload["on_member_absent_loc"] = on_member_absent_loc
        if on_absent is not None:
            payload["on_absent"] = on_absent
        payload["changes"] = changes
        return self.post(
            f"/api/v6.1.0.3/hubs/{hub}/definition/import", None, headers, payload, True
        )

    def post_hubs_definition_import_analyze(
        self,
        hub,
        changes,
        x_hvr_classified_transport_key=None,
        export_header=None,
        allowed_changes=None,
        loc_context=None,
        channel_context=None,
        table_context=None,
    ):

        headers = {}
        if x_hvr_classified_transport_key:
            headers["X-Hvr-Classified-Transport-Key"] = x_hvr_classified_transport_key
        payload = {}
        if export_header is not None:
            payload["export_header"] = export_header
        if allowed_changes is not None:
            payload["allowed_changes"] = allowed_changes
        if loc_context is not None:
            payload["loc_context"] = loc_context
        if channel_context is not None:
            payload["channel_context"] = channel_context
        if table_context is not None:
            payload["table_context"] = table_context
        payload["changes"] = changes
        return self.post(
            f"/api/v6.1.0.3/hubs/{hub}/definition/import/analyze",
            None,
            headers,
            payload,
            True,
        )

    def post_hubs_definition_locs(
        self, hub, loc, props, x_hvr_classified_transport_key=None, actions=None
    ):

        headers = {}
        if x_hvr_classified_transport_key:
            headers["X-Hvr-Classified-Transport-Key"] = x_hvr_classified_transport_key
        payload = {}
        payload["loc"] = loc
        payload["props"] = props
        if actions is not None:
            payload["actions"] = actions
        return self.post(
            f"/api/v6.1.0.3/hubs/{hub}/definition/locs", None, headers, payload, True
        )

    def post_hubs_definition_locs_actions_delete(self, hub, loc, actions):

        payload = {}
        payload["actions"] = actions
        return self.post(
            f"/api/v6.1.0.3/hubs/{hub}/definition/locs/{loc}/actions_delete",
            None,
            {},
            payload,
            True,
        )

    def post_hubs_definition_locs_copy(self, hub, loc, new_name):

        payload = {}
        payload["new_name"] = new_name
        return self.post(
            f"/api/v6.1.0.3/hubs/{hub}/definition/locs/{loc}/copy",
            None,
            {},
            payload,
            True,
        )

    def post_hubs_definition_locs_props_delete(self, hub, loc, props):

        payload = {}
        payload["props"] = props
        return self.post(
            f"/api/v6.1.0.3/hubs/{hub}/definition/locs/{loc}/props_delete",
            None,
            {},
            payload,
            True,
        )

    def post_hubs_definition_locs_rename(self, hub, loc, new_name):

        payload = {}
        payload["new_name"] = new_name
        return self.post(
            f"/api/v6.1.0.3/hubs/{hub}/definition/locs/{loc}/rename",
            None,
            {},
            payload,
            True,
        )

    def post_hubs_events_cancel(self, hub, ev_ids):

        payload = {}
        payload["ev_ids"] = ev_ids
        return self.post(
            f"/api/v6.1.0.3/hubs/{hub}/events_cancel", None, {}, payload, True
        )

    def post_hubs_freeze(self, hub):

        return self.post(f"/api/v6.1.0.3/hubs/{hub}/freeze", None, {}, None, True)

    def post_hubs_jobs_delete(self, hub, jobs):

        payload = {}
        payload["jobs"] = jobs
        return self.post(
            f"/api/v6.1.0.3/hubs/{hub}/jobs_delete", None, {}, payload, True
        )

    def post_hubs_jobs_start(self, hub, jobs, unsuspend=None, trigger_failed=None):

        payload = {}
        payload["jobs"] = jobs
        if unsuspend is not None:
            payload["unsuspend"] = self.from_bool(unsuspend)
        if trigger_failed is not None:
            payload["trigger_failed"] = self.from_bool(trigger_failed)
        return self.post(
            f"/api/v6.1.0.3/hubs/{hub}/jobs_start", None, {}, payload, True
        )

    def post_hubs_jobs_suspend(self, hub, jobs):

        payload = {}
        payload["jobs"] = jobs
        return self.post(
            f"/api/v6.1.0.3/hubs/{hub}/jobs_suspend", None, {}, payload, True
        )

    def post_hubs_jobs_unsuspend(self, hub, jobs):

        payload = {}
        payload["jobs"] = jobs
        return self.post(
            f"/api/v6.1.0.3/hubs/{hub}/jobs_unsuspend", None, {}, payload, True
        )

    def post_hubs_locs_agent_props_delete(
        self,
        hub,
        loc,
        agent_props,
        setup_token=None,
        setup_timed=None,
        auth_user_password=None,
    ):

        payload = {}
        if setup_token is not None:
            payload["setup_token"] = setup_token
        if setup_timed is not None:
            payload["setup_timed"] = self.from_bool(setup_timed)
        if auth_user_password is not None:
            payload["auth_user_password"] = auth_user_password
        payload["agent_props"] = agent_props
        return self.post(
            f"/api/v6.1.0.3/hubs/{hub}/locs/{loc}/agent/props_delete",
            None,
            {},
            payload,
            True,
        )

    def post_hubs_locs_agent_props_get(
        self,
        hub,
        loc,
        x_hvr_classified_access=None,
        setup_token=None,
        setup_timed=None,
        auth_user_password=None,
        fetch=None,
    ):

        headers = {}
        if x_hvr_classified_access:
            headers["X-Hvr-Classified-Access"] = x_hvr_classified_access
        payload = {}
        if setup_token is not None:
            payload["setup_token"] = setup_token
        if setup_timed is not None:
            payload["setup_timed"] = self.from_bool(setup_timed)
        if auth_user_password is not None:
            payload["auth_user_password"] = auth_user_password
        if fetch is not None:
            payload["fetch"] = fetch
        return self.post(
            f"/api/v6.1.0.3/hubs/{hub}/locs/{loc}/agent/props_get",
            None,
            headers,
            payload,
            True,
        )

    def post_hubs_locs_agent_props_patch(
        self,
        hub,
        loc,
        agent_props,
        x_hvr_classified_transport_key=None,
        setup_token=None,
        setup_timed=None,
        auth_user_password=None,
    ):

        headers = {}
        if x_hvr_classified_transport_key:
            headers["X-Hvr-Classified-Transport-Key"] = x_hvr_classified_transport_key
        payload = {}
        if setup_token is not None:
            payload["setup_token"] = setup_token
        if setup_timed is not None:
            payload["setup_timed"] = self.from_bool(setup_timed)
        if auth_user_password is not None:
            payload["auth_user_password"] = auth_user_password
        payload["agent_props"] = agent_props
        return self.post(
            f"/api/v6.1.0.3/hubs/{hub}/locs/{loc}/agent/props_patch",
            None,
            headers,
            payload,
            True,
        )

    def post_hubs_locs_agent_props_put(
        self,
        hub,
        loc,
        agent_props,
        x_hvr_classified_transport_key=None,
        setup_token=None,
        setup_timed=None,
        auth_user_password=None,
    ):

        headers = {}
        if x_hvr_classified_transport_key:
            headers["X-Hvr-Classified-Transport-Key"] = x_hvr_classified_transport_key
        payload = {}
        if setup_token is not None:
            payload["setup_token"] = setup_token
        if setup_timed is not None:
            payload["setup_timed"] = self.from_bool(setup_timed)
        if auth_user_password is not None:
            payload["auth_user_password"] = auth_user_password
        payload["agent_props"] = agent_props
        return self.post(
            f"/api/v6.1.0.3/hubs/{hub}/locs/{loc}/agent/props_put",
            None,
            headers,
            payload,
            True,
        )

    def post_hubs_locs_agent_test(
        self, hub, loc, setup_token=None, setup_timed=None, auth_user_password=None
    ):

        payload = {}
        if setup_token is not None:
            payload["setup_token"] = setup_token
        if setup_timed is not None:
            payload["setup_timed"] = self.from_bool(setup_timed)
        if auth_user_password is not None:
            payload["auth_user_password"] = auth_user_password
        return self.post(
            f"/api/v6.1.0.3/hubs/{hub}/locs/{loc}/agent/test", None, {}, payload, True
        )

    def post_hubs_locs_agent_users(
        self,
        hub,
        loc,
        user,
        authentication,
        setup_token=None,
        setup_timed=None,
        auth_user_password=None,
        password=None,
    ):

        payload = {}
        if setup_token is not None:
            payload["setup_token"] = setup_token
        if setup_timed is not None:
            payload["setup_timed"] = self.from_bool(setup_timed)
        if auth_user_password is not None:
            payload["auth_user_password"] = auth_user_password
        payload["user"] = user
        payload["authentication"] = authentication
        if password is not None:
            payload["password"] = password
        return self.post(
            f"/api/v6.1.0.3/hubs/{hub}/locs/{loc}/agent/users", None, {}, payload, True
        )

    def post_hubs_locs_agent_users_delete(
        self,
        hub,
        loc,
        user,
        setup_token=None,
        setup_timed=None,
        auth_user_password=None,
    ):

        payload = {}
        if setup_token is not None:
            payload["setup_token"] = setup_token
        if setup_timed is not None:
            payload["setup_timed"] = self.from_bool(setup_timed)
        if auth_user_password is not None:
            payload["auth_user_password"] = auth_user_password
        payload["user"] = user
        return self.post(
            f"/api/v6.1.0.3/hubs/{hub}/locs/{loc}/agent/users_delete",
            None,
            {},
            payload,
            True,
        )

    def post_hubs_locs_agent_users_get(
        self,
        hub,
        loc,
        setup_token=None,
        setup_timed=None,
        auth_user_password=None,
        user=None,
    ):

        payload = {}
        if setup_token is not None:
            payload["setup_token"] = setup_token
        if setup_timed is not None:
            payload["setup_timed"] = self.from_bool(setup_timed)
        if auth_user_password is not None:
            payload["auth_user_password"] = auth_user_password
        if user is not None:
            payload["user"] = user
        return self.post(
            f"/api/v6.1.0.3/hubs/{hub}/locs/{loc}/agent/users_get",
            None,
            {},
            payload,
            True,
        )

    def post_hubs_locs_agent_users_password(
        self,
        hub,
        loc,
        user,
        new_password,
        setup_token=None,
        setup_timed=None,
        auth_user_password=None,
        current_password=None,
    ):

        payload = {}
        if setup_token is not None:
            payload["setup_token"] = setup_token
        if setup_timed is not None:
            payload["setup_timed"] = self.from_bool(setup_timed)
        if auth_user_password is not None:
            payload["auth_user_password"] = auth_user_password
        payload["user"] = user
        payload["new_password"] = new_password
        if current_password is not None:
            payload["current_password"] = current_password
        return self.post(
            f"/api/v6.1.0.3/hubs/{hub}/locs/{loc}/agent/users_password",
            None,
            {},
            payload,
            True,
        )

    def post_hubs_locs_test(self, hub, loc, channel=None):

        payload = {}
        if channel is not None:
            payload["channel"] = channel
        return self.post(
            f"/api/v6.1.0.3/hubs/{hub}/locs/{loc}/test", None, {}, payload, True
        )

    def post_hubs_mapdoc_parse(self, hub, mapdoc):

        payload = {}
        payload["mapdoc"] = mapdoc
        return self.post(
            f"/api/v6.1.0.3/hubs/{hub}/mapdoc/parse", None, {}, payload, True
        )

    def post_hubs_new_loc_agent_get(self, hub, loc_props, loc_props_from=None):

        payload = {}
        if loc_props_from is not None:
            payload["loc_props_from"] = loc_props_from
        payload["loc_props"] = loc_props
        return self.post(
            f"/api/v6.1.0.3/hubs/{hub}/new_loc/agent_get", None, {}, payload, True
        )

    def post_hubs_new_loc_agent_props_delete(
        self,
        hub,
        loc_props,
        agent_props,
        loc_props_from=None,
        setup_token=None,
        setup_timed=None,
        auth_user_password=None,
    ):

        payload = {}
        if loc_props_from is not None:
            payload["loc_props_from"] = loc_props_from
        payload["loc_props"] = loc_props
        if setup_token is not None:
            payload["setup_token"] = setup_token
        if setup_timed is not None:
            payload["setup_timed"] = self.from_bool(setup_timed)
        if auth_user_password is not None:
            payload["auth_user_password"] = auth_user_password
        payload["agent_props"] = agent_props
        return self.post(
            f"/api/v6.1.0.3/hubs/{hub}/new_loc/agent/props_delete",
            None,
            {},
            payload,
            True,
        )

    def post_hubs_new_loc_agent_props_get(
        self,
        hub,
        loc_props,
        x_hvr_classified_access=None,
        loc_props_from=None,
        setup_token=None,
        setup_timed=None,
        auth_user_password=None,
        fetch=None,
    ):

        headers = {}
        if x_hvr_classified_access:
            headers["X-Hvr-Classified-Access"] = x_hvr_classified_access
        payload = {}
        if loc_props_from is not None:
            payload["loc_props_from"] = loc_props_from
        payload["loc_props"] = loc_props
        if setup_token is not None:
            payload["setup_token"] = setup_token
        if setup_timed is not None:
            payload["setup_timed"] = self.from_bool(setup_timed)
        if auth_user_password is not None:
            payload["auth_user_password"] = auth_user_password
        if fetch is not None:
            payload["fetch"] = fetch
        return self.post(
            f"/api/v6.1.0.3/hubs/{hub}/new_loc/agent/props_get",
            None,
            headers,
            payload,
            True,
        )

    def post_hubs_new_loc_agent_props_patch(
        self,
        hub,
        loc_props,
        agent_props,
        x_hvr_classified_transport_key=None,
        loc_props_from=None,
        setup_token=None,
        setup_timed=None,
        auth_user_password=None,
    ):

        headers = {}
        if x_hvr_classified_transport_key:
            headers["X-Hvr-Classified-Transport-Key"] = x_hvr_classified_transport_key
        payload = {}
        if loc_props_from is not None:
            payload["loc_props_from"] = loc_props_from
        payload["loc_props"] = loc_props
        if setup_token is not None:
            payload["setup_token"] = setup_token
        if setup_timed is not None:
            payload["setup_timed"] = self.from_bool(setup_timed)
        if auth_user_password is not None:
            payload["auth_user_password"] = auth_user_password
        payload["agent_props"] = agent_props
        return self.post(
            f"/api/v6.1.0.3/hubs/{hub}/new_loc/agent/props_patch",
            None,
            headers,
            payload,
            True,
        )

    def post_hubs_new_loc_agent_props_put(
        self,
        hub,
        loc_props,
        agent_props,
        x_hvr_classified_transport_key=None,
        loc_props_from=None,
        setup_token=None,
        setup_timed=None,
        auth_user_password=None,
    ):

        headers = {}
        if x_hvr_classified_transport_key:
            headers["X-Hvr-Classified-Transport-Key"] = x_hvr_classified_transport_key
        payload = {}
        if loc_props_from is not None:
            payload["loc_props_from"] = loc_props_from
        payload["loc_props"] = loc_props
        if setup_token is not None:
            payload["setup_token"] = setup_token
        if setup_timed is not None:
            payload["setup_timed"] = self.from_bool(setup_timed)
        if auth_user_password is not None:
            payload["auth_user_password"] = auth_user_password
        payload["agent_props"] = agent_props
        return self.post(
            f"/api/v6.1.0.3/hubs/{hub}/new_loc/agent/props_put",
            None,
            headers,
            payload,
            True,
        )

    def post_hubs_new_loc_agent_test(
        self,
        hub,
        loc_props,
        loc_props_from=None,
        setup_token=None,
        setup_timed=None,
        auth_user_password=None,
    ):

        payload = {}
        if loc_props_from is not None:
            payload["loc_props_from"] = loc_props_from
        payload["loc_props"] = loc_props
        if setup_token is not None:
            payload["setup_token"] = setup_token
        if setup_timed is not None:
            payload["setup_timed"] = self.from_bool(setup_timed)
        if auth_user_password is not None:
            payload["auth_user_password"] = auth_user_password
        return self.post(
            f"/api/v6.1.0.3/hubs/{hub}/new_loc/agent/test", None, {}, payload, True
        )

    def post_hubs_new_loc_agent_users(
        self,
        hub,
        loc_props,
        user,
        authentication,
        loc_props_from=None,
        setup_token=None,
        setup_timed=None,
        auth_user_password=None,
        password=None,
    ):

        payload = {}
        if loc_props_from is not None:
            payload["loc_props_from"] = loc_props_from
        payload["loc_props"] = loc_props
        if setup_token is not None:
            payload["setup_token"] = setup_token
        if setup_timed is not None:
            payload["setup_timed"] = self.from_bool(setup_timed)
        if auth_user_password is not None:
            payload["auth_user_password"] = auth_user_password
        payload["user"] = user
        payload["authentication"] = authentication
        if password is not None:
            payload["password"] = password
        return self.post(
            f"/api/v6.1.0.3/hubs/{hub}/new_loc/agent/users", None, {}, payload, True
        )

    def post_hubs_new_loc_agent_users_delete(
        self,
        hub,
        loc_props,
        user,
        loc_props_from=None,
        setup_token=None,
        setup_timed=None,
        auth_user_password=None,
    ):

        payload = {}
        if loc_props_from is not None:
            payload["loc_props_from"] = loc_props_from
        payload["loc_props"] = loc_props
        if setup_token is not None:
            payload["setup_token"] = setup_token
        if setup_timed is not None:
            payload["setup_timed"] = self.from_bool(setup_timed)
        if auth_user_password is not None:
            payload["auth_user_password"] = auth_user_password
        payload["user"] = user
        return self.post(
            f"/api/v6.1.0.3/hubs/{hub}/new_loc/agent/users_delete",
            None,
            {},
            payload,
            True,
        )

    def post_hubs_new_loc_agent_users_get(
        self,
        hub,
        loc_props,
        loc_props_from=None,
        setup_token=None,
        setup_timed=None,
        auth_user_password=None,
        user=None,
    ):

        payload = {}
        if loc_props_from is not None:
            payload["loc_props_from"] = loc_props_from
        payload["loc_props"] = loc_props
        if setup_token is not None:
            payload["setup_token"] = setup_token
        if setup_timed is not None:
            payload["setup_timed"] = self.from_bool(setup_timed)
        if auth_user_password is not None:
            payload["auth_user_password"] = auth_user_password
        if user is not None:
            payload["user"] = user
        return self.post(
            f"/api/v6.1.0.3/hubs/{hub}/new_loc/agent/users_get", None, {}, payload, True
        )

    def post_hubs_new_loc_agent_users_password(
        self,
        hub,
        loc_props,
        user,
        new_password,
        loc_props_from=None,
        setup_token=None,
        setup_timed=None,
        auth_user_password=None,
        current_password=None,
    ):

        payload = {}
        if loc_props_from is not None:
            payload["loc_props_from"] = loc_props_from
        payload["loc_props"] = loc_props
        if setup_token is not None:
            payload["setup_token"] = setup_token
        if setup_timed is not None:
            payload["setup_timed"] = self.from_bool(setup_timed)
        if auth_user_password is not None:
            payload["auth_user_password"] = auth_user_password
        payload["user"] = user
        payload["new_password"] = new_password
        if current_password is not None:
            payload["current_password"] = current_password
        return self.post(
            f"/api/v6.1.0.3/hubs/{hub}/new_loc/agent/users_password",
            None,
            {},
            payload,
            True,
        )

    def post_hubs_new_loc_db_schemas(self, hub, props, channel=None, props_from=None):

        payload = {}
        if channel is not None:
            payload["channel"] = channel
        if props_from is not None:
            payload["props_from"] = props_from
        payload["props"] = props
        return self.post(
            f"/api/v6.1.0.3/hubs/{hub}/new_loc/db/schemas", None, {}, payload, True
        )

    def post_hubs_new_loc_dirs(
        self,
        hub,
        props,
        path=None,
        pattern=None,
        local=None,
        channel=None,
        props_from=None,
    ):

        payload = {}
        if path is not None:
            payload["path"] = path
        if pattern is not None:
            payload["pattern"] = pattern
        if local is not None:
            payload["local"] = self.from_bool(local)
        if channel is not None:
            payload["channel"] = channel
        if props_from is not None:
            payload["props_from"] = props_from
        payload["props"] = props
        return self.post(
            f"/api/v6.1.0.3/hubs/{hub}/new_loc/dirs", None, {}, payload, True
        )

    def post_hubs_new_loc_env_odbc_drivers(
        self, hub, props, odbcinst=None, odbcsysini=None, channel=None, props_from=None
    ):

        payload = {}
        if odbcinst is not None:
            payload["odbcinst"] = odbcinst
        if odbcsysini is not None:
            payload["odbcsysini"] = odbcsysini
        if channel is not None:
            payload["channel"] = channel
        if props_from is not None:
            payload["props_from"] = props_from
        payload["props"] = props
        return self.post(
            f"/api/v6.1.0.3/hubs/{hub}/new_loc/env/odbc_drivers",
            None,
            {},
            payload,
            True,
        )

    def post_hubs_new_loc_env_oratab(self, hub, props, channel=None, props_from=None):

        payload = {}
        if channel is not None:
            payload["channel"] = channel
        if props_from is not None:
            payload["props_from"] = props_from
        payload["props"] = props
        return self.post(
            f"/api/v6.1.0.3/hubs/{hub}/new_loc/env/oratab", None, {}, payload, True
        )

    def post_hubs_new_loc_env_vars(
        self, hub, vars, props, channel=None, props_from=None
    ):

        payload = {}
        payload["vars"] = vars
        if channel is not None:
            payload["channel"] = channel
        if props_from is not None:
            payload["props_from"] = props_from
        payload["props"] = props
        return self.post(
            f"/api/v6.1.0.3/hubs/{hub}/new_loc/env/vars", None, {}, payload, True
        )

    def post_hubs_new_loc_test(self, hub, props, channel=None, props_from=None):

        payload = {}
        if channel is not None:
            payload["channel"] = channel
        if props_from is not None:
            payload["props_from"] = props_from
        payload["props"] = props
        return self.post(
            f"/api/v6.1.0.3/hubs/{hub}/new_loc/test", None, {}, payload, True
        )

    def post_hubs_props_delete(self, hub, props):

        payload = {}
        payload["props"] = props
        return self.post(
            f"/api/v6.1.0.3/hubs/{hub}/props_delete", None, {}, payload, True
        )

    def post_hubs_snapshot(
        self,
        hub,
        x_hvr_classified_access=None,
        reason=None,
        channel_focus=None,
        event_trim=None,
        log_trim=None,
        stats_trim=None,
        definition_trim=None,
        dblog_dump=None,
        txfiles=None,
    ):

        headers = {}
        if x_hvr_classified_access:
            headers["X-Hvr-Classified-Access"] = x_hvr_classified_access
        payload = {}
        if reason is not None:
            payload["reason"] = reason
        if channel_focus is not None:
            payload["channel_focus"] = channel_focus
        if event_trim is not None:
            payload["event_trim"] = event_trim
        if log_trim is not None:
            payload["log_trim"] = log_trim
        if stats_trim is not None:
            payload["stats_trim"] = stats_trim
        if definition_trim is not None:
            payload["definition_trim"] = definition_trim
        if dblog_dump is not None:
            payload["dblog_dump"] = dblog_dump
        if txfiles is not None:
            payload["txfiles"] = txfiles
        return self.post(
            f"/api/v6.1.0.3/hubs/{hub}/snapshot", None, headers, payload, True
        )

    def post_hubs_stats_metrics_export(
        self,
        hub,
        format,
        channel=None,
        loc=None,
        table=None,
        metric=None,
        time_gran=None,
        scope=None,
        tstamp_begin=None,
        tstamp_end=None,
    ):

        payload = {}
        if channel is not None:
            payload["channel"] = channel
        if loc is not None:
            payload["loc"] = loc
        if table is not None:
            payload["table"] = table
        if metric is not None:
            payload["metric"] = metric
        if time_gran is not None:
            payload["time_gran"] = time_gran
        if scope is not None:
            payload["scope"] = scope
        if tstamp_begin is not None:
            payload["tstamp_begin"] = tstamp_begin
        if tstamp_end is not None:
            payload["tstamp_end"] = tstamp_end
        payload["format"] = format
        return self.post(
            f"/api/v6.1.0.3/hubs/{hub}/stats/metrics/export", None, {}, payload, True
        )

    def post_hubs_unfreeze(self, hub):

        return self.post(f"/api/v6.1.0.3/hubs/{hub}/unfreeze", None, {}, None, True)

    def post_hubs_users_props_delete(self, hub, user, props):

        payload = {}
        payload["props"] = props
        return self.post(
            f"/api/v6.1.0.3/hubs/{hub}/users/{user}/props_delete",
            None,
            {},
            payload,
            True,
        )

    def post_hubserver_props_delete(self, props):

        payload = {}
        payload["props"] = props
        return self.post(
            "/api/v6.1.0.3/hubserver/props_delete", None, {}, payload, True
        )

    def post_hubserver_props_test(self, props, props_from=None):

        payload = {}
        if props_from is not None:
            payload["props_from"] = self.from_bool(props_from)
        payload["props"] = props
        return self.post("/api/v6.1.0.3/hubserver/props_test", None, {}, payload, True)

    def post_hubserver_restart(self):

        return self.post("/api/v6.1.0.3/hubserver/restart", None, {}, None, True)

    def post_hubserver_stop(self):

        return self.post("/api/v6.1.0.3/hubserver/stop", None, {}, None, True)

    def post_hubserver_test(self):

        return self.post("/api/v6.1.0.3/hubserver/test", None, {}, None, True)

    def post_hubserver_upload(self, file):

        payload = {}
        payload["file"] = file
        return self.post("/api/v6.1.0.3/hubserver/upload", None, {}, payload, True)

    def post_licenses(self, license, raw):

        payload = {}
        payload["license"] = license
        payload["raw"] = raw
        return self.post("/api/v6.1.0.3/licenses", None, {}, payload, True)

    def post_licensing_license_agreement_accepted(self):

        return self.post(
            "/api/v6.1.0.3/licensing/license_agreement_accepted", None, {}, None, True
        )

    def post_metering_license_acquire(self):

        return self.post("/api/v6.1.0.3/metering/license_acquire", None, {}, None, True)

    def post_metering_purge(self, period_end=None):

        payload = {}
        if period_end is not None:
            payload["period_end"] = period_end
        return self.post("/api/v6.1.0.3/metering/purge", None, {}, payload, True)

    def post_metering_registration_status(self):

        return self.post(
            "/api/v6.1.0.3/metering/registration_status", None, {}, None, True
        )

    def post_metering_upload(self, period_begin=None, period_end=None, snapshots=None):

        payload = {}
        if period_begin is not None:
            payload["period_begin"] = period_begin
        if period_end is not None:
            payload["period_end"] = period_end
        if snapshots is not None:
            payload["snapshots"] = self.from_bool(snapshots)
        return self.post("/api/v6.1.0.3/metering/upload", None, {}, payload, True)

    def post_repos(self):

        return self.post("/api/v6.1.0.3/repos", None, {}, None, True)

    def post_repos_props_delete(self, props):

        payload = {}
        payload["props"] = props
        return self.post("/api/v6.1.0.3/repos/props_delete", None, {}, payload, True)

    def post_snapshot(
        self, ref, hub, x_hvr_classified_transport_key=None, description=None
    ):

        headers = {}
        if x_hvr_classified_transport_key:
            headers["X-Hvr-Classified-Transport-Key"] = x_hvr_classified_transport_key
        payload = {}
        payload["ref"] = ref
        payload["hub"] = hub
        if description is not None:
            payload["description"] = description
        return self.post("/api/v6.1.0.3/snapshot", None, headers, payload, True)

    def post_snapshot_inspect(self, ref, x_hvr_classified_transport_key=None):

        headers = {}
        if x_hvr_classified_transport_key:
            headers["X-Hvr-Classified-Transport-Key"] = x_hvr_classified_transport_key
        payload = {}
        payload["ref"] = ref
        return self.post("/api/v6.1.0.3/snapshot_inspect", None, headers, payload, True)

    def post_users(self, user, authentication, password=None, props=None):

        payload = {}
        payload["user"] = user
        payload["authentication"] = authentication
        if password is not None:
            payload["password"] = password
        if props is not None:
            payload["props"] = props
        return self.post("/api/v6.1.0.3/users", None, {}, payload, True)

    def post_users_props_delete(self, user, props):

        payload = {}
        payload["props"] = props
        return self.post(
            f"/api/v6.1.0.3/users/{user}/props_delete", None, {}, payload, True
        )

    def post_wallet(self, props, x_hvr_classified_transport_key=None, password=None):

        headers = {}
        if x_hvr_classified_transport_key:
            headers["X-Hvr-Classified-Transport-Key"] = x_hvr_classified_transport_key
        payload = {}
        payload["props"] = props
        if password is not None:
            payload["password"] = password
        return self.post("/api/v6.1.0.3/wallet", None, headers, payload, True)

    def post_wallet_change(
        self, x_hvr_classified_transport_key=None, props=None, password=None
    ):

        headers = {}
        if x_hvr_classified_transport_key:
            headers["X-Hvr-Classified-Transport-Key"] = x_hvr_classified_transport_key
        payload = {}
        if props is not None:
            payload["props"] = props
        if password is not None:
            payload["password"] = password
        return self.post("/api/v6.1.0.3/wallet/change", None, headers, payload, True)

    def post_wallet_disable(self, force=None):

        payload = {}
        if force is not None:
            payload["force"] = self.from_bool(force)
        return self.post("/api/v6.1.0.3/wallet/disable", None, {}, payload, True)

    def post_wallet_key_history_delete(
        self, before_key_sequence=None, before_rotation_tstamp=None
    ):

        payload = {}
        if before_key_sequence is not None:
            payload["before_key_sequence"] = before_key_sequence
        if before_rotation_tstamp is not None:
            payload["before_rotation_tstamp"] = before_rotation_tstamp
        return self.post(
            "/api/v6.1.0.3/wallet/key_history_delete", None, {}, payload, True
        )

    def post_wallet_key_rotate(self):

        return self.post("/api/v6.1.0.3/wallet/key_rotate", None, {}, None, True)

    def post_wallet_migrate(
        self,
        props,
        x_hvr_classified_transport_key=None,
        password=None,
        rotate_encryption_key=None,
    ):

        headers = {}
        if x_hvr_classified_transport_key:
            headers["X-Hvr-Classified-Transport-Key"] = x_hvr_classified_transport_key
        payload = {}
        payload["props"] = props
        if password is not None:
            payload["password"] = password
        if rotate_encryption_key is not None:
            payload["rotate_encryption_key"] = self.from_bool(rotate_encryption_key)
        return self.post("/api/v6.1.0.3/wallet/migrate", None, headers, payload, True)

    def post_wallet_reencrypt_continue(self, force=None):

        payload = {}
        if force is not None:
            payload["force"] = self.from_bool(force)
        return self.post(
            "/api/v6.1.0.3/wallet/reencrypt_continue", None, {}, payload, True
        )

    def put_hubs_alerts_props(
        self, hub, alert, x_hvr_classified_transport_key=None, **payload
    ):

        headers = {}
        if x_hvr_classified_transport_key:
            headers["X-Hvr-Classified-Transport-Key"] = x_hvr_classified_transport_key

        return self.put(
            f"/api/v6.1.0.3/hubs/{hub}/alerts/{alert}/props",
            None,
            headers,
            payload,
            True,
        )

    def put_hubs_definition_channels(
        self, hub, channel, description=None, loc_groups=None, tables=None, actions=None
    ):

        payload = {}
        if description is not None:
            payload["description"] = description
        if loc_groups is not None:
            payload["loc_groups"] = loc_groups
        if tables is not None:
            payload["tables"] = tables
        if actions is not None:
            payload["actions"] = actions
        return self.put(
            f"/api/v6.1.0.3/hubs/{hub}/definition/channels/{channel}",
            None,
            {},
            payload,
            True,
        )

    def put_hubs_definition_channels_actions(self, hub, channel, actions):

        payload = {}
        payload["actions"] = actions
        return self.put(
            f"/api/v6.1.0.3/hubs/{hub}/definition/channels/{channel}/actions",
            None,
            {},
            payload,
            True,
        )

    def put_hubs_definition_channels_loc_groups(
        self, hub, channel, loc_group, members=None
    ):

        payload = {}
        if members is not None:
            payload["members"] = members
        return self.put(
            f"/api/v6.1.0.3/hubs/{hub}/definition/channels/{channel}/loc_groups/{loc_group}",
            None,
            {},
            payload,
            True,
        )

    def put_hubs_definition_channels_loc_groups_members(
        self, hub, channel, loc_group, members
    ):

        payload = {}
        payload["members"] = members
        return self.put(
            f"/api/v6.1.0.3/hubs/{hub}/definition/channels/{channel}/loc_groups/{loc_group}/members",
            None,
            {},
            payload,
            True,
        )

    def put_hubs_definition_channels_tables(self, hub, channel, **payload):

        return self.put(
            f"/api/v6.1.0.3/hubs/{hub}/definition/channels/{channel}/tables",
            None,
            {},
            payload,
            True,
        )

    def put_hubs_definition_channels_tables_cols(self, hub, channel, table, **payload):

        return self.put(
            f"/api/v6.1.0.3/hubs/{hub}/definition/channels/{channel}/tables/{table}/cols",
            None,
            {},
            payload,
            True,
        )

    def put_hubs_definition_channels_tables_table(
        self, hub, channel, table, base_name=None, table_group=None, cols=None
    ):

        payload = {}
        if base_name is not None:
            payload["base_name"] = base_name
        if table_group is not None:
            payload["table_group"] = table_group
        if cols is not None:
            payload["cols"] = cols
        return self.put(
            f"/api/v6.1.0.3/hubs/{hub}/definition/channels/{channel}/tables/{table}",
            None,
            {},
            payload,
            True,
        )

    def put_hubs_definition_hub_actions(self, hub, actions):

        payload = {}
        payload["actions"] = actions
        return self.put(
            f"/api/v6.1.0.3/hubs/{hub}/definition/hub_actions", None, {}, payload, True
        )

    def put_hubs_definition_locs(
        self, hub, loc, props, x_hvr_classified_transport_key=None, actions=None
    ):

        headers = {}
        if x_hvr_classified_transport_key:
            headers["X-Hvr-Classified-Transport-Key"] = x_hvr_classified_transport_key
        payload = {}
        payload["props"] = props
        if actions is not None:
            payload["actions"] = actions
        return self.put(
            f"/api/v6.1.0.3/hubs/{hub}/definition/locs/{loc}",
            None,
            headers,
            payload,
            True,
        )

    def put_hubs_definition_locs_actions(self, hub, loc, actions):

        payload = {}
        payload["actions"] = actions
        return self.put(
            f"/api/v6.1.0.3/hubs/{hub}/definition/locs/{loc}/actions",
            None,
            {},
            payload,
            True,
        )

    def put_hubs_job_system_attributes(self, hub, attr, arg1, arg2=None):

        payload = {}
        payload["arg1"] = arg1
        if arg2 is not None:
            payload["arg2"] = arg2
        return self.put(
            f"/api/v6.1.0.3/hubs/{hub}/job_system/attributes/{attr}",
            None,
            {},
            payload,
            True,
        )

    def put_hubs_job_system_env_vars(self, hub, var, val):

        payload = {}
        payload["val"] = val
        return self.put(
            f"/api/v6.1.0.3/hubs/{hub}/job_system/env_vars/{var}",
            None,
            {},
            payload,
            True,
        )

    def put_hubs_jobs_attributes(self, hub, job, attr, arg1, arg2=None):

        payload = {}
        payload["arg1"] = arg1
        if arg2 is not None:
            payload["arg2"] = arg2
        return self.put(
            f"/api/v6.1.0.3/hubs/{hub}/jobs/{job}/attributes/{attr}",
            None,
            {},
            payload,
            True,
        )

    def put_hubs_jobs_env_vars(self, hub, job, var, val):

        payload = {}
        payload["val"] = val
        return self.put(
            f"/api/v6.1.0.3/hubs/{hub}/jobs/{job}/env_vars/{var}",
            None,
            {},
            payload,
            True,
        )

    def put_hubs_props(self, hub, **payload):

        return self.put(f"/api/v6.1.0.3/hubs/{hub}/props", None, {}, payload, True)

    def put_hubs_users_props(self, hub, user, **payload):

        return self.put(
            f"/api/v6.1.0.3/hubs/{hub}/users/{user}/props", None, {}, payload, True
        )

    def put_hubserver_props(self, x_hvr_classified_transport_key=None, **payload):

        headers = {}
        if x_hvr_classified_transport_key:
            headers["X-Hvr-Classified-Transport-Key"] = x_hvr_classified_transport_key

        return self.put("/api/v6.1.0.3/hubserver/props", None, headers, payload, True)

    def put_licenses(self, license, raw):

        payload = {}
        payload["raw"] = raw
        return self.put(f"/api/v6.1.0.3/licenses/{license}", None, {}, payload, True)

    def put_repos_props(self, x_hvr_classified_transport_key=None, **payload):

        headers = {}
        if x_hvr_classified_transport_key:
            headers["X-Hvr-Classified-Transport-Key"] = x_hvr_classified_transport_key

        return self.put("/api/v6.1.0.3/repos/props", None, headers, payload, True)

    def put_users_password(self, user, new_password, current_password=None):

        payload = {}
        payload["new_password"] = new_password
        if current_password is not None:
            payload["current_password"] = current_password
        return self.put(f"/api/v6.1.0.3/users/{user}/password", None, {}, payload, True)

    def put_users_props(self, user, **payload):

        return self.put(f"/api/v6.1.0.3/users/{user}/props", None, {}, payload, True)
