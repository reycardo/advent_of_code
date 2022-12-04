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

class Assignments():

    def __init__(self, input: list):
        self.input = input
        self.contained = self.count_contained()
        self.overlaped = self.count_overlaped()
        self.answer1 = self.sum_contained()
        self.answer2 = self.answer1 + self.sum_overlaped()

    def get_contained(self, section):
        # first contained in second -- 456 , 34567
        if section[0][0] >= section[1][0]:
            if section[0][1] <= section[1][1]:
                return len(range(section[0][0],section[0][1]+1))                    
        # second contained in first -- 34567 , 456
        if section[0][0] <= section[1][0]:
            if section[0][1] >= section[1][1]:
                return len(range(section[1][0],section[1][1]+1))
        return 0

    def get_overlaped(self, section):
        # first overlaps second -- 123 , 234
        if section[0][1] >= section[1][0] and section[1][1] >= section[0][0]:
            return len(range(section[1][0],section[0][1]+1))
        # second overlaps in first -- 234 , 123
        if section[1][1] >= section[0][0] and section[0][0] >= section[1][1]:
            return len(range(section[0][0],section[1][1]+1))
        return 0        
    
    def count_overlaped(self):
        overlaped = [self.get_overlaped(section) if contained == 0 else 0 for section,contained in zip(self.input, self.contained)]
        return overlaped

    def count_contained(self):
        contained = [self.get_contained(section) for section in self.input]
        return contained

    def sum_contained(self):
        return sum(x > 0 for x in self.contained)

    def sum_overlaped(self):
        return sum(x > 0 for x in self.overlaped)

def parse_input(input):
    return [[[int(z) for z in x.split('-')] for x in i.split(',')] for i in input]

def main(raw,part):
    input = tools.read_input(raw)
    input = parse_input(input)
    assignments = Assignments(input)        
    if part == 1:
        return assignments.answer1
    elif part == 2:        
        return assignments.answer2
    else:
        raise ValueError("part must be 1 or 2, instead of: " + part)


def run_tests():
    assert main(test_raw,1) == 2
    assert main(test_raw,2) == 4
    # solutions
    assert main(input_raw,1) == 540
    #assert main(input_raw,2) == 2641


if __name__ == '__main__':
    run_tests()
    answer1 = main(input_raw,1)
    answer2 = main(input_raw,2)
    print("Answer part1: {}".format(answer1))
    print("Answer part2: {}".format(answer2))