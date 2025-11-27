import os
import sys

sys.path.insert(0, "./")
from utils import tools
import numpy as np
from itertools import product

raw = r"2021\Day11\test.txt"

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
input_raw = os.path.join(__location__, "input.txt")
test_raw = os.path.join(__location__, "test.txt")

#########
# Start #
#########


class Dumbos:
    def __init__(self, start_matrix: np.matrix):
        self.state = start_matrix
        self.step = 0
        self.flashes = 0
        self.have_flashed = set()
        self.flashbang_step = None

    def is_inside(self, coords: tuple):
        if all(
            (
                coords[0] >= 0,
                coords[0] < self.state.shape[0],
                coords[1] >= 0,
                coords[1] < self.state.shape[1],
            )
        ):
            return True
        else:
            return False

    def get_adjacents(self, coords: tuple):
        for r_offset, c_offset in product(
            range(-1, 2), range(-1, 2)
        ):  # get all offsets
            if not (r_offset == 0 and c_offset == 0):  # if not own
                adjacent = (coords[0] + r_offset, coords[1] + c_offset)
                if self.is_inside(adjacent):
                    yield adjacent

    def flash(self, coords):
        self.have_flashed.add(coords)
        adjacents = self.get_adjacents(coords)
        for adjacent in adjacents:
            self.state[adjacent] += 1

    def increment_energy(self):
        self.state += 1

    def get_to_flash(self):
        it = np.nditer(self.state, flags=["multi_index"])
        to_flash = [
            it.multi_index
            for energy in it
            if energy > 9 and it.multi_index not in self.have_flashed
        ]
        return to_flash

    def is_flashbang(self):
        if (
            np.array_equal(self.state, np.zeros(self.state.shape, dtype=int))
            and not self.flashbang_step
        ):
            return True
        else:
            return False

    def increment_step(self):
        self.have_flashed = set()
        self.step += 1
        self.increment_energy()
        to_flash = self.get_to_flash()
        while to_flash:
            for coords in to_flash:
                self.flash(coords)
            to_flash = self.get_to_flash()
        for coords in self.have_flashed:
            self.state[coords] = 0
            self.flashes += 1
        if self.is_flashbang():
            self.flashbang_step = self.step


def parse_input(input):
    return np.matrix([[int(digit) for digit in row] for row in input])


def main(raw, part):
    # read inputs from file
    input = tools.read_input(raw)
    input = parse_input(input)

    dumbos = Dumbos(input.copy())
    if part == 1:
        for step in range(100):
            dumbos.increment_step()
        return dumbos.flashes
    elif part == 2:
        while not dumbos.flashbang_step:
            dumbos.increment_step()
        return dumbos.flashbang_step
    else:
        raise ValueError("part must be 1 or 2, instead of: " + str(part))


def run_tests():
    assert main(test_raw, 1) == 1656
    assert main(test_raw, 2) == 195
    # solutions
    assert main(input_raw, 1) == 1773
    assert main(input_raw, 2) == 494


if __name__ == "__main__":
    run_tests()
    answer1 = main(input_raw, 1)
    answer2 = main(input_raw, 2)
    print("Answer part1: {}".format(answer1))
    print("Answer part2: {}".format(answer2))
