from advent_of_code.utils.tools import get_txt_files, read_input, timing_decorator
from advent_of_code.utils.colors import magenta_color, reset_color
import networkx as nx
from functools import cache

files = get_txt_files(__file__)

class Puzzle:
    def __init__(self, text_input):
        self.input = text_input
        self.parse_input()
        self.build_graph()        

    def parse_input(self):
        self.connections = {}
        for line in self.input:
            key, values = line.split(':')
            self.connections[key.strip()] = [v.strip() for v in values.split() if v.strip()]

    def build_graph(self):
        self.graph = nx.DiGraph()
        for node, neighbors in self.connections.items():
            for neighbor in neighbors:
                self.graph.add_edge(node, neighbor)

    # Did it better for p2
    def find_paths(self, start, end):
        return list(nx.all_simple_paths(self.graph, source=start, target=end))
        
    @cache
    def count_paths_with_required_nodes(self, node, end, required_nodes=frozenset()):        
        if node == end:
            # Only count path if all required nodes have been visited
            return int(len(required_nodes) == 0)
        # Remove node from required_nodes if visited
        new_required = required_nodes - {node}
        return sum(
            self.count_paths_with_required_nodes(neighbor, end, new_required)
            for neighbor in self.graph.successors(node)
        )

    def solve(self, part):
        if part == 1:
            # return len(self.find_paths('you', 'out'))
            return self.count_paths_with_required_nodes("you", "out", frozenset({}))
        if part == 2:            
            return self.count_paths_with_required_nodes("svr", "out", frozenset({"dac", "fft"}))


@timing_decorator
def main(raw, part):
    text_input = read_input(raw)
    input_parsed = [i if i else "" for i in text_input]
    puzzle = Puzzle(input_parsed)    
    return puzzle.solve(part)


def run_tests():
    print("\nRunning Tests:")
    assert main(raw=files["test"], part=1) == 5
    assert main(raw=files["test2"], part=2) == 2

    # solutions
    print("\nRunning Solutions:")
    assert main(raw=files["input"], part=1) == 701
    assert main(raw=files["input"], part=2) == 390108778818526


def solve():
    print("\nSolving:")
    answer1 = main(raw=files["input"], part=1)
    print(f"Answer part1: {magenta_color}{answer1}{reset_color}")
    answer2 = main(raw=files["input"], part=2)
    print(f"Answer part2: {magenta_color}{answer2}{reset_color}")


if __name__ == "__main__":
    run_tests()
    solve()
