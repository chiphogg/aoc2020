from functools import reduce
import sys

import aoc


def main():
    harness = aoc.Harness()
    harness.attempt_part(
        _count_valid_lines, "./19.txt", [("./19_test.txt", 2)],
    )


def _count_valid_lines(filename):
    with open(filename) as f:
        rule_lines, example_lines = f.read().rstrip("\n").split("\n\n")
    rules = _precompute(_parse_rules(rule_lines))
    return sum(1 for example in example_lines.splitlines() if _valid(rules, example))


def _precompute(rules):
    simplified = dict()
    for k in rules:
        _simplify(k, rules, simplified)
    return simplified


def _simplify(k, rules, simplified):
    if k in simplified:
        return
    for choice in rules[k]:
        for k2 in choice:
            if not k2.startswith('"'):
                _simplify(k2, rules, simplified)

    simplified[k] = set(
        reduce(
            lambda a, b: a.union(b),
            (
                _join_direct_product(
                    [
                        [k2.strip('"')] if k2.startswith('"') else simplified[k2]
                        for k2 in choice
                    ]
                )
                for choice in rules[k]
            ),
        )
    )


def _join_direct_product(string_lists):
    first_list, *other_lists = string_lists
    return (
        {f + j for f in first_list for j in _join_direct_product(other_lists)}
        if other_lists
        else first_list
    )


def _parse_rules(rule_lines):
    return {
        k: _parse_rule(rule)
        for k, rule in (line.split(": ") for line in rule_lines.splitlines())
    }


def _parse_rule(rule_line):
    return [choice.split() for choice in rule_line.split(" | ")]


def _valid(rules, example):
    return example in rules["0"]


if __name__ == "__main__":
    sys.exit(main())
