from jinja2 import Template
from .templates.help_doc_template import HelpDocTemplateData
from pathlib import Path
import os


class HelpDocGenerator:
    def __init__(self, config_folder_loc, user_input):
        self.config_folder_loc = config_folder_loc
        self.user_input = user_input
        self.help_doc_data = None
        self.help_doc_string = None
        self.component_folder_name = ""

    def generate_help_docs(self):
        self.get_help_doc_data()
        self.fill_in_template()

    def get_short_description_text(self):
        with open(os.path.join(self.config_folder_loc, "component_short_description.md")) as f:
            short_description = f.read()
        return short_description

    def get_long_description_text(self):
        with open(f'{self.config_folder_loc}/component_long_description.md') as f:
            long_description = f.read()
        return long_description

    @staticmethod
    def get_component_type_name(comp_type):
        if comp_type == "extractors":
            return "Data Source (Extractor)"
        elif comp_type == "writers":
            return "Data Destination (Writer)"
        elif comp_type == "applications":
            return "Application"

    @staticmethod
    def get_component_folder_name(comp_name):
        return comp_name.lower().replace(" ", "-")

    def get_help_doc_data(self):
        component_name = self.user_input.get("component_name")
        component_type = "".join([self.user_input.get("component_type"), "s"])
        component_type_category = self.user_input.get("component_type_category")

        component_type_new_names = self.get_component_type_name(component_type)

        self.component_folder_name = self.get_component_folder_name(component_name)

        short_description = self.get_short_description_text()
        long_description = self.get_long_description_text()

        component_main_configuration = ""
        component_further_configuration = ""

        self.help_doc_data = HelpDocTemplateData(component_name=component_name,
                                                 component_type=component_type,
                                                 component_type_new_names=component_type_new_names,
                                                 component_type_category=component_type_category,
                                                 component_folder_name=self.component_folder_name,
                                                 short_description=short_description,
                                                 long_description=long_description,
                                                 component_main_configuration=component_main_configuration,
                                                 component_further_configuration=component_further_configuration)

    def fill_in_template(self):
        here = Path(__file__).parent
        with open(os.path.join(here, "templates", "help_doc_template.md")) as f:
            template = f.read()

        tm = Template(template)
        self.help_doc_string = tm.render(template=self.help_doc_data)

    def save_help_docs(self, output_dir):
        output_file = os.path.join(output_dir, "index.md")
        with open(output_file, "w") as out:
            out.write(self.help_doc_string)
