import os
import sys
sys.path.insert(0, './')
from utils import tools
from itertools import groupby

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
input_raw = os.path.join(__location__,'input.txt')
test_raw = os.path.join(__location__,'test.txt')

#########
# Start #
#########

class Elf_Calories():  

    def __init__(self, input: list):
        self.input = input
        self.elf_calorie_dict = self.get_elf_dict()
        self.elf_count = len(self.elf_calorie_dict)        

    def get_elf_dict(self):                
        d = {elf: list(sub[1]) for elf, sub in enumerate(groupby(self.input, key = bool)) if sub[0]}  # groups into an enumerated dict if key is not ''
        return {k:(v,sum(v)) for k,v in d.items()}  # returns dict where key is elf number, v is list of elf calories, sum(v) is total cals elf has
    
    def get_max(self,number):
        # sorts descending, gets top number
        return sum(n for _, n in sorted(self.elf_calorie_dict.values(), key=lambda t: t[1], reverse=True)[:number])
        

def main(raw,part):    
    input = tools.read_input(raw)
    input = [int(i) if i else '' for i in input]
    elf_cals = Elf_Calories(input)    
    if part == 1:                
        return elf_cals.get_max(1)
    elif part == 2:        
        return elf_cals.get_max(3)
    else:
        raise ValueError("part must be 1 or 2, instead of: " + part)


def run_tests():
    assert main(test_raw,1) == 24000
    assert main(test_raw,2) == 45000
    # solutions
    assert main(input_raw,1) == 66616
    assert main(input_raw,2) == 199172
    
    
if __name__ == '__main__':
    run_tests()
    answer1 = main(input_raw,1)
    answer2 = main(input_raw,2)    
    print("Answer part1: {}".format(answer1))
    print("Answer part2: {}".format(answer2))