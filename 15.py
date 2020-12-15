import collections
import sys

import aoc


def main():
    harness = aoc.Harness()
    harness.attempt_part(
        _find_2020th_spoken,
        "5,2,8,16,18,0,1",
        [
            ("0,3,6", 436),
            ("1,3,2", 1),
            ("2,1,3", 10),
            ("1,2,3", 27),
            ("2,3,1", 78),
            ("3,2,1", 438),
            ("3,1,2", 1836),
        ],
    )
    harness.attempt_part(
        _find_30000000th_spoken,
        "5,2,8,16,18,0,1",
        [
            ("0,3,6", 175594),
            ("1,3,2", 2578),
            ("2,1,3", 3544142),
            ("1,2,3", 261214),
            ("2,3,1", 6895259),
            ("3,2,1", 18),
            ("3,1,2", 362),
        ],
    )


def _find_30000000th_spoken(numbers_string):
    return _find_nth_spoken(numbers_string, 30000000)


def _find_2020th_spoken(numbers_string):
    return _find_nth_spoken(numbers_string, 2020)


def _find_nth_spoken(numbers_string, n):
    game = Game([int(x) for x in numbers_string.split(",")])
    while game.turn < n:
        game.speak_next()
    return game.last_number_spoken


class Game:
    def __init__(self, numbers):
        self.last_turn_spoken = {n: i for (i, n) in enumerate(numbers, 1)}
        self.num_times_spoken = collections.Counter(numbers)
        self.last_number_spoken = numbers[-1]
        self.turn = len(self.last_turn_spoken)

    def speak_next(self):
        self.turn += 1

        previous_last = self.last_number_spoken
        self.last_number_spoken = self._next_to_speak()
        self.num_times_spoken[self.last_number_spoken] += 1

        self.last_turn_spoken[previous_last] = self.turn - 1

    def _next_to_speak(self):
        if self.num_times_spoken[self.last_number_spoken] <= 1:
            return 0
        else:
            return self.turn - self.last_turn_spoken[self.last_number_spoken] - 1


if __name__ == "__main__":
    sys.exit(main())
