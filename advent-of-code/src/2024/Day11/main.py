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
    def __init__(self, value):
        self.value = value

    def blink(self):
        string_value = str(self.value)
        if self.value == 0:
            return [Stone(1)]
        elif len(string_value) % 2 == 0:
            left = int(string_value[: len(string_value) // 2])
            right = int(string_value[len(string_value) // 2 :])
            return [Stone(left), Stone(right)]
        else:
            return [Stone(self.value * 2024)]


class Puzzle:
    def __init__(self, text_input):
        self.input = text_input[0]
        self.input_parsed = list(map(int, self.input.split()))
        self.init_stones()
        self.blinks = 0

    def init_stones(self):
        self.stones = [Stone(i) for i in self.input_parsed]

    def blink(self):
        new_stones = []
        for stone in self.stones:
            new_stones.extend(stone.blink())

        self.stones = new_stones
        self.blinks += 1

    def solve(self, part, blinks):
        for _ in range(blinks):
            self.blink()

        return len(self.stones)


@timing_decorator
def main(raw, part, blinks):
    text_input = read_input(raw)
    input_parsed = [i if i else "" for i in text_input]
    puzzle = Puzzle(input_parsed)
    return puzzle.solve(part, blinks)


def run_tests():
    print(f"\nRunning Tests:")
    assert main(raw=files["test"], part=1, blinks=6) == 22
    assert main(raw=files["test"], part=1, blinks=25) == 55312

    # solutions
    print(f"\nRunning Solutions:")
    assert main(raw=files["input"], part=1, blinks=25) == 188902
    # assert main(raw=files["input"], part=2) == 1686


def solve():
    print(f"\nSolving:")
    answer1 = main(raw=files["input"], part=1, blinks=25)
    print(f"Answer part1: {magenta_color}{answer1}{reset_color}")
    # answer2 = main(raw=files["input"], part=2, blinks=75)
    # print(f"Answer part2: {magenta_color}{answer2}{reset_color}")


if __name__ == "__main__":
    run_tests()
    solve()
