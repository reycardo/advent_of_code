import os
import sys
from re import findall
sys.path.insert(0, './')
from utils import tools

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
input_raw = os.path.join(__location__,'input.txt')
test_raw = os.path.join(__location__,'test.txt')

#########
# Start #
#########

class Crates():

    def __init__(self, input: list):
        self.input = input
        self.stack_count = int(self.input[-1][-2])
        self.crate_stacks = {key: [] for key in range(1,self.stack_count+1)}
        self.parse_crates()
        self.clean_dict()

    def parse_row(self, string: str):        
        for i in range(self.stack_count):
            self.crate_stacks[i+1].append(string[4*i:4*i+3])        
    
    def parse_crates(self):
        for string in self.input[:-1]:
            self.parse_row(string)

    def replace_excess(self, val: str):
        replaced = [ele.replace('[','').replace(']','').strip() for ele in val]
        replaced.reverse()        
        return [ele for ele in replaced if ele]

    def clean_dict(self):
        self.crate_stacks = {k: self.replace_excess(v) for k, v in self.crate_stacks.items()}        
    

class Procedure():

    def __init__(self, input: list, crates: dict):
        self.input = input
        self.parsed_procedure = self.parse_procedure()
        self.crates = crates

    def parse_procedure(self):
        return [[int(digit) for digit in findall(r'\d+',procedure)] for procedure in self.input]

    def do_procedure(self, proccess,part):
        # get orders
        amount, from_stack, to_stack = proccess[0], proccess[1], proccess[2]
        to_move = self.crates[from_stack][-amount:]
        del self.crates[from_stack][-amount:]
        if len(to_move) > 1:
            if part == 1:
                to_move.reverse()            
        self.crates[to_stack].extend(to_move)

    def get_top_crates(self):
        return ''.join([stack[-1] for stack in self.crates.values()])

    def run(self, part):
        [self.do_procedure(process, part) for process in self.parsed_procedure]   


def read_input(file,sep: str = '\n'):
    with open(file, "r") as tf:        
        return tf.read().split(sep)

def parse_input(input: list):
    # split setup from procedure
    index = input.index('')
    setup, procedure = input[:index], input[index + 1:]            
    return setup, procedure


def main(raw,part):
    input = read_input(raw)    
    setup, procedure = parse_input(input)        
    crates = Crates(input=setup)
    procedure = Procedure(input=procedure, crates=crates.crate_stacks)
    if part == 1:        
        procedure.run(part=1)
        return procedure.get_top_crates()
    elif part == 2:
        procedure.run(part=2)
        return procedure.get_top_crates()
    else:
        raise ValueError("part must be 1 or 2, instead of: " + part)


def run_tests():
    assert main(test_raw,1) == 'CMZ'
    assert main(test_raw,2) == 'MCD'
    # solutions
    assert main(input_raw,1) == 'TLFGBZHCN'
    assert main(input_raw,2) == 'QRQFHFWCL'


if __name__ == '__main__':
    run_tests()
    answer1 = main(input_raw,1)
    answer2 = main(input_raw,2)
    print("Answer part1: {}".format(answer1))
    print("Answer part2: {}".format(answer2))