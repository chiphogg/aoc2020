import numpy as np


class IndexedCube:
    def __init__(self, data, i_start=None):
        self.data = data

        self.i_start = i_start if i_start else (0,) * len(data.shape)
        assert len(self.i_start) == len(data.shape)

        self.i_stop = tuple(i + s for (i, s) in zip(self.i_start, data.shape))

        self._default = self._get_default_value()

    def get(self, i_tuple):
        return (
            self.data[self._data_indices(i_tuple)]
            if self._have_data(i_tuple)
            else self._default
        )

    def set(self, i_tuple, val):
        self.data[self._data_indices(i_tuple)] = val

    def d(self):
        return len(self.i_start)

    def _get_default_value(self):
        return type(self.data[self._data_indices((0,) * self.d())])()

    def _data_indices(self, i_tuple):
        return tuple(i - i_start for (i, i_start) in zip(i_tuple, self.i_start))

    def _range(self, dim, expand=0):
        return range(self.i_start[dim] - expand, self.i_stop[dim] + expand)

    def _shape(self, expand=0):
        return tuple((2 * expand + b - a) for a, b in zip(self.i_start, self.i_stop))

    def _have_data(self, i_tuple):
        return all(
            (start <= i < stop)
            for start, i, stop in zip(self.i_start, i_tuple, self.i_stop)
        )

    def _expand(self):
        copy = self.__class__(
            data=np.full(self._shape(expand=1), fill_value=".", dtype=self.data.dtype),
            i_start=tuple(i - 1 for i in self.i_start),
        )
        for i_tuple in self._full_range():
            copy.set(i_tuple, self.get(i_tuple))
        return copy

    def _full_range(self):
        return self._partial_range(0)

    def _partial_range(self, i_start):
        if i_start >= self.d():
            yield tuple()
            return
        for i in self._range(i_start):
            for rest in self._partial_range(i_start + 1):
                yield (i,) + rest


class ConwayCube(IndexedCube):
    def __init__(self, data, i_start=None):
        super().__init__(data=data, i_start=i_start)

    def count_active(self):
        return np.sum(self.data == "#")

    def execute_bootup_cycle(self):
        copy = self._expand()
        neighbour_counts = copy._all_active_neghbour_counts()
        for i_tuple in copy._full_range():
            if copy.active(i_tuple) and (not 2 <= neighbour_counts.get(i_tuple) <= 3):
                copy.set(i_tuple, ".")
            if (not copy.active(i_tuple)) and neighbour_counts.get(i_tuple) == 3:
                copy.set(i_tuple, "#")
        return copy._trim()

    def active(self, i_tuple):
        return self.get(i_tuple) == "#"

    def _trim(self):
        nonempty = [set() for _ in range(self.d())]
        for i_tuple in self._full_range():
            if self.active(i_tuple):
                for i, index in enumerate(i_tuple):
                    nonempty[i].add(index)

        data_indices = tuple(
            slice(min(ii) - i0, max(ii) + 1 - i0)
            for ii, i0 in zip(nonempty, self.i_start)
        )
        return ConwayCube(
            data=self.data[data_indices], i_start=tuple(min(ii) for ii in nonempty)
        )

    def _neighbour_indices(self, i_tuple):
        return (
            n_tuple
            for n_tuple in self._partial_neighbour_indices(i_tuple)
            if n_tuple != i_tuple
        )

    def _partial_neighbour_indices(self, i_tuple):
        if len(i_tuple) < 1:
            yield tuple()
            return
        i = i_tuple[0]
        for rest in self._partial_neighbour_indices(i_tuple[1:]):
            yield (i - 1,) + rest
            yield (i,) + rest
            yield (i + 1,) + rest

    def _all_active_neghbour_counts(self):
        data = np.zeros_like(self.data, dtype=int)
        for i_tuple in self._full_range():
            data[self._data_indices(i_tuple)] = self._count_active_neighbours(i_tuple)
        return IndexedCube(data=data, i_start=self.i_start)

    def _count_active_neighbours(self, i_tuple):
        return sum(self.active(n_tuple) for n_tuple in self._neighbour_indices(i_tuple))

    def _get_default_value(self):
        return "."
