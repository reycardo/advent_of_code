from __future__ import annotations
from utils.tools import get_txt_files, read_input, timing_decorator
from advent_of_code.utils.colors import magenta_color, reset_color
from typing import List, Tuple
import itertools

files = get_txt_files(__file__)
#########
# Start #
#########


class Puzzle:
    def __init__(self, text_input):
        self.input: List[str] = text_input
        self.keys = []
        self.locks = []
        self.split_keys_from_locks()
        self.fits = []

    def split_keys_from_locks(self):
        result = [
            list(group)
            for key, group in itertools.groupby(self.input, lambda x: x == "")
            if not key
        ]
        for entry in result:
            transposed = ["".join(row) for row in zip(*entry)]
            if entry[0].startswith("#"):
                transposed_new = [row[1:] for row in transposed]
                counts = [element.count("#") for element in transposed_new]
                self.locks.append(counts)
            else:
                transposed_new = [row[:-1] for row in transposed]
                counts = [element.count("#") for element in transposed_new]
                self.keys.append(counts)

    def check_if_key_fits(self, key, lock):
        summed_list = [a + b for a, b in zip(key, lock)]
        return all(i <= 5 for i in summed_list)

    def solve(self, part):
        if part == 1:
            combinations = list(itertools.product(self.keys, self.locks))
            for key, lock in combinations:
                if self.check_if_key_fits(key, lock):
                    self.fits.append((key, lock))
            return len(self.fits)
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
    assert main(raw=files["test"], part=1) == 3
    # assert main(raw=files["test"], part=2) == "co,de,ka,ta"

    # solutions
    print(f"\nRunning Solutions:")
    assert main(raw=files["input"], part=1) == 3127
    # assert main(raw=files["input"], part=2) == 662726441391898


def solve():
    print(f"\nSolving:")
    answer1 = main(raw=files["input"], part=1)
    print(f"Answer part1: {magenta_color}{answer1}{reset_color}")
    # answer2 = main(raw=files["input"], part=2)
    # print(f"Answer part2: {magenta_color}{answer2}{reset_color}")


if __name__ == "__main__":
    run_tests()
    solve()
