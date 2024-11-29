from utils.tools import get_txt_files, read_input, timing_decorator
from utils.colors import magenta_color, reset_color
import networkx as nx

files = get_txt_files(__file__)
#########
# Start #
#########

class Block:
    def __init__(self, heat_loss, pos) -> None:
        self.heat_loss = heat_loss
        self.pos = pos

class Puzzle:
    def __init__(self, text_input):
        self.input = text_input
        self.input_parsed = [
            [
                Block(
                    heat_loss=int(heat_loss),
                    pos=(x, y)
                ) for x, heat_loss in enumerate(row)
            ]
            for y, row in enumerate(self.input)
        ]
        self.rows = len(self.input_parsed)
        self.cols = len(self.input_parsed[0])

    def find_min_heat_loss_path(self):        
        G = nx.DiGraph()
        
        # Add nodes and edges to the graph
        for y in range(self.rows):
            for x in range(self.cols):
                if x + 1 < self.cols:
                    G.add_edge((x, y), (x + 1, y), weight=self.input_parsed[y][x + 1].heat_loss, direction='right')
                    G.add_edge((x + 1, y), (x, y), weight=self.input_parsed[y][x].heat_loss, direction='left')
                if y + 1 < self.rows:
                    G.add_edge((x, y), (x, y + 1), weight=self.input_parsed[y + 1][x].heat_loss, direction='down')
                    G.add_edge((x, y + 1), (x, y), weight=self.input_parsed[y][x].heat_loss, direction='up')
        
        # Find the shortest path using Dijkstra's algorithm
        start = (0, 0)
        end = (self.cols - 1, self.rows - 1)
        path = nx.dijkstra_path(G, start, end, weight='weight')
        
        # Calculate the total heat loss for the path
        total_heat_loss = sum(self.input_parsed[y][x].heat_loss for x, y in path)
        
        return total_heat_loss, path

    def solve(self, part):
        if part == 1:
            result, path = self.find_min_heat_loss_path()
            print("Total heat loss:", result)
            print("Path:", path)      
            return result      
        if part == 2:
            pass


@timing_decorator
def main(raw, part):
    text_input = read_input(raw)
    input_parsed = [i if i else "" for i in text_input]
    puzzle = Puzzle(input_parsed)
    puzzle.solve(part)
    return puzzle.solve(part)


def run_tests():
    print(f"\nRunning Tests:")
    assert main(raw=files["test"], part=1) == 102
    # assert main(raw=files["test"], part=2) == 51

    # solutions
    # print(f"\nRunning Solutions:")
    # assert main(raw=files["input"], part=1) == 6978
    # assert main(raw=files["input"], part=2) == 7315


def solve():
    print(f"\nSolving:")
    answer1 = main(raw=files["input"], part=1)
    print(f"Answer part1: {magenta_color}{answer1}{reset_color}")
    # answer2 = main(raw=files["input"], part=2)
    # print(f"Answer part2: {magenta_color}{answer2}{reset_color}")


if __name__ == "__main__":
    run_tests()
    solve()
