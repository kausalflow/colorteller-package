import matplotlib.pyplot as plt
from loguru import logger
from colorteller.utils.chart import distance_matrix, noticable_matrix
from pathlib import Path
import colorteller.data.dataset as ds
import seaborn as sns

sns.set(style="white")


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


class ApplicationCharts(Charts):
    def __init__(self, colors, save_folder=None) -> None:
        super().__init__(save_folder=save_folder)
        self.colors = colors
        self.hex_strings = self.colors.hex
        self.data = self._data()

    def _data(self):
        tds = ds.TwoDimScalar(column=self.hex_strings, index=5, seed=42)
        ods_constant = ds.OneDimScalar(index=self.hex_strings, seed=42, mode="constant")

        return {"two_dim_scalar": tds, "one_dim_scalar__const": ods_constant}

    def bar_chart(self, ax=None, show=False, save_to=None):
        filename = "ac_bar_chart.png"
        tds = self.data["two_dim_scalar"]
        ax = tds.data().plot.bar(stacked=True, color=self.hex_strings)
        if show:
            plt.show()

        if save_to is None:
            return ax
        else:
            self._save_fig(save_to=save_to, name=filename)

        return {"filename": filename}

    def line_chart(self, ax=None, show=False, save_to=None):
        filename = "ac_line_chart.png"
        tds = self.data["two_dim_scalar"]

        ax = tds.data().plot.line(color=self.hex_strings)
        if show:
            plt.show()

        if save_to is None:
            return ax
        else:
            self._save_fig(save_to=save_to, name=filename)

        return {"filename": filename}

    def scatter_chart(self, ax=None, show=False, save_to=None):
        filename = "ac_scatter_chart.png"
        tds = self.data["two_dim_scalar"]
        df = tds.data().reset_index()

        ax = df.plot.scatter(
            x="index", y=self.hex_strings[0], color=self.hex_strings[0],
            label=self.hex_strings[0]
        )
        for h in self.hex_strings[1:]:
            df.plot.scatter(x="index", y=h, ax=ax, color=h, label=h)

        ax.set_xlabel("")
        ax.set_ylabel("")
        plt.legend()
        if show:
            plt.show()

        if save_to is None:
            return ax
        else:
            self._save_fig(save_to=save_to, name=filename)

        return {"filename": filename}

    def donut_chart(self, ax=None, show=False, save_to=None):
        filename = "ac_donut_chart.png"
        ods_const = self.data["one_dim_scalar__const"]
        df = ods_const.data()

        ax = df.plot.pie(
            colors=self.hex_strings
        )
        centre_circle = plt.Circle((0, 0), 0.70, fc='white')
        fig = plt.gcf()
        fig.gca().add_artist(centre_circle)
        ax.set_xlabel("")
        ax.set_ylabel("")

        if show:
            plt.show()

        if save_to is None:
            return ax
        else:
            self._save_fig(save_to=save_to, name=filename)

        return {"filename": filename}

    def charts(self, save_to=None):
        dispatcher = {
            "bar_chart": self.bar_chart(save_to=save_to),
            "line_chart": self.line_chart(save_to=save_to),
            "scatter_chart": self.scatter_chart(save_to=save_to),
            "donut_chart": self.donut_chart(save_to=save_to),
        }

        res = {}

        for k in dispatcher:
            res[k] = dispatcher[k]

        return res

