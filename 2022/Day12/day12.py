import sys
sys.path.insert(0, './')
import os
from utils import tools
import numpy as np
import networkx as nx
from itertools import product

__location__ = os.path.realpath(os.path.join(
    os.getcwd(), os.path.dirname(__file__)))
input_raw = os.path.join(__location__, 'input.txt')
test_raw = os.path.join(__location__, 'test.txt')

#########
# Start #
#########

class Hill_Climb():

    def __init__(self, input: list[str]):
        self.input = input
        self.matrix = self.parse_input()
        self.start, self.end = self.get_start_end_pos()
        self.change_start_end_val()                

    def parse_input(self) -> np.ndarray:
        matrix = np.array([[ord(char) - 96 for char in ele] for ele in self.input])
        return matrix

    def get_start_end_pos(self):
        return np.where(self.matrix == -13), np.where(self.matrix == -27)
    
    def change_start_end_val(self):
        self.matrix[self.start] = 1
        self.matrix[self.end] = 26

    def make_graph(self, edges):
        G = nx.DiGraph()    
        G.add_edges_from(edges)
        #nx.set_node_attributes(G, { node: (self.matrix[node]) for node in G.nodes }, "weight")
        #nx.set_edge_attributes(G, { edge: self.matrix[edge[1]] for edge in G.edges() }, "weight")
        #nx.set_node_attributes(G, { node: 1 for node in G.nodes }, "weight")
        nx.set_edge_attributes(G, { edge: 1 for edge in G.edges() }, "weight")        
        return G

    def is_inside(self, coords: tuple):
        if all((coords[0] >= 0, coords[0] < self.matrix.shape[0], coords[1] >= 0, coords[1] < self.matrix.shape[1])):
            return True
        else:
            return False

    def get_adjacents(self, coords: tuple):
        for r_offset, c_offset in product(range(-1, 2), range(-1, 2)): # get all offsets
            if not (r_offset == 0 and c_offset == 0) and (c_offset == 0 or r_offset == 0): # if not own and not diagonal
                adjacent = (coords[0] + r_offset, coords[1] + c_offset)
                if self.is_inside(adjacent): 
                    yield adjacent

    def get_paths(self):    
        path_list = []
        for row in range(self.matrix.shape[0]):
            for col in range(self.matrix.shape[1]):
                edges = self.get_adjacents((row,col))
                for end_path in edges:
                    if self.matrix[(row,col)] + 1 >= self.matrix[end_path]:
                        path = ((row,col),end_path)
                        path_list.append(path)
        return path_list


    def get_possible_starts(self):
        return list(zip(*np.where(self.matrix == 1)))

    def run(self, part):
        edge_list = self.get_paths()
        self.G = self.make_graph(edge_list)
        if part == 1:
            self.shortest_path = nx.single_source_dijkstra(
                self.G, 
                source=(self.start[0][0],self.start[1][0]),
                target=(self.end[0][0],self.end[1][0]),
                weight='weight'
            )
        else:
            starts_list = self.get_possible_starts()
            self.shortest_path = []
            for start in starts_list:
                try:
                    self.shortest_path.append(nx.single_source_dijkstra(
                        self.G, 
                        source=start,
                        target=(self.end[0][0],self.end[1][0]),
                        weight='weight'
                    ))
                except nx.exception.NetworkXNoPath:
                    pass

    def get_answer(self, part):
        if part == 1:
            return self.shortest_path[0]
        else:
            return min([vals[0] for vals in self.shortest_path])

def main(raw, part):
    input = tools.read_input(raw)
    hill_climb = Hill_Climb(input=input)     
    if part in (1,2):      
        hill_climb.run(part)  
        return hill_climb.get_answer(part)
    else:
        raise ValueError("part must be 1 or 2, instead of: " + part)


def run_tests():
    assert main(test_raw, 1) == 31
    assert main(test_raw, 2) == 29

    # solutions
    assert main(input_raw, 1) == 481
    #assert main(input_raw, 2) == 11614682178


if __name__ == '__main__':
    run_tests()
    answer1 = main(input_raw, 1)
    answer2 = main(input_raw, 2)
    print("Answer part1: {}".format(answer1))
    print("Answer part2: {}".format(answer2))
