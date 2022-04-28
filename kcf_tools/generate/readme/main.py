import os

from .readme_maker import ReadMeMaker

DEFAULT_DATA_FOLDER_DIR = "data"
DEFAULT_COMPONENT_CONFIG_FOLDER_DIR = "component_config"
DEFAULT_OUTPUT_LOC = "generated.md"


def create_dir(directory):
    generated_folder = directory
    isExist = os.path.exists(generated_folder)
    if not isExist:
        os.mkdir(generated_folder)


def generate_readme(data_dir: str = DEFAULT_DATA_FOLDER_DIR,
                    component_config_dir: str = DEFAULT_COMPONENT_CONFIG_FOLDER_DIR,
                    output_loc: str = DEFAULT_OUTPUT_LOC):
    create_dir("generated")
    create_dir("generated/readme")
    rm = ReadMeMaker(component_config_dir, data_dir)
    rm.generate_readme()
    output_loc = os.path.join("generated", "readme", output_loc)
    rm.save_readme(output_loc)


if __name__ == "__main__":
    generate_readme()
