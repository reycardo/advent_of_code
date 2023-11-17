import os
import sys
sys.path.insert(0, './')
from utils import tools

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
input_raw = os.path.join(__location__,'input.txt')
test_raw = os.path.join(__location__,'test.txt')
test_raw2 = os.path.join(__location__,'test2.txt')
test_raw3 = os.path.join(__location__,'test3.txt')
test_raw4 = os.path.join(__location__,'test4.txt')
test_raw5 = os.path.join(__location__,'test5.txt')

#########
# Start #
#########

class Buffer():

    def __init__(self, input: list):
        self.input = input
        self.input_parsed = input[0]
        _, self.answer1, _ = self.find_marker(4)
        _, self.answer2, _ = self.find_marker(14)

    def find_marker(self, number:int):
        found = False
        i=0
        while not found:
            if len(self.input_parsed[i:i+number]) == len(set(self.input_parsed[i:i+number])):
                found = True
                return self.input_parsed[i:i+number], i+number, self.input_parsed[:i+number]
            i+=1

def main(raw,part):
    input = tools.read_input(raw)    
    buffer = Buffer(input=input)
    if part == 1:        
        return buffer.answer1
    elif part == 2:
        return buffer.answer2
    else:
        raise ValueError("part must be 1 or 2, instead of: " + part)


def run_tests():
    assert main(test_raw,1) == 7
    assert main(test_raw2,1) == 5
    assert main(test_raw3,1) == 6
    assert main(test_raw4,1) == 10
    assert main(test_raw5,1) == 11

    assert main(test_raw,2) == 19
    assert main(test_raw2,2) == 23
    assert main(test_raw3,2) == 23
    assert main(test_raw4,2) == 29
    assert main(test_raw5,2) == 26
    # solutions
    assert main(input_raw,1) == 1134
    assert main(input_raw,2) == 2263


if __name__ == '__main__':
    run_tests()
    answer1 = main(input_raw,1)
    answer2 = main(input_raw,2)
    print("Answer part1: {}".format(answer1))
    print("Answer part2: {}".format(answer2))