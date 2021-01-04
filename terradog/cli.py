#!/usr/bin/env python
import click
import logging
import traceback
import coloredlogs


from . import TerraDog
from .docs import Docs
from .helpers import parse_yaml_file

logger = logging.getLogger(__name__)


@click.group()
@click.version_option()
def cli(*args, **kwargs):
    pass


@cli.command()
@click.option('--file', '-f', required=True, help='File to read Datadog object configurations from')
@click.option('--log-level', default="INFO", help="Log Level DEBUG,INFO,WARN,ERROR")
@click.option('--output', '-o', default="./", help="Directory to output the generated terraform files")
def create(**kwargs):
    """ Create All defined Datadog objects in input file to Terraform in output directory """
    coloredlogs.install(level=kwargs.get("log_level"))
    try:
        data = parse_yaml_file(kwargs.get('file'))
        location = kwargs.get('output')
        TerraDog(data, location).create()
    except Exception as e:
        logger.debug(traceback.format_exc())
        click.Abort(e)


@cli.command()
def docs(*args, **kwargs):
    """ Generates annotated documentation of the monitors available """
    print(Docs.monitors())
