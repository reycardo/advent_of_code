from utils.tools import get_txt_files, read_input, timing_decorator
from utils.colors import magenta_color, reset_color
from dataclasses import dataclass, field
from itertools import groupby
import re
from typing import List, Optional
import cvxpy as cp  # required cylp install for CBC solver


files = get_txt_files(__file__)
#########
# Start #
#########


@dataclass(frozen=True)
class ClawMachine:
    button_A: List[int]
    button_B: List[int]
    prize: List[int]
    tokens_cost = [
        3,
        1,
    ]  # it costs 3 tokens to push the A button and 1 token to push the B button.
    boundaries = [
        (0, 100),
        (0, 100),
    ]  # Each button would need to be pressed no more than 100 times to win a prize
    possible: Optional[bool] = field(default=None, init=False)
    tokens_used: Optional[int] = field(default=None, init=False)
    solution: Optional[List[int]] = field(default=None, init=False)

    def __post_init__(self):
        self._optimize()

    @property
    def lhs(self) -> List[List[int]]:
        return self._transpose([self.button_A] + [self.button_B])

    def _transpose(self, matrix):
        return [list(row) for row in zip(*matrix)]

    def _optimize(self):
        # Define the variables
        a = cp.Variable(integer=True)
        b = cp.Variable(integer=True)

        objective = cp.Minimize(3 * a + b)

        # Define the constraints
        constraints = [
            a * lhs[0] + lhs[1] * b == prize for lhs, prize in zip(self.lhs, self.prize)
        ]

        # Define the problem
        problem = cp.Problem(objective, constraints)

        # Solve the problem
        problem.solve(solver=cp.CBC)

        # Extract the results
        possible = problem.status == cp.OPTIMAL
        solution = [a.value, b.value] if possible else None
        tokens_used = problem.value if possible else None

        object.__setattr__(self, "possible", possible)
        object.__setattr__(self, "tokens_used", int(tokens_used) if possible else None)
        object.__setattr__(self, "solution", solution if possible else None)


class Puzzle:
    def __init__(self, text_input, part):
        self.input = text_input
        self.part = part
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
                prize=self.extract_values(instruction[2], increment=True)
                if self.part == 2
                else self.extract_values(instruction[2]),
            )
            for instruction in self.input_parsed
        ]

    def extract_values(self, input_string, increment=False):
        # Use regular expression to find all numbers in the string
        values = re.findall(r"\d+", input_string)
        # Convert the extracted values to integers
        if increment:
            return list(map(lambda x: x + 10000000000000, map(int, values)))
        return list(map(int, values))

    def solve(self, part):
        if part == 1:
            return sum(
                [
                    claw_machine.tokens_used
                    for claw_machine in self.claw_machines
                    if claw_machine.possible
                ]
            )
        elif part == 2:
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
    print(f"\nRunning Tests:")
    assert main(raw=files["test"], part=1) == 480
    assert main(raw=files["test"], part=2) == 459236326669 + 416082282239

    # solutions
    print(f"\nRunning Solutions:")
    assert main(raw=files["input"], part=1) == 31623
    # assert main(raw=files["input"], part=2) == 1686


def solve():
    print(f"\nSolving:")
    answer1 = main(raw=files["input"], part=1)
    print(f"Answer part1: {magenta_color}{answer1}{reset_color}")
    answer2 = main(raw=files["input"], part=2)
    print(f"Answer part2: {magenta_color}{answer2}{reset_color}")


if __name__ == "__main__":
    run_tests()
    solve()
