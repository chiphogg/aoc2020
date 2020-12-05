import collections
import itertools
import sys


def main():
    with open("2a.txt") as f:
        print(sum(filter(None, (is_valid_part_2(*parse_line(line)) for line in f))))
    print(is_valid_part_2(*parse_line("1-3 a: abcde")))
    print(is_valid_part_2(*parse_line("1-3 b: cdefg")))
    print(is_valid_part_2(*parse_line("2-9 c: ccccccccc")))


def parse_line(line):
    target_range, letter, password = line.split(" ")
    min_count, max_count = (int(x) for x in target_range.split("-"))
    return (min_count, max_count, letter[0], password)


def is_valid(min_count, max_count, letter, password):
    count = collections.Counter(password)
    return count[letter] >= min_count and count[letter] <= max_count


def is_valid_part_2(i, j, letter, password):
    return (password[i - 1] == letter) + (password[j - 1] == letter) == 1


if __name__ == "__main__":
    sys.exit(main())
