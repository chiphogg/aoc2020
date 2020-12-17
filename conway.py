import numpy as np


class IndexedCube:
    def __init__(self, data, min_z=0, min_row=0, min_col=0):
        self.data = data
        (num_layers, num_rows, num_cols) = self.data.shape
        self.range = {
            "z": (min_z, min_z + num_layers),
            "row": (min_row, min_row + num_rows),
            "col": (min_col, min_col + num_cols),
        }

    def get(self, z, row, col):
        return (
            self.data[self._data_indices(z, row, col)]
            if self._have_data(z, row, col)
            else "."
        )

    def set(self, z, row, col, val):
        self.data[self._data_indices(z, row, col)] = val

    def print(self):
        for z in self._range("z"):
            print(f"\nz={z}")
            print(f"(first col {self._min('col')})")
            for row in self._range("row"):
                row_vals = "".join(self.get(z, row, col) for col in self._range("col"))
                print(f"{row_vals} {row:3}")

    def _data_indices(self, z, row, col):
        return (
            z - self._min("z"),
            row - self._min("row"),
            col - self._min("col"),
        )

    def _range(self, label, expand=0):
        return range(self.range[label][0] - expand, self.range[label][1] + expand)

    def _min(self, label):
        return self.range[label][0]

    def _in_range(self, label, x):
        return self.range[label][0] <= x < self.range[label][1]

    def _have_data(self, z, row, col):
        return (
            self._in_range("z", z)
            and self._in_range("row", row)
            and self._in_range("col", col)
        )


class ConwayCube(IndexedCube):
    def __init__(self, data, min_z=0, min_row=0, min_col=0):
        super().__init__(data=data, min_z=min_z, min_row=min_row, min_col=min_col)

    def count_active(self):
        return sum(c == "#" for layer in self.data for row in layer for c in row)

    def execute_bootup_cycle(self):
        copy = self._expand()
        neighbour_counts = copy._all_active_neghbour_counts()
        for z, row, col in copy._full_range():
            if copy.active(z, row, col) and not (
                2 <= neighbour_counts.get(z, row, col) <= 3
            ):
                copy.set(z, row, col, ".")
            if (not copy.active(z, row, col)) and neighbour_counts.get(
                z, row, col
            ) == 3:
                copy.set(z, row, col, "#")
        return copy._trim()

    def active(self, z, row, col):
        return self.get(z, row, col) == "#"

    def _full_range(self):
        for z in self._range("z"):
            for row in self._range("row"):
                for col in self._range("col"):
                    yield (z, row, col)

    def _trim(self):
        zs = set()
        rows = set()
        cols = set()
        for z, row, col in self._full_range():
            if self.active(z, row, col):
                zs.add(z)
                rows.add(row)
                cols.add(col)

        z0, r0, c0 = (self._min("z"), self._min("row"), self._min("col"))
        return ConwayCube(
            data=self.data[
                (min(zs) - z0) : (max(zs) + 1 - z0),
                (min(rows) - r0) : (max(rows) + 1 - r0),
                (min(cols) - c0) : (max(cols) + 1 - c0),
            ],
            min_z=min(zs),
            min_row=min(rows),
            min_col=min(cols),
        )

    def _all_active_neghbour_counts(self):
        data = np.array(
            [
                [
                    [
                        self._count_active_neighbours(z, row, col)
                        for col in self._range("col")
                    ]
                    for row in self._range("row")
                ]
                for z in self._range("z")
            ]
        )
        return IndexedCube(
            data=data,
            min_z=self._min("z"),
            min_row=self._min("row"),
            min_col=self._min("col"),
        )

    def _count_active_neighbours(self, z, row, col):
        return sum(
            1
            for n_z in range(z - 1, z + 2)
            for n_row in range(row - 1, row + 2)
            for n_col in range(col - 1, col + 2)
            if self.get(n_z, n_row, n_col) == "#"
        ) - (self.get(z, row, col) == "#")

    def _expand(self):
        new_data = np.array(
            [
                [
                    [self.get(z, row, col) for col in self._range("col", expand=1)]
                    for row in self._range("row", expand=1)
                ]
                for z in self._range("z", expand=1)
            ]
        )
        return ConwayCube(
            new_data, self._min("z") - 1, self._min("row") - 1, self._min("col") - 1,
        )
