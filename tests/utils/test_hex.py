from nose import tools as _tools
from colorteller.utils import hex


def test__hex__Hex():

    hex_colors = ["#0000FF", "#800000", "#008000"]

    rgb_results = [(0, 0, 255), (128, 0, 0), (0, 128, 0)]

    for h, r in zip(hex_colors, rgb_results):
        _tools.eq_(hex.Hex(h).rgb, r)
