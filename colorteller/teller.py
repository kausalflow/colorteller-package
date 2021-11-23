import json

from colormath.color_conversions import convert_color
from colormath.color_objects import LabColor, sRGBColor
from loguru import logger

from .utils.hex import Hex


class ColorTeller:
    """A middleware for colorteller web service and benchmarking colors."""

    def __init__(self, colorteller_raw=None, hex_strings=None) -> None:

        if (hex_strings is not None) and (colorteller_raw is not None):
            logger.warning(f"hex_strings is provided, will ignore colorteller_raw.")

        if hex_strings is not None:
            self.hex_strings = hex_strings
        elif colorteller_raw is not None:
            if isinstance(colorteller_raw, str):
                colorteller_raw = self.str_to_json(colorteller_raw)
            if colorteller_raw and (not isinstance(colorteller_raw, dict)):
                raise TypeError(f"colorteller_raw has to be a dict; {colorteller_raw}")

            self.hex_strings = self.get_hex_strings(colorteller_raw)
        else:
            raise Exception("No hex_strings or colorteller_raw provided.")

    def from_hex(self, hex_string):
        self.hex_strings = hex_string

    @property
    def hex(self):
        return self.hex_strings

    @property
    def rgb(self):
        rgb_tuples = [Hex(h).rgb for h in self.hex]
        return rgb_tuples

    def get_hex_strings(self, colorteller_raw):
        if colorteller_raw is None:
            return []
        colorteller_raw = colorteller_raw
        colors_raw = colorteller_raw.get("colors", [])
        self.hex_strings = [color.get("hex") for color in colors_raw]

        return self.hex_strings

    @staticmethod
    def str_to_json(data_raw):
        return json.loads(data_raw)


class Colors:
    """
    Basic information about the provided colors.
    """

    def __init__(self, color_palette=None, colorteller=None):

        if (color_palette is not None) and (colorteller is not None):
            logger.warning(f"colorteller is provided, will ignore color_palette.")

        if colorteller is not None:
            self.colorteller = colorteller
        elif color_palette is not None:
            if not isinstance(color_palette, list):
                raise TypeError(
                    f"colorteller has to be a list of dictionaries; {color_palette}"
                )
            self.color_palette = color_palette
            self.colorteller = ColorTeller(hex_strings=color_palette)
        else:
            raise Exception("No color_palette or colorteller provided.")

    @property
    def hex(self):
        return self.colorteller.hex

    @property
    def rgb(self):
        return self.colorteller.rgb

    @property
    def sRGBColor(self):
        return [sRGBColor(*rgb, is_upscaled=True) for rgb in self.rgb]

    @property
    def LabColor(self):
        return [convert_color(c, LabColor) for c in self.sRGBColor]

    def metrics(self, methods=None):
        if methods is None:
            methods = []

        metrics = []
        for m in methods:
            m_b = m(self)
            metrics.append(m_b.metric())

        return metrics
