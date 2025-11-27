import os
import sys
import copy
sys.path.insert(0, './')
from utils import tools

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
input_raw = os.path.join(__location__,'input.txt')
test_raw = os.path.join(__location__,'test.txt')

# For interactive testing
raw = r'2020\Day8\test.txt'

#########
# Start #
#########

def preprocess(instruction):
    instruction = instruction.split()
    action = instruction[0]
    arg = int(instruction[1])
    return [action, arg]


def acc(instructions,accumulator,i):
    accumulator += instructions[i][1]
    return accumulator, i+1


def jmp(instructions,accumulator,i):    
    return accumulator, i+instructions[i][1]


def nop(accumulator,i):    
    return accumulator, i+1


def find_nop_jmp(instructions):    
    return [i for i, x in enumerate(instructions) if x[0] == "jmp" or x[0] == "nop"]


def change_nop_jmp(instructions,i):
    if instructions[i][0] == 'jmp':
        instructions[i][0] = 'nop'
    elif instructions[i][0] == 'nop':
        instructions[i][0] = 'jmp'
    else:
        raise ValueError("instruction had to be either jmp or nop and was: " + instructions[i][0])
    return instructions

def perf_action(instructions, i = 0, accumulator = 0, ran = []):
    while check_if_dup(i,ran):
        if instructions[i][0] == 'acc':                        
            ran.append(i)
            accumulator, i = acc(instructions,accumulator,i)
        elif instructions[i][0] == 'jmp':
            ran.append(i)
            accumulator, i = jmp(instructions,accumulator,i)            
        elif instructions[i][0] == 'nop':
            ran.append(i)
            accumulator, i = nop(accumulator,i)
        if i == len(instructions):
            break
    return accumulator , i
    

def check_if_dup(i, ran = []):
    # checks if instruction already ran
    if i in ran:
        return False
    else:
        return True

def main(raw,part):    
    input = tools.read_input(raw)
    instructions = [preprocess(instruction) for instruction in input]
    if part == 1:        
        accumulator , i = perf_action(instructions, 0, 0, [])
        return accumulator
    elif part == 2:
        nops_jmps = find_nop_jmp(instructions)
        for i in nops_jmps:
            changed_instructions = copy.deepcopy(instructions)
            changed_instructions = change_nop_jmp(changed_instructions, i)
            accumulator ,stopped = perf_action(changed_instructions, 0, 0, [])
            if stopped == len(changed_instructions):
                break
        return accumulator
    else:
        raise ValueError("part must be 1 or 2, instead of: " + part)
    

def run_tests():                  
    assert main(test_raw,1) == 5
    assert main(test_raw,2) == 8
    # solutions
    assert main(input_raw,1) == 1744
    assert main(input_raw,2) == 1174



if __name__ == '__main__':
    run_tests()
    answer1 = main(input_raw,1)    
    answer2 = main(input_raw,2)    
    print("Answer part1: {}".format(answer1))        
    print("Answer part2: {}".format(answer2))    
