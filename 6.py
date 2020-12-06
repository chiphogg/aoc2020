import sys
from functools import reduce

import aoc


def main():
    harness = aoc.Harness()
    harness.attempt_part(_count_anyone_yes_per_group, "6.txt", [("6_test.txt", 11)])
    harness.attempt_part(_count_everyone_yes_per_group, "6.txt", [("6_test.txt", 6)])


def _count_anyone_yes_per_group(filename):
    return sum(_count_all_yes(group) for group in _customs_groups(filename))


def _count_everyone_yes_per_group(filename):
    return sum(_count_universal_yes(group) for group in _customs_groups(filename))


def _count_all_yes(group):
    return len(reduce(lambda a, b: set(a).union(set(b)), group))


def _count_universal_yes(group):
    return len(reduce(lambda a, b: set(a).intersection(set(b)), group))


def _customs_groups(filename):
    with open(filename) as f:
        return (
            (set(filter(_is_yes, set(x))) for x in group_lines.split("\n"))
            for group_lines in f.read().rstrip("\n").split("\n\n")
        )


def _is_yes(key):
    return "a" <= key <= "z"


if __name__ == "__main__":
    sys.exit(main())
