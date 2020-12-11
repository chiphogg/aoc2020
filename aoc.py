class Harness:
    def __init__(self):
        self.next_part_num = 1

    def attempt_part(self, solve, realfile, tests):
        print("\nPart {}".format(self.next_part_num))

        if _all_tests_pass(solve, tests):
            print(solve(realfile))

        self.next_part_num += 1


def _all_tests_pass(solve, tests):
    return all(
        _test_passes(solve, test_inputs, expected) for (test_inputs, expected) in tests
    )


def _test_passes(solve, test_inputs, expected):
    inputs_tuple = test_inputs if type(test_inputs) is tuple else (test_inputs,)
    test_result = solve(*inputs_tuple)

    ok = test_result == expected

    if not ok:
        print("Failed test (got {}, expected {}).".format(test_result, expected))

    return ok


def assume_all_identical(iterable):
    (common_value,) = set(iterable)
    return common_value
