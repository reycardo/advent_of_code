from __future__ import annotations
from utils.tools import get_txt_files, read_input, timing_decorator
from utils.colors import magenta_color, reset_color
from typing import List, Tuple
import networkx as nx
import numpy as np
from itertools import combinations


files = get_txt_files(__file__)
#########
# Start #
#########


class Puzzle:
    def __init__(self, text_input):
        self.input: List[str] = text_input
        self.input_parsed = self.parse_input()
        self.setup_graph()

    def parse_input(self):
        return [path.split("-") for path in self.input]

    def setup_graph(self):
        self.G = nx.Graph()
        self.G.add_edges_from(self.input_parsed)

    def find_sets_of_count(self, count: int):
        sets = set()
        for node, adjacents in self.G._adj.items():
            if node.startswith("t"):
                for combo in combinations(adjacents, count - 1):
                    if all(
                        combo[i] in self.G._adj[combo[j]]
                        for i in range(len(combo))
                        for j in range(i + 1, len(combo))
                    ):
                        sets.add(frozenset((node, *combo)))
        return sets

    def find_cliques(self):
        biggest_clique = max(nx.find_cliques(self.G), key=len)
        return biggest_clique

    def solve(self, part):
        if part == 1:
            sets_of_3 = self.find_sets_of_count(3)
            return len(sets_of_3)
        elif part == 2:
            biggest_clique = self.find_cliques()
            ordered_biggest_clique = ",".join((sorted(biggest_clique)))
            return ordered_biggest_clique


@timing_decorator
def main(raw, part):
    text_input = read_input(raw)
    input_parsed = [i if i else "" for i in text_input]
    puzzle = Puzzle(input_parsed)
    return puzzle.solve(part)


def run_tests():
    print(f"\nRunning Tests:")
    assert main(raw=files["test"], part=1) == 7
    assert main(raw=files["test"], part=2) == "co,de,ka,ta"

    # solutions
    print(f"\nRunning Solutions:")
    assert main(raw=files["input"], part=1) == 1476
    # assert main(raw=files["input"], part=2) == 662726441391898


def solve():
    print(f"\nSolving:")
    answer1 = main(raw=files["input"], part=1)
    print(f"Answer part1: {magenta_color}{answer1}{reset_color}")
    answer2 = main(raw=files["input"], part=2)
    print(f"Answer part2: {magenta_color}{answer2}{reset_color}")


if __name__ == "__main__":
    run_tests()
    solve()
