class HelpDocTemplateData:
    def __init__(self,
                 component_name="",
                 component_type="",
                 component_type_new_names="",
                 component_type_category="",
                 component_folder_name="",
                 short_description="",
                 long_description="",
                 component_main_configuration="",
                 component_further_configuration=""):
        self.component_name = component_name
        self.component_type = component_type
        self.component_type_new_names = component_type_new_names
        self.component_type_category = component_type_category
        self.component_folder_name = component_folder_name
        self.short_description = short_description
        self.long_description = long_description
        self.component_main_configuration = component_main_configuration
        self.component_further_configuration = component_further_configuration


