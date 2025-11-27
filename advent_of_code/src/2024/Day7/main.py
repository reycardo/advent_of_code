from utils.tools import get_txt_files, read_input, timing_decorator
from advent_of_code.utils.colors import magenta_color, reset_color
import operator
import itertools
from typing import List

files = get_txt_files(__file__)
#########
# Start #
#########


class Equation:
    def __init__(self, left, right, part):
        self.result = left
        self.available_numbers = right
        self.available_operations = {"+": operator.add, "*": operator.mul}
        if part == 2:
            self.available_operations["||"] = operator.concat

        self.possible = False
        self.successful_combinations = []  # List to store successful combinations
        self.solve()

    def solve(self):
        # Generate all combinations of operations
        operation_combinations = itertools.product(
            self.available_operations.keys(), repeat=len(self.available_numbers) - 1
        )

        for operations in operation_combinations:
            current_result = self.available_numbers[0]
            for i, operation in enumerate(operations):
                if operation == "||":
                    current_result = int(
                        self.available_operations[operation](
                            str(current_result), str(self.available_numbers[i + 1])
                        )
                    )
                else:
                    current_result = self.available_operations[operation](
                        current_result, self.available_numbers[i + 1]
                    )

            # Check if the current result matches the desired result
            if current_result == self.result:
                self.possible = True
                self.successful_combinations.append(
                    operations
                )  # Append successful combination


class Puzzle:
    def __init__(self, text_input):
        self.input = text_input

    def parse_input(self, part):
        equations = []

        for item in self.input:
            parts = item.split(":")
            left = int(parts[0])
            right = list(map(int, parts[1].strip().split()))
            equations.append(Equation(left, right, part=part))

        return equations

    def solve(self, part):
        if part == 1:
            self.equations: List[Equation] = self.parse_input(part)
        elif part == 2:
            self.equations: List[Equation] = self.parse_input(part)

        return sum(
            [equation.result for equation in self.equations if equation.possible]
        )


@timing_decorator
def main(raw, part):
    text_input = read_input(raw)
    input_parsed = [i if i else "" for i in text_input]
    puzzle = Puzzle(input_parsed)
    return puzzle.solve(part)


def run_tests():
    print("\nRunning Tests:")
    assert main(raw=files["test"], part=1) == 3749
    assert main(raw=files["test"], part=2) == 11387

    # solutions
    print("\nRunning Solutions:")
    assert main(raw=files["input"], part=1) == 1611660863222
    assert main(raw=files["input"], part=2) == 945341732469724


def solve():
    print("\nSolving:")
    answer1 = main(raw=files["input"], part=1)
    print(f"Answer part1: {magenta_color}{answer1}{reset_color}")
    answer2 = main(raw=files["input"], part=2)
    print(f"Answer part2: {magenta_color}{answer2}{reset_color}")


if __name__ == "__main__":
    run_tests()
    solve()
