import os
import sys

sys.path.insert(0, "./")
from utils import tools
from operator import itemgetter
import numpy as np

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
input_raw = os.path.join(__location__, "input.txt")
test_raw = os.path.join(__location__, "test.txt")

#########
# Start #
#########


def parse_input(input):
    vents = [line.split(" -> ") for line in input]
    return [[tuple(map(int, points.split(","))) for points in vent] for vent in vents]


def draw_board(vents):
    max_x = max(tools.flatten(vents), key=itemgetter(0))[0]
    max_y = max(tools.flatten(vents), key=itemgetter(1))[1]
    return np.zeros((max_y + 1, max_x + 1), dtype=int)


def draw_vents(vents, board, part):
    for vent in vents:
        x1 = vent[0][0]
        x2 = vent[1][0]
        y1 = vent[0][1]
        y2 = vent[1][1]
        if x1 == x2:
            for num in range(min(y1, y2), max(y1, y2) + 1):
                board[num, x1] += 1
        elif y1 == y2:
            for num in range(min(x1, x2), max(x1, x2) + 1):
                board[y1, num] += 1
        elif part == 2 and ((y1 < y2 and x1 < x2) or (y1 > y2 and x1 > x2)):  # -45º
            for num_x, num_y in zip(
                range(min(x1, x2), max(x1, x2) + 1), range(min(y1, y2), max(y1, y2) + 1)
            ):
                board[num_y, num_x] += 1
        elif part == 2 and ((y1 > y2 and x1 < x2) or (y1 < y2 and x1 > x2)):  # 45º
            for num_x, num_y in zip(
                range(max(x1, x2), min(x1, x2) - 1, -1),
                range(min(y1, y2), max(y1, y2) + 1),
            ):
                board[num_y, num_x] += 1
    return board


def main(raw, part):
    # read inputs from file
    input = tools.read_input(raw)

    vents = parse_input(input)
    board = draw_board(vents)
    if part == 1:
        board_finale = draw_vents(vents, board, 1)
        intersections = board_finale > 1
        return intersections.sum()
    elif part == 2:
        board_finale = draw_vents(vents, board, 2)
        intersections = board_finale > 1
        return intersections.sum()
    else:
        raise ValueError("part must be 1 or 2, instead of: " + part)


def run_tests():
    assert main(test_raw, 1) == 5
    assert main(test_raw, 2) == 12
    # solutions
    assert main(input_raw, 1) == 7473
    assert main(input_raw, 2) == 24164


if __name__ == "__main__":
    run_tests()
    answer1 = main(input_raw, 1)
    answer2 = main(input_raw, 2)
    print("Answer part1: {}".format(answer1))
    print("Answer part2: {}".format(answer2))
