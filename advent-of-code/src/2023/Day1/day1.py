from utils.tools import get_txt_files, read_input, timing_decorator
from utils.colors import magenta_color, reset_color
from itertools import groupby

files = get_txt_files(__file__)
#########
# Start #
#########


class Calibration:
    def __init__(self, text_input: list):
        self.input = text_input

    def get_calib_values(self, input_string: str):
        # Find the first digit
        first_digit = next((char for char in input_string if char.isdigit()), None)

        # Find the last digit
        reversed_string = input_string[::-1]
        last_digit = next((char for char in reversed_string if char.isdigit()), None)

        return first_digit, last_digit

    def get_calib_doc(self):
        return self.get_calib_values(self.input)


@timing_decorator
def main(raw, part):
    text_input = read_input(raw)
    input_parsed = [i if i else "" for i in text_input]
    calibration = Calibration(input_parsed)
    if part == 1:
        return calibration.get_calib_doc()
    elif part == 2:
        pass
    else:
        raise ValueError("part must be 1 or 2, instead of: " + part)


def run_tests():
    print(f"\nRunning Tests:")
    assert main(files["test"], 1) == 24000
    # assert main(files["test"], 2) == 45000

    # solutions
    # assert main(files["input"], 1) == 66616
    # assert main(files["input"], 2) == 199172


def run_solution():
    print(f"\nRunning Solutions:")
    answer1 = main(files["input"], 1)
    print(f"Answer part1: {magenta_color}{answer1}{reset_color}")
    # answer2 = main(files["input"], 2)
    # print(f"Answer part2: {magenta_color}{answer2}{reset_color}")


if __name__ == "__main__":
    run_tests()
    run_solution()
