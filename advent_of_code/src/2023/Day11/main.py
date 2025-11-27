from utils.tools import get_txt_files, read_input, timing_decorator, get_adjacents
from utils.colors import magenta_color, reset_color
import networkx as nx
from typing import List


files = get_txt_files(__file__)
#########
# Start #
#########


class Cell:
    def __init__(self, value, position):
        self.value = value
        self.coords = position


class Puzzle:
    def __init__(self, text_input, part, weight=1):
        self.weight = weight
        self.input = text_input
        self.input_parsed = [[point for point in row] for row in self.input]
        self.expanded_universe, self.empties_x, self.empties_y = self.expand_universe()
        if part == 1:
            self.expanded_grid = [
                [Cell(point, (y, x)) for y, point in enumerate(row)]
                for x, row in enumerate(self.expanded_universe)
            ]
            self.edge_list = self.get_paths(self.expanded_grid)
            self.galaxies = self.get_galaxies(matrix=self.expanded_grid)

        if part == 2:
            self.not_expanded_grid = [
                [Cell(point, (y, x)) for y, point in enumerate(row)]
                for x, row in enumerate(self.input_parsed)
            ]
            self.edge_list = self.get_paths(self.not_expanded_grid)

            self.galaxies = self.get_galaxies(matrix=self.not_expanded_grid)
        self.graph = self.make_graph(self.edge_list)

    def get_galaxies(self, matrix) -> List[Cell]:
        galaxies = []
        counter = 1
        for row in matrix:
            for cell in row:
                if cell.value == "#":
                    galaxies.append(cell)
                    cell.number = counter
                    counter += 1
        return galaxies

    def is_empty(self, line):
        for cell in line:
            if cell == "#":
                return False
        return True

    def get_paths(self, matrix):
        path_list = []
        for row in range(len(matrix[0])):
            for col in range(len(matrix)):
                edges = get_adjacents(matrix, (row, col))
                for end_path in edges:
                    path = ((row, col), end_path)
                    path_list.append(path)
        return path_list

    def make_graph(self, edges):
        G = nx.DiGraph()
        G.add_edges_from(edges)
        return G

    def expand_grid(self, matrix):
        new_matrix = []
        empties = []
        for i, row in enumerate(matrix):
            if self.is_empty(row):
                empty_line = ["."] * len(row)
                empties.append(i)
                new_matrix.append(row)
                new_matrix.append(empty_line)
            else:
                new_matrix.append(row)
        return new_matrix, empties

    def expand_universe(self):
        expand_rows, empties_x = self.expand_grid(self.input_parsed)
        expand_rows_transposed = list(map(list, zip(*expand_rows)))
        expanded_universe_transposed, empties_y = self.expand_grid(
            expand_rows_transposed
        )
        return list(map(list, zip(*expanded_universe_transposed))), empties_x, empties_y

    def get_shortest_path(self, start, target, part=1):
        # return nx.single_source_dijkstra(self.graph, source=start, target=target) # OVERKILL
        # using manhattan distance
        if part == 1:
            return abs(start[0] - target[0]) + abs(start[1] - target[1])
        if part == 2:
            empties = self.count_empties_between(start, target)
            return (
                abs(start[0] - target[0])
                + abs(start[1] - target[1])
                + empties * self.weight
                - empties
            )

    def count_empties_between(self, start, target):
        empties = 0
        for i in range(min(start[0], target[0]), max(start[0], target[0])):
            if i in self.empties_y:
                empties += 1
        for i in range(min(start[1], target[1]), max(start[1], target[1])):
            if i in self.empties_x:
                empties += 1
        return empties

    def get_all_shortest_paths(self, part):
        galaxy_paths = {}
        for i, start in enumerate(self.galaxies):
            for target in self.galaxies[i + 1 :]:
                if start != target:
                    path = self.get_shortest_path(start.coords, target.coords, part)
                    galaxy_paths[(start.number, target.number)] = path
        return galaxy_paths

    def solve(self, part):
        self.galaxy_paths = self.get_all_shortest_paths(part)
        result = sum([element for element in self.galaxy_paths.values()])
        return result


@timing_decorator
def main(raw, part, weight=1):
    text_input = read_input(raw)
    input_parsed = [i if i else "" for i in text_input]
    puzzle = Puzzle(input_parsed, part, weight)
    return puzzle.solve(part)


def run_tests():
    print(f"\nRunning Tests:")
    assert main(raw=files["test"], part=1) == 374
    assert main(raw=files["test"], part=2, weight=10) == 1030
    assert main(raw=files["test"], part=2, weight=100) == 8410

    # solutions
    print(f"\nRunning Solutions:")
    assert main(raw=files["input"], part=1) == 9274989
    assert main(raw=files["input"], part=2, weight=1000000) == 357134560737


def solve():
    print(f"\nSolving:")
    answer1 = main(raw=files["input"], part=1)
    print(f"Answer part1: {magenta_color}{answer1}{reset_color}")
    answer2 = main(raw=files["input"], part=2, weight=1000000)
    print(f"Answer part2: {magenta_color}{answer2}{reset_color}")


if __name__ == "__main__":
    run_tests()
    solve()
