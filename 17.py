import sys

import numpy as np

import aoc
import conway


def main():
    harness = aoc.Harness()
    harness.attempt_part(
        _count_active_3D_after_6, "./17.txt", [("./17_test.txt", 112)],
    )
    harness.attempt_part(
        _count_active_4D_after_6, "./17.txt", [("./17_test.txt", 848)],
    )


def _count_active_4D_after_6(filename):
    return _count_active_after(data=np.array([[_initial_state(filename)]]), n=6)


def _count_active_3D_after_6(filename):
    return _count_active_after(data=np.array([_initial_state(filename)]), n=6)


def _count_active_after(data, n):
    cube = conway.ConwayCube(data)
    for _ in range(n):
        cube = cube.execute_bootup_cycle()
    return cube.count_active()


def _initial_state(filename):
    with open(filename) as f:
        return [list(line) for line in f.read().splitlines()]


if __name__ == "__main__":
    sys.exit(main())
