from utils.tools import get_txt_files, read_input, timing_decorator
from utils.colors import magenta_color, reset_color
import networkx as nx
from typing import Tuple, Dict, Any, List
from heapq import heappop, heappush
from itertools import count

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

        def _weight_function(G, weight):
            """Returns a function that returns the weight of an edge.

            The returned function is specifically suitable for input to
            functions :func:`_dijkstra` and :func:`_bellman_ford_relaxation`.

            Parameters
            ----------
            G : NetworkX graph.

            weight : string or function
                If it is callable, `weight` itself is returned. If it is a string,
                it is assumed to be the name of the edge attribute that represents
                the weight of an edge. In that case, a function is returned that
                gets the edge weight according to the specified edge attribute.

            Returns
            -------
            function
                This function returns a callable that accepts exactly three inputs:
                a node, an node adjacent to the first one, and the edge attribute
                dictionary for the eedge joining those nodes. That function returns
                a number representing the weight of an edge.

            If `G` is a multigraph, and `weight` is not callable, the
            minimum edge weight over all parallel edges is returned. If any edge
            does not have an attribute with key `weight`, it is assumed to
            have weight one.

            """
            if callable(weight):
                return weight
            # If the weight keyword argument is not callable, we assume it is a
            # string representing the edge attribute containing the weight of
            # the edge.
            if G.is_multigraph():
                return lambda u, v, d: min(attr.get(weight, 1) for attr in d.values())
            return lambda u, v, data: data.get(weight, 1)


        def custom_dijkstra_multisource(
            G: nx.Graph, sources: List[Any], weight: Any, pred: Dict[Any, List[Any]] = None,
            paths: Dict[Any, List[Any]] = None, cutoff: Any = None, target: Any = None
        ) -> Dict[Any, float]:
            """
                Custom version of Dijkstra's algorithm to find shortest weighted paths with additional constraints.

                Parameters
                ----------
                G : NetworkX graph
                    The graph on which to perform the search.

                sources : list
                    Starting nodes for paths.

                weight: function
                    Function with (u, v, data) input that returns that edge's weight or None to indicate a hidden edge.

                pred: dict of lists, optional (default=None)
                    Dictionary to store a list of predecessors keyed by that node. If None, predecessors are not stored.

                paths: dict, optional (default=None)
                    Dictionary to store the path list from source to each node, keyed by node. If None, paths are not stored.

                target : node label, optional
                    Ending node for path. Search is halted when target is found.

                cutoff : integer or float, optional
                    Length (sum of edge weights) at which the search is stopped. If cutoff is provided, only return paths with summed weight <= cutoff.

                direction: dict, optional (default=None)
                    Dictionary to store the direction of edges keyed by (u, v). If None, directions are not considered.

                penalty: float, optional (default=1.0)
                    Penalty to apply if the direction of the new edge matches the direction of the last two edges.

                Returns
                -------
                distance : dict
                    A mapping from node to shortest distance to that node from one of the source nodes.

                Raises
                ------
                NodeNotFound
                    If any of `sources` is not in `G`.
                """
            G_succ = G._adj  # For speed-up (and works for both directed and undirected graphs)

            # Initialize the direction dictionary if not provided
            direction = {}
            for u, v, data in G.edges(data=True):
                direction[(u, v)] = data.get('direction', None)

            push = heappush
            pop = heappop
            dist = {}  # dictionary of final distances
            seen = {}
            # fringe is heapq with 3-tuples (distance, c, node, last_edge, second_last_edge)
            # use the count c to avoid comparing nodes (may not be able to)
            c = count()
            fringe = []
            penalty = 10000
            for source in sources:
                seen[source] = 0
                push(fringe, (0, next(c), source, []))
            while fringe:
                (d, _, v, path) = pop(fringe)
                if v in dist:
                    continue  # already searched this node.
                dist[v] = d
                if v == target:
                    break
                for u, e in G_succ[v].items():
                    cost = weight(v, u, e)
                    if cost is None:
                        continue
                    if len(path) >= 2:
                        last_edge = path[-1]
                        second_last_edge = path[-2]
                        if direction[(last_edge[0], last_edge[1])] == direction[(second_last_edge[0], second_last_edge[1])] == direction[(v, u)]:
                            cost += penalty
                    vu_dist = dist[v] + cost
                    if cutoff is not None:
                        if vu_dist > cutoff:
                            continue
                    if u in dist:
                        u_dist = dist[u]
                        if vu_dist < u_dist:
                            raise ValueError("Contradictory paths found:", "negative weights?")
                        elif pred is not None and vu_dist == u_dist:
                            pred[u].append(v)
                    elif u not in seen or vu_dist < seen[u]:
                        seen[u] = vu_dist
                        push(fringe, (vu_dist, next(c), u, path + [(v, u)]))
                        if paths is not None:
                            paths[u] = paths[v] + [u]
                        if pred is not None:
                            pred[u] = [v]
                    elif vu_dist == seen[u]:
                        if pred is not None:
                            pred[u].append(v)

            # The optional predecessor and path dictionaries can be accessed
            # by the caller via the pred and paths objects passed as arguments.
            return dist


        # Find the shortest path using Dijkstra's algorithm
        start = (0, 0)
        end = (self.cols - 1, self.rows - 1)
        weight = _weight_function(G, "weight")

        path = custom_dijkstra_multisource(G, sources={start}, target=end, weight=weight)
        
        # Calculate the total heat loss for the path
        total_heat_loss = path[end]
        
        return total_heat_loss, path

    def solve(self, part):
        if part == 1:
            result, path = self.find_min_heat_loss_path()
            print("Total heat loss:", result)
            print("Path:", path)            
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
