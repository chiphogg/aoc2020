import sys

import aoc

REQUIRED_FIELDS = ("byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid")


def main():
    harness = aoc.Harness()
    harness.attempt_part(
        _count_valid_passports, realfile="4.txt", tests=[("4_test.txt", 2)]
    )
    harness.attempt_part(
        _count_really_valid_passports,
        realfile="4.txt",
        tests=[("4b_test_invalid.txt", 0), ("4b_test_valid.txt", 4)],
    )


def _count_valid_passports(filename):
    passports = (_parse_passport(p) for p in _read_raw_passports(filename))
    return sum(map(_has_required_fields, passports))


def _count_really_valid_passports(filename):
    passports = (_parse_passport(p) for p in _read_raw_passports(filename))
    return sum(map(_passes_validation, passports))


def _read_raw_passports(filename):
    with open(filename) as f:
        return f.read().split("\n\n")


def _parse_passport(passport_lines):
    fields = passport_lines.split()
    split_fields = (f.split(":") for f in fields)
    return {k: v for (k, v) in split_fields}


def _has_required_fields(passport):
    for req in REQUIRED_FIELDS:
        if req not in passport:
            return False
    return True


def _passes_validation(passport):
    return _has_required_fields(passport) and all(
        _validate_field(field, passport[field]) for field in REQUIRED_FIELDS
    )


def _validate_field(field, x):
    if field == "byr":
        return (len(x) == 4) and (1920 <= int(x) <= 2002)

    if field == "iyr":
        return (len(x) == 4) and (2010 <= int(x) <= 2020)

    if field == "eyr":
        return (len(x) == 4) and (2020 <= int(x) <= 2030)

    if field == "hgt":
        return _validate_height(x)

    if field == "hcl":
        return (
            (len(x) == 7)
            and (x[0] == "#")
            and all(c in "abcdef0123456789" for c in x[1:])
        )

    if field == "ecl":
        return x in ("amb", "blu", "brn", "gry", "grn", "hzl", "oth")

    if field == "pid":
        return (len(x) == 9) and all(c.isdigit() for c in x)


def _validate_height(x):
    if len(x) < 3:
        return False

    number_part = int(x[:-2])

    if x.endswith("cm"):
        return 150 <= number_part <= 193

    if x.endswith("in"):
        return 59 <= number_part <= 76

    return False


if __name__ == "__main__":
    sys.exit(main())
