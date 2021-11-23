from colorteller import teller
from colorteller.utils import benchmark
from loguru import logger
from nose import tools as _tools


def test__teller__ColorTeller():
    ct_raw = '{"author":"KausalFlow","colors":[{"hex":"#8de4d3","name":""},{"hex":"#344b46"},{"hex":"#74ee65"},{"hex":"#238910"},{"hex":"#a6c363"},{"hex":"#509d99"}],"date":1637142696,"expirydate":-62135596800,"file":"bobcat-yellow","hex":["8de4d3","344b46","74ee65","238910","a6c363","509d99"],"images":null,"objectID":"e0e129c8ed58316127909db84c67efcb","permalink":"//localhost:1234/colors/bobcat-yellow/","publishdate":"2021-11-17T10:51:36+01:00","summary":"This is an experiment","tags":null,"title":"Bobcat Yellow"}'

    hex_results = ["#8de4d3", "#344b46", "#74ee65", "#238910", "#a6c363", "#509d99"]

    ct = teller.ColorTeller(ct_raw)

    for r_h, h in zip(ct.hex, hex_results):
        _tools.eq_(r_h, h)


def test__teller__ColorTeller__None():

    hex_strings = ["#8de4d3", "#344b46", "#74ee65", "#238910", "#a6c363", "#509d99"]

    ct = teller.ColorTeller(hex_strings=hex_strings)

    for r_h, h in zip(ct.hex, hex_strings):
        _tools.eq_(r_h, h)


def test__teller_Colors___perceptual_distance():
    hex_strings = ["#8de4d3", "#344b46", "#74ee65", "#238910", "#a6c363", "#509d99"]

    ct = teller.ColorTeller(hex_strings=hex_strings)

    c = teller.Colors(colorteller=ct)

    logger.info(f"{c.perceptual_distance}")


def test__teller_Colors___perceptual_distance():
    hex_strings = ["#8de4d3", "#344b46", "#74ee65", "#238910", "#a6c363", "#509d99"]

    ct = teller.ColorTeller(hex_strings=hex_strings)

    c = teller.Colors(colorteller=ct)

    logger.info(f"{c.metrics(methods=[benchmark.PerceptualDistanceBenchmark])}")


def test__teller_Colors___lightness():
    hex_strings = ["#8de4d3", "#344b46", "#74ee65", "#238910", "#a6c363", "#509d99"]

    ct = teller.ColorTeller(hex_strings=hex_strings)

    c = teller.Colors(colorteller=ct)

    logger.info(f"{c.metrics(methods=[benchmark.LightnessBenchmark])}")


def test__teller_Colors___benchmark_multiple():
    hex_strings = ["#8de4d3", "#344b46", "#74ee65", "#238910", "#a6c363", "#509d99"]

    ct = teller.ColorTeller(hex_strings=hex_strings)

    c = teller.Colors(colorteller=ct)

    logger.info(
        f"{c.metrics(methods=[benchmark.PerceptualDistanceBenchmark, benchmark.LightnessBenchmark])}"
    )
