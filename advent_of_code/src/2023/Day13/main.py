from utils.tools import get_txt_files, read_input, timing_decorator
from advent_of_code.utils.colors import magenta_color, reset_color
from itertools import groupby

files = get_txt_files(__file__)
#########
# Start #
#########


class Pattern:
    def __init__(self, pattern) -> None:
        self.pattern = pattern
        self.value1 = self.check_mirror(difference_threshold=0)
        self.value2 = self.check_mirror(difference_threshold=1)

    def count_differences(self, l, r):
        return sum(a != b for a, b in zip(l, r))

    def check_mirror(self, difference_threshold=0):
        for X in range(1, len(self.pattern)):  # horizontal
            Y = min(X, len(self.pattern) - X)
            upper = self.pattern[X - Y : X]
            lower = self.pattern[X : X + Y][::-1]
            diff_count = sum(self.count_differences(a, b) for a, b in zip(upper, lower))
            if diff_count == difference_threshold:
                return 100 * X

        for X in range(1, len(self.pattern[0])):  # vertical
            Y = min(X, len(self.pattern[0]) - X)
            left = [pattern[X - Y : X] for pattern in self.pattern]
            right = [pattern[X : X + Y][::-1] for pattern in self.pattern]
            diff_count = sum(self.count_differences(a, b) for a, b in zip(left, right))
            if diff_count == difference_threshold:
                return X


class Puzzle:
    def __init__(self, text_input):
        self.input = text_input
        self.patterns = self.parse_input()
        a = 1

    def parse_input(self):
        d = [Pattern(list(sub[1])) for sub in groupby(self.input, key=bool) if sub[0]]
        return d

    def solve(self, part):
        if part == 1:
            return sum(pattern.value1 for pattern in self.patterns)
        if part == 2:
            return sum(pattern.value2 for pattern in self.patterns)


@timing_decorator
def main(raw, part):
    text_input = read_input(raw)
    input_parsed = [i if i else "" for i in text_input]
    puzzle = Puzzle(input_parsed)
    return puzzle.solve(part)


def run_tests():
    print(f"\nRunning Tests:")
    assert main(raw=files["test"], part=1) == 405
    assert main(raw=files["test"], part=2) == 400

    # solutions
    print(f"\nRunning Solutions:")
    assert main(raw=files["input"], part=1) == 34202
    assert main(raw=files["input"], part=2) == 34230


def solve():
    print(f"\nSolving:")
    answer1 = main(raw=files["input"], part=1)
    print(f"Answer part1: {magenta_color}{answer1}{reset_color}")
    answer2 = main(raw=files["input"], part=2)
    print(f"Answer part2: {magenta_color}{answer2}{reset_color}")


if __name__ == "__main__":
    run_tests()
    solve()
