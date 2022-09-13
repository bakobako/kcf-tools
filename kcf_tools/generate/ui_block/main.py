import ui_blocks
import json
from PyInquirer import prompt


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


def _get_schema(row=False):
    filename = "configRowSchema" if row else "configSchema"
    with open(f"component_config/{filename}.json", 'r') as config_schema:
        return json.loads(config_schema.read())


def _init_row_schema():
    print("ConfigRowSchema was empty, initializing it")
    return ui_blocks.base_schema


def _add_ui_block(block_name, schema):
    if block_name == "ssh":
        print("Adding SSH Block")
        key_name = list(ui_blocks.use_ssh_block.keys())[0]
        schema["properties"][key_name] = ui_blocks.use_ssh_block[key_name]
        key_name = list(ui_blocks.ssh_block.keys())[0]
        schema["properties"][key_name] = ui_blocks.ssh_block[key_name]
    elif block_name == "sync-options":
        print("Adding Sync Options Block")
        key_name = list(ui_blocks.sync_options_block.keys())[0]
        schema["properties"][key_name] = ui_blocks.sync_options_block[key_name]
    elif block_name == "sync-options-with-custom-field":
        print("Adding Sync Options with custom Incremental Field Block")
        key_name = list(ui_blocks.sync_options_with_custom_field_block.keys())[0]
        schema["properties"][key_name] = ui_blocks.sync_options_with_custom_field_block[key_name]
    elif block_name == "destination":
        print("Adding Destination Block")
        key_name = list(ui_blocks.destination_block.keys())[0]
        schema["properties"][key_name] = ui_blocks.destination_block[key_name]
    elif block_name == "report-settings":
        print("Adding Report Settings Block")
        key_name = list(ui_blocks.report_settings_block.keys())[0]
        schema["properties"][key_name] = ui_blocks.report_settings_block[key_name]
    return schema


def _update_schema(schema, row=True):
    filename = "configRowSchema" if row else "configSchema"
    with open(f"component_config/{filename}.json", 'w') as config_schema:
        config_schema.write(json.dumps(schema))


def generate_ui_block():
    questions = [
        {
            'type': 'list',
            'choices': ['Main Configuration', 'Row Configuration'],
            'name': 'schema',
            'message': 'Where do you want to add the UI Block?'
        },
        {
            'type': 'list',
            'choices': ['ssh', 'sync-options', 'sync-options-with-custom-field', 'destination', 'report-settings'],
            'name': 'ui_block',
            'message': 'Which UI block would you like to add?'
        }
    ]
    answers = prompt(questions)
    block_name = answers.get("ui_block")
    row_answer = answers.get("schema")
    row = row_answer == 'Row Configuration'
    schema = _get_schema(row=row) or _init_row_schema()
    schema = _add_ui_block(block_name, schema)
    _update_schema(schema, row=row)
