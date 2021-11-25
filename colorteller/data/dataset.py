import numpy as np
import pandas as pd


class Dataset:
    def __init__(self) -> None:
        pass


class TwoDimScalar(Dataset):
    def __init__(self, ranks=None, index=None, limits=None, seed=None):
        super().__init__()

        if ranks is None:
            ranks = 2
        if index is None:
            index = ['x', 'y']
        if limits is None:
            limits = [0, 100]

        if not isinstance(ranks, int):
            raise TypeError("ranks must be a int")
        if not isinstance(index, (list, tuple)):
            raise TypeError("index must be a list or tuple")
        if not isinstance(limits, (list, tuple)):
            raise TypeError("limits must be a list or tuple")

        self.ranks = ranks
        self.limits = limits
        self.index = index
        self.columns = self._columns()
        self.seed = seed

    def _columns(self):
        column_names = []

        for i in range(self.ranks):
            column_names.append(f"col_{i}")

        return column_names

    def data(self):
        data = self._rand_data()
        dataframe = pd.DataFrame(data, columns=self.columns)

        return dataframe

    def _rand_data(self):
        np.random.seed(self.seed)
        return np.random.rand(self.ranks, self.rows)

    @property
    def rows(self):
        return len(self.index)

    @property
    def min(self):
        return self.limits[0]

    @property
    def max(self):
        return self.limits[1]

    def __len__(self):
        return self.rows
