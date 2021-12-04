import os
import sys
sys.path.insert(0, './')
from utils import tools
import pandas as pd
import numpy as np

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
input_raw = os.path.join(__location__,'input.txt')
test_raw = os.path.join(__location__,'test.txt')

#########
# Start #
#########

def parse_input(input):                     
    draws = input[0].split(',')
    return pd.DataFrame([[*x] for x in input if x])


def main(raw,part):
    # read inputs from file
    input = tools.read_input(raw)
        
    input = parse_input(input)
    if part == 1:        
        pass
    elif part == 2:        
        pass
    else:
        raise ValueError("part must be 1 or 2, instead of: " + part)


def run_tests():
    assert main(test_raw,1) == 4512
    #assert main(test_raw,2) == 230
    # solutions
    #assert main(input_raw,1) == 3813416
    #assert main(input_raw,2) == 2990784
    

    
if __name__ == '__main__':
    run_tests()
    answer1 = main(input_raw,1)
    answer2 = main(input_raw,2)    
    print("Answer part1: {}".format(answer1))
    print("Answer part2: {}".format(answer2))