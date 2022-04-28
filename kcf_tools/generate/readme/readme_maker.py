from jinja2 import Template
from .templates.readme_template import ReadmeTemplateData
from pathlib import Path
import json


class ReadMeMaker:
    def __init__(self, config_folder_loc, data_folder_loc):
        self.config_folder_loc = config_folder_loc
        self.data_folder_loc = data_folder_loc
        self.readme_data = None
        self.readme_string = None

    def generate_readme(self):
        self.get_readme_data()
        self.fill_in_template()

    def get_short_description_text(self):
        with open(f'{self.config_folder_loc}/component_short_description.md') as f:
            short_description = f.read()
        return short_description

    def get_long_description_text(self):
        with open(f'{self.config_folder_loc}/component_long_description.md') as f:
            long_description = f.read()
        return long_description

    def get_configuration_schema(self, is_row_config=False):

        schema_location = f'{self.config_folder_loc}/configSchema.json'
        if is_row_config:
            schema_location = f'{self.config_folder_loc}/configRowSchema.json'

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

    def get_sample_configuration(self):
        config_loc = f'{self.data_folder_loc}/config.json'

        with open(config_loc) as json_file:
            config_data = json.load(json_file)

        params = config_data.get("parameters", [])
        if not params:
            print("No parameters in data/config.json")

        for value, key in enumerate(params):
            if "#" in key:
                params[key] = "SECRET_VALUE"

        return json.dumps(config_data, indent=4)

    def get_readme_data(self):
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

    def fill_in_template(self):
        here = Path(__file__).parent
        with open(f'{here}/templates/readme_template.md') as f:
            template = f.read()

        tm = Template(template)
        self.readme_string = tm.render(template=self.readme_data)

    def print_readme(self):
        pass

    def save_readme(self, output_file):
        with open(output_file, "w") as out:
            out.write(self.readme_string)
