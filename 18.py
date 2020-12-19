import math
import sys

import aoc


def main():
    harness = aoc.Harness()
    harness.attempt_part(
        _sum_homework_lines,
        "./18.txt",
        [
            ("./18_test.txt", 26386),
            ("./18_test2.txt", 124198272),
            ("./18_test3.txt", 160707),
        ],
    )
    harness.attempt_part(
        _sum_homework_lines_with_precedence, "./18.txt", [("./18_test.txt", 693942)],
    )


def _sum_homework_lines(filename):
    with open(filename) as f:
        return sum(_evaluate_expression(line, _eval) for line in f.read().splitlines())


def _sum_homework_lines_with_precedence(filename):
    with open(filename) as f:
        return sum(
            _evaluate_expression(line, _eval_with_precedence)
            for line in f.read().splitlines()
        )


def _evaluate_expression(line, evaluate):
    while line.find("(") != -1:
        line = _evaluate_first_complete_bracketed(line, evaluate)
    return evaluate(line)


def _evaluate_first_complete_bracketed(line, evaluate):
    end = line.find(")") + 1
    start = line.rfind("(", 0, end)
    return line[:start] + str(evaluate(line[start:end].strip("()"))) + line[end:]


def _eval(expression):
    assert expression.find("(") == -1
    total = 1
    op = "*"
    for token in expression.split():
        if token in "+*":
            op = token
        else:
            value = int(token)
            if op == "*":
                total *= value
            elif op == "+":
                total += value
    return total


def _eval_with_precedence(expression):
    assert expression.find("(") == -1
    return math.prod(
        sum(int(x) for x in chunk.split("+")) for chunk in expression.split("*")
    )


if __name__ == "__main__":
    sys.exit(main())
