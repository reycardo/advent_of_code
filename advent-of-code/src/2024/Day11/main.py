from __future__ import annotations
from utils.tools import get_txt_files, read_input, timing_decorator
from utils.colors import magenta_color, reset_color
from typing import List, Dict

files = get_txt_files(__file__)
#########
# Start #
#########


class Puzzle:
    def __init__(self, text_input):
        self.input = text_input[0]
        self.input_parsed = list(map(int, self.input.split()))
        self.init_stones()
        self.blinks = 0

    def init_stones(self):
        self.stones = [i for i in self.input_parsed]
        self.repeated_stones_counter: Dict[int] = {}
        for stone in self.stones:  # add first stones
            self.addStones(self.repeated_stones_counter, stone, 1)

    def blink(self, new_counter: Dict[int], stone: int, old_counter: Dict[int]):
        if stone == 0:
            self.addStones(new_counter, 1, old_counter[stone])

        elif len(string_value := str(stone)) % 2 == 0:
            left = int(string_value[: len(string_value) // 2])
            right = int(string_value[len(string_value) // 2 :])
            self.addStones(new_counter, left, old_counter[stone])
            self.addStones(new_counter, right, old_counter[stone])

        else:
            self.addStones(new_counter, stone * 2024, old_counter[stone])

    def addStones(self, counter: set, stone: int, stoneCount: int):
        if stone in counter:
            counter[stone] += stoneCount
        else:
            counter[stone] = stoneCount

    def blink_all_stones(self):
        new_stones = {}
        for stone in self.repeated_stones_counter:
            self.blink(new_stones, stone, self.repeated_stones_counter)

        self.repeated_stones_counter = new_stones
        self.blinks += 1

    def solve(self, blinks):
        for _ in range(blinks):
            self.blink_all_stones()

        return sum([x for x in self.repeated_stones_counter.values()])


@timing_decorator
def main(raw, part, blinks):
    text_input = read_input(raw)
    input_parsed = [i if i else "" for i in text_input]
    puzzle = Puzzle(input_parsed)
    return puzzle.solve(blinks)


def run_tests():
    print(f"\nRunning Tests:")
    assert main(raw=files["test"], part=1, blinks=6) == 22
    assert main(raw=files["test"], part=1, blinks=25) == 55312
    assert main(raw=files["test"], part=2, blinks=25) == 55312

    # solutions
    print(f"\nRunning Solutions:")
    assert main(raw=files["input"], part=1, blinks=25) == 188902
    assert main(raw=files["input"], part=2, blinks=25) == 188902
    assert main(raw=files["input"], part=2, blinks=75) == 223894720281135


def solve():
    print(f"\nSolving:")
    answer1 = main(raw=files["input"], part=1, blinks=25)
    print(f"Answer part1: {magenta_color}{answer1}{reset_color}")
    answer2 = main(raw=files["input"], part=2, blinks=75)
    print(f"Answer part2: {magenta_color}{answer2}{reset_color}")


if __name__ == "__main__":
    run_tests()
    solve()
