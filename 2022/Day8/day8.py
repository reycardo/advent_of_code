import os
import sys
sys.path.insert(0, './')
from utils import tools
import numpy as np
from typing_1 import Tuple

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
input_raw = os.path.join(__location__,'input.txt')
test_raw = os.path.join(__location__,'test.txt')

#########
# Start #
#########

class Tree_Grid():

    def __init__(self, input: list):
        self.input = input
        self.matrix, self.matrix_t = self.parse_input()
        self.visibles = self.check_visible()
        self.answer1 = sum(self.visibles)
        self.answer2 = max(self.get_scenic_scores())

    def parse_input(self) -> Tuple[np.array, np.array]:
        matrix = np.array([[int(char) for char in ele] for ele in self.input])
        return (matrix, matrix.transpose())

    def get_left(self, x, y):
        return self.matrix[y][:x]

    def get_right(self, x, y):
        return self.matrix[y][x+1:]
    
    def get_top(self, x, y):
        return self.matrix_t[x][:y]

    def get_bot(self, x, y):
        return self.matrix_t[x][y+1:]

    def is_visible(self, x, y):
        val = self.matrix[y][x]
        return (all(val > tree for tree in self.get_left(x,y))
                or
                all(val > tree for tree in self.get_right(x,y))
                or
                all(val > tree for tree in self.get_top(x,y))
                or
                all(val > tree for tree in self.get_bot(x,y)))
            
    def check_visible(self):        
        return [self.is_visible(x,y) for (x, y), val in np.ndenumerate(self.matrix)]

    def get_view(self, x, y, v, dir):
        if dir == "left":
            look_list = list(reversed(self.get_left(x,y)))
        elif dir == "right":
            look_list = self.get_right(x,y)
        elif dir == "top":
            look_list = list(reversed(self.get_top(x,y)))
        elif dir == "bot":
            look_list = self.get_bot(x,y)
        res = 0
        for tree in look_list:
            res += 1
            if tree < v:
                continue
            else:                
                break
        return res

    def check_scenic_score(self, x, y):
        val = self.matrix[y][x]
        left_score = self.get_view(x,y,v=val,dir="left")
        right_score = self.get_view(x,y,v=val,dir="right")
        top_score = self.get_view(x,y,v=val,dir="top")
        bot_score = self.get_view(x,y,v=val,dir="bot")

        return left_score * right_score * top_score * bot_score

    
    def get_scenic_scores(self):        
        return [self.check_scenic_score(x,y) for (x, y), val in np.ndenumerate(self.matrix)]

def main(raw,part):
    input = tools.read_input(raw)
    tree_grid = Tree_Grid(input=input)    
    if part == 1:
        return tree_grid.answer1
    elif part == 2:
        return tree_grid.answer2
    else:
        raise ValueError("part must be 1 or 2, instead of: " + part)


def run_tests():
    assert main(test_raw,1) == 21
    assert main(test_raw,2) == 8

    # solutions
    assert main(input_raw,1) == 1785
    assert main(input_raw,2) == 345168


if __name__ == '__main__':
    run_tests()
    answer1 = main(input_raw,1)
    answer2 = main(input_raw,2)
    print("Answer part1: {}".format(answer1))
    print("Answer part2: {}".format(answer2))