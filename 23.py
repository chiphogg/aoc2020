import sys

import aoc


def main():
    harness = aoc.Harness()
    harness.attempt_part(
        _collect_labels_after_100_moves, "925176834", [("389125467", "67384529")],
    )
    harness.attempt_part(
        _multiply_2_labels_after_1e7_moves_1e6_cups,
        "925176834",
        [("389125467", 149245887792)],
    )


def _multiply_2_labels_after_1e7_moves_1e6_cups(cup_indices):
    next_cups = _find_next_cup(cup_indices, total=1_000_000)
    i = int(cup_indices[0])
    for _ in range(10_000_000):
        i = _make_move(next_cups, i)
    j = next_cups[1]
    return j * next_cups[j]


def _collect_labels_after_100_moves(cup_indices):
    next_cups = _find_next_cup(cup_indices)
    i = int(cup_indices[0])
    for _ in range(100):
        i = _make_move(next_cups, i)
    return "".join(str(c) for c in _cups_after_1(next_cups))


def _make_move(next_cups, current):
    removed = _pick_up_3(next_cups, current)
    destination = _find_destination(next_cups, current, forbidden=removed)
    next_cups[current] = next_cups[removed[-1]]
    next_cups[removed[-1]] = next_cups[destination]
    next_cups[destination] = removed[0]
    return next_cups[current]


def _find_destination(next_cups, current, forbidden):
    d = _next_lowest_cup(current, highest=len(next_cups) - 1)
    while d in forbidden:
        d = _next_lowest_cup(d, highest=len(next_cups) - 1)
    return d


def _next_lowest_cup(current, highest):
    return highest if current <= 1 else current - 1


def _pick_up_3(next_cups, current):
    pickup = next_cups[current]
    results = [pickup]
    for _ in range(2):
        pickup = next_cups[pickup]
        results.append(pickup)
    return results


def _cups_after_1(next_cups):
    i = next_cups[1]
    results = []
    while i != 1:
        results.append(i)
        i = next_cups[i]
    return results


def _find_next_cup(labels, total=None):
    highest = total if total else len(labels)
    next_cup = [0] + [i + 2 for i in range(highest)]

    for i in range(len(labels) - 1):
        next_cup[int(labels[i])] = int(labels[i + 1])

    if highest > len(labels):
        next_cup[int(labels[-1])] = len(labels) + 1
        next_cup[highest] = int(labels[0])
    else:
        next_cup[int(labels[-1])] = int(labels[0])

    return next_cup


if __name__ == "__main__":
    sys.exit(main())
