import math
from scipy.cluster.hierarchy import DisjointSet
import itertools
from advent_of_code.utils.tools import get_txt_files, read_input, timing_decorator
from advent_of_code.utils.colors import magenta_color, reset_color
from typing import NamedTuple

files = get_txt_files(__file__)
#########
# Start #
#########

class Junction(NamedTuple):
    x: int
    y: int
    z: int

class Puzzle:
    def __init__(self, text_input):
        self.input = text_input
        self.parse_input()
        self.connected_junctions = []

    def parse_input(self):        
        self.junctions = [Junction(*map(int, row.split(','))) for row in self.input]

    def connect_junctions(self, num_connections: int = None):        
        ds = DisjointSet(self.junctions)
        edges = [
            (math.dist(a, b), a, b)
            for a, b in itertools.combinations(self.junctions, 2)
        ]
        edges.sort()
        connections_made = 0
        for _, a, b in edges:
            if num_connections is not None and connections_made >= num_connections:
                break
            ds.merge(a, b)
            connections_made += 1
            if ds.n_subsets == 1:
                return a.x, b.x
        self.connected_junctions = ds.subsets()

    def solve(self, part, num_connections: int = None):
        if part == 1:
            self.connect_junctions(num_connections)
            largest_three = sorted([len(s) for s in self.connected_junctions], reverse=True)[:3]
            return math.prod(largest_three)
        if part == 2:
            a, b = self.connect_junctions()
            return a * b




@timing_decorator
def main(raw, part, num_connections=None):
    text_input = read_input(raw)
    input_parsed = [i if i else "" for i in text_input]
    puzzle = Puzzle(input_parsed)    
    return puzzle.solve(part, num_connections)


def run_tests():
    print("\nRunning Tests:")
    assert main(raw=files["test"], part=1, num_connections=10) == 40
    assert main(raw=files["test"], part=2) == 25272

    # solutions
    print("\nRunning Solutions:")
    assert main(raw=files["input"], part=1, num_connections=1000) == 352584
    assert main(raw=files["input"], part=2) == 9617397716


def solve():
    print("\nSolving:")
    answer1 = main(raw=files["input"], part=1, num_connections=1000)
    print(f"Answer part1: {magenta_color}{answer1}{reset_color}")
    answer2 = main(raw=files["input"], part=2)
    print(f"Answer part2: {magenta_color}{answer2}{reset_color}")


if __name__ == "__main__":
    run_tests()
    solve()
