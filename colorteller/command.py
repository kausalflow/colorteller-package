import json
import os
import sys
from pathlib import Path
from typing import Optional, Union

import click
from loguru import logger

from colorteller.teller import Colors, ColorTeller
from colorteller.utils.benchmark import LightnessBenchmark, PerceptualDistanceBenchmark
import colorteller.visualize as cvis

logger.remove()
logger.add(sys.stderr, level="INFO", enqueue=True)


__CWD__ = os.getcwd()


@click.group(invoke_without_command=True)
@click.pass_context
def colorteller(ctx):
    if ctx.invoked_subcommand is None:
        click.echo("Hello {}".format(os.environ.get("USER", "")))
        click.echo("Welcome to colorteller. Use colorteller --help for help.")
    else:
        pass


@colorteller.command()
@click.option("--hex_strings", "-h", help="RGB hex color", multiple=True)
@click.option(
    "--metrics_to",
    "-mt",
    help="Save metric JSON results to file",
    type=click.Path(exists=False),
    required=False,
    default=None,
)
def benchmark(hex_strings, metrics_to, charts_to):
    """Benchmark input colors

    :param hex: Paper DOI, optional, can be multiple
    :type hex: Union[str, list]
    """

    ct = ColorTeller(hex_strings=hex_strings)

    colors = Colors(colorteller=ct)

    metrics = colors.metrics(methods=[PerceptualDistanceBenchmark, LightnessBenchmark])

    if metrics_to:
        with open(metrics_to, "w") as fp:
            json.dump(metrics, fp)
    else:
        click.echo(json.dumps(metrics, indent=2))

    if charts_to:
        ax_dm = cvis.distance_matrix(metrics)

    return metrics
