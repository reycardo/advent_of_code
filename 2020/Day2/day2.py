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

def read_input_d2(file):
    with open(file, "r") as tf:
        input = tf.read().split('\n')        
    input = [x.replace(':', '').split(' ') for x in input if x]        
    return [[y for x in group for y in x.split('-')] for group in input]


def check_corrupted_p1(list):
    lower = list[3].count(list[2]) <= int(list[1])
    greater = list[3].count(list[2]) >= int(list[0])
    if lower & greater:
        return True
    else:
        return False

def check_corrupted_p2(list):
    lower = list[3][int(list[0])-1] == list[2]
    greater = list[3][int(list[1])-1] == list[2]
    if lower != greater:
        return True
    else:
        return False

def main(raw,part):
    # read inputs from file
    input = read_input_d2(raw)    
    if part == 1:
        # return a*b if a+b=2020 for any a,b in input
        return sum([check_corrupted_p1(group) for group in input])
    elif part == 2:
        # return a*b*c if a+b+c=2020 for any a,b,c in input
        return sum([check_corrupted_p2(group) for group in input])
    else:
        raise ValueError("part must be 1 or 2, instead of: " + part)
    


def run_tests():
    assert main(test_raw,1) == 2
    assert main(test_raw,2) == 1

    
if __name__ == '__main__':
    run_tests()
    answer1 = main(input_raw,1)    
    answer2 = main(input_raw,2)    
    print("Answer part1: {}".format(answer1))        
    print("Answer part1: {}".format(answer2))    