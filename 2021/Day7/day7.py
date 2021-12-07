import os
import sys
sys.path.insert(0, './')
from utils import tools
from collections import Counter
import statistics
import math

raw = r'2021\Day7\test.txt'

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
input_raw = os.path.join(__location__,'input.txt')
test_raw = os.path.join(__location__,'test.txt')

#########
# Start #
#########

def parse_input(input):            
    return [list(map(int,line.split(','))) for line in input][0]


def fuel(input,part):
    if part == 1:
        stat = int(statistics.median(input))
        return sum([abs(crab - stat) for crab in input])
    elif part == 2:
        stat_plus = math.ceil(statistics.mean(input))
        stat = round(statistics.mean(input))
        stat_minus = math.floor(statistics.mean(input))
        stats = [stat_minus, stat_plus, stat]
        tries = []
        for stat_ in stats:
            tries.append(sum([int((abs(crab - stat_) * (abs(crab - stat_) + 1))/2) for crab in input]))
        return min(tries)

def main(raw,part):
    # read inputs from file
    input = tools.read_input(raw)
    input = parse_input(input)
    if part == 1:                                
        return fuel(input,1)
    elif part == 2:        
        return fuel(input,2)
    else:
        raise ValueError("part must be 1 or 2, instead of: " + part)


def run_tests():
    assert main(test_raw,1) == 37
    assert main(test_raw,2) == 168
    # solutions
    assert main(input_raw,1) == 344535
    #assert main(input_raw,2) == 1639854996917
    

    
if __name__ == '__main__':
    run_tests()
    answer1 = main(input_raw,1)
    answer2 = main(input_raw,2)    
    print("Answer part1: {}".format(answer1))
    print("Answer part2: {}".format(answer2))