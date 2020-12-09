import sys
import pprint
from copy import deepcopy

import aoc


def main():
    harness = aoc.Harness()
    harness.attempt_part(
        _find_accumulator_before_first_repeat_instruction,
        "./8.txt",
        [("./8_test.txt", 5)],
    )
    harness.attempt_part(
        _find_accumulator_with_fixed_program, "./8.txt", [("./8_test.txt", 8)],
    )


def _find_accumulator_before_first_repeat_instruction(filename):
    program = Program(filename)
    program.run_until_repeat_or_termination()
    return program.accumulator


def _find_accumulator_with_fixed_program(filename):
    program = Program(filename)
    program.find_instruction_to_change()
    return program.accumulator


class Program:
    def __init__(self, filename):
        with open(filename) as f:
            self.instructions = [
                (i, *_parse_instruction(line))
                for (i, line) in enumerate(f.read().splitlines())
            ]
        self.reset()

    def reset(self):
        self.accumulator = 0
        self.next_to_execute = 0

    def run_until_repeat_or_termination(self, swap_instruction=-1):
        seen = set()
        self.reset()
        while (
            self.next_to_execute < len(self.instructions)
            and self.next_to_execute not in seen
        ):
            seen.add(self.next_to_execute)
            self.run_next_instruction(swap_instruction)

    def run_next_instruction(self, swap_instruction=-1):
        i, command, value = self.instructions[self.next_to_execute]
        assert i == self.next_to_execute
        if command == "nop" or (i == swap_instruction and command == "jmp"):
            self.next_to_execute += 1
        elif command == "acc":
            self.next_to_execute += 1
            self.accumulator += value
        elif command == "jmp" or (i == swap_instruction and command == "nop"):
            self.next_to_execute += value

    def find_instruction_to_change(self):
        for i in range(len(self.instructions)):
            self.run_until_repeat_or_termination(swap_instruction=i)
            if self.next_to_execute >= len(self.instructions):
                return self.accumulator


def _parse_instruction(line):
    command, value = line.split()
    return (command, int(value))


if __name__ == "__main__":
    sys.exit(main())
