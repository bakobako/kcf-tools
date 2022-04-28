import os
from .doc_generator import HelpDocGenerator
from .cli_help_doc import cli_questions


def create_dir(directory):
    generated_folder = directory
    isExist = os.path.exists(generated_folder)
    if not isExist:
        os.mkdir(generated_folder)


def generate_help_doc():
    create_dir("generated")
    create_dir(os.path.join("generated", "help_docs"))

    user_input = cli_questions()

    help_generator = HelpDocGenerator("component_config", user_input)
    help_generator.generate_help_docs()
    dir_name = help_generator.component_folder_name
    create_dir(os.path.join("generated", "help_docs", dir_name))
    help_generator.save_help_docs(os.path.join("generated", "help_docs", dir_name))


if __name__ == "__main__":
    generate_help_doc()
