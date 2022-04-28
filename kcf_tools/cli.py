import click
import logging
from os import path

from kcf_tools import generate as gen

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

logging.basicConfig(level=logging.INFO, format='%(message)s')

NECESSARY_PATHS = ["data",
                   "component_config",
                   path.join("data", "config.json"),
                   path.join("component_config", "component_short_description.md"),
                   path.join("component_config", "component_long_description.md"),
                   path.join("component_config", "configSchema.json"),
                   path.join("component_config", "configRowSchema.json")]


class DirectoryError(SystemExit):
    pass


def check_directories():
    for necessary_path in NECESSARY_PATHS:
        if not path.exists(necessary_path):
            raise DirectoryError(
                f"You can only run \'generate\' in a component directory. Could not find {necessary_path}")


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option()
@click.pass_context
def main(context):
    """
    The command line interface provides tools for Keboola Component development.
    This includes generating documentation and UI schemas.
    """
    if context.obj is None:
        context.obj = {}


@click.group()
def generate():
    """
    Command for generating specific files like readme docs.
    """


@click.option(
    '-w',
    is_flag=True,
    help='Writes files to component'
)
@click.command(name='readme', short_help='generate readme for component')
def generate_readme(w: bool):
    """This function generates a README file for your component"""
    logging.info("Generating Readme...")
    logging.info(f"write : {w}")
    check_directories()
    gen.generate_readme(write_live=w)


@click.command(name='docs', short_help='generate help.keboola.com documentation for component')
def generate_docs():
    """This function generates documentation for help.keboola.com for your component"""
    logging.info("Generating Help...")


generate.add_command(generate_readme)
generate.add_command(generate_docs)
main.add_command(generate)
