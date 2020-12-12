import sys
import numpy as np

import aoc


def main():
    harness = aoc.Harness()
    harness.attempt_part(
        _action_manhattan_distance, "./12.txt", [("./12_test.txt", 25)],
    )
    harness.attempt_part(
        _waypoint_manhattan_distance, "./12.txt", [("./12_test.txt", 286)],
    )


def _action_manhattan_distance(filename):
    position = np.array([0, 0])
    direction = np.array([1, 0])
    with open(filename) as f:
        for line in f.read().splitlines():
            _apply_instruction(position, direction, line)
    return abs(position[0]) + abs(position[1])


def _waypoint_manhattan_distance(filename):
    position = np.array([0, 0])
    waypoint = np.array([10, 1])
    with open(filename) as f:
        for line in f.read().splitlines():
            _apply_waypoint_instructions(position, waypoint, line)
    return abs(position[0]) + abs(position[1])


def _apply_waypoint_instructions(position, waypoint, line):
    move, size = line[0], int(line[1:])
    if move == "R":
        _turn_right(waypoint, size // 90)
    if move == "L":
        _turn_right(waypoint, 4 - (size // 90))
    if move == "F":
        position += waypoint * size
    if move == "N":
        waypoint += np.array([0, size])
    if move == "S":
        waypoint += np.array([0, -size])
    if move == "E":
        waypoint += np.array([size, 0])
    if move == "W":
        waypoint += np.array([-size, 0])


def _apply_instruction(position, direction, line):
    move, size = line[0], int(line[1:])
    if move == "R":
        _turn_right(direction, size // 90)
    if move == "L":
        _turn_right(direction, 4 - (size // 90))
    if move == "F":
        position += direction * size
    if move == "N":
        position += np.array([0, size])
    if move == "S":
        position += np.array([0, -size])
    if move == "E":
        position += np.array([size, 0])
    if move == "W":
        position += np.array([-size, 0])


def _turn_right(direction, size):
    for _ in range(size):
        (direction[0], direction[1]) = (direction[1], -direction[0])


if __name__ == "__main__":
    sys.exit(main())
