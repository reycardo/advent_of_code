import os
import sys
sys.path.insert(0, './')
from utils import tools
import networkx as nx


raw = r'2021\Day12\test.txt'

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
input_raw = os.path.join(__location__,'input.txt')
test_raw = os.path.join(__location__,'test.txt')
test_raw2 = os.path.join(__location__,'test2.txt')
test_raw3 = os.path.join(__location__,'test3.txt')

#########
# Start #
#########

def parse_input(input):
    return [path.split('-') for path in input]    


def make_graph(edges):
    G = nx.Graph()    
    G.add_edges_from(edges)
    nx.set_node_attributes(G, { node: ('small' if node.islower() else 'big') for node in G.nodes }, "size")
    return G


def visit(G, part, node='start', visited=set(), double = False):
    if node == 'end': # hits end add 1 to sum
        return 1
    if node in visited:
        if part == 1:
            return 0  # hits a visited stops recursion without adding
        elif part == 2:
            if double:
                return 0 # has been visited and a double was discovered already
            else:
                if node == 'start': # start cannot be a double
                    return 0
                double = True # continues recursion but a double has been found for the 1st time
        else:
            raise ValueError("part must be 1 or 2, instead of: " + part)                        
    visited_copy = visited.copy() # do not change original visited
    if G.nodes[node]['size'] == 'small': # if the node is a small cave
        visited_copy.add(node) 
    sum = 0
    for child in G[node]: # get all paths available from that node (the childs)
        sum += visit(G,part,child,visited_copy,double) # recursively visits childs
    return sum

def main(raw,part):    
    input = tools.read_input(raw)    
    edges = parse_input(input)
    G = make_graph(edges)
    if part == 1:
        return visit(G,part=1)
    elif part == 2:
        return visit(G,part=2)
    else:
        raise ValueError("part must be 1 or 2, instead of: " + part)


def run_tests():
    assert main(test_raw,1) == 10
    assert main(test_raw2,1) == 19
    assert main(test_raw3,1) == 226
    
    assert main(test_raw,2) == 36
    assert main(test_raw2,2) == 103
    assert main(test_raw3,2) == 3509
    # solutions
    assert main(input_raw,1) == 3708
    assert main(input_raw,2) == 93858
    
    
if __name__ == '__main__':
    run_tests()
    answer1 = main(input_raw,1)
    answer2 = main(input_raw,2)    
    print("Answer part1: {}".format(answer1))
    print("Answer part2: {}".format(answer2))