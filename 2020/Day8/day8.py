import os
import sys

sys.path.insert(0, './')
from utils import tools

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
input_raw = os.path.join(__location__,'input.txt')
test_raw = os.path.join(__location__,'test.txt')

#########
# Start #
#########

def main(raw,part):    
    input = tools.read_input(raw)        
    if part == 1:               
        pass        
    elif part == 2:
        pass
    else:
        raise ValueError("part must be 1 or 2, instead of: " + part)
    

def run_tests():          
    assert main(test_raw,1) == 0
    #assert main(test_raw,2) == 0
    # solutions
    #assert main(input_raw,1) == 0
    #assert main(input_raw,2) == 0



if __name__ == '__main__':
    run_tests()
    answer1 = main(input_raw,1)    
    answer2 = main(input_raw,2)    
    print("Answer part1: {}".format(answer1))        
    print("Answer part2: {}".format(answer2))    
