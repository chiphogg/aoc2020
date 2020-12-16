import sys
import math

import aoc


def main():
    harness = aoc.Harness()
    harness.attempt_part(
        _add_all_definitely_invalid_values, "./16.txt", [("./16_test.txt", 71)],
    )
    harness.attempt_part(
        _product_of_departures, "./16.txt", [],
    )


def _product_of_departures(filename):
    rules, my_ticket, nearby_tickets = _read_file(filename)
    valid_tickets = _discard_invalid(nearby_tickets, rules)
    field_indices = _solve(_map_possible_field_indices(rules, valid_tickets))
    return math.prod(
        my_ticket[field_indices[name][0]]
        for name in field_indices
        if name.startswith("departure")
    )


def _solve(index_map):
    while any(len(indices) > 1 for indices in index_map.values()):
        for name in index_map:
            if len(index_map[name]) == 1:
                index = index_map[name][0]
                for other_name in index_map:
                    if name != other_name:
                        if index in index_map[other_name]:
                            index_map[other_name].remove(index)
    assert all(len(indices) == 1 for indices in index_map.values())
    return index_map


def _map_possible_field_indices(rules, tickets):
    num_fields = aoc.assume_all_identical(len(t) for t in tickets)
    return {
        name: [
            i
            for i in range(num_fields)
            if all(any(a <= t[i] <= b for a, b in bounds_list) for t in tickets)
        ]
        for name, bounds_list in rules
    }


def _discard_invalid(tickets, rules):
    return list(
        filter(lambda t: all(not _definitely_invalid(x, rules) for x in t), tickets)
    )


def _add_all_definitely_invalid_values(filename):
    rules, _, nearby_tickets = _read_file(filename)
    return sum(
        x for ticket in nearby_tickets for x in ticket if _definitely_invalid(x, rules)
    )


def _definitely_invalid(x, rules):
    return all(not (a <= x <= b) for (_, ranges) in rules for (a, b) in ranges)


def _read_file(filename):
    with open(filename) as f:
        r, my, nearby = f.read().rstrip("\n").split("\n\n")
    return (_parse_rules(r), _parse_ticket_group(my)[0], _parse_ticket_group(nearby))


def _parse_rules(rule_chunk):
    rule_lines = rule_chunk.splitlines()
    return [_parse_rule(line) for line in rule_lines]


def _parse_rule(line):
    field, range_text = line.split(": ")
    ranges = range_text.split(" or ")
    return (field, [tuple(int(x) for x in r.split("-")) for r in ranges])


def _parse_ticket_group(group):
    group_lines = group.splitlines()
    assert group_lines[0].find("ticket") != -1
    assert group_lines[0].endswith(":")
    return [tuple(int(x) for x in line.split(",")) for line in group_lines[1:]]


if __name__ == "__main__":
    sys.exit(main())
