import sys

import aoc


def main():
    harness = aoc.Harness()
    harness.attempt_part(
        _collect_labels_after_100_moves, "925176834", [("389125467", "67384529")],
    )


def _collect_labels_after_100_moves(cup_indices):
    cups = [int(i) for i in cup_indices]
    for _ in range(100):
        _make_move(cups, 3)
    return "".join(str(i) for i in _place_at_front(cups, 1)[1:])


def _make_move(cups, n):
    i_dest_stop = cups.index(_find_destination(cups, n_pickup=n)) + 1
    cups[:] = (
        cups[(n + 1) : i_dest_stop] + _pick_up(cups, n) + cups[i_dest_stop:] + [cups[0]]
    )


def _pick_up(cups, n):
    return cups[1 : (n + 1)]


def _find_destination(cups, n_pickup):
    i = cups[0]
    candidates = cups[n_pickup + 1 :]
    for _ in range(len(candidates)):
        i -= 1
        if i < 1:
            return max(candidates)
        if i in candidates:
            return i


def _place_at_front(cups, target):
    i = cups.index(target)
    return cups[i:] + cups[:i]


if __name__ == "__main__":
    sys.exit(main())
