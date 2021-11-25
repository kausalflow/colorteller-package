import numpy as np
import pandas as pd


class Dataset:
    def __init__(self) -> None:
        pass


class TwoDimScalar(Dataset):
    def __init__(self, column=None, index=None, limits=None, seed=None):
        super().__init__()

        if column is None:
            column = 2
        if index is None:
            index = 5
        if limits is None:
            limits = [0, 100]

        if isinstance(column, int):
            column = self._columns(column)
        elif not isinstance(column, (list, tuple)):
            raise TypeError("column should be: int, list or tuple")
        if isinstance(index, int):
            index = self._indices(index)
        elif not isinstance(index, (list, tuple)):
            raise TypeError("index should be int, list or tuple")
        if not isinstance(limits, (list, tuple)):
            raise TypeError("limits must be a list or tuple")

        self.column = column
        self.limits = limits
        self.index = index
        self.seed = seed

    def _columns(self, length):
        column_names = []

        for i in range(length):
            column_names.append(f"col_{i}")

        return column_names

    def _indices(self, length):
        index = []

        for i in range(length):
            index.append(f"idx_{i}")

        return index

    def data(self):
        data = self._rand_data()
        dataframe = pd.DataFrame(data, columns=self.column, index=self.index)

        return dataframe

    def _rand_data(self):
        np.random.seed(self.seed)
        return np.random.rand(self.rows, self.columns)

    @property
    def rows(self):
        return len(self.index)

    @property
    def columns(self):
        return len(self.column)

    @property
    def min(self):
        return self.limits[0]

    @property
    def max(self):
        return self.limits[1]

    def __len__(self):
        return self.rows


class OneDimScalar(Dataset):
    def __init__(self, index=None, limits=None, seed=None, mode=None):
        super().__init__()

        if index is None:
            index = 5
        if limits is None:
            limits = [0, 100]

        if isinstance(index, int):
            index = self._indices(index)
        elif not isinstance(index, (list, tuple)):
            raise TypeError("index should be int, list or tuple")
        if not isinstance(limits, (list, tuple)):
            raise TypeError("limits must be a list or tuple")

        if mode is None:
            mode = "rand"

        self.limits = limits
        self.index = index
        self.seed = seed
        self.mode = mode

    def _indices(self, length):
        index = []

        for i in range(length):
            index.append(f"idx_{i}")

        return index

    def data(self):
        data = self._rand_data()
        series = pd.Series(data, index=self.index)

        return series

    def _rand_data(self):
        if self.mode == "rand":
            np.random.seed(self.seed)
            return np.random.rand(self.rows)
        elif self.mode == "constant":
            return np.ones(self.rows) * self.max
        else:
            raise ValueError("mode should be: rand, linear or constant")

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
