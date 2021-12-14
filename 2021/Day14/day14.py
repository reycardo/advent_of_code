import os
import sys
sys.path.insert(0, './')
from utils import tools
from collections import Counter

raw = r'2021\Day14\test.txt'

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
input_raw = os.path.join(__location__,'input.txt')
test_raw = os.path.join(__location__,'test.txt')

#########
# Start #
#########

class Polymer():
    def __init__(self,template,rules):
        self.poli = template
        self.step = 0
        self.rules = rules

    def apply_step(self,poli,n=2):        
        pairs = [poli[j: j + n] for j in range(len(poli) - n + 1)]
        for count, pair in enumerate(pairs, start=0):
            if pair in self.rules.keys():
                poli = poli[:2*count+1] + self.rules[pair] + poli[2*count+1:]
        return poli
                

    def loop_steps(self,steps):        
        while True:            
            self.poli = self.apply_step(self.poli)
            self.step += 1
            if self.step == steps:
                break
        return self.poli

    def count_answer(self):
        counts = Counter(self.poli)
        most= counts.most_common(1)
        least =counts.most_common()[:-2:-1]
        return most[0][1]-least[0][1]

def parse_input(input):
    template = [x for x in input if "->" not in x and x][0]
    rules = [x.split(" -> ") for x in input if "->" in x and x]    
    rules_dict = {}
    for rule in rules:
        rules_dict[rule[0]] = rule[1]
    return template, rules_dict

def main(raw,part):    
    input = tools.read_input(raw)    
    template, rules = parse_input(input)        
    if part == 1:
        polymer = Polymer(template,rules)
        polymer.poli = polymer.loop_steps(steps=10)
        return polymer.count_answer()
    elif part == 2:
        polymer = Polymer(template,rules)        
        polymer.poli = polymer.loop_steps(steps=40)
        return polymer.count_answer()
    else:
        raise ValueError("part must be 1 or 2, instead of: " + part)


def run_tests():    
    assert main(test_raw,1) == 1588
    assert main(test_raw,2) == 2188189693529
    
    # solutions
    #assert main(input_raw,1) == 807
    #assert main(input_raw,2) == LGHEGUEJ
    
if __name__ == '__main__':
    run_tests()
    answer1 = main(input_raw,1)
    answer2 = main(input_raw,2)    
    print("Answer part1: {}".format(answer1))
    print("Answer part2: {}".format(answer2))