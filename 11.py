import sys

import aoc


def main():
    harness = aoc.Harness()
    harness.attempt_part(
        _find_steady_state_occupancy, "./11.txt", [("./11_test.txt", 37)],
    )
    harness.attempt_part(
        _find_updated_steady_state_occupancy, "./11.txt", [("./11_test.txt", 26)],
    )


def _find_steady_state_occupancy(filename):
    layout = SeatingLayout(filename, tolerance=4)
    layout.find_steady_state_occupancy()
    return layout.occupancy()


def _find_updated_steady_state_occupancy(filename):
    layout = VisibilityBasedSeatingLayout(filename, tolerance=5)
    layout.find_steady_state_occupancy()
    return layout.occupancy()


class SeatingLayout:
    def __init__(self, filename, tolerance):
        self.tolerance = tolerance
        with open(filename) as f:
            self.layout = list(list(line) for line in f.read().splitlines())
        self.num_rows = len(self.layout)
        self.num_cols = aoc.assume_all_identical(len(r) for r in self.layout)
        self.adjacent_seats = self.map_adjacent_seats()

    def map_adjacent_seats(self):
        return [
            [self.find_adjacent_seats(i, j) for j in range(self.num_cols)]
            for i in range(self.num_rows)
        ]

    def find_adjacent_seats(self, i, j):
        i_vals = list(filter(lambda x: x >= 0 and x < self.num_rows, (i - 1, i, i + 1)))
        j_vals = list(filter(lambda x: x >= 0 and x < self.num_cols, (j - 1, j, j + 1)))
        return list(
            filter(
                lambda coords: (coords[0] != i) or (coords[1] != j),
                ((i, j) for i in i_vals for j in j_vals),
            )
        )

    def find_steady_state_occupancy(self):
        while self.flip_and_count_seats():
            pass

    def flip_and_count_seats(self):
        to_flip = self.find_seats_to_flip()
        for (i, j) in to_flip:
            self.layout[i][j] = "L" if self.layout[i][j] == "#" else "#"
        return len(to_flip)

    def find_seats_to_flip(self):
        return list(
            filter(
                self.should_flip,
                ((i, j) for i in range(self.num_rows) for j in range(self.num_cols)),
            )
        )

    def should_flip(self, indices):
        i, j = indices
        value = self.layout[i][j]
        if value == ".":
            return False

        neighbours = self.count_occupied_neighbours(i, j)
        if value == "L":
            return neighbours == 0
        if value == "#":
            return neighbours >= self.tolerance

    def count_occupied_neighbours(self, i, j):
        return sum(
            1 for (ni, nj) in self.adjacent_seats[i][j] if self.layout[ni][nj] == "#"
        )

    def occupancy(self):
        return sum(1 for row in self.layout for x in row if x == "#")


class VisibilityBasedSeatingLayout(SeatingLayout):
    def __init__(self, filename, tolerance):
        super().__init__(filename, tolerance)

    def find_adjacent_seats(self, i, j):
        adjacent_seats = []
        dirs = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
        for (di, dj) in dirs:
            (ni, nj) = (i + di, j + dj)
            while (0 <= ni < self.num_rows) and (0 <= nj < self.num_cols):
                if self.layout[ni][nj] != ".":
                    adjacent_seats.append((ni, nj))
                    break
                ni += di
                nj += dj
        return adjacent_seats


if __name__ == "__main__":
    sys.exit(main())
