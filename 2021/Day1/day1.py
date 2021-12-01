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
    # read inputs from file
    input = tools.read_input(raw)
    
    # convert to all elements int
    input = [int(i) for i in input if i]
    
    if part == 1:
        # return a*b if a+b=2020 for any a,b in input
        return [a*b for a in input for b in input if a+b==2020][0]
    elif part == 2:
        # return a*b*c if a+b+c=2020 for any a,b,c in input
        return [a*b*c for a in input for b in input for c in input if a+b+c==2020][0]
    else:
        raise ValueError("part must be 1 or 2, instead of: " + part)


def run_tests():
    assert main(test_raw,1) == 514579
    # assert main(test_raw,2) == 241861950
    # solutions
    assert main(input_raw,1) == 545379
    # assert main(input_raw,2) == 257778836
    

    
if __name__ == '__main__':
    run_tests()
    answer1 = main(input_raw,1)
    answer2 = main(input_raw,2)    
    print("Answer part1: {}".format(answer1))
    print("Answer part2: {}".format(answer2))