import os
import sys
import itertools
import math

sys.path.insert(0, './')
from utils import tools

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
input_raw = os.path.join(__location__,'input.txt')
test_raw = os.path.join(__location__,'test.txt')

# For interactive testing
raw = r'2020\Day10\test.txt'
raw2 = r'2020\Day10\test2.txt'

#########
# Start #
#########

def give_answer1(my_tuple):
    return my_tuple[0]*my_tuple[1]

def split_list(my_list,i):
    return my_list[:i], my_list[i:]

def give_combinations(my_list): # gotta implement my own
    n = len(my_list)  
    final = []  
    for i in range(n-1):
        if my_list[i+1]-my_list[i]==3:
            a, b = split_list(my_list,i)
            final.append(a)
            give_combinations(b) # 995 calls redo
    return final    


def check_valid_numbers(my_list):
    ones = 0
    threes = 1
    if my_list[0] == 1:
        ones += 1
    elif my_list[0] == 3:
        threes += 1        
    for i in range(len(my_list)-1):
        if my_list[i+1] - my_list[i]==1:
            ones+=1
        if my_list[i+1] - my_list[i]==3:
            threes+=1
    return ones, threes


def main(raw,part):    
    input = tools.read_input(raw)    
    # convert all elements to int
    input = list(set([int(i) for i in input if i]))
    
    if part == 1:
        return give_answer1(check_valid_numbers(input))
    elif part == 2:
        pass
    else:
        raise ValueError("part must be 1 or 2, instead of: " + part)
    

def run_tests():                  
    assert main(test_raw,1) == 220
    #assert main(test_raw,2) == 62
    # solutions
    assert main(input_raw,1) == 2059
    #assert main(input_raw,2) == 5407707


if __name__ == '__main__':
    run_tests()
    answer1 = main(input_raw,1)    
    #answer2 = main(input_raw,2)    
    print("Answer part1: {}".format(answer1))        
    #print("Answer part2: {}".format(answer2))    
