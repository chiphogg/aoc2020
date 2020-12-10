import collections
import math
import sys

import aoc


def main():
    harness = aoc.Harness()
    harness.attempt_part(
        _multiply_1_jolt_diffs_by_3_jolt_diffs,
        "./10.txt",
        [("./10_test_a.txt", 35), ("./10_test_b.txt", 220)],
    )
    harness.attempt_part(
        _count_arrangements,
        "./10.txt",
        [("./10_test_a.txt", 8), ("./10_test_b.txt", 19208)],
    )


def _count_arrangements(filename):
    joltages = _get_all_joltages(filename)
    return math.prod(
        _count_valid_paths(joltages, i, j) for i, j in _optional_regions(joltages)
    )


def _count_valid_paths(joltages, i, j):
    if i == j:
        return 1
    total = 0
    for step in (1, 2, 3):
        i_next = i + step
        if i_next <= j and (joltages[i_next] <= joltages[i] + 3):
            total += _count_valid_paths(joltages, i_next, j)

    return total


def _optional_regions(joltages):
    i = 0
    j = 1
    while j < len(joltages):
        if joltages[j] - joltages[j - 1] == 3:
            if (j - 2) > i:
                yield (i, j - 1)
            i = j
        j += 1


def _multiply_1_jolt_diffs_by_3_jolt_diffs(filename):
    joltages = _get_all_joltages(filename)
    joltage_diffs = collections.Counter(
        j - i for i, j in zip(joltages[:-1], joltages[1:])
    )
    return joltage_diffs[1] * joltage_diffs[3]


def _get_all_joltages(filename):
    return sorted(_append_device_and_outlet_joltages(_get_adapter_joltages(filename)))


def _get_adapter_joltages(filename):
    with open(filename) as f:
        return [int(x) for x in f.read().splitlines()]


def _append_device_and_outlet_joltages(adapter_joltages):
    adapter_joltages.extend([0, max(adapter_joltages) + 3])
    return adapter_joltages


if __name__ == "__main__":
    sys.exit(main())
