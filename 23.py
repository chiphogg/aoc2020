import sys

import aoc


def main():
    harness = aoc.Harness()
    harness.attempt_part(
        _collect_labels_after_100_moves, "925176834", [("389125467", "67384529")],
    )


def _collect_labels_after_100_moves(cup_indices):
    next_cups = _find_next_cup(cup_indices)
    i = int(cup_indices[0])
    for _ in range(100):
        i = _make_move(next_cups, i)
    return "".join(str(c) for c in _cups_after_1(next_cups))


def _print(next_cups, current):
    cups = [f"({current})"]
    i = current
    for _ in range(len(next_cups) - 2):
        i = next_cups[i]
        cups.append(str(i))
    print(" ".join(cups))


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


def _find_next_cup(labels):
    ids = [int(x) for x in labels]
    next_cup = {ids[i]: ids[(i + 1) % len(ids)] for i in range(len(ids))}
    return [0] + [next_cup[i + 1] for i in range(len(ids))]


if __name__ == "__main__":
    sys.exit(main())
