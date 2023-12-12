from utils.tools import get_txt_files, read_input, timing_decorator
from utils.colors import magenta_color, reset_color
import networkx as nx

files = get_txt_files(__file__)
#########
# Start #
#########


class Cell:
    def __init__(self, value, position):
        self.value = value
        self.coords = position


class Puzzle:
    def __init__(self, text_input):
        self.input = text_input
        self.input_parsed = [[point for point in row] for row in self.input]
        self.expanded_universe = self.expand_universe()

        self.expanded_grid = [
            [Cell(point, (y, x)) for y, point in enumerate(row)]
            for x, row in enumerate(self.expanded_universe)
        ]
        a = 1

    def is_empty(self, line):
        for cell in line:
            if cell == "#":
                return False
        return True

    def expand_grid(self, matrix):
        new_matrix = []
        for row in matrix:
            if self.is_empty(row):
                empty_line = ["."] * len(row)
                new_matrix.append(row)
                new_matrix.append(empty_line)
            else:
                new_matrix.append(row)
        return new_matrix

    def expand_universe(self):
        expand_rows = self.expand_grid(self.input_parsed)
        expand_rows_transposed = list(map(list, zip(*expand_rows)))
        expanded_universe_transposed = self.expand_grid(expand_rows_transposed)
        return list(map(list, zip(*expanded_universe_transposed)))

    def solve(self, part):
        if part == 1:
            pass
        if part == 2:
            pass


@timing_decorator
def main(raw, part):
    text_input = read_input(raw)
    input_parsed = [i if i else "" for i in text_input]
    puzzle = Puzzle(input_parsed)
    return puzzle.solve(part)


def run_tests():
    print(f"\nRunning Tests:")
    assert main(raw=files["test"], part=1) == 374
    # assert main(raw=files["test"], part=2) == 71503

    # solutions
    print(f"\nRunning Solutions:")
    assert main(raw=files["input"], part=1) == 503424
    assert main(raw=files["input"], part=2) == 32607562


def solve():
    print(f"\nSolving:")
    answer1 = main(raw=files["input"], part=1)
    print(f"Answer part1: {magenta_color}{answer1}{reset_color}")
    answer2 = main(raw=files["input"], part=2)
    print(f"Answer part2: {magenta_color}{answer2}{reset_color}")


if __name__ == "__main__":
    run_tests()
    solve()
