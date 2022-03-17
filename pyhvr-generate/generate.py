import sys

import yaml
from jinja2 import Environment, FileSystemLoader

# from pprint import pprint


def generate(yaml_file):
    function_mapping = yaml.safe_load(open("function_mapping.yaml"))
    # pprint(function_mapping)

    openapi = yaml.safe_load(open(yaml_file))
    # pprint(openapi["paths"])

    python_functions = {}

    for path_openapi in openapi["paths"]:
        for verb in openapi["paths"][path_openapi]:
            verb_path_openapi = openapi["paths"][path_openapi][verb]

            uri = "/" + ("/".join(path_openapi.split("/")[3:]))
            # print (">"+uri)
            python_function_name = None
            if function_mapping.get(uri):
                if function_mapping[uri].get(verb):
                    python_function_name = function_mapping[uri][verb]
                    # print ("override")
            if python_function_name == "skip":
                continue
            if python_function_name is None:
                python_function_name = verb + uri.replace("{hub}", "").replace(
                    "{file}", ""
                ).replace("{loc}", "").replace("{loc_group}", "").replace(
                    "{job}", ""
                ).replace(
                    "{table}", ""
                ).replace(
                    "{task}", ""
                ).replace(
                    "{ev_id}", ""
                ).replace(
                    "{archive}", ""
                ).replace(
                    "{ctrl_id}", ""
                ).replace(
                    "{user}", ""
                ).replace(
                    "{license}", ""
                ).replace(
                    "{channel}", ""
                ).replace(
                    "{prop}", ""
                ).replace(
                    "{member}", ""
                ).replace(
                    "{alert}", ""
                ).replace(
                    "{attr}", ""
                ).replace(
                    "{var}", ""
                ).replace(
                    "/", "_"
                ).replace(
                    "__", "_"
                ).rstrip(
                    "_"
                )

            print(python_function_name)

            if python_functions.get(python_function_name):
                print("Duplicate: " + python_function_name)

            python_functions[python_function_name] = generate_function(
                python_function_name, verb, path_openapi, verb_path_openapi, openapi
            )

    env = Environment(loader=FileSystemLoader("./"))

    main_template = env.get_template("pyhvr_client.py.jinja")

    main_rendered = main_template.render(function_definitions=python_functions)

    with open("pyhvr_client.py", "w") as text_file:
        text_file.write(main_rendered)
    # print(main_rendered)


def generate_function(function_name, verb, uri, openapi, full_openapi):

    # pprint(uri)

    parameters = ["self"]
    query_builder_entries = []
    header_builder_entries = []

    if openapi.get("parameters"):
        for p in openapi["parameters"]:
            if p["in"] == "path":
                parameters.append(p["name"])
            elif p["in"] == "query":
                param = p["name"]
                schema = p["schema"]
                is_bool = schema.get("type") == "boolean"
                if is_bool:
                    value = f"self.from_bool({param})"
                else:
                    value = f"{param}"
                parameters.append(param + "=None")
                query_builder_entries.append(
                    f'        if {param}:\n          query["{param}"]={value}'
                )
            elif p["in"] == "header":
                param = p["name"]
                py_name = param.replace("-", "_").lower()
                schema = p["schema"]
                parameters.append(py_name + "=None")
                header_builder_entries.append(
                    f'        if {py_name}:\n          headers["{param}"]={py_name}'
                )
            else:
                print("Unsupported parameter type: " + p["in"])

    payload_builder = ""
    if openapi.get("requestBody"):
        schema = openapi["requestBody"]["content"]["application/json"]["schema"]
        payload_builder_entries = []
        payload_builder = "payload=''"

        if schema.get("properties"):
            schema_to_parse = schema["properties"]
            required = schema.get("required", [])
            param_passthrough = False
        elif schema.get("x-patternProperties"):
            schema_ref = schema["x-patternProperties"]["(*)"]["$ref"]
            # example: '#/components/schemas/Location'
            path = schema_ref.split("/")
            schema_reffed = full_openapi[path[1]][path[2]][path[3]]

            schema_to_parse = schema_reffed["properties"]
            required = schema_reffed.get("required", [])
            param_passthrough = False
        else:
            # print("Schema has no properties?")
            # pprint(schema)
            param_passthrough = True

        if param_passthrough:
            parameters.append("**payload")
            payload_builder = ""
        else:
            for property in schema_to_parse:
                is_bool = False
                try:
                    is_bool = schema_to_parse[property].get("type") == "boolean"
                    is_bool = schema_to_parse[property]["schema"]["type"] == "boolean"
                except KeyError:
                    pass

                if is_bool:
                    value = f"self.from_bool({property})"
                else:
                    value = f"{property}"
                if property in required:
                    parameters.append(property)
                    payload_builder_entries.append(
                        f'        payload["{property}"] = {value}'
                    )
                else:
                    parameters.append(property + "=None")
                    payload_builder_entries.append(
                        f'        if {property} is not None:\n          payload["{property}"]={value}'
                    )

            if payload_builder_entries:
                payload_builder = "        payload={}\n" + "\n".join(
                    payload_builder_entries
                )

        # pprint(schema)
        payload = "payload"
    else:
        payload = "None"

    if query_builder_entries:
        query_builder = "        query={}\n" + "\n".join(query_builder_entries)
        query = "query"
    else:
        query_builder = ""
        query = "None"

    if header_builder_entries:
        header_builder = "        headers={}\n" + "\n".join(header_builder_entries)
        header = "headers"
    else:
        header_builder = ""
        header = "{}"

    is_json = True
    if openapi.get("responses"):
        r = openapi["responses"]
        ok_resp = r.get("200", r.get("201", r.get("202", r.get("204"))))
        # pprint(ok_resp)
        if ok_resp:
            try:
                rt_payload = list(ok_resp.get("content", {}).keys())[0]
                # pprint(rt_payload)
                if "text/plain" in rt_payload:
                    is_json = False
            except IndexError:
                pass

    required_params = [
        param for param in parameters if ("=" not in param and "**" not in param)
    ]
    passthrough_params = [param for param in parameters if ("**" in param)]
    optional_params = [param for param in parameters if ("=" in param)]
    parameters_joined = ", ".join(
        required_params + optional_params + passthrough_params
    )

    # if uri is parametrized, make it so
    if "{" in uri:
        f = "f"
    else:
        f = ""

    fun = f"""
    def {function_name}({parameters_joined}):
{query_builder}
{header_builder}
{payload_builder}
        return self.{verb}(
            {f}"{uri}", {query}, {header}, {payload}, {is_json}
        )
"""

    return fun
    # print(fun)


generate(sys.argv[1])
