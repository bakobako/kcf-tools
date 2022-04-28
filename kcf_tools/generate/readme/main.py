import os
import logging

from .readme_maker import ReadMeMaker

DEFAULT_DATA_FOLDER_DIR = "data"
DEFAULT_COMPONENT_CONFIG_FOLDER_DIR = "component_config"

logging.basicConfig(level=logging.INFO, format='%(message)s')


def create_dir(directory: str) -> None:
    generated_folder = directory
    isExist = os.path.exists(generated_folder)
    if not isExist:
        os.mkdir(generated_folder)


def generate_readme(write_live: bool,
                    data_dir: str = DEFAULT_DATA_FOLDER_DIR,
                    component_config_dir: str = DEFAULT_COMPONENT_CONFIG_FOLDER_DIR) -> None:
    """
    Generates a readme based on the component configuration schema and the configuration JSON file
    Args:
        write_live (bool): Write to live readme file if true, if false write to 'generated/readme' directory
        data_dir (str): relative location of the data directory
        component_config_dir (str): relative location of the component configuration directory

    """
    if write_live:
        output_loc = os.path.join("README.md")
    else:
        create_dir("generated")
        create_dir("generated/readme")
        output_loc = os.path.join("generated", "readme", "README.md")

    readme_maker = ReadMeMaker(component_config_dir, data_dir)
    logging.info(f"Saving readme to {output_loc}")
    readme_maker.generate_readme(output_loc)
