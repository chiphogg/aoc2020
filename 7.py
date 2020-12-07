import sys
import pprint
from copy import deepcopy

import aoc


def main():
    harness = aoc.Harness()
    harness.attempt_part(
        _count_types_containing_shiny_gold, "./7.txt", [("./7_test_1.txt", 4)]
    )
    harness.attempt_part(
        _count_contents_of_shiny_gold,
        "./7.txt",
        [("./7_test_1.txt", 32), ("./7_test_2.txt", 126)],
    )


def _count_contents_of_shiny_gold(filename):
    return _num_bags_inside(_build_bag_digraph(filename), "shiny gold")


def _num_bags_inside(bag_dag, colour):
    return sum(n * (1 + _num_bags_inside(bag_dag, c)) for (n, c) in bag_dag[colour])


def _count_types_containing_shiny_gold(filename):
    bag_dag = _build_bag_digraph(filename)
    return sum(1 for good_colour in filter(_can_reach("shiny gold", bag_dag), bag_dag))


def _can_reach(goal_colour, bag_dag):
    return lambda starting_colour: (starting_colour != goal_colour) and _path_exists(
        bag_dag, start=starting_colour, end=goal_colour
    )


def _path_exists(dag, start, end):
    return (start == end) or any(
        _path_exists(dag, next_colour, end) for (_, next_colour) in dag[start]
    )


def _build_bag_digraph(filename):
    with open(filename) as f:
        return {
            k: _parse_rules(v)
            for (k, v) in (
                line.split(" bags contain ") for line in f.read().splitlines()
            )
        }


def _parse_rules(rule_description):
    if "no other bags" in rule_description:
        return []
    cleaned_description = (
        rule_description.replace(" bags", "").replace(" bag", "").rstrip(".")
    )
    return [_parse_num_and_color(rule) for rule in cleaned_description.split(", ")]


def _parse_num_and_color(num_and_color):
    split_num_and_color = num_and_color.split(" ", maxsplit=1)
    return (int(split_num_and_color[0]), split_num_and_color[1])


if __name__ == "__main__":
    sys.exit(main())
