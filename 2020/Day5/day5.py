import re
import os
import sys
sys.path.insert(0, './')
from utils import tools

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
input_raw = os.path.join(__location__,'input.txt')
test_raw = os.path.join(__location__,'test.txt')

# For interactive testing
raw = r'2020\Day5\test.txt'

#########
# Start #
#########


def calc_seat_id(row, column,multiple):
    return row * multiple + column

def read_binary_cols(my_string):
    row = int(my_string[:7].replace('F','0').replace('B','1'),2)
    column = int(my_string[7:].replace('L','0').replace('R','1'),2)
    id = calc_seat_id(row, column,8)
    return (row, column, id)

def main(raw,part):
    # read inputs from file
    input = tools.read_input(raw)    
    if part == 1:        
        bps_result = [read_binary_cols(bp) for bp in input]
        return max([bp[2] for bp in bps_result])
    elif part == 2:        
        bps_result = [read_binary_cols(bp) for bp in input]
        bps_ids = [bp[2] for bp in bps_result]
        return [b+1 for a in bps_ids for b in bps_ids if (b+2==a and b+1 not in bps_ids)]
        
    else:
        raise ValueError("part must be 1 or 2, instead of: " + part)
    

def run_tests():    
    assert main(test_raw,1) == 820  
    #assert main(test_raw,2) == 0


if __name__ == '__main__':
    run_tests()
    answer1 = main(input_raw,1)    
    answer2 = main(input_raw,2)    
    print("Answer part1: {}".format(answer1))        
    print("Answer part2: {}".format(answer2))    