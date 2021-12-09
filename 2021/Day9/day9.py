import os
import sys
sys.path.insert(0, './')
from utils import tools
import numpy as np

raw = r'2021\Day9\test.txt'

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
input_raw = os.path.join(__location__,'input.txt')
test_raw = os.path.join(__location__,'test.txt')

#########
# Start #
#########

def parse_input(input):                
    return np.matrix([[int(digit) for digit in row] for row in input])

def compare_adjacent(input,i,j):
    pass

def find_low(input):
    lows = []
    for i in range(input.shape[0]):
        for j in range(input.shape[1]):
            if compare_adjacent(input,i,j):
                lows.append(input[i,j])
    return lows

def main(raw,part):
    # read inputs from file
    input = tools.read_input(raw)
    input = parse_input(input)
    if part == 1:                                
        pass
    elif part == 2:        
        pass
    else:
        raise ValueError("part must be 1 or 2, instead of: " + str(part))


def run_tests():
    assert main(test_raw,1) == 15
    #assert main(test_raw,2) == 61229
    # solutions
    #assert main(input_raw,1) == 303
    #assert main(input_raw,2) == 961734
    
    
if __name__ == '__main__':
    run_tests()
    answer1 = main(input_raw,1)
    answer2 = main(input_raw,2)    
    print("Answer part1: {}".format(answer1))
    print("Answer part2: {}".format(answer2))