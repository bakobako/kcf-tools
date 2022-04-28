from jinja2 import Template
from .templates.readme_template import ReadmeTemplateData
from pathlib import Path
import os
import json


class ReadMeMaker:
    def __init__(self, config_folder_loc: str, data_folder_loc: str) -> None:
        self.config_folder_loc = config_folder_loc
        self.data_folder_loc = data_folder_loc
        self.readme_data = None
        self.readme_string = None

    def generate_readme(self, file_name: str) -> None:
        self.set_readme_data()
        self.fill_in_template()
        self.save_readme(file_name)

    def get_short_description_text(self) -> str:
        with open(os.path.join(self.config_folder_loc, "component_short_description.md")) as f:
            short_description = f.read()
        return short_description

    def get_long_description_text(self) -> str:
        with open(os.path.join(self.config_folder_loc, "component_long_description.md")) as f:
            long_description = f.read()
        return long_description

    def get_configuration_schema(self, is_row_config: bool = False) -> str:

        schema_location = os.path.join(self.config_folder_loc, "configSchema.json")
        if is_row_config:
            schema_location = os.path.join(self.config_folder_loc, "configRowSchema.json")

        with open(schema_location) as json_file:
            data = json.load(json_file)

        keys = list(data.keys())

        if len(keys) == 0:
            return ""

        config_desc_str = ""

        title = data.get("title", "")
        config_desc_str += "##" + title + "\n"

        required = data.get("required", [])
        for key in data["properties"]:
            opt = "OPT"
            if key in required:
                opt = "REQ"
            description = "description"
            if "description" in data["properties"][key]:
                description = data["properties"][key]["description"]
            row = "".join(
                [" - ", data["properties"][key]["title"], " (", key, ") - [", opt, "] ", description])
            config_desc_str += row + "\n"

        return config_desc_str

    def get_sample_configuration(self) -> str:
        config_loc = os.path.join(self.data_folder_loc, "config.json")

        with open(config_loc) as json_file:
            config_data = json.load(json_file)

        params = config_data.get("parameters", [])
        if not params:
            print("No parameters in data/config.json")

        for value, key in enumerate(params):
            if "#" in key:
                params[key] = "SECRET_VALUE"

        return json.dumps(config_data, indent=4)

    def set_readme_data(self) -> None:
        component_name = ""
        short_description = self.get_short_description_text()
        long_description = self.get_long_description_text()
        configuration = self.get_configuration_schema()
        row_configuration = self.get_configuration_schema(is_row_config=True)
        sample_configuration = self.get_sample_configuration()

        self.readme_data = ReadmeTemplateData(component_name=component_name,
                                              short_description=short_description,
                                              long_description=long_description,
                                              configuration=configuration,
                                              row_configuration=row_configuration,
                                              sample_configuration=sample_configuration)

    def fill_in_template(self) -> None:
        here = Path(__file__).parent
        template_location = os.path.join(here, "templates", "readme_template.md")
        with open(template_location) as f:
            template = f.read()

        tm = Template(template)
        self.readme_string = tm.render(template=self.readme_data)

    def save_readme(self, output_file: str) -> None:
        with open(output_file, "w") as out:
            out.write(self.readme_string)
