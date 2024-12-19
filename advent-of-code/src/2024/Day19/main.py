from __future__ import annotations
from utils.tools import get_txt_files, read_input, timing_decorator
from utils.colors import magenta_color, reset_color
from utils.tools import Point, Grid, InvertedVectors
from typing import List

files = get_txt_files(__file__)
#########
# Start #
#########

class Towel:
    def __init__(self, raw):
        self.stripe = raw

class Pattern:
    def __init__(self, raw):
        self.pattern = raw

class Puzzle:
    def __init__(self, text_input):
        self.input: List[str] = text_input
        self.split_towels_from_patterns()
    
    def split_towels_from_patterns(self):
        separator_index = self.input.index("")
        self.available_towels = [Towel(raw) for raw in self.input[:separator_index]]
        self.desired_patterns = [Pattern(raw) for raw in self.input[separator_index + 1 :]]

    def solve(self, part):
        if part == 1:
            pass
        elif part == 2:            
            pass        

@timing_decorator
def main(raw, part):
    text_input = read_input(raw)
    input_parsed = [i if i else "" for i in text_input]
    puzzle = Puzzle(input_parsed)
    return puzzle.solve(part)


def run_tests():
    print(f"\nRunning Tests:")
    assert main(raw=files["test"], part=1) == 6
    # assert main(raw=files["test"], part=2) == 22

    # solutions
    # print(f"\nRunning Solutions:")
    # assert main(raw=files["input"], part=1) == 312
    # assert main(raw=files["input"], part=2) == 1509724


def solve():
    print(f"\nSolving:")
    answer1 = main(raw=files["input"], part=1)    
    print(f"Answer part1: {magenta_color}{answer1}{reset_color}")
    # answer2 = main(raw=files["input"], part=2)
    # print(f"Answer part2: {magenta_color}{answer2}{reset_color}")


if __name__ == "__main__":
    run_tests()
    solve()
