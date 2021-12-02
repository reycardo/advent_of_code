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

def count(input):
    acc = 0
    for i in range(len(input)-1) :
        if input[i+1] > input[i]:
            acc += 1 
    return acc

def count_slide(input):
    acc = 0
    for i in range(len(input)-2) :
        if i == 0:
            pass
        elif input[i] + input[i+1] + input[i+2] > input[i-1] + input[i] + input[i+1]:
            acc += 1 
    return acc

def main(raw,part):
    # read inputs from file
    input = tools.read_input(raw)
    
    # convert to all elements int
    input = [int(i) for i in input if i]
    
    if part == 1:        
        return count(input)
    elif part == 2:        
        return count_slide(input)
    else:
        raise ValueError("part must be 1 or 2, instead of: " + part)


def run_tests():
    assert main(test_raw,1) == 7
    assert main(test_raw,2) == 5
    # solutions
    assert main(input_raw,1) == 1301
    assert main(input_raw,2) == 1346
    

    
if __name__ == '__main__':
    run_tests()
    answer1 = main(input_raw,1)
    answer2 = main(input_raw,2)    
    print("Answer part1: {}".format(answer1))
    print("Answer part2: {}".format(answer2))