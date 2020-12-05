import sys

import aoc


def main():
    harness = aoc.Harness()
    harness.attempt_part(
        solve=_get_highest_seat_id, realfile="5.txt", tests=[("5a_test.txt", 820)]
    )
    harness.attempt_part(solve=_find_missing_seat_ids, realfile="5.txt", tests=[])


def _get_highest_seat_id(filename):
    return max(_seat_id(p) for p in _boarding_passes(filename))


def _find_missing_seat_ids(filename):
    ids = sorted(_seat_id(p) for p in _boarding_passes(filename))

    i_last = len(ids) - 1
    expected_id = lambda i: ids[0] + i
    assert ids[i_last] == expected_id(i_last) + 1

    i_range = [0, len(ids)]
    while i_range[1] - i_range[0] > 1:
        i = (i_range[0] + i_range[1]) // 2
        if ids[i] != expected_id(i):
            i_range[1] = i
        else:
            i_range[0] = i

    assert i_range[1] == i_range[0] + 1
    assert ids[i_range[1]] == ids[i_range[0]] + 2
    return ids[i_range[0]] + 1


def _seat_id(boarding_pass):
    (row, col) = _decode_boarding_pass(boarding_pass)
    return row * 8 + col


def _boarding_passes(filename):
    with open(filename) as f:
        return f.read().splitlines()


def _decode_boarding_pass(boarding_pass):
    row_range = [0, 128]
    col_range = [0, 8]
    for c in boarding_pass:
        row_dist = (row_range[1] - row_range[0]) // 2
        col_dist = (col_range[1] - col_range[0]) // 2
        if c == "F":
            row_range[1] -= row_dist
        if c == "B":
            row_range[0] += row_dist
        if c == "L":
            col_range[1] -= col_dist
        if c == "R":
            col_range[0] += col_dist
    return (row_range[0], col_range[0])


if __name__ == "__main__":
    sys.exit(main())
