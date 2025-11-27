from utils.tools import get_txt_files, read_input, timing_decorator
from advent_of_code.utils.colors import magenta_color, reset_color
import networkx as nx
from heapq import heappop, heappush

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
                Block(heat_loss=int(heat_loss), pos=(x, y))
                for x, heat_loss in enumerate(row)
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
                    G.add_edge(
                        (x, y),
                        (x + 1, y),
                        weight=self.input_parsed[y][x + 1].heat_loss,
                        direction="right",
                    )
                    G.add_edge(
                        (x + 1, y),
                        (x, y),
                        weight=self.input_parsed[y][x].heat_loss,
                        direction="left",
                    )
                if y + 1 < self.rows:
                    G.add_edge(
                        (x, y),
                        (x, y + 1),
                        weight=self.input_parsed[y + 1][x].heat_loss,
                        direction="down",
                    )
                    G.add_edge(
                        (x, y + 1),
                        (x, y),
                        weight=self.input_parsed[y][x].heat_loss,
                        direction="up",
                    )

        # Find the shortest path using Dijkstra's algorithm
        start = (0, 0)
        end = (self.cols - 1, self.rows - 1)
        path = self.custom_dijkstra(G, start, end)
        return path, path[end]

    def custom_dijkstra(self, G: nx.DiGraph, source, target):
        G_adj = G._adj
        previous = {v: (None, None) for v in G_adj.keys()}
        visited = {v: False for v in G_adj.keys()}
        distances = {v: float("inf") for v in G_adj.keys()}
        distances[source] = 0
        queue = []  # use heapq with (distance, (node, direction, count))
        heappush(queue, (0, (source, None, 1)))
        while queue:
            removed_distance, (removed_node, prev_direction, count) = heappop(queue)
            visited[removed_node] = True
            if removed_node == target:
                break
            for adj_node, edge in G_adj[removed_node].items():
                if visited[adj_node]:
                    continue
                new_distance = removed_distance + edge.get("weight")
                current_direction = edge.get("direction")
                if prev_direction == current_direction:
                    count += 1
                else:
                    count = 1
                if count == 3:
                    new_distance += 10000
                if new_distance < distances[adj_node]:
                    distances[adj_node] = new_distance
                    previous[adj_node] = removed_node, current_direction
                    heappush(
                        queue, (new_distance, (adj_node, current_direction, count))
                    )

        return distances

    def get_path(self, previous, target):
        path = []
        current_node = target
        while current_node is not None:
            path.append(current_node)
            current_node = previous[current_node][0]
        path.reverse()
        return path

    def solve(self, part):
        if part == 1:
            path, heat_loss = self.find_min_heat_loss_path()
            print("Path:", path)
            return heat_loss
        if part == 2:
            pass


@timing_decorator
def main(raw, part):
    text_input = read_input(raw)
    input_parsed = [i if i else "" for i in text_input]
    puzzle = Puzzle(input_parsed)
    return puzzle.solve(part)


def run_tests():
    print("\nRunning Tests:")
    assert main(raw=files["test"], part=1) == 102
    # assert main(raw=files["test"], part=2) == 51

    # solutions
    # print(f"\nRunning Solutions:")
    # assert main(raw=files["input"], part=1) == 6978
    # assert main(raw=files["input"], part=2) == 7315


def solve():
    print("\nSolving:")
    answer1 = main(raw=files["input"], part=1)
    print(f"Answer part1: {magenta_color}{answer1}{reset_color}")
    # answer2 = main(raw=files["input"], part=2)
    # print(f"Answer part2: {magenta_color}{answer2}{reset_color}")


if __name__ == "__main__":
    run_tests()
    solve()
