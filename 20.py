from collections import defaultdict
import math
import sys

import numpy as np

import aoc


def main():
    harness = aoc.Harness()
    harness.attempt_part(
        _prod_corner_ids, "./20.txt", [("./20_test.txt", 20899048083289)],
    )


def _prod_corner_ids(filename):
    tiles = _read_tiles(filename)
    square = _make_square(tiles)
    assert _solve_square(tiles, square)
    return _corner_product(square)


def _solve_square(tiles, square, row=0, col=0):
    if None not in square:
        return True
    for tile_id in filter(lambda i: i not in square, tiles):
        for _ in range(2):
            for _ in range(4):
                if _tile_fits(tiles, tile_id, square, row, col):
                    square[row, col] = tile_id
                    if _solve_square(
                        tiles, square, *_next_place(row, col, len(square))
                    ):
                        return True
                    else:
                        square[row, col] = None
                tiles[tile_id].turn()
            tiles[tile_id].flip()
    return False


def _next_place(row, col, n):
    return (row, col + 1) if (col + 1 < n) else (row + 1, 0)


def _tile_fits(tiles, tile_id, square, row, col):
    return (row == 0 or tiles[tile_id].matches_up(tiles[square[row - 1][col]])) and (
        col == 0 or tiles[tile_id].matches_left(tiles[square[row][col - 1]])
    )


def _make_square(tiles):
    n = _integer_square_root(len(tiles))
    return np.array([[None for _ in range(n)] for _ in range(n)])


def _integer_square_root(n):
    i = 0
    while i * i < n:
        i += 1
    assert i * i == n
    return i


def _corner_product(square):
    return math.prod(square[i, j] for i in (0, -1) for j in (0, -1))


def _read_tiles(filename):
    with open(filename) as f:
        tiles = [ImageTile(lines) for lines in f.read().rstrip("\n").split("\n\n")]
    return {t.id: t for t in tiles}


class ImageTile:
    def __init__(self, lines):
        header, data = lines.split("\n", maxsplit=1)
        self.id = int(header.lstrip("Tile ").rstrip(":"))
        self.data = np.array([list(line) for line in data.split("\n")])
        self.size = aoc.assume_all_identical(self.data.shape)
        self.coords = Orientation(self.size)
        self._up_match_results = defaultdict(dict)
        self._left_match_results = defaultdict(dict)

    def _matches(self, them, my_start, their_start, direction):
        return all(
            self.get(my_start + i * direction) == them.get(their_start + i * direction)
            for i in range(self.size)
        )

    def _signature(self):
        return (self.id, self.coords.turned, self.coords.flipped)

    def matches_left(self, tile):
        return self._match_with_cache(
            tile,
            cache=self._left_match_results[self._signature()],
            their_start=np.array((0, self.size - 1)),
            direction=np.array((1, 0)),
        )

    def matches_up(self, tile):
        return self._match_with_cache(
            tile,
            cache=self._up_match_results[self._signature()],
            their_start=np.array((self.size - 1, 0)),
            direction=np.array((0, 1)),
        )

    def _match_with_cache(self, tile, cache, their_start, direction):
        signature = tile._signature()
        if signature in cache:
            return cache[signature]

        result = self._matches(
            them=tile,
            my_start=np.array((0, 0)),
            their_start=their_start,
            direction=direction,
        )
        cache[signature] = result
        return result

    def get(self, i_tuple):
        return self.data[self.coords.indices(i_tuple)]

    def turn(self):
        self.coords.turn()

    def flip(self):
        self.coords.flip()


class Orientation:
    def __init__(self, n):
        self.n = n
        self.turned = 0
        self.flipped = False
        self._rotation = np.array([[1, 0], [0, 1]])

    def indices(self, i_tuple):
        coords = self._origin() + self._rotation.dot(np.asarray(i_tuple))
        if self.flipped:
            coords[0] = self.n - 1 - coords[0]
        return tuple(coords)

    def turn(self):
        self.turned = (self.turned + 1) % 4
        self._rotation = self._rotation.dot(np.array([[0, -1], [1, 0]]))

    def flip(self):
        self.flipped = not self.flipped

    def _origin(self):
        return (self.n - 1) * np.array([((self.turned + 1) // 2) % 2, self.turned // 2])


if __name__ == "__main__":
    sys.exit(main())
