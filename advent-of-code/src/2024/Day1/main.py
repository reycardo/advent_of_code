from utils.tools import get_txt_files, read_input, timing_decorator
from utils.colors import magenta_color, reset_color

files = get_txt_files(__file__)
#########
# Start #
#########

class Puzzle:
    def __init__(self, text_input):
        self.input = text_input


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
    puzzle.solve(part)
    return puzzle.solve(part)


def run_tests():
    print(f"\nRunning Tests:")
    # assert main(raw=files["test"], part=1) == 102
    # assert main(raw=files["test"], part=2) == 51

    # solutions
    # print(f"\nRunning Solutions:")
    # assert main(raw=files["input"], part=1) == 6978
    # assert main(raw=files["input"], part=2) == 7315


def solve():
    print(f"\nSolving:")
    answer1 = main(raw=files["input"], part=1)
    print(f"Answer part1: {magenta_color}{answer1}{reset_color}")
    # answer2 = main(raw=files["input"], part=2)
    # print(f"Answer part2: {magenta_color}{answer2}{reset_color}")


if __name__ == "__main__":
    run_tests()
    solve()
