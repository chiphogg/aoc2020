import collections
import sys

import numpy as np

import aoc


def main():
    harness = aoc.Harness()
    harness.attempt_part(
        _count_black_tiles, "./24.txt", [("./24_test.txt", 10)],
    )


def _count_black_tiles(filename):
    flips = _count_flips(_read_tile_lines(filename))
    return sum(i % 2 for i in flips.values())


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
