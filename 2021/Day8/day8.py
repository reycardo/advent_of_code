import os
import sys
sys.path.insert(0, './')
from utils import tools

raw = r'2021\Day8\test.txt'

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
input_raw = os.path.join(__location__,'input.txt')
test_raw = os.path.join(__location__,'test.txt')

#########
# Start #
#########

def parse_input(input):            
    return [line.split('|') for line in input]

# match_digit_segment
mds = {
    0: ['top','top_L','top_R','bot','bot_L','bot_R'],
    1: ['top_R','bot_R'],
    2: ['top','top_R','mid','bot','bot_L'],
    3: ['top','top_R','mid','bot','bot_R'],
    4: ['top_L','top_R','mid','bot_R'],
    5: ['top','top_L','mid','bot','bot_R'],
    6: ['top','top_L','mid','bot','bot_L','bot_R'],
    7: ['top','top_R','bot_R'],
    8: ['top','top_L','top_R','mid','bot','bot_L','bot_R'],
    9: ['top','top_L','top_R','mid','bot','bot_R']
}

signal2segment = {
    'a' : [],
    'b' : [],
    'c' : [],
    'd' : [],
    'e' : [],
    'f' : [],
    'g' : []
}



def count_easy_digits(input):
    output_length = [list(map(len,entry[1].split())) for entry in input]
    return len([length for length in tools.flatten(output_length) if length in [len(mds[1]),len(mds[4]),len(mds[7]),len(mds[8])]])

def main(raw,part):
    # read inputs from file
    input = tools.read_input(raw)
    input = parse_input(input)
    if part == 1:                                
        return count_easy_digits(input)
    elif part == 2:        
        pass
    else:
        raise ValueError("part must be 1 or 2, instead of: " + str(part))


def run_tests():
    assert main(test_raw,1) == 26
    assert main(test_raw,2) == 168
    # solutions
    assert main(input_raw,1) == 303
    #assert main(input_raw,2) == 95581659
    

    
if __name__ == '__main__':
    run_tests()
    answer1 = main(input_raw,1)
    #answer2 = main(input_raw,2)    
    print("Answer part1: {}".format(answer1))
    #print("Answer part2: {}".format(answer2))