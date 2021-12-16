import os
import sys

cur_path = os.path.abspath(".")
sys.path.insert(0, cur_path)
from utils import tools
import numpy as np
from itertools import product
from collections import defaultdict
import networkx as nx

raw = r"2021\Day16\test.txt"

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
input_raw = os.path.join(__location__, "input.txt")
test_raw = os.path.join(__location__, "test.txt")

#########
# Start #
#########


def main(raw, part):
    input = tools.read_input(raw)    
    if part == 1:
        pass        
    elif part == 2:
        pass
    else:
        raise ValueError("part must be 1 or 2, instead of: " + part)


def run_tests():
    assert main(test_raw, 1) == 40
    #assert main(test_raw,2) == 315

    # solutions
    #assert main(input_raw, 1) == 824
    #assert main(input_raw,2) == 3063


if __name__ == "__main__":
    run_tests()
    answer1 = main(input_raw, 1)
    #answer2 = main(input_raw,2)
    print("Answer part1: {}".format(answer1))
    #print("Answer part2: {}".format(answer2))
