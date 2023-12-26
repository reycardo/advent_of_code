from utils.tools import get_txt_files, read_input, timing_decorator
from utils.colors import magenta_color, reset_color
import re

files = get_txt_files(__file__)
#########
# Start #
#########

class Step:
    def __init__(self, step: str) -> None:
        self.step = step
        self.sequence = re.split('=|-', step)[0]
        self.value = re.split('=|-', step)[1]
        self.current_value = 0
        self.hashed_value = self.hash(self.current_value)

    def hash(self, value):
        for char in self.step:
            value += ord(char)
            value *= 17
            value = value % 256
        return value

class Puzzle:
    def __init__(self, text_input):
        self.input = text_input  
        self.input_parsed = [Step(step=step) for step in self.input[0].split(",")]        

    def solve(self, part):
        if part == 1:
            return sum([step.hashed_value for step in self.input_parsed])
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
    assert main(raw=files["test"], part=1) == 1320
    # assert main(raw=files["test"], part=2) == 64

    # solutions
    print(f"\nRunning Solutions:")
    assert main(raw=files["input"], part=1) == 510273
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
