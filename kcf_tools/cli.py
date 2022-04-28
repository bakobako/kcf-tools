import click
import logging


@click.group()
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


@click.command(name='readme')
def generate_readme():
    logging.info("Generating Readme...")


@click.command(name='help')
def generate_help():
    logging.info("Generating Help...")


generate.add_command(generate_readme)
generate.add_command(generate_help)
main.add_command(generate)
