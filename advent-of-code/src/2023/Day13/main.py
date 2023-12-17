from utils.tools import get_txt_files, read_input, timing_decorator
from utils.colors import magenta_color, reset_color
from itertools import groupby

files = get_txt_files(__file__)
#########
# Start #
#########

class Pattern:
    def __init__(self, pattern) -> None:
        self.pattern = pattern
        self.value = self.check_mirror()

    def check_mirror(self):
        for X in range(1,len(self.pattern)): # horizontal
            Y = min(X, len(self.pattern) - X)
            if self.pattern[X-Y:X] == self.pattern[X:X+Y][::-1]:
                return 100 * X
        for X in range(1,len(self.pattern[0])): # vertical
            Y = min(X, len(self.pattern[0]) - X)
            if [pattern[X-Y:X] for pattern in self.pattern] == [pattern[X:X+Y][::-1] for pattern in self.pattern]:
                return X

class Puzzle:
    def __init__(self, text_input):
        self.input = text_input 
        self.patterns = self.parse_input()
        a=1       

    def parse_input(self):
        d = [
            Pattern(list(sub[1]))
            for sub in groupby(self.input, key=bool)
            if sub[0]
        ]
        return d

    def solve(self, part):
        if part == 1:
            return sum(pattern.value for pattern in self.patterns)
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
    assert main(raw=files["test"], part=1) == 405
    # assert main(raw=files["test"], part=2) == 71503

    # solutions
    print(f"\nRunning Solutions:")
    assert main(raw=files["input"], part=1) == 34202
    # assert main(raw=files["input"], part=2) == 32607562


def solve():
    print(f"\nSolving:")
    answer1 = main(raw=files["input"], part=1)
    print(f"Answer part1: {magenta_color}{answer1}{reset_color}")
    # answer2 = main(raw=files["input"], part=2)
    # print(f"Answer part2: {magenta_color}{answer2}{reset_color}")


if __name__ == "__main__":
    run_tests()
    solve()
