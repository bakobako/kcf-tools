import os

from .readme_maker import ReadMeMaker

DEFAULT_DATA_FOLDER_DIR = "data"
DEFAULT_COMPONENT_CONFIG_FOLDER_DIR = "component_config"
DEFAULT_FILE_NAME = "generated.md"


def create_dir(directory):
    generated_folder = directory
    isExist = os.path.exists(generated_folder)
    if not isExist:
        os.mkdir(generated_folder)


def generate_readme(data_dir: str = DEFAULT_DATA_FOLDER_DIR,
                    component_config_dir: str = DEFAULT_COMPONENT_CONFIG_FOLDER_DIR,
                    file_name: str = DEFAULT_FILE_NAME,
                    write_live: bool = False):
    print(write_live)
    if not write_live:
        create_dir("generated")
        create_dir("generated/readme")

    rm = ReadMeMaker(component_config_dir, data_dir)
    rm.generate_readme()

    if write_live:
        output_loc = os.path.join("README.md")
    else:
        output_loc = os.path.join("generated", "readme", file_name)

    print(f"Saving readme to {output_loc}")
    rm.save_readme(output_loc)


if __name__ == "__main__":
    generate_readme()
