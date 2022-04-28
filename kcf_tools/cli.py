import click
import logging

from kcf_tools import generate as gen

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

logging.basicConfig(level=logging.INFO, format='%(message)s')


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
    help='Overwrites existing files'
)
@click.command(name='readme', short_help='generate readme for component')
def generate_readme(w):
    """This function generates a README file for your component"""
    logging.info("Generating Readme...")
    logging.info(f"write : {w}")
    gen.generate_readme()


@click.command(name='docs', short_help='generate help.keboola.com documentation for component')
def generate_docs():
    """This function generates documentation for help.keboola.com for your component"""
    logging.info("Generating Help...")


generate.add_command(generate_readme)
generate.add_command(generate_docs)
main.add_command(generate)
