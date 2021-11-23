import matplotlib.pyplot as plt
from loguru import logger
from .utils.chart import distance_matrix, noticable_matrix
from pathlib import Path


class Charts:
    def __init__(self, save_folder=None) -> None:

        self.save_folder = save_folder
        if not (self.save_folder is None):
            if isinstance(self.save_folder, str):
                self.save_folder = Path(self.save_folder)

    def _save_fig(self, save_to, name):
        """save fig to file

        Call this method after establishing ax
        """

        if save_to is None:
            pass
        elif save_to is True:
            if self.save_folder is None:
                logger.error("No save folder specified for Charts")
            else:
                plt.savefig(self.save_folder / name)
        else:
            plt.savefig(save_to)

        plt.clf()


class BenchmarkCharts(Charts):
    def __init__(self, metrics, save_folder=None) -> None:
        super().__init__(save_folder=save_folder)

        self.metrics = metrics

    def distance_matrix(self, ax=None, show=False, save_to=None):

        for b in self.metrics:
            if b["method"] == "perceptual_distance":
                data = b["data"]
                hex_strings = data["colors"]
                dist_mat = data["distances"]

                break

        ax = distance_matrix(dist_mat, hex_strings, ax=ax)
        if show:
            plt.show()

        if save_to is None:
            return ax
        else:
            self._save_fig(save_to=save_to, name="distance_matrix.png")

    def noticable_matrix(self, ax=None, show=False, save_to=None):

        for b in self.metrics:
            if b["method"] == "perceptual_distance":
                data = b["data"]
                hex_strings = data["colors"]
                noti_mat = data["noticable"]

                break

        ax = noticable_matrix(noti_mat, hex_strings, ax=ax)
        if show:
            plt.show()

        if save_to is None:
            return ax
        else:
            self._save_fig(save_to=save_to, name="noticable_matrix.png")
