import os
import json
from PyInquirer import prompt

START_DATE = ["start_date", "date_from"]
END_DATE = ["end_date", "date_to"]

DEFAULT_DESCRIPTIONS = {
    "date_from": "Date from which data will be downloaded. In relative format eg. 3 days ago, yesterday, or exact date in format YYYY-MM-DD",
    "start_date": "Date from which data will be downloaded. In relative format eg. 3 days ago, yesterday, or exact date in format YYYY-MM-DD",
    "date_to": "Date to which data will be downloaded. In relative format eg. 1 days ago, now, or exact date in format YYYY-MM-DD",
    "end_date": "Date to which data will be downloaded. In relative format eg. 1 days ago, now, or exact date in format YYYY-MM-DD",
    "backfill": "If backfill mode is enabled, each consecutive run of the component will continue from the end of the last run period, until current date is reached. The From and To date parameters are used to define Start date of the back-fill and also relative window of each run.",
    "backfill_mode": "If backfill mode is enabled, each consecutive run of the component will continue from the end of the last run period, until current date is reached. The From and To date parameters are used to define Start date of the back-fill and also relative window of each run.",
    "incremental": "If set to Incremental update, the result tables will be updated based on primary key and new records will be fetched. Full load overwrites the destination table each time.",
    "load_type": "If set to Incremental update, the result tables will be updated based on primary key and new records will be fetched. Full load overwrites the destination table each time."
}


def create_dir(directory):
    generated_folder = directory
    isExist = os.path.exists(generated_folder)
    if not isExist:
        os.mkdir(generated_folder)


def get_element_type(object_):
    if isinstance(object_, list):
        if len(object_) >= 1:
            if isinstance(object_[0], dict):
                return "list_dict"
        return "list"
    elif isinstance(object_, str):
        return "string"
    elif isinstance(object_, dict):
        return "dict"
    elif isinstance(object_, bool):
        return "boolean"
    elif isinstance(object_, int):
        return "integer"
    else:
        return "string"


def cli_fill_in_required(schema_elements):
    all_elements = []

    choices = []

    for config_schema_element in schema_elements:
        choices.append({"name": schema_elements[config_schema_element]["name"]})
        all_elements.append(schema_elements[config_schema_element]["name"])

    questions = [
        {
            'type': 'checkbox',
            'name': 'required',
            'message': 'What config elements are required?',
            'choices': choices
        }]
    answers = prompt(questions)

    for config_schema_element in schema_elements:
        schema_elements[config_schema_element]["required"] = False
        if config_schema_element in answers.get("required"):
            schema_elements[config_schema_element]["required"] = True

    return schema_elements


def cli_fill_in_enum(schema_elements):
    all_elements = []

    choices = []

    for config_schema_element in schema_elements:
        choices.append({"name": schema_elements[config_schema_element]["name"]})
        all_elements.append(schema_elements[config_schema_element]["name"])
        for child in schema_elements[config_schema_element].get("children", []):
            choices.append(
                {"name": "".join(["    ", schema_elements[config_schema_element]["children"][child]["name"]])})
            all_elements.append(schema_elements[config_schema_element]["children"][child]["name"])

    questions = [
        {
            'type': 'checkbox',
            'name': 'enum',
            'message': 'What config elements are Enums?',
            'choices': choices
        }]
    answers = prompt(questions)

    for config_schema_element in schema_elements:
        if schema_elements[config_schema_element].get("children"):
            for child in schema_elements[config_schema_element].get("children"):
                schema_elements[config_schema_element]["children"][child]["enum"] = False
                if "".join(["    ", schema_elements[config_schema_element]["children"][child]["name"]]) in answers.get(
                        "enum"):
                    schema_elements[config_schema_element]["children"][child]["enum"] = True

        schema_elements[config_schema_element]["enum"] = False
        if config_schema_element in answers.get("enum"):
            schema_elements[config_schema_element]["enum"] = True

    return schema_elements


def cli_select_config_type(schema_elements):
    all_elements = []

    choices = []

    for config_schema_element in schema_elements:
        choices.append({"name": schema_elements[config_schema_element]["name"]})
        all_elements.append(schema_elements[config_schema_element]["name"])

    questions = [
        {
            'type': 'checkbox',
            'name': 'row_config',
            'message': 'What config elements do you want to add to the row config?',
            'choices': choices
        }]
    row_schema = prompt(questions).get("row_config")
    main_schema = [x for x in all_elements if x not in row_schema]
    return main_schema, row_schema


def generate_config_schema(write_live: bool):
    create_dir("generated")
    create_dir(os.path.join("generated", "config_schemas"))

    config = get_config()

    config_schema_elements, _ = get_config_elements(config)

    config_schema_elements = cli_fill_in_required(config_schema_elements)
    config_schema_elements = cli_fill_in_enum(config_schema_elements)
    main_schema, row_schema = cli_select_config_type(config_schema_elements)
    if row_schema:
        generate_and_save_schema(write_live, row_schema, config_schema_elements, row=True)
    generate_and_save_schema(write_live, main_schema, config_schema_elements)


def get_config_elements(config, order=10):
    config_schema_elements = {}
    for config_element_name in config:
        config_element_value = config[config_element_name]
        config_element_type = get_element_type(config_element_value)
        config_schema_elements[config_element_name] = {}
        config_schema_elements[config_element_name]["name"] = config_element_name
        config_schema_elements[config_element_name]["type"] = config_element_type
        config_schema_elements[config_element_name]["enum"] = False
        config_schema_elements[config_element_name]["order"] = order

        if config_element_type == "dict":
            config_schema_elements[config_element_name]["children"], order = get_config_elements(
                config[config_element_name])
        if config_element_type == "list_dict":
            config_schema_elements[config_element_name]["children"], order = get_config_elements(
                config[config_element_name][0])

        order += 10

    return config_schema_elements, order


def get_property_type(element_type):
    prop_type = "string"
    if element_type == "integer":
        prop_type = "integer"
    elif element_type == "boolean":
        prop_type = "boolean"
    return prop_type


def generate_and_save_schema(write_live, schema_elements, config_schema_elements, row=False):
    config_schema = {
        "title": "Configuration Schema",
        "type": "object",
        "required": [
        ],
        "properties": {}
    }
    for schema_element in schema_elements:
        if config_schema_elements[schema_element]["required"]:
            config_schema["required"].append(schema_element)

        title = schema_element.replace("#", "").replace("_", " ").capitalize()

        prop_type = get_property_type(config_schema_elements[schema_element]["type"])

        property_dict = {
            "propertyOrder": config_schema_elements[schema_element]["order"],
            "title": title,
            "type": prop_type,
            "description": ""
        }

        if config_schema_elements[schema_element]["type"] == "dict":
            property_dict["type"] = "object"
            property_dict["properties"] = {}
            for i, child in enumerate(config_schema_elements[schema_element]["children"]):
                child_prop_type = get_property_type(config_schema_elements[schema_element]["children"][child])
                property_dict["properties"][child] = {"propertyOrder": (i + 1) * 10,
                                                      "title": child.replace("#", "").replace("_", " ").capitalize(),
                                                      "type": child_prop_type}
                if config_schema_elements[schema_element]["children"][child]["enum"]:
                    property_dict["properties"][child]["enum"] = ["ENUM_1", "ENUM_2", "ENUM_3"]
                    property_dict["properties"][child]["options"] = {}
                    property_dict["properties"][child]["options"]["enum_titles"] = ["ENUM_1_TITLE", "ENUM_2_TITLE",
                                                                                    "ENUM_3_TITLE"]
                if config_schema_elements[schema_element]["children"][child]["type"] == "boolean":
                    property_dict["properties"][child]["format"] = "checkbox"

        if config_schema_elements[schema_element]["type"] == "list_dict":
            property_dict["type"] = "array"
            property_dict["format"] = "table"
            property_dict["uniqueItems"] = True
            property_dict["items"] = {"type": "object", "title": title, "properties": {}}

            for i, child in enumerate(config_schema_elements[schema_element]["children"]):
                child_prop_type = get_property_type(config_schema_elements[schema_element]["children"][child])
                property_dict["items"]["properties"][child] = {"propertyOrder": (i + 1) * 10,
                                                               "title": child.replace("#", "").replace("_",
                                                                                                       " ").capitalize(),
                                                               "type": child_prop_type}
                if config_schema_elements[schema_element]["children"][child]["enum"]:
                    property_dict["items"]["properties"][child]["enum"] = ["ENUM_1", "ENUM_2", "ENUM_3"]
                    property_dict["items"]["properties"][child]["options"] = {}
                    property_dict["items"]["properties"][child]["options"]["enum_titles"] = ["ENUM_1_TITLE",
                                                                                             "ENUM_2_TITLE",
                                                                                             "ENUM_3_TITLE"]
                if config_schema_elements[schema_element]["children"][child]["type"] == "boolean":
                    property_dict["items"]["properties"][child]["format"] = "checkbox"

        if config_schema_elements[schema_element]["type"] == "list":
            property_dict["type"] = "array"
            property_dict["format"] = "select"
            property_dict["uniqueItems"] = True
            property_dict["items"] = {"type": "object", "title": title, "properties": {}}
            property_dict["items"]["type"] = "string"
            property_dict["items"]["enum"] = ["ENUM_1", "ENUM_2", "ENUM_3"]
            property_dict["items"]["options"] = {}
            property_dict["items"]["options"]["enum_titles"] = ["ENUM_1_TITLE", "ENUM_2_TITLE", "ENUM_3_TITLE"]

        if config_schema_elements[schema_element]["enum"]:
            property_dict["enum"] = ["ENUM_1", "ENUM_2", "ENUM_3"]
            property_dict["options"] = {}
            property_dict["options"]["enum_titles"] = ["ENUM_1_TITLE", "ENUM_2_TITLE", "ENUM_3_TITLE"]

        if schema_element in DEFAULT_DESCRIPTIONS:
            property_dict["description"] = DEFAULT_DESCRIPTIONS[schema_element]

        config_schema["properties"][schema_element] = property_dict

        if config_schema_elements[schema_element]["type"] == "boolean":
            property_dict["format"] = "checkbox"

        if "#" in config_schema_elements[schema_element]["name"]:
            property_dict["format"] = "password"

    if not config_schema["required"]:
        config_schema.pop("required")

    row_schema_str = ""
    if row:
        row_schema_str = "Row"

    if write_live:
        config_file_name = os.path.join("component_config", f"config{row_schema_str}Schema.json")
    else:
        config_file_name = os.path.join("generated", "config_schemas", f"config{row_schema_str}Schema.json")

    with open(config_file_name, "w") as out_config_file:
        json.dump(config_schema, out_config_file, indent=6)


def get_config():
    with open(os.path.join("data", "config.json")) as json_file:
        return json.load(json_file).get("parameters")
