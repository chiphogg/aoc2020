import sys

import numpy as np

import aoc
import conway


def main():
    harness = aoc.Harness()
    harness.attempt_part(
        _count_active_after_6, "./17.txt", [("./17_test.txt", 112)],
    )


def _count_active_after_6(filename):
    cube = conway.ConwayCube(_initial_state(filename))
    for _ in range(6):
        cube = cube.execute_bootup_cycle()
    return cube.count_active()


def _initial_state(filename):
    with open(filename) as f:
        return np.array([[list(line) for line in f.read().splitlines()]])


if __name__ == "__main__":
    sys.exit(main())
