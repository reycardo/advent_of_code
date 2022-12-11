import sys
sys.path.insert(0, './')
import os
from utils import tools
import numpy as np

__location__ = os.path.realpath(os.path.join(
    os.getcwd(), os.path.dirname(__file__)))
input_raw = os.path.join(__location__, 'input.txt')
test_raw = os.path.join(__location__, 'test.txt')
test_raw_2 = os.path.join(__location__, 'test2.txt')
solution_pt2 = os.path.join(__location__, 'solution_pt2.txt')

#########
# Start #
#########

class Clock_circuit():

    def __init__(self, input: list[str]):
        self.input = input
        self.parsed = self.parse_input()
        self.cycle = 0
        self.X = 1
        self.crt = np.full((6,40),'.')
        self.current_pixel_x = 0
        self.current_pixel_y = 0
        self.str_cycles = [20+40*n for n in range(6)]
        self.screen_cycles = [40*n for n in range(6)]
        self.str_signal = {}        
        self.run()
        self.answer1 = sum(self.str_signal.values())
        self.answer2 = [''.join(element) for element in self.crt.tolist()]

    def parse_input(self):
        parsed = []
        for order in self.input:
            if order.startswith('addx'):
                splited = order.split(' ')
                parsed.append([splited[0], int(splited[1])])
            else:
                parsed.append([order])
        return parsed

    def increment_current_pixel(self):
        if self.cycle in self.screen_cycles:
            self.current_pixel_x = 0
            self.current_pixel_y += 1
        else:
            self.current_pixel_x += 1

    def increment_cycle(self):
        self.cycle += 1
        self.draw_pixel()
        self.increment_current_pixel()

    def do_addx(self, amount, n):
        for i in range(n):
            self.increment_cycle()
            self.get_strenght()
            if i == n-1:
                self.X += amount
            
    def do_noop(self):
        self.increment_cycle()
        self.get_strenght()

    def get_strenght(self):
        if self.cycle in self.str_cycles and self.cycle not in self.str_signal:
            self.str_signal[self.cycle] = self.cycle * self.X

    def do_cycle(self, instruction):        
        if instruction[0].startswith('addx'):            
            self.do_addx(instruction[1], 2)
        else:
            self.do_noop()

    def draw_pixel(self):
        # if sprite on top of drawing pixel then draw
        if self.current_pixel_x in [self.X - 1,self.X, self.X + 1]:
            self.crt[(self.current_pixel_y,self.current_pixel_x)] = '#'        

    def run(self):
        [self.do_cycle(instruction) for instruction in self.parsed]

def main(raw, part):
    input = tools.read_input(raw)
    circuit = Clock_circuit(input=input)
    if part == 1:
        return circuit.answer1
    elif part == 2:
        return circuit.answer2
    else:
        raise ValueError("part must be 1 or 2, instead of: " + part)


def run_tests():
    assert main(test_raw, 1) == 13140
    test2_expected = tools.read_input(test_raw_2)
    assert main(test_raw, 2) == test2_expected

    # solutions
    assert main(input_raw, 1) == 12880
    assert main(input_raw, 2) == tools.read_input(solution_pt2)


if __name__ == '__main__':
    run_tests()
    answer1 = main(input_raw, 1)
    answer2 = main(input_raw, 2)
    print("Answer part1: {}".format(answer1))
    print("Answer part2:")
    [print(string) for string in answer2]
    
