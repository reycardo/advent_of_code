from advent_of_code.utils.tools import get_txt_files, read_input, timing_decorator
from advent_of_code.utils.colors import magenta_color, reset_color
from dataclasses import dataclass, field
from itertools import groupby
import re
from typing import List, Optional


files = get_txt_files(__file__)
#########
# Start #
#########


@dataclass
class ClawMachine:
    button_A: List[int]
    button_B: List[int]
    prize: List[int]
    tokens_cost = [
        3,
        1,
    ]  # it costs 3 tokens to push the A button and 1 token to push the B button.
    possible: Optional[bool] = field(default=None, init=False)
    tokens_used: Optional[int] = field(default=None, init=False)
    solution: Optional[List[int]] = field(default=None, init=False)

    # solve the problem as soon as the object is created
    def __post_init__(self):
        self._solve()

    def _solve(self):
        a1, b1, c1 = self.button_A[0], self.button_B[0], self.prize[0]
        a2, b2, c2 = self.button_A[1], self.button_B[1], self.prize[1]

        determinant = a1 * b2 - a2 * b1

        if determinant == 0:
            self.possible = False
            self.tokens_used = None
            self.solution = None
        else:
            a = (c1 * b2 - c2 * b1) / determinant
            b = (a1 * c2 - a2 * c1) / determinant

            if a >= 0 and b >= 0 and a.is_integer() and b.is_integer():
                a, b = int(a), int(b)
                self.possible = True
                self.tokens_used = self.tokens_cost[0] * a + self.tokens_cost[1] * b
                self.solution = [a, b]
            else:
                self.possible = False
                self.tokens_used = None
                self.solution = None


class Puzzle:
    def __init__(self, text_input, part):
        self.input = text_input
        self.increment_prize = 0 if part == 1 else 10000000000000
        self.input_parsed = self.split_by_machines()
        self.claw_machines = self.create_claw_machines()

    def split_by_machines(self):
        return [
            list(group)
            for key, group in groupby(self.input, lambda x: x == "")
            if not key
        ]

    def create_claw_machines(self):
        return [
            ClawMachine(
                button_A=self.extract_values(instruction[0]),
                button_B=self.extract_values(instruction[1]),
                prize=self.extract_values(
                    instruction[2], increment=self.increment_prize
                ),
            )
            for instruction in self.input_parsed
        ]

    def extract_values(self, input_string, increment=0):
        # Use regular expression to find all numbers in the string
        values = re.findall(r"\d+", input_string)
        # Convert the extracted values to integers
        return list(map(lambda x: x + increment, map(int, values)))

    def solve(self, part):
        return sum(
            [
                claw_machine.tokens_used
                for claw_machine in self.claw_machines
                if claw_machine.possible
            ]
        )


@timing_decorator
def main(raw, part):
    text_input = read_input(raw)
    input_parsed = [i if i else "" for i in text_input]
    puzzle = Puzzle(input_parsed, part=part)
    return puzzle.solve(part)


def run_tests():
    print("\nRunning Tests:")
    assert main(raw=files["test"], part=1) == 480
    assert (
        main(raw=files["test"], part=2) == 459236326669 + 416082282239
    )  # calculated before # 2nd and 4th claw machines are the only ones with valid solutions

    # solutions
    print("\nRunning Solutions:")
    assert main(raw=files["input"], part=1) == 31623
    assert main(raw=files["input"], part=2) == 93209116744825


def solve():
    print("\nSolving:")
    answer1 = main(raw=files["input"], part=1)
    print(f"Answer part1: {magenta_color}{answer1}{reset_color}")
    answer2 = main(raw=files["input"], part=2)
    print(f"Answer part2: {magenta_color}{answer2}{reset_color}")


if __name__ == "__main__":
    run_tests()
    solve()
