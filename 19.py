from functools import reduce
import sys

import aoc


def main():
    harness = aoc.Harness()
    harness.attempt_part(
        _count_valid_lines, "./19.txt", [("./19_test.txt", 2), ("./19_test_2.txt", 3)],
    )
    harness.attempt_part(
        _count_valid_lines_goofy_ad_hoc, "./19.txt", [("./19_test_2.txt", 12)],
    )


def _count_valid_lines_goofy_ad_hoc(filename):
    rules, examples = _read_rules_and_examples(filename)
    return sum(_goofy_ad_hoc_valid(rules, x) for x in examples)


def _goofy_ad_hoc_valid(rules, example):
    for remainder in _remove_matches_of_rule_8(rules, example):
        if _rule_11_matches(rules, remainder):
            return True
    return False


def _remove_matches_of_rule_8(rules, example):
    for target in rules["42"]:
        if example.startswith(target):
            remainder = example[len(target) :]
            yield remainder
            for x in _remove_matches_of_rule_8(rules, remainder):
                yield x


def _rule_11_matches(rules, example):
    for left_target in rules["42"]:
        if example.startswith(left_target):
            removed_left = example[len(left_target) :]
            for right_target in rules["31"]:
                if removed_left.endswith(right_target):
                    remainder = removed_left[: -len(right_target)]
                    if (not remainder) or _rule_11_matches(rules, remainder):
                        return True
    return False


def _count_valid_lines(filename):
    rules, examples = _read_rules_and_examples(filename)
    return sum(_valid(rules, x) for x in examples)


def _read_rules_and_examples(filename):
    with open(filename) as f:
        rule_lines, example_lines = f.read().rstrip("\n").split("\n\n")
    return _precompute(_parse_rules(rule_lines)), example_lines.splitlines()


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
