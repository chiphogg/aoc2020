import itertools
import sys

import aoc


def main():
    harness = aoc.Harness()
    harness.attempt_part(
        _find_first_not_sum_of_preamble, "./9.txt", [(("./9_test.txt", 5), 127)],
    )
    harness.attempt_part(
        _sum_bounds_of_contiguous_set_summing_to_first_invalid,
        "./9.txt",
        [(("./9_test.txt", 5), 62)],
    )


def _sum_bounds_of_contiguous_set_summing_to_first_invalid(
    filename, preamble_length=25
):
    target = _find_first_not_sum_of_preamble(filename, preamble_length)
    all_numbers = _read_values(filename)
    return sum(_bounds_of_contiguous_set_summing_to_first_invalid(all_numbers, target))


def _find_first_not_sum_of_preamble(filename, preamble_length=25):
    with open(filename) as f:
        preamble = list(map(int, itertools.islice(f, preamble_length)))
        i = 0

        for line in f:
            value = int(line)
            if _is_valid(value, preamble):
                preamble[i] = value
                i = (i + 1) % preamble_length
            else:
                return value


def _bounds_of_contiguous_set_summing_to_first_invalid(numbers, target):
    i = 0
    j = 0
    total = numbers[i]
    while j < len(numbers):
        if total == target:
            return (min(numbers[i : (j + 1)]), max(numbers[i : (j + 1)]))
        elif total < target:
            j += 1
            total += numbers[j]
        elif total > target:
            if i == j:
                i += 1
                j += 1
                total = numbers[i]
            else:
                total -= numbers[i]
                i += 1


def _read_values(filename):
    with open(filename) as f:
        return list(map(int, f))


def _is_valid(value, preamble):
    for i in range(len(preamble)):
        for j in range(i + 1, len(preamble)):
            if preamble[i] + preamble[j] == value:
                return True
    return False


if __name__ == "__main__":
    sys.exit(main())
