import json
from .utils.hex import Hex
from loguru import logger
from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000


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

    def metrics(self):
        colors = self.LabColor

        self.metrics = {
            # "name_difference": self._name_difference(colors),
            "perceptual_distance": self._perceptual_distance(colors),
            # "pair_preference": self._pair_preference(colors),
        }

        return self.metrics

    @staticmethod
    def _name_difference(colors):
        raise NotImplementedError(f"_name_difference has not yet been implamented.")

    def _perceptual_distance(self, colors, matrix=False):
        if matrix is False:
            return self._perceptual_distance_list(colors)
        else:
            return self._perceptual_distance_matrix(colors)

    @staticmethod
    def _pair_preference(colors):
        raise NotImplementedError(f"_pair_preference has not yet been implamented.")

    @staticmethod
    def _name_uniqueness(colors):
        raise NotImplementedError(f"_name_uniqueness has not yet been implamented.")

    @staticmethod
    def _perceptual_distance_matrix(colors):
        pd = []
        for ci in colors:
            ci_pd = []
            for cj in colors:
                ci_pd.append(delta_e_cie2000(ci, cj))
            pd.append(ci_pd)

        return pd

    def _perceptual_distance_list(self, colors, sort=True):
        logger.debug(f"Calculating perceptual distance for {len(colors)} colors: {colors}.")
        if sort is True:
            logger.debug("Sorting colors by perceptual distance.")
            sorted_lab_colors_ = self._sort_on_distance(colors, delta_e_cie2000)
            logger.debug(f"Sorted colors by perceptual distance: {sorted_lab_colors_}")
            sorted_lab_colors = sorted_lab_colors_["colors"]
            logger.debug(f"Sorted colors by perceptual distance: {sorted_lab_colors}")
            sorted_colors = [self.hex[i] for i in sorted_lab_colors_["indices"]]
            logger.debug(f"Sorted colors by perceptual distance: {sorted_colors}")
            distances = [
                delta_e_cie2000(c1, c2)
                for c1, c2 in zip(sorted_lab_colors[:-1], sorted_lab_colors[1:])
            ]
            res = {
                "colors": sorted_colors,
                "lab": [c.get_value_tuple() for c in sorted_lab_colors],
                "distances": distances,
            }
        else:
            distances = [
                delta_e_cie2000(c1, c2) for c1, c2 in zip(colors[:-2], colors[1:])
            ]
            res = {
                "colors": self.hex,
                "lab": [c.get_value_tuple() for c in colors],
                "distances": distances
            }

        return res

    @staticmethod
    def _sort_on_distance(lab_colors, distance_metric):
        ref = lab_colors[0]
        ref_distances = [distance_metric(c, ref) for c in lab_colors]
        sorted_index = sorted(range(len(ref_distances)), key=ref_distances.__getitem__)

        return {
            "colors": [lab_colors[i] for i in sorted_index],
            "indices": sorted_index,
        }


class ColorsBenchmark:
    """
    Create charts to benchmark the color palettes.
    """

    def __init__(self) -> None:
        pass

    def save(self):
        pass


if __name__ == "__main__":

    data_raw = '[{"author":"KausalFlow","colors":[{"hex":"#8de4d3","name":""},{"hex":"#344b46"},{"hex":"#74ee65"},{"hex":"#238910"},{"hex":"#a6c363"},{"hex":"#509d99"}],"date":1637142696,"expirydate":-62135596800,"file":"bobcat-yellow","hex":["8de4d3","344b46","74ee65","238910","a6c363","509d99"],"images":null,"objectID":"e0e129c8ed58316127909db84c67efcb","permalink":"//localhost:1234/colors/bobcat-yellow/","publishdate":"2021-11-17T10:51:36+01:00","summary":"This is an experiment","tags":null,"title":"Bobcat Yellow"}]'

    ct = ColorTeller(data_raw)
    c = Colors(colorteller=ct)

    logger.info(f"{c.perceptual_distance}")

    print(c)
