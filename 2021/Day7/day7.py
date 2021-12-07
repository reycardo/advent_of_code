import os
import sys
sys.path.insert(0, './')
from utils import tools
from collections import Counter

raw = r'2021\Day7\test.txt'

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
input_raw = os.path.join(__location__,'input.txt')
test_raw = os.path.join(__location__,'test.txt')

#########
# Start #
#########

def parse_input(input):            
    return [list(map(int,line.split(','))) for line in input][0]


def new_days(input,days,max_int_timer):
    new_babies = []
    for day in range(days):
        input = [fish - 1 if fish > 0 else 6 for fish in input] # new day
        input = input + new_babies
        new_babies = [max_int_timer] * input.count(0)
    return len(input)

def calc_fish(input,days,max_int_timer):
    counts = Counter(input)
    fish_counter = [0] * (max_int_timer + 1) # fish_counter[x] represents the number of fishes with internal time x
    for i in range(max_int_timer + 1):
        fish_counter[i] = counts[i]
    for day in range(days):
        new_babies = fish_counter.pop(0) # transforms 0s into 6s
        fish_counter[6] += new_babies    # transforms 0s into 6s
        fish_counter.append(new_babies)  # pop and append shifts everyone one position (simulates a new day)
    return sum(fish_counter)

def main(raw,part):
    # read inputs from file
    input = tools.read_input(raw)
    input = parse_input(input)
    if part == 1:                                
        return new_days(input,80,8)
    elif part == 2:        
        return calc_fish(input,256,8)
    else:
        raise ValueError("part must be 1 or 2, instead of: " + part)


def run_tests():
    assert main(test_raw,1) == 5934
    assert main(test_raw,2) == 26984457539
    # solutions
    assert main(input_raw,1) == 362639
    assert main(input_raw,2) == 1639854996917
    

    
if __name__ == '__main__':
    run_tests()
    answer1 = main(input_raw,1)
    answer2 = main(input_raw,2)    
    print("Answer part1: {}".format(answer1))
    print("Answer part2: {}".format(answer2))