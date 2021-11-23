from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000
from colormath.color_objects import LabColor, sRGBColor
from loguru import logger


class ColorsBenchmark:
    """
    Create charts to benchmark the color palettes.

    :colors: teller.Colors objects which has properties such as hex.
    """

    def __init__(self, colors) -> None:
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
        pass


class PerceptualDistanceBenchmark(ColorsBenchmark):
    def __init__(self, colors):
        super().__init__(colors)

    def metric(self):
        return {
            "method": "perceptual_distance",
            "data": self._perceptual_distance(self.LabColor),
        }

    def _perceptual_distance(self, colors, matrix=True):
        if matrix is False:
            return self._perceptual_distance_list(colors)
        else:
            return self._perceptual_distance_matrix(colors)

    def _perceptual_distance_matrix(self, colors):
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

    def _delta_e_noticable_distance(self, distance, threshold=5):
        """Decide whether the two colors are noticable based on deltaE distance

        The choice of the threshold is based on the following paper:

        Mokrzycki WS, Tatol M. Color difference Delta E - A survey. Machine Graphics and Vision. 2011;20: 383–411. Available: https://www.semanticscholar.org/paper/Color-difference-Delta-E-A-survey/67d9178f7bad9686c002b721138e26124f6e2e35
        """
        if distance > threshold:
            return True
        else:
            return False

    @staticmethod
    def _sort_on_distance(lab_colors, distance_metric, reference_color=None):
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
    def __init__(self, colors):
        super().__init__(colors)

    def metric(self):
        return {
            "method": "lightness",
            "data": self._lightness_benchmark(
                self.LabColor, min_lightness=25, max_lightness=85
            ),
        }

    def _smaller_than_max(self, color, max_lightness=85):
        return color.lab_l <= max_lightness

    def _greater_than_min(self, color, min_lightness=25):
        return color.lab_l >= min_lightness

    def _bounded_by_min_max(self, color, min_lightness=25, max_lightness=85):
        return self._greater_than_min(color, min_lightness) and self._smaller_than_max(
            color, max_lightness
        )

    def _lightness_benchmark(self, colors, min_lightness=25, max_lightness=85):
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


class Template:
    def __init__(self) -> None:
        pass

    @staticmethod
    def _name_difference(colors):
        raise NotImplementedError(f"_name_difference has not yet been implamented.")

    @staticmethod
    def _pair_preference(colors):
        raise NotImplementedError(f"_pair_preference has not yet been implamented.")

    @staticmethod
    def _name_uniqueness(colors):
        raise NotImplementedError(f"_name_uniqueness has not yet been implamented.")
