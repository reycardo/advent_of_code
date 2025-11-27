from utils.tools import get_txt_files, read_input, timing_decorator
from advent_of_code.utils.colors import magenta_color, reset_color

files = get_txt_files(__file__)
#########
# Start #
#########


class Record:
    def __init__(self, row) -> None:
        self.records = [x for x in row.split(" ")[0]]
        self.contiguous_group = [int(x) for x in row.split(" ")[1].split(",")]
        self.count = 0


class Puzzle:
    def __init__(self, text_input):
        self.input = text_input
        self.input_parsed = [Record(row) for row in self.input]

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
    print("\nRunning Tests:")
    assert main(raw=files["test"], part=1) == 21
    # assert main(raw=files["test"], part=2) == 71503

    # solutions
    print("\nRunning Solutions:")
    # assert main(raw=files["input"], part=1) == 503424
    # assert main(raw=files["input"], part=2) == 32607562


def solve():
    print("\nSolving:")
    answer1 = main(raw=files["input"], part=1)
    print(f"Answer part1: {magenta_color}{answer1}{reset_color}")
    # answer2 = main(raw=files["input"], part=2)
    # print(f"Answer part2: {magenta_color}{answer2}{reset_color}")


if __name__ == "__main__":
    run_tests()
    solve()
