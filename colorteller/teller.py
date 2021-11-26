import json
from typing import Optional, Union

from colormath.color_conversions import convert_color
from colormath.color_objects import LabColor, sRGBColor
from loguru import logger

from .utils.hex import Hex


class ColorTeller:
    """A middleware for colorteller web service and benchmarking colors. It takes the color representations on the colorteller web service and converts them to an easy-to-use object.

    There are two different methods to instantiate a ColorTeller object:

    1. Provide a list of hex strings.
    2. Provide a dictionary or json string from the colorteller web service.

    Here are some examples:

    1. Using a list of hex strings:

        ```python
        from colorteller import teller

        hex_strings = [
            "#8de4d3", "#344b46", "#74ee65", "#238910", "#a6c363", "#509d99"
        ]
        ct = teller.ColorTeller(hex_strings=hex_strings)
        ```

    2. Using a json string:

        ```python
        from colorteller import teller

        ct_raw = '{"author":"KausalFlow","colors":[{"hex":"#8de4d3","name":""},{"hex":"#344b46"},{"hex":"#74ee65"},{"hex":"#238910"},{"hex":"#a6c363"},{"hex":"#509d99"}],"date":1637142696,"expirydate":-62135596800,"file":"bobcat-yellow","hex":["8de4d3","344b46","74ee65","238910","a6c363","509d99"],"images":null,"objectID":"e0e129c8ed58316127909db84c67efcb","permalink":"//localhost:1234/colors/bobcat-yellow/","publishdate":"2021-11-17T10:51:36+01:00","summary":"This is an experiment","tags":null,"title":"Bobcat Yellow"}'
        hex_results = [
            "#8de4d3", "#344b46", "#74ee65", "#238910", "#a6c363", "#509d99"
        ]
        ct = teller.ColorTeller(ct_raw)
        ```

    !!! note
        While we can use this to get some properties of the palette, this is mostly for downstream tasks.

    :param colorteller_raw: A dict (or json string of dict) of the raw response from colorteller web service, defaults to [DefaultParamVal]
    :type colorteller_raw: Union[dict, str]
    :param hex_strings: A list of hex strings for the color palette.
    :type hex_strings: list
    """

    def __init__(
        self,
        colorteller_raw: Optional[Union[dict, str]] = None,
        hex_strings: Optional[list] = None,
    ) -> None:

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

    def from_hex(self, hex_strings: list) -> None:
        """set `hex_strings` property using a list of hex_strings.

        There is no return value. The `hex_strings` property is set using the input.

        :param hex_strings: A list of hex strings for the color palette.
        """
        self.hex_strings = hex_strings

    @property
    def hex(self):
        """a list of hex strings of the palette"""
        return self.hex_strings

    @property
    def rgb(self):
        """a list of rgb tuples of the palette"""
        rgb_tuples = [Hex(h).rgb for h in self.hex]
        return rgb_tuples

    def get_hex_strings(self, colorteller_raw: Union[dict, str, None]) -> list:
        """Extract hex_strings from colorteller web service json or dict representation of the color palette.

        :param colorteller_raw: A dict (or json string of dict) of the raw response from colorteller web service.
        :return: A list of hex strings for the color palette.
        :rtype: list
        """
        if colorteller_raw is None:
            return []
        colorteller_raw = colorteller_raw
        colors_raw = colorteller_raw.get("colors", [])
        self.hex_strings = [color.get("hex") for color in colors_raw]

        return self.hex_strings

    @staticmethod
    def str_to_json(data_raw):
        """convert the json string to dictionary

        :param data_raw: A json string of the raw response from colorteller web service.
        :return: dictionary of the raw response from colorteller web service.
        :rtype: dict
        """
        return json.loads(data_raw)


class Colors:
    """A color palette container with benchmark results.

    To instantiate a Colors object, provide a list of hex strings (`color_palette`) or a ColorTeller object (`colorteller`).

    !!! warning
        If `colorteller` is provided, the `color_palette` argument will be ignored.

    ```python
    from colorteller import teller

    hex_strings = [
        "#8de4d3", "#344b46", "#74ee65", "#238910", "#a6c363", "#509d99"
    ]
    ct = teller.ColorTeller(hex_strings=hex_strings)
    c = teller.Colors(colorteller=ct)
    ```

    We could get the metrics from the Colors object.

    ```python
    from colorteller.utils import benchmark

    m = c.metrics(methods=[benchmark.PerceptualDistanceBenchmark])
    ```

    :param color_palette: A list of hex strings.
    :type color_palette: list
    :param colorteller: an ColorTeller object
    :type colorteller: ColorTeller
    """

    def __init__(
        self,
        color_palette: Optional[list] = None,
        colorteller: Optional[ColorTeller] = None,
    ):

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
        """a list of hex strings"""
        return self.colorteller.hex

    @property
    def rgb(self):
        """a list of rgb tuples"""
        return self.colorteller.rgb

    @property
    def sRGBColor(self):
        """a list of sRGBColor objects"""
        return [sRGBColor(*rgb, is_upscaled=True) for rgb in self.rgb]

    @property
    def LabColor(self):
        """a list of LabColor objects"""
        return [convert_color(c, LabColor) for c in self.sRGBColor]

    def metrics(self, methods: Optional[list] = None):
        """Calculates a list of metrics using the methods provided.

        :param methods: A list of methods to use to calculate the metrics.
        :type methods: list
        :return: A list of metrics.
        :rtype: list
        """
        if methods is None:
            methods = []

        metrics = []
        for m in methods:
            m_b = m(self)
            metrics.append(m_b.metric())

        return metrics
