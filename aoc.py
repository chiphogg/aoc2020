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
        _test_passes(solve, testfile, expected) for (testfile, expected) in tests
    )


def _test_passes(solve, testfile, expected):
    test_result = solve(testfile)

    ok = test_result == expected

    if not ok:
        print("Failed test (got {}, expected {}).".format(test_result, expected))

    return ok
