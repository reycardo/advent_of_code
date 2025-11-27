import os
import sys

sys.path.insert(0, "./")
from utils import tools
import numpy as np
from scipy.ndimage import measurements
from collections import Counter
import math

raw = r"2021\Day9\test.txt"

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
input_raw = os.path.join(__location__, "input.txt")
test_raw = os.path.join(__location__, "test.txt")

#########
# Start #
#########


def parse_input(input):
    return np.matrix([[int(digit) for digit in row] for row in input])


def compare_adjacent(input, i, j):
    if j == 0:
        left = float("inf")
    else:
        left = input[i, j - 1]
    if i == 0:
        up = float("inf")
    else:
        up = input[i - 1, j]
    if i == input.shape[0] - 1:
        down = float("inf")
    else:
        down = input[i + 1, j]
    if j == input.shape[1] - 1:
        right = float("inf")
    else:
        right = input[i, j + 1]
    if (
        input[i, j] < left
        and input[i, j] < right
        and input[i, j] < up
        and input[i, j] < down
    ):
        return True
    else:
        return False


def find_low(input):
    lows = []
    for j in range(input.shape[1]):
        for i in range(input.shape[0]):
            if compare_adjacent(input, i, j):
                lows.append(input[i, j])
    return lows


def get_risk(lows):
    return sum([low + 1 for low in lows])


def get_basins(input):
    basins, total_bs = measurements.label(np.where(input < 9, True, False))
    return basins, total_bs


def find_biggest(basins, n):
    basin_sizes = Counter(tools.flatten(basins.tolist()))
    del basin_sizes[0]  # 0s are the 9s (falses)
    return sorted(list(basin_sizes.values()))[-n:]


def main(raw, part):
    # read inputs from file
    input = tools.read_input(raw)
    input = parse_input(input)
    if part == 1:
        lows = find_low(input)
        return get_risk(lows)
    elif part == 2:
        basins, _ = get_basins(input)
        biggest3 = find_biggest(basins, 3)
        return math.prod(biggest3)
    else:
        raise ValueError("part must be 1 or 2, instead of: " + str(part))


def run_tests():
    assert main(test_raw, 1) == 15
    assert main(test_raw, 2) == 1134
    # solutions
    assert main(input_raw, 1) == 572
    assert main(input_raw, 2) == 847044


if __name__ == "__main__":
    run_tests()
    answer1 = main(input_raw, 1)
    answer2 = main(input_raw, 2)
    print("Answer part1: {}".format(answer1))
    print("Answer part2: {}".format(answer2))
