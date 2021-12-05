import os
import sys
sys.path.insert(0, './')
from utils import tools
import numpy as np

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
input_raw = os.path.join(__location__,'input.txt')
test_raw = os.path.join(__location__,'test.txt')

#########
# Start #
#########

def parse_input(input):                     
    draws = input[0].split(',')

    filter_object = filter(lambda x: x != '', input)
    input = list(filter_object)        
    boards = []
    for i in range(int((len(input)-1)/5)):
        boards.append(input[i*5+1:i*5+6])    
    boards = [[row.strip().split() for row in board] for board in boards]
    m_boards = [np.matrix(ele).astype(int) for ele in boards]
    return draws, m_boards

def bingo_draw(draws, m_boards):    
    winners = []
    checks = [] # total of -1 in winning boards
    last_draws = []
    cleared = []
    for draw in draws:        
        for index, m_board in enumerate(m_boards):
            if index not in cleared:                
                if np.isin(draw,m_board):
                    pos = np.where(np.array(m_board) == int(draw)) # row and column of draw in board
                    m_board[int(pos[0]), int(pos[1])] = -1 # if draw hits number gets replaced by -1
                    if check_bingo(m_board):
                        winners.append(m_board) # append board to winners
                        checks.append(np.count_nonzero(m_board < 0)) # append total of numbers hit to checks
                        cleared.append(index)
                        last_draws.append(draw) 
    return winners, last_draws, checks                            

def check_bingo(m_board):   
    if -5 in m_board.sum(axis=0) or -5 in m_board.sum(axis=1):
        return True
    else:
        return False

def main(raw,part):
    # read inputs from file
    input = tools.read_input(raw)
        
    draws , m_boards = parse_input(input)
    winners, last_draws, checks = bingo_draw(draws, m_boards)
    if part == 1:                
        return (winners[0].sum() + checks[0]) * int(last_draws[0]) # sum of remaining digits in winning board * last draw
    elif part == 2:        
        return (winners[-1].sum() + checks[-1]) * int(last_draws[-1]) # sum of remaining digits in losing board * last draw
    else:
        raise ValueError("part must be 1 or 2, instead of: " + part)


def run_tests():
    assert main(test_raw,1) == 4512
    assert main(test_raw,2) == 1924
    # solutions
    assert main(input_raw,1) == 11536
    assert main(input_raw,2) == 1284
    

    
if __name__ == '__main__':
    run_tests()
    answer1 = main(input_raw,1)
    answer2 = main(input_raw,2)    
    print("Answer part1: {}".format(answer1))
    print("Answer part2: {}".format(answer2))