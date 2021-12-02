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

def parse_input(input):            
    input = [x.split(' ') for x in input if x]
    return [(i[0],int(i[1])) for i in input]

def get_pos(input):
    depth = 0
    h = 0
    for i in range(len(input)):
        if input[i][0] == 'forward':
            h += input[i][1]
        elif input[i][0] == 'up':
            depth -= input[i][1]
        elif input[i][0] == 'down':
            depth += input[i][1]                        
    return depth, h

def get_pos_aim(input):
    depth = 0
    h = 0
    aim = 0
    for i in range(len(input)):
        if input[i][0] == 'forward':
            h += input[i][1]
            depth += aim * input[i][1]
        elif input[i][0] == 'up':
            aim -= input[i][1]
        elif input[i][0] == 'down':
            aim += input[i][1]                        
    return depth, h

def main(raw,part):
    # read inputs from file
    input = tools.read_input(raw)
        
    input = parse_input(input)
    if part == 1:        
        depth, h = get_pos(input)
        return depth * h
    elif part == 2:        
        depth, h = get_pos_aim(input)
        return depth * h
    else:
        raise ValueError("part must be 1 or 2, instead of: " + part)


def run_tests():
    assert main(test_raw,1) == 150
    assert main(test_raw,2) == 900
    # solutions
    assert main(input_raw,1) == 1507611
    #assert main(input_raw,2) == 1880593125
    

    
if __name__ == '__main__':
    run_tests()
    answer1 = main(input_raw,1)
    answer2 = main(input_raw,2)    
    print("Answer part1: {}".format(answer1))
    print("Answer part2: {}".format(answer2))