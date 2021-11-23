from colorteller import teller
from colorteller.utils import benchmark
from colorteller.visualize import BenchmarkCharts
from loguru import logger
from nose import tools as _tools


def test__visualize___Charts():
    hex_strings = ["#8de4d3", "#344b46", "#74ee65", "#238910", "#a6c363", "#509d99"]

    ct = teller.ColorTeller(hex_strings=hex_strings)

    c = teller.Colors(colorteller=ct)

    m = c.metrics(
        methods=[benchmark.PerceptualDistanceBenchmark, benchmark.LightnessBenchmark]
    )

    charts = BenchmarkCharts(metrics=m, save_folder=".")

    charts.distance_matrix(show=False)

    charts.noticable_matrix(show=False)
