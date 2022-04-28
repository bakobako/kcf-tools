import click
import logging

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


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
    Generate commands.
    """


@click.command(name='readme', short_help='generate readme for component')
def generate_readme():
    """This function generates a README file for your component"""
    logging.info("Generating Readme...")


@click.command(name='help', short_help='generate help.keboola.com documentation for component')
def generate_help():
    """This function generates documentation for help.keboola.com for your component"""
    logging.info("Generating Help...")


generate.add_command(generate_readme)
generate.add_command(generate_help)
main.add_command(generate)
