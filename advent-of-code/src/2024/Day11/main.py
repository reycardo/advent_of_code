from __future__ import annotations
from utils.tools import get_txt_files, read_input, timing_decorator
from utils.colors import magenta_color, reset_color
from typing import List, Tuple
from utils.tools import Grid, Point, Vectors
from collections import deque

files = get_txt_files(__file__)
#########
# Start #
#########

class Stone:
    def __init__(self, value, position):
        self.value = value
        self.position = position

    def blink(self, stones: List[Stone]):
        if self.value == 0:
            self.value = 1
        elif len(str(self.value)) % 2:
            stones[self.position:]


class Puzzle:
    
    def __init__(self, text_input):
        self.input = text_input[0]
        self.input_parsed = list(map(int,self.input.split()))

    def init_stones(self):
        self.stones = [Stone(i, idx) for idx, i in enumerate(self.input_parsed)]

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
    assert main(raw=files["test"], part=1) == 55312
    # assert main(raw=files["test"], part=2) == 81
    

    # solutions
    # print(f"\nRunning Solutions:")
    # assert main(raw=files["input"], part=1) == 717
    # assert main(raw=files["input"], part=2) == 1686


def solve():
    print(f"\nSolving:")
    answer1 = main(raw=files["input"], part=1)
    print(f"Answer part1: {magenta_color}{answer1}{reset_color}")
    # answer2 = main(raw=files["input"], part=2)
    # print(f"Answer part2: {magenta_color}{answer2}{reset_color}")


if __name__ == "__main__":
    run_tests()
    solve()
