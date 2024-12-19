from __future__ import annotations
from utils.tools import get_txt_files, read_input, timing_decorator
from utils.colors import magenta_color, reset_color
from typing import List
from functools import cache

files = get_txt_files(__file__)
#########
# Start #
#########

class Puzzle:
    def __init__(self, text_input):
        self.input: List[str] = text_input
        self.split_towels_from_patterns()
        self.possible_patterns = {}
    
    def split_towels_from_patterns(self):
        separator_index = self.input.index("")
        self.available_towels = [item for sublist in self.input[:separator_index] for item in sublist.split(', ')]
        self.desired_designs = [raw for raw in self.input[separator_index + 1 :]]
    
    @cache
    def is_possible(self, current_design: str) -> bool:
        """
        Checks if a given design can be built by concatenating one or more 
        patterns from the `available_towels` set.
        
        Returns:
            bool: count of ways the `current_design` can be constructed using the patterns
        """
        count = 0
        if current_design == "":
            return 1
        
        # We need to check if we can contruct a "prefix" of the design from available patterns.
        # If so, we recurse into the remainder        
        for pattern in self.available_towels:
            if current_design.startswith(pattern):
                count += self.is_possible(current_design[len(pattern):])

        return count
        

    def solve(self, part):
        if part == 1:
            return len([pattern for pattern in self.desired_designs if self.is_possible(pattern)])
        elif part == 2:                                                
            return sum([self.is_possible(pattern) for pattern in self.desired_designs])

@timing_decorator
def main(raw, part):
    text_input = read_input(raw)
    input_parsed = [i if i else "" for i in text_input]
    puzzle = Puzzle(input_parsed)
    return puzzle.solve(part)


def run_tests():
    print(f"\nRunning Tests:")
    assert main(raw=files["test"], part=1) == 6
    assert main(raw=files["test"], part=2) == 16

    # solutions
    print(f"\nRunning Solutions:")
    assert main(raw=files["input"], part=1) == 308
    assert main(raw=files["input"], part=2) == 662726441391898


def solve():
    print(f"\nSolving:")
    answer1 = main(raw=files["input"], part=1)    
    print(f"Answer part1: {magenta_color}{answer1}{reset_color}")
    answer2 = main(raw=files["input"], part=2)
    print(f"Answer part2: {magenta_color}{answer2}{reset_color}")


if __name__ == "__main__":
    run_tests()
    solve()
