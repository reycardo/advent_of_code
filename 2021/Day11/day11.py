import os
import sys
sys.path.insert(0, './')
from utils import tools

raw = r'2021\Day11\test.txt'

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
input_raw = os.path.join(__location__,'input.txt')
test_raw = os.path.join(__location__,'test.txt')

#########
# Start #
#########


def main(raw,part):
    # read inputs from file
    input = tools.read_input(raw)

    if part == 1:
        pass
    elif part == 2:        
        pass
    else:
        raise ValueError("part must be 1 or 2, instead of: " + str(part))


def run_tests():
    assert main(test_raw,1) == 26397
    #assert main(test_raw,2) == 288957
    # solutions
    #assert main(input_raw,1) == 316851
    #assert main(input_raw,2) == 2182912364
    
    
if __name__ == '__main__':
    run_tests()
    answer1 = main(input_raw,1)
    #answer2 = main(input_raw,2)    
    print("Answer part1: {}".format(answer1))
    #print("Answer part2: {}".format(answer2))