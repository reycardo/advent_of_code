from utils.tools import get_txt_files, read_input, timing_decorator
from utils.colors import magenta_color, reset_color
from scipy.optimize import linprog
from dataclasses import dataclass, field
from itertools import groupby
import re
from typing import List, Optional

files = get_txt_files(__file__)
#########
# Start #
#########

@dataclass(frozen=True)
class ClawMachine:    
    button_A: List[int]
    button_B: List[int]
    prize: List[int]
    tokens_cost = [3,1] # it costs 3 tokens to push the A button and 1 token to push the B button.
    boundaries = [(0,100),(0,100)] # Each button would need to be pressed no more than 100 times to win a prize
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
        result = linprog(
            c = self.tokens_cost,
            A_eq = self.lhs,
            b_eq = self.prize,
            bounds = self.boundaries
        )            
        possible = result.success
        # tokens_used = round(result.fun) if result.success else None
        solution = list(map(round,result.x)) if result.success else None        
        tokens_used = sum(a * b for a, b in zip(solution, self.tokens_cost)) if result.success else None
        object.__setattr__(self, 'possible', possible)
        object.__setattr__(self, 'tokens_used', tokens_used)
        object.__setattr__(self, 'solution', solution)

class Puzzle:
    def __init__(self, text_input):
        self.input = text_input
        self.input_parsed = self.split_by_machines()
        self.claw_machines = self.create_claw_machines()

    
    def split_by_machines(self):
        return [list(group) for key, group in groupby(self.input, lambda x: x == '') if not key]

    def create_claw_machines(self):
        return [
            ClawMachine(
                button_A=self.extract_values(instruction[0]), 
                button_B=self.extract_values(instruction[1]),
                prize=self.extract_values(instruction[2])
            ) for instruction in self.input_parsed
        ]

    def extract_values(self, input_string):
        # Use regular expression to find all numbers in the string
        values = re.findall(r'\d+', input_string)
        # Convert the extracted values to integers
        return list(map(int, values))


    def solve(self, part):
        if part == 1:
            return sum([claw_machine.tokens_used for claw_machine in  self.claw_machines if claw_machine.possible])
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
    assert main(raw=files["test"], part=1) == 480
    # assert main(raw=files["test"], part=2) == 81
    

    # solutions
    # print(f"\nRunning Solutions:")
    # assert main(raw=files["input"], part=1) == 717
    # assert main(raw=files["input"], part=2) == 1686


def solve():
    print(f"\nSolving:")
    answer1 = main(raw=files["input"], part=1)
    print(f"Answer part1: {magenta_color}{answer1}{reset_color}")
    # answer2 = main(raw=files["input"], part=2)
    # print(f"Answer part2: {magenta_color}{answer2}{reset_color}")


if __name__ == "__main__":
    run_tests()
    solve()
