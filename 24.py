import collections
import sys

import numpy as np

import aoc


def main():
    harness = aoc.Harness()
    harness.attempt_part(
        _count_black_tiles, "./24.txt", [("./24_test.txt", 10)],
    )
    harness.attempt_part(
        _count_black_after_100_days, "./24.txt", [("./24_test.txt", 2208)],
    )


def _count_black_after_100_days(filename):
    black = _black_tiles(_count_flips(_read_tile_lines(filename)))
    for _ in range(100):
        black = set.symmetric_difference(black, _coords_to_flip(black))
    return len(black)


def _coords_to_flip(black):
    return {
        c
        for c in _all_coords(black)
        if (c in black and _num_black_neighbours(c, black) not in (1, 2))
        or (c not in black and _num_black_neighbours(c, black) == 2)
    }


def _all_coords(black):
    return set.union(
        black, {(a + i, b + j) for (a, b) in black for (i, j) in _neighbour_coords()}
    )


def _num_black_neighbours(c, black):
    a, b = c
    return sum((a + i, b + j) in black for (i, j) in _neighbour_coords())


def _neighbour_coords():
    return ((1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1), (1, -1))


def _count_black_tiles(filename):
    return len(_black_tiles(_count_flips(_read_tile_lines(filename))))


def _black_tiles(flips):
    return {i for i in flips if flips[i] % 2}


def _count_flips(tile_lines):
    return collections.Counter(_tile_coords(t) for t in tile_lines)


def _read_tile_lines(filename):
    with open(filename) as f:
        return f.read().splitlines()


def _tile_coords(tile_line):
    return tuple(sum(np.array(m) for m in _moves(tile_line)))


def _moves(tile_line):
    n = s = 0
    for c in tile_line:
        if c == "n":
            n = 1
        if c == "s":
            s = 1
        if c == "e":
            yield (1 - n, n - s)
        if c == "w":
            yield (s - 1, n - s)
        if c in "ew":
            n = s = 0


if __name__ == "__main__":
    sys.exit(main())
