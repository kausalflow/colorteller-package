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
from colorteller.utils.cmd import prepare_paths

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
    "--target",
    "-t",
    help="Folder for save results",
    type=click.Path(exists=False),
    required=False,
    default=None,
)
@click.option(
    "--with_benchmark_charts",
    "-wbc",
    help="whether to create benchmark charts",
    type=bool,
    required=False,
    default=False,
)
def benchmark(hex_strings, target, with_benchmark_charts):
    """Benchmark input colors

    :param hex: Paper DOI, optional, can be multiple
    :type hex: Union[str, list]
    """

    ct = ColorTeller(hex_strings=hex_strings)

    colors = Colors(colorteller=ct)

    metrics = colors.metrics(methods=[PerceptualDistanceBenchmark, LightnessBenchmark])


    if target:
        paths = prepare_paths(target)
        target = paths["target"]

    if paths.get("metrics_to"):
        metrics_to = paths["metrics_to"]
        with open(metrics_to, "w") as fp:
            json.dump(metrics, fp)
    else:
        click.echo(json.dumps(metrics, indent=2))

    if with_benchmark_charts and target:
        # create visualizations
        click.echo("Creating benchmark charts...")
        vis_bm = cvis.BenchmarkCharts(metrics=metrics, save_folder=target)
        vis_bm.distance_matrix(show=False, save_to=True)
        click.echo(f"Saved distance_matrix chart to folder {target}.")
        vis_bm.noticable_matrix(show=False, save_to=True)
        click.echo(f"Saved noticable_matrix chart to folder {target}.")



