import sys

import aoc


def main():
    harness = aoc.Harness()
    harness.attempt_part(
        _add_all_definitely_invalid_values, "./16.txt", [("./16_test.txt", 71)],
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
    return (_parse_rules(r), _parse_ticket_group(my), _parse_ticket_group(nearby))


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
