from utils.tools import get_txt_files, read_input, timing_decorator
from utils.colors import magenta_color, reset_color
from typing import List, Dict, Union
from itertools import product
from collections import defaultdict


files = get_txt_files(__file__)
#########
# Start #
#########


class Engine:
    def __init__(self, text_input: List[str]):
        self.input = self.parse_input(text_input)
        self.gears: dict = defaultdict(list)
        self.gear_number_coords: dict = defaultdict(list)

    def parse_input(self, input):
        return [[digit for digit in row] for row in input]

    def get_adjacents(self, coords: tuple):
        for r_offset, c_offset in product(
            range(-1, 2), range(-1, 2)
        ):  # get all offsets
            if not (r_offset == 0 and c_offset == 0):  # if not own
                adjacent = (coords[0] + r_offset, coords[1] + c_offset)
                if self.is_inside(adjacent):
                    yield adjacent

    def is_inside(self, coords: tuple):
        if all(
            (
                coords[0] >= 0,
                coords[0] < len(self.input),
                coords[1] >= 0,
                coords[1] < len(self.input[0]),
            )
        ):
            return True
        else:
            return False

    def check_next_to_symbol(self, current_digit_coord):
        part_digit = False
        next_to_gear = False
        for adjacent in self.get_adjacents(current_digit_coord):
            row = adjacent[0]
            column = adjacent[1]
            target_adjacent = self.input[row][column]
            if target_adjacent != "." and not target_adjacent.isdigit():  # is symbol
                part_digit = True
                if (
                    target_adjacent == "*"
                    and self.input[current_digit_coord[0]][
                        current_digit_coord[1]
                    ].isdigit()
                ):
                    next_to_gear = True
                    self.gears[(row, column)].append(current_digit_coord)
        return part_digit, next_to_gear

    def check_digit_is_in_part_number(self, row, part_digit_row, i):
        result = []
        part_numbers = []
        current_number = ""
        current_coords = []
        part_number = False
        for j, (char, part_digit) in enumerate(zip(row, part_digit_row)):
            if char.isdigit():
                current_number += char
                current_coords.append((i, j))
                if part_digit:
                    part_number = True
            else:
                if current_number:
                    if part_number:
                        self.gear_number_coords[
                            current_number + "_" + str(current_coords[0])
                        ].append(current_coords)
                        part_numbers.append(int(current_number))
                    result.append(int(current_number))
                    current_number = ""
                    current_coords = []
                    part_number = False

        # Check for any remaining digits after the last '.'
        if current_number:
            result.append(int(current_number))
            if part_number:
                part_numbers.append(int(current_number))
                self.gear_number_coords[current_number].append(current_coords)

        return result, part_numbers

    def solve(self, part):
        if part == 1:
            result = []
            for i, row in enumerate(self.input):
                part_digit_row = []
                for j, x in enumerate(row):
                    part_digit_row.append(self.check_next_to_symbol((i, j))[0])
                result.append(
                    self.check_digit_is_in_part_number(row, part_digit_row, i)[1]
                )
            return sum(sum(sublist) for sublist in result)
        if part == 2:
            result = []
            for i, row in enumerate(self.input):
                part_digit_row = []
                for j, x in enumerate(row):
                    part_digit_row.append(self.check_next_to_symbol((i, j))[1])
                result.append(
                    self.check_digit_is_in_part_number(row, part_digit_row, i)[1]
                )
            correct_gears_dict = {}
            for key_A, value_A in self.gears.items():
                matching_keys = [
                    key_B
                    for key_B, value_B_list in self.gear_number_coords.items()
                    if any(
                        any(val_A in sublist for sublist in value_B_list)
                        for val_A in value_A
                    )
                ]
                correct_gears_dict[key_A] = matching_keys
            return self.solve_gears(correct_gears_dict)

    def solve_gears(self, dict):
        corrected_dict = {key: value for key, value in dict.items() if len(value) == 2}
        trimmed_dict = {
            key: [value.split("_")[0] for value in values]
            for key, values in corrected_dict.items()
        }
        result_dict = {
            key: [int(values[0]) * int(values[1])]
            for key, values in trimmed_dict.items()
        }
        return sum(value for values in result_dict.values() for value in values)


@timing_decorator
def main(raw, part):
    text_input = read_input(raw)
    input_parsed = [i if i else "" for i in text_input]
    engine = Engine(input_parsed)
    return engine.solve(part)


def run_tests():
    print(f"\nRunning Tests:")
    assert main(raw=files["test"], part=1) == 4361
    assert main(raw=files["test"], part=2) == 467835

    # solutions
    print(f"\nRunning Solutions:")
    assert main(raw=files["input"], part=1) == 544664
    assert main(raw=files["input"], part=2) == 84495585


def solve():
    print(f"\nSolving:")
    answer1 = main(raw=files["input"], part=1)
    print(f"Answer part1: {magenta_color}{answer1}{reset_color}")
    answer2 = main(raw=files["input"], part=2)
    print(f"Answer part2: {magenta_color}{answer2}{reset_color}")


if __name__ == "__main__":
    run_tests()
    solve()
