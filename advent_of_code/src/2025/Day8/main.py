import math
import heapq
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

class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        xr, yr = self.find(x), self.find(y)
        if xr == yr:
            return False
        # Union by size
        if self.size[xr] < self.size[yr]:
            xr, yr = yr, xr
        self.parent[yr] = xr
        self.size[xr] += self.size[yr]
        return True

    def groups(self):
        roots = {}
        for i in range(len(self.parent)):
            r = self.find(i)
            if r not in roots:
                roots[r] = set()
            roots[r].add(i)
        return list(roots.values())

class Puzzle:
    def __init__(self, text_input):
        self.input = text_input
        self.parse_input()
        self.connected_junctions = []

    def parse_input(self):        
        self.junctions = [Junction(*map(int, row.split(','))) for row in self.input]

    def connect_junctions(self, num_connections: int = None):
        n = len(self.junctions)
        uf = UnionFind(n)
        heap = []
        for i, j in itertools.combinations(range(n), 2):
            a, b = self.junctions[i], self.junctions[j]
            dist = ((a.x - b.x) ** 2 + (a.y - b.y) ** 2 + (a.z - b.z) ** 2) ** 0.5
            heapq.heappush(heap, (dist, i, j))
        connections_made = 0
        while (num_connections is None or connections_made < num_connections) and heap:
            if len(uf.groups()) == 1:
                return self.junctions[i].x, self.junctions[j].x
            _, i, j = heapq.heappop(heap)
            uf.union(i, j)
            connections_made += 1
        self.connected_junctions = uf.groups()

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
