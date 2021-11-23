from .utils.color import distance_matrix, noticable_matrix


class Charts:
    def __init__(self, metrics) -> None:
        self.metrics = metrics

    def _distance_matrix(self, ax=None):

        return distance_matrix(self.metrics.distance_matrix, ax=ax)


