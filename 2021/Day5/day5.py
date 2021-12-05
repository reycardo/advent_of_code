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
    return [line.split(' -> ') for line in input]

                          
def main(raw,part):
    # read inputs from file
    input = tools.read_input(raw)
        
    vents = parse_input(input)
    if part == 1:                
        return (winners[0].sum() + checks[0]) * int(last_draws[0]) # sum of remaining digits in winning board * last draw
    elif part == 2:        
        return (winners[-1].sum() + checks[-1]) * int(last_draws[-1]) # sum of remaining digits in losing board * last draw
    else:
        raise ValueError("part must be 1 or 2, instead of: " + part)


def run_tests():
    assert main(test_raw,1) == 5
    #assert main(test_raw,2) == 1924
    # solutions
    #assert main(input_raw,1) == 11536
    #assert main(input_raw,2) == 1284
    

    
if __name__ == '__main__':
    run_tests()
    answer1 = main(input_raw,1)
    #answer2 = main(input_raw,2)    
    print("Answer part1: {}".format(answer1))
    #print("Answer part2: {}".format(answer2))