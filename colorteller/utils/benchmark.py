from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000
from colormath.color_objects import LabColor, sRGBColor
from loguru import logger
from typing import Union, Optional
from colorteller.teller import Colors


class ColorsBenchmark:
    """A base class to create charts to benchmark the color palettes.

    :param colors: teller.Colors objects which has properties such as hex.
    """

    def __init__(self, colors: Colors) -> None:
        self.colors = colors

    @property
    def hex(self):
        return self.colors.hex

    @property
    def rgb(self):
        return self.colors.rgb

    @property
    def sRGBColor(self):
        return self.colors.sRGBColor

    @property
    def LabColor(self):
        return self.colors.LabColor

    def metric(self):
        raise NotImplementedError(
            f"metric method is not implementetd in the ColorsBenchmark base class."
        )

    def save(self):
        raise NotImplementedError(
            f"save method is not implementetd in the ColorsBenchmark base class."
        )


class PerceptualDistanceBenchmark(ColorsBenchmark):
    """Create benchmark based on perceptual distances.

    !!! note "Used in `teller.Colors.metrics`"
        While this class can be used independently, it is mostly designed for the `methods` argument of `teller.Colors.metrics`, e.g., `methods=[PerceptualDistanceBenchmark]`.

    :param colors: teller.Colors object which has properties such as hex.
    """

    def __init__(self, colors: Colors) -> None:
        super().__init__(colors)

    def metric(self):
        """calculate the metrics of the current benchmark"""
        return {
            "method": "perceptual_distance",
            "data": self._perceptual_distance(self.LabColor),
        }

    def _perceptual_distance(self, colors: Colors, matrix=True):
        """_perceptual_distance takes a Colors object and returns a dict with the perceptual distance between each color in it.

        :param colors: a Colors object
        :param matrix: whether to create a distance matrix, defaults to True
        :type matrix: bool, optional
        :return: a dictionary of the benchmark result
        :rtype: dict
        """
        if matrix is False:
            return self._perceptual_distance_list(colors)
        else:
            return self._perceptual_distance_matrix(colors)

    def _perceptual_distance_matrix(self, colors):
        """Calculates the perceptual distance matrix

        :param colors: a Colors object
        :return: a dictionary of the benchmark result
        :rtype: dict
        """
        pd = []
        for ci in colors:
            ci_pd = []
            for cj in colors:
                ci_pd.append(delta_e_cie2000(ci, cj))
            pd.append(ci_pd)

        pd_noticable = []
        for pd_row in pd:
            pd_noticable_row = []
            for d in pd_row:
                pd_noticable_row.append(self._delta_e_noticable_distance(d))
            pd_noticable.append(pd_noticable_row)

        return {
            "colors": self.hex,
            "lab": [c.get_value_tuple() for c in colors],
            "distances": pd,
            "noticable": pd_noticable,
        }

    def _perceptual_distance_list(self, colors, sort=False):
        """Calculates a list of perceptual distance

        :param colors: a Colors object
        :return: a dictionary of the benchmark result
        :rtype: dict
        """
        logger.debug(
            f"Calculating perceptual distance for {len(colors)} colors: {colors}."
        )
        if sort is True:
            logger.debug("Sorting colors by perceptual distance.")
            sorted_lab_colors_ = self._sort_on_distance(colors, delta_e_cie2000)
            logger.debug(f"Sorted colors by perceptual distance: {sorted_lab_colors_}")
            sorted_lab_colors = sorted_lab_colors_["colors"]
            logger.debug(f"Sorted colors by perceptual distance: {sorted_lab_colors}")
            sorted_hex = [self.hex[i] for i in sorted_lab_colors_["indices"]]
            logger.debug(f"Sorted colors by perceptual distance: {sorted_hex}")
            distances = [
                delta_e_cie2000(c1, c2)
                for c1, c2 in zip(sorted_lab_colors[:-1], sorted_lab_colors[1:])
            ]
            res = {
                "hex": sorted_hex,
                "lab": [c.get_value_tuple() for c in sorted_lab_colors],
                "distances": distances,
            }
        else:
            distances = [
                delta_e_cie2000(c1, c2) for c1, c2 in zip(colors[:-1], colors[1:])
            ]
            res = {
                "hex": self.hex,
                "lab": [c.get_value_tuple() for c in colors],
                "distances": distances,
            }

        res["noticable"] = [
            self._delta_e_noticable_distance(d) for d in res["distances"]
        ]

        return res

    def _delta_e_noticable_distance(
        self, distance: float, threshold: Union[int, float] = 5
    ):
        """Decide whether the two colors are noticable based on deltaE distance.

        If the distance is larger than threshold, the two colors are noticable.

        !!! note "References"
            The choice of the threshold is based on the following paper:

            Mokrzycki WS, Tatol M. Color difference Delta E - A survey. Machine Graphics and Vision. 2011;20: 383–411. Available: https://www.semanticscholar.org/paper/Color-difference-Delta-E-A-survey/67d9178f7bad9686c002b721138e26124f6e2e35

        :param distance: the deltaE distance
        :type distance: float
        :param threshold: the threshold to decide whether the two colors are noticable, defaults to 5
        :type threshold: int, optional
        :return: whether the two colors are noticable
        :rtype: bool
        """
        if distance > threshold:
            return True
        else:
            return False

    @staticmethod
    def _sort_on_distance(lab_colors: list, distance_metric, reference_color=None):
        """sort the colors based on distance between each other.

        :param lab_colors: a list of colors in lab color space
        :type lab_colors: list
        :param distance_metric: the distance metric to use, it should be a function that takes two colors as arguments and returns the distance.
        :param reference_color: the reference color to use, defaults to None
        """
        if reference_color is None:
            reference_color_rgb = sRGBColor(rgb_r=255, rgb_g=255, rgb_b=255)
            reference_color = convert_color(reference_color_rgb, LabColor)
        elif isinstance(reference_color, str):
            if reference_color == "white":
                reference_color = convert_color(
                    sRGBColor(rgb_r=255, rgb_g=255, rgb_b=255), LabColor
                )
            elif reference_color == "black":
                reference_color = convert_color(
                    sRGBColor(rgb_r=0, rgb_g=0, rgb_b=0), LabColor
                )

        ref_distances = [distance_metric(c, reference_color) for c in lab_colors]
        sorted_index = sorted(range(len(ref_distances)), key=ref_distances.__getitem__)

        return {
            "colors": [lab_colors[i] for i in sorted_index],
            "indices": sorted_index,
        }


class LightnessBenchmark(ColorsBenchmark):
    """Benchmark color palette based on lightness.

    !!! note "Lightness"
        If a color is too light, it would be very hard to read on white background. If a color is too dark, it would be hard to read on black background.

    :param colors: teller.Colors object which has properties such as hex.
    """

    def __init__(self, colors):
        super().__init__(colors)

    def metric(self):
        """calculate the metrics of the current benchmark"""
        return {
            "method": "lightness",
            "data": self._lightness_benchmark(
                self.LabColor, min_lightness=25, max_lightness=85
            ),
        }

    def _smaller_than_max(self, color, max_lightness: int = 85):
        """Whether the lightness of the color is larger than the max value set here

        :param color: a color in Lab color space with a `lab_l` property
        :param max_lightness: the max lightness value, defaults to 85
        """
        return color.lab_l <= max_lightness

    def _greater_than_min(self, color, min_lightness: int = 25):
        """Whether the lightness of the color is lighter than the min value set here.

        :param color: a color in Lab color space with a `lab_l` property
        :param min_lightness: the min lightness value, defaults to 25
        """
        return color.lab_l >= min_lightness

    def _bounded_by_min_max(self, color, min_lightness=25, max_lightness=85):
        """Wheter the color lightness is bounded by min and max.

        :param color: a color in Lab color space with a `lab_l` property
        :param min_lightness: the min lightness value, defaults to 25
        :param max_lightness: the max lightness value, defaults to 85
        """
        return self._greater_than_min(color, min_lightness) and self._smaller_than_max(
            color, max_lightness
        )

    def _lightness_benchmark(self, colors, min_lightness=25, max_lightness=85):
        """_lightness_benchmark calculates all the benchmarks based on lightness.

        :param colors: a list of colors in Lab color space
        :type colors: list
        :param min_lightness: the min lightness value, defaults to 25
        :type min_lightness: int, optional
        :param max_lightness: the max lightness value, defaults to 85
        :type max_lightness: int, optional
        :return: the benchmark results
        :rtype: dict
        """
        return {
            "lightness": [c.lab_l for c in colors],
            "min_lightness": min_lightness,
            "max_lightness": max_lightness,
            "smaller_than_max": [
                self._smaller_than_max(c, max_lightness) for c in colors
            ],
            "greater_than_min": [
                self._greater_than_min(c, min_lightness) for c in colors
            ],
            "bounded_by_min_max": [
                self._bounded_by_min_max(c, min_lightness, max_lightness)
                for c in colors
            ],
        }
