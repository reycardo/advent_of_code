import os
import sys

import networkx as nx

sys.path.insert(0, './')
from utils import tools

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
input_raw = os.path.join(__location__,'input.txt')
test_raw = os.path.join(__location__,'test.txt')
test_raw2 = os.path.join(__location__,'test2.txt')

# For interactive testing
raw = r'2020\Day7\input.txt'

#########
# Start #
#########

def parse_rule(rule):
    main_bag = [' '.join(rule.split(' ')[:2])]
    contains = ' '.join(rule.split(' ')[4:]).split(', ')
    if contains == ['no other bags.']:
        contains_each = []
    elif contains != ['no other bags.']:
        contains_each = [(int(x.split(' ')[0]),' '.join(x.split(' ')[1:3])) for x in contains]
    else:
        raise ValueError("You fucked up on contains: " + contains)    
    rule = dict(zip(main_bag, [contains_each]))
    weighted_edges = [main_bag+list(tup) for tup in contains_each if contains_each]
    order = [0, 2, 1]
    weighted_edges = [[weighted_edge[i] for i in order] for weighted_edge in weighted_edges if weighted_edges]
    return rule, weighted_edges

def count_bags(DG, start):
    total = 0
    for inside, num in dict(DG[start]).items():
        total += num['weight'] + num['weight'] * count_bags(DG, inside)
    return total


def bag_di_graph(weighted_edges):
    DG = nx.DiGraph()    
    DG.add_weighted_edges_from(weighted_edges)    
    return DG

def main(raw,part):
    # read inputs from file
    input = tools.read_input_new_line_sep(raw)    
    rules, weighted_edges = zip(*[parse_rule(rule) for rule in input])
    rules = {k: v for d in rules for k, v in d.items()}
    weighted_edges = [item for sublist in weighted_edges for item in sublist]    
    DG = bag_di_graph(weighted_edges)
    if part == 1:               
        return len(nx.algorithms.dag.ancestors(DG,'shiny gold'))
    elif part == 2:
        return count_bags(DG, 'shiny gold')
    else:
        raise ValueError("part must be 1 or 2, instead of: " + part)
    

def run_tests():        
    assert main(test_raw,1) == 4
    assert main(test_raw,2) == 32
    assert main(test_raw2,2) == 126


if __name__ == '__main__':
    run_tests()
    answer1 = main(input_raw,1)    
    answer2 = main(input_raw,2)    
    print("Answer part1: {}".format(answer1))        
    print("Answer part2: {}".format(answer2))    
