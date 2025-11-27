import os
from advent_of_code.utils import tools
import numpy as np
from itertools import product
import networkx as nx

raw = r"2021\Day15\test.txt"

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
input_raw = os.path.join(__location__, "input.txt")
test_raw = os.path.join(__location__, "test.txt")

#########
# Start #
#########


def parse_input(input):
    return np.matrix([[int(digit) for digit in row] for row in input])


def enlarge_map(input):
    input += 1
    input[input == 10] = 1
    return input


# For PT2
def increment_tiles(input):
    big_map = input.copy()
    for _ in range(4):
        new_input = enlarge_map(input)
        big_map = np.concatenate((big_map, new_input), axis=0)
    biggest_map = big_map.copy()
    for _ in range(4):
        new_input = enlarge_map(biggest_map)
        big_map = np.concatenate((big_map, new_input), axis=1)
    return big_map


def make_graph(edges, state: np.matrix):
    G = nx.DiGraph()
    G.add_edges_from(edges)
    nx.set_node_attributes(G, {node: (state[node]) for node in G.nodes}, "weight")
    nx.set_edge_attributes(G, {edge: state[edge[1]] for edge in G.edges()}, "weight")
    return G


def is_inside(state: np.matrix, coords: tuple):
    if all(
        (
            coords[0] >= 0,
            coords[0] < state.shape[0],
            coords[1] >= 0,
            coords[1] < state.shape[1],
        )
    ):
        return True
    else:
        return False


def get_adjacents(state: np.matrix, coords: tuple):
    for r_offset, c_offset in product(range(-1, 2), range(-1, 2)):  # get all offsets
        if not (r_offset == 0 and c_offset == 0) and (
            c_offset == 0 or r_offset == 0
        ):  # if not own and not diagonal
            adjacent = (coords[0] + r_offset, coords[1] + c_offset)
            if is_inside(state, adjacent):
                yield adjacent


def get_paths(state: np.matrix):
    path_list = []
    for row in range(state.shape[0]):
        for col in range(state.shape[1]):
            edges = get_adjacents(state, (row, col))
            for end_path in edges:
                path = ((row, col), end_path)
                path_list.append(path)
    return path_list


def main(raw, part):
    input = tools.read_input(raw)
    input = parse_input(input)
    if part == 1:
        edge_list = get_paths(input)
        G = make_graph(edge_list, input)
        start = (0, 0)
        target = (input.shape[0] - 1, input.shape[1] - 1)
        shortest_path = nx.single_source_dijkstra(
            G, source=start, target=target, weight="weight"
        )
        # print(shortest_path)
        return shortest_path[0]
    elif part == 2:
        input = increment_tiles(input)
        edge_list = get_paths(input)
        G = make_graph(edge_list, input)
        start = (0, 0)
        target = (input.shape[0] - 1, input.shape[1] - 1)
        shortest_path = nx.single_source_dijkstra(
            G, source=start, target=target, weight="weight"
        )
        # print(shortest_path)
        return shortest_path[0]
    else:
        raise ValueError("part must be 1 or 2, instead of: " + part)


def run_tests():
    assert main(test_raw, 1) == 40
    assert main(test_raw, 2) == 315

    # solutions
    assert main(input_raw, 1) == 824
    assert main(input_raw, 2) == 3063


if __name__ == "__main__":
    run_tests()
    answer1 = main(input_raw, 1)
    answer2 = main(input_raw, 2)
    print("Answer part1: {}".format(answer1))
    print("Answer part2: {}".format(answer2))
