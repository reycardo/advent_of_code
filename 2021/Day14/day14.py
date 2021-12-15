import os
import sys
sys.path.insert(0, './')
from utils import tools
from collections import Counter
from collections import defaultdict

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
        self.letter_count, self.pair_count = self.parse_pairs(self.poli)

    # Added for Pt2
    def parse_pairs(self,poli,n=2):
        self.pair_count = defaultdict(int)
        self.letter_count = defaultdict(int)
        pairs = [poli[j: j + n] for j in range(len(poli) - n + 1)]
        for pair in pairs:
            self.pair_count[pair] += 1
        for letter in self.poli:
            self.letter_count[letter] += 1        
        return self.letter_count, self.pair_count

    # Added for Pt2
    def poli_counter(self,steps):
        for _ in range(steps):
            for pair, count in self.pair_count.copy().items(): # if pair = "CB" and count = 5 means there are 5 CB's across the poli
                added_letter = self.rules[pair] # fetch the rule for pair "CB" to added_letter = "H"
                
                # remove all pairs of "CB" from polimer since the new rule puts a "H" in the middle of "CB"
                # removing all "CB" entries in the polymer
                self.pair_count[pair] -= count
                self.pair_count[pair[0] + added_letter] += count # Add the amount of counts = 5 to the new pair generated "CH"
                self.pair_count[added_letter + pair[1]] += count # Add the amount of counts = 5 to the new pair generated "HB"
                self.letter_count[added_letter] += count # There are now 5 more entries of H in the polymer
                self.step += 1 # Increment number of steps
        return max(self.letter_count.values()) - min(self.letter_count.values())

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
            elif self.step == 13:
                print(f"Calm down with your exponential increments boy we are dealing with arrays of lenght: {len(self.poli)}")
                print(f"Stoped at step: {self.step}")
                break
        return self.poli

    def count_answer(self):
        counts = Counter(self.poli)
        most = counts.most_common(1)
        least = counts.most_common()[:-2:-1]
        return most[0][1]-least[0][1]

def parse_input(input):
    template = [x for x in input if "->" not in x and x][0]
    rules = dict(x.split(" -> ") for x in input if "->" in x and x)
    return template, rules

def main(raw,part):    
    input = tools.read_input(raw)    
    template, rules = parse_input(input)        
    if part == 1:
        polymer = Polymer(template,rules)
        polymer.poli = polymer.loop_steps(steps=10)
        return polymer.count_answer()
    elif part == 2:        
        polymer = Polymer(template,rules)        
        return polymer.poli_counter(steps=40)
    else:
        raise ValueError("part must be 1 or 2, instead of: " + part)


def run_tests():    
    assert main(test_raw,1) == 1588
    assert main(test_raw,2) == 2188189693529
    
    # solutions
    assert main(input_raw,1) == 2975
    assert main(input_raw,2) == 3015383850689
    

if __name__ == '__main__':
    run_tests()
    answer1 = main(input_raw,1)
    answer2 = main(input_raw,2)    
    print("Answer part1: {}".format(answer1))
    print("Answer part2: {}".format(answer2))