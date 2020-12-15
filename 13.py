import sys
import math
from functools import reduce

import aoc


def main():
    harness = aoc.Harness()
    harness.attempt_part(
        _bus_id_times_wait, "./13.txt", [("./13_test.txt", 295)],
    )
    harness.attempt_part(
        _find_earliest_aligned_time,
        "./13.txt",
        [
            ("./13_test.txt", 1068781),
            ("./13_test_a.txt", 3417),
            ("./13_test_b.txt", 754018),
            ("./13_test_c.txt", 779210),
            ("./13_test_d.txt", 1261476),
            ("./13_test_e.txt", 1202161486),
        ],
    )


def _find_earliest_aligned_time(filename):
    ids_and_targets = _get_bus_id_remainder_pairs(filename)
    return reduce(_find_common_target, ids_and_targets)[1]


def _find_common_target(id_and_target_1, id_and_target_2):
    n1, r1 = id_and_target_1
    n2, r2 = id_and_target_2
    n = n1 * n2 // math.gcd(n1, n2)
    r = r1
    while r % n2 != r2:
        r += n1
    return (n, r)


def _get_bus_id_remainder_pairs(filename):
    with open(filename) as f:
        _, schedule_line = f.read().splitlines()
    schedules = filter(lambda x: x[1] != "x", enumerate(schedule_line.split(",")))
    return [(int(id), -i % int(id)) for i, id in schedules]


def _bus_id_times_wait(filename):
    timestamp, bus_ids = _get_present_bus_ids(filename)
    wait_times_per_id = _compute_wait_times(timestamp, bus_ids)
    best_id, shortest_wait = sorted(wait_times_per_id, key=lambda x: x[1])[0]
    return best_id * shortest_wait


def _get_present_bus_ids(filename):
    with open(filename) as f:
        timestamp_line, schedule_line = f.read().splitlines()
    return (
        int(timestamp_line),
        [int(id) for id in schedule_line.split(",") if id != "x"],
    )


def _compute_wait_times(timestamp, bus_ids):
    return [(x, -timestamp % x) for x in bus_ids]


if __name__ == "__main__":
    sys.exit(main())
