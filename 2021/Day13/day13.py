import os
import sys
sys.path.insert(0, './')
from utils import tools
from operator import itemgetter
import numpy as np
import pandas as pd

raw = r'2021\Day13\test.txt'

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
input_raw = os.path.join(__location__,'input.txt')
test_raw = os.path.join(__location__,'test.txt')
marta_input_raw = os.path.join(__location__,'input_day_13.txt')


#########
# Start #
#########

def parse_input(input):
    dots = [x for x in input if "," in x]
    folds = [x for x in input if "fold along " in x]
    folds = [(fold.split('=')[0][-1],int(fold.split('=')[1])) for fold in folds]
    return dots, folds

def dots_2_tuple(dots):            
    return [tuple(map(int, coords.split(','))) for coords in dots]

def make_sheet(dots):
    max_x = max(dots,key=itemgetter(0))[0]
    max_y = max(dots,key=itemgetter(1))[1]
    return np.zeros((max_y + 1,max_x + 1), dtype=int)

def add_dots2sheet(sheet,dots):
    for dot in dots:
        col,row = dot
        sheet[(row,col)] = 1
    return sheet

def fold_it(fold,sheet):
    if 'y' == fold[0]:
        base = sheet[:fold[1] , :]
        over = sheet[fold[1]+1: , :]
        fliped_over = np.flipud(over)
        while fliped_over.shape[1] < base.shape[1]:
            fliped_over = np.vstack(np.zeros(1,fliped_over.shape[0]),fliped_over)
        return np.where(base + fliped_over > 0, 1, 0)
    else:
        base = sheet[: , :fold[1]]
        over = sheet[: , fold[1]+1:]        
        fliped_over = np.fliplr(over)
        while fliped_over.shape[0] < base.shape[0]:
            fliped_over = np.hstack(np.zeros(fliped_over.shape[1],1),fliped_over)
        return np.where(base + fliped_over > 0, 1, 0)

class Paper():

    def __init__(self,sheet: np.matrix,dots: tuple, folds: list):
        self.dots = dots
        self.fold_count = 0
        self.to_fold = folds
        self.sheet = add_dots2sheet(sheet,dots)
       
    def fold_sheet(self,part):
        sheet = self.sheet.copy()
        for fold in self.to_fold:            
            sheet = fold_it(fold,sheet)            
            self.fold_count += 1
            if part==1 and self.fold_count == 1:
                break
        return sheet

def main(raw,part):    
    input = tools.read_input(raw)    
    dots, folds = parse_input(input)
    dots = dots_2_tuple(dots)
    sheet = make_sheet(dots)
    paper = Paper(sheet, dots, folds)
    if part == 1:
        new_sheet = paper.fold_sheet(part=1)
        return np.sum(new_sheet)
    elif part == 2:
        new_sheet = paper.fold_sheet(part=2)
        print(pd.DataFrame(new_sheet))
        pass
    else:
        raise ValueError("part must be 1 or 2, instead of: " + part)


def run_tests():    
    assert main(test_raw,1) == 17
    #assert main(test_raw,2) == 36
    
    # solutions
    #assert main(input_raw,1) == 807
    #assert main(input_raw,2) == LGHEGUEJ
    
if __name__ == '__main__':
    run_tests()
    #answer1 = main(input_raw,1)
    answer2 = main(marta_input_raw,2)    
    #print("Answer part1: {}".format(answer1))
    print("Answer part2: {}".format(answer2))


# [[  # #     # # #     #     #       # #   # # # #   # # #       # #       # #    ]
#  [#     #   #     #   #   #           #   #         #     #   #     #   #     #  ]
#  [#     #   # # #     # #             #   # # #     # # #     #         #        ]
#  [# # # #   #     #   #   #           #   #         #     #   #   # #   #        ]
#  [#     #   #     #   #   #     #     #   #         #     #   #     #   #     #  ]
#  [#     #   # # #     #     #     # #     #         # # #       # # #     # #    ]]    