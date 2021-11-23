from colormath.color_conversions import convert_color
from colormath.color_objects import LabColor, sRGBColor
from loguru import logger


def sort_on_distance_to_reference(lab_colors, distance_metric, reference_color):
    """sort colors based on distance metric"""

    ref_distances = [distance_metric(c, reference_color) for c in lab_colors]
    sorted_index = sorted(range(len(ref_distances)), key=ref_distances.__getitem__)

    return {
        "colors": [lab_colors[i] for i in sorted_index],
        "indices": sorted_index,
    }


def sort_on_distance_matrix(lab_colors, distance_metric):
    """sort colors based on distance metric

    TODO: To be extended.
    """

    s = len(lab_colors)

    dist = [[distance_metric(c1, c2) for c1 in lab_colors] for c2 in lab_colors]

    # calculate the shortest path
    min_distances = []
    min_distance_indices = []
    for r in range(s - 1):
        c = r + 1
        r_dist = dist[r][c:]
        r_min_d_index = min(range(len(r_dist)), key=r_dist.__getitem__)

        min_distance = r_dist[r_min_d_index]
        min_index = (r, c + r_min_d_index)

        min_distances.append(min_distance)
        min_distance_indices.append(min_index)

    return min_distances, min_distance_indices
