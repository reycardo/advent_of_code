from __future__ import annotations
from utils.tools import get_txt_files, read_input, timing_decorator
from utils.colors import magenta_color, reset_color
from typing import List
from collections import deque
from functools import lru_cache

files = get_txt_files(__file__)
#########
# Start #
#########

class Puzzle:
    def __init__(self, text_input):
        self.input: List[str] = text_input
        self.split_towels_from_patterns()        
    
    def split_towels_from_patterns(self):
        separator_index = self.input.index("")
        self.available_towels = [item for sublist in self.input[:separator_index] for item in sublist.split(', ')]
        self.desired_patterns = [raw for raw in self.input[separator_index + 1 :]]

    def get_possible_frontiers(self, pattern: str):
        frontiers = []
        possible_towels = [towel for towel in self.available_towels if towel in pattern]
        # initialize all posible frontiers
        for i in range(1,len(pattern)):
            for towel in possible_towels:
                if towel == pattern[:i]:
                    frontiers.append(deque([[towel]]))
                    break
            i += 1
        return frontiers
    
    @lru_cache(None)
    def get_possible_towel_patterns(self, pattern: str):
        frontiers: List[deque] = self.get_possible_frontiers(pattern)
        patterns = []
        possible_towels = [towel for towel in self.available_towels if towel in pattern]
        pattern_length = len(pattern)
        for frontier in frontiers:
            while frontier:
                stripe_list = frontier.popleft()
                stripes = ''.join(stripe_list)
                
                if stripes == pattern:
                    patterns.append(stripe_list)
                    continue
                
                for towel in possible_towels:
                    new_pattern = stripe_list + [towel]
                    new_stripes = ''.join(new_pattern)                                        
                    if new_stripes == pattern[:len(new_stripes)]:
                        frontier.append(new_pattern)
                        if len(new_stripes) == pattern_length: # no more possible towels
                            break
        return patterns
    
    def check_if_next_pattern_fits(self, pattern: str, towel: str):



    def solve(self, part):
        if part == 1:
            self.possible_towel_patterns = {}
            for pattern in self.desired_patterns:
                print(pattern)
                self.possible_towel_patterns[pattern] = self.get_possible_towel_patterns(pattern)                
            return sum([1 for v in self.possible_towel_patterns.values() if len(v) > 0])
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
    assert main(raw=files["test"], part=1) == 6
    # assert main(raw=files["test"], part=2) == 22

    # solutions
    # print(f"\nRunning Solutions:")
    # assert main(raw=files["input"], part=1) == 312
    # assert main(raw=files["input"], part=2) == 1509724


def solve():
    print(f"\nSolving:")
    answer1 = main(raw=files["input"], part=1)    
    print(f"Answer part1: {magenta_color}{answer1}{reset_color}")
    # answer2 = main(raw=files["input"], part=2)
    # print(f"Answer part2: {magenta_color}{answer2}{reset_color}")


if __name__ == "__main__":
    run_tests()
    solve()
