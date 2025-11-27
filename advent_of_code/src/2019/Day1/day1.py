from advent_of_code.utils.tools import get_txt_files, read_input, timing_decorator
from advent_of_code.utils.colors import magenta_color, reset_color

files = get_txt_files(__file__)
#########
# Start #
#########


class Fuel:
    def __init__(self, text_input: list):
        self.input = text_input

    def get_module_fuel(self, mass):
        return (mass // 3) - 2

    def get_module_fuel_recursive(self, mass):
        result = (mass // 3) - 2
        if result <= 0:
            return 0
        else:
            return result + self.get_module_fuel_recursive(result)

    def get_fuel(self, part):
        if part == 1:
            return sum([self.get_module_fuel(element) for element in self.input])
        elif part == 2:
            return sum(
                [self.get_module_fuel_recursive(element) for element in self.input]
            )
        else:
            raise ValueError("part must be 1 or 2, instead of: " + part)


@timing_decorator
def main(raw, part):
    text_input = read_input(raw)
    input_parsed = [int(i) if i else "" for i in text_input]
    fuel = Fuel(input_parsed)
    return fuel.get_fuel(part)


def run_tests():
    print("\nRunning Tests:")
    assert main(files["test1_1"], 1) == 654
    assert main(files["test1_2"], 1) == 33583
    assert main(files["test2_1"], 2) == 2
    assert main(files["test2_2"], 2) == 966
    assert main(files["test2_3"], 2) == 50346

    # solutions
    assert main(files["input"], 1) == 3481005
    assert main(files["input"], 2) == 5218616


def run_solution():
    print("\nRunning Solutions:")
    answer1 = main(files["input"], 1)
    print(f"Answer part1: {magenta_color}{answer1}{reset_color}")
    answer2 = main(files["input"], 2)
    print(f"Answer part2: {magenta_color}{answer2}{reset_color}")


if __name__ == "__main__":
    run_tests()
    run_solution()
