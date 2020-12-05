from math import prod
import sys


def main():
    _part_1()
    _part_2()


def _part_2():
    slopes = [(1, 1), (1, 3), (1, 5), (1, 7), (2, 1)]

    test_result = _multiply_badness_over_slopes(slopes, "3_test.txt")

    print("Part 2")
    if test_result == 336:
        print(_multiply_badness_over_slopes(slopes, "3.txt"))
    else:
        print("Failed test (got {}, expected 336)".format(test_result))


def _multiply_badness_over_slopes(slopes, filename):
    map = Map(filename)
    return prod(_count_trees(slope, map) for slope in slopes)


def _part_1():
    slope = (1, 3)

    test_result = _count_trees(slope, Map("3_test.txt"))

    print("Part 1")
    if test_result == 7:
        print(_count_trees(slope, Map("3.txt")))
    else:
        print("Failed test (got {}, expected 7).".format(test_result))


def _count_trees(slope, map):
    (i, j) = (0, 0)
    count = 0

    while i < map.num_rows:
        count += map.is_tree(i, j)
        i += slope[0]
        j += slope[1]

    return count


class Map:
    def __init__(self, filename):
        with open(filename) as f:
            self.lines = f.read().splitlines()

        self.num_rows = len(self.lines)
        self.num_cols = _assume_all_identical(len(l) for l in self.lines)

    def is_tree(self, i, j):
        return self.lines[i][j % self.num_cols] == "#"


def _assume_all_identical(iterable):
    (common_value,) = set(iterable)
    return common_value


if __name__ == "__main__":
    sys.exit(main())
