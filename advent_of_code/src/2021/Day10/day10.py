import os
import sys
sys.path.insert(0, './')
from utils import tools

raw = r'2021\Day10\test.txt'

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
input_raw = os.path.join(__location__,'input.txt')
test_raw = os.path.join(__location__,'test.txt')

#########
# Start #
#########


illegals = [['{)','[)','<)'],['{]','(]','<]'],['(}','[}','<}'],['{>','(>','[>']]

def remove_valid(entry):
    has = True
    while has:
        b4=len(entry)
        entry = entry.replace('()','').replace(r'[]','').replace(r'<>','').replace(r'{}','')
        if b4 == len(entry):
            has = False
    return entry

def search_pos(entry,illegal):
    pos = []
    for item in illegal:
        if item in entry:            
            pos.append(entry.find(item))
    return min(pos)

def find_corrupted(input):
    i_points = [
    0, # )
    0, # ]
    0, # }
    0  # >
    ]
    for entry in input:
        corrupted = False
        entry = remove_valid(entry)        
        mins = [float('inf'),float('inf'),float('inf'),float('inf')]
        for num, illegal in enumerate(illegals):
            if any(item in entry for item in illegal):
                mins[num] = search_pos(entry,illegal)
                corrupted = True
        if corrupted:
            for i in range(len(mins)):
                if mins[i] == min(mins):
                    i_points[i] += 1
               
    return i_points[0] * 3 + i_points[1] * 57 + i_points[2] * 1197 + i_points[3] * 25137

# PT2
def is_corrupted(entry):    
    for illegal in illegals:
        if any(item in entry for item in illegal):
            return True
    return False

def complete_sintax(input):
    auto_correct = []
    for entry in input:
        entry = remove_valid(entry)
        if not is_corrupted(entry):
            auto_correct.append(entry[::-1].replace('(',')').replace(r'[',']').replace(r'<','>').replace(r'{','}'))
    return auto_correct

def convert_2_score(auto_correct):
    word_score = [entry.replace(r')','1').replace(r']','2').replace(r'}','3').replace(r'>','4') for entry in auto_correct]
    score_list = []
    for word in word_score:
        score = 0
        for char in word:
            score = score * 5 + int(char)
        score_list.append(score)            
    return sorted(score_list)[int(len(score_list) / 2)]

def main(raw,part):
    # read inputs from file
    input = tools.read_input(raw)

    if part == 1:
        return find_corrupted(input)
    elif part == 2:        
        auto_correct = complete_sintax(input)        
        return convert_2_score(auto_correct)
    else:
        raise ValueError("part must be 1 or 2, instead of: " + str(part))


def run_tests():
    assert main(test_raw,1) == 26397
    assert main(test_raw,2) == 288957
    # solutions
    assert main(input_raw,1) == 316851
    assert main(input_raw,2) == 2182912364
    
    
if __name__ == '__main__':
    run_tests()
    answer1 = main(input_raw,1)
    answer2 = main(input_raw,2)    
    print("Answer part1: {}".format(answer1))
    print("Answer part2: {}".format(answer2))