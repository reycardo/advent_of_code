from utils.tools import get_txt_files, read_input, timing_decorator
from utils.colors import magenta_color, reset_color
from typing import List, Tuple
from utils.tools import Grid, Point, Vectors
from collections import deque

files = get_txt_files(__file__)
#########
# Start #
#########

directions = [Vectors.N, Vectors.E, Vectors.S, Vectors.W]

class Trailhead:
    def __init__(self, head: Point) -> None:
        self.head = head
        self.score = None
        self.trails = []
        self.pt2_score = None

    def find_trails(self, grid: Grid):        
        queue = deque()
        queue.append((self.head, 0, [self.head]))  # current_point, count, trail        
        while queue:
            current_point: Point
            count: int
            trail: List[Point]
            current_point, count, trail = queue.popleft()
            neighbours = current_point.get_specific_neighbours(directions=directions)
            for neighbour in neighbours:                
                if grid.valid_location(neighbour) and grid.value_at_point(neighbour) == count + 1: # checks if neighbour is valid and uphill slope (+1)
                    new_trail = trail + [neighbour]
                    if count + 1 == 9: # add to trails when neighbour is 9
                        self.trails.append(new_trail)
                    else:
                        queue.append((neighbour, count + 1, new_trail))
        self.find_distinct_ends()
        self.pt2_score = len(self.trails)

    def find_distinct_ends(self):
        ends = []
        for trail in self.trails:
            ends.append(trail[-1])
        self.ends = list(set(ends))
        self.score = len(self.ends)

class Puzzle:
    def __init__(self, text_input):
        self.input = text_input
        self.input_parsed = [list(map(int,line)) for line in self.input]
        self.grid = Grid(self.input_parsed)        
        self.trailheads = self.find_trailheads()
        self.find_all_trails()

    def find_trailheads(self):
        return [Trailhead(point) for point in self.grid._all_points if self.grid.value_at_point(point=point) == 0]

    def find_all_trails(self):
        for trailhead in self.trailheads:
            trailhead.find_trails(self.grid)

    def solve(self, part):
        if part == 1:
            return sum([trail_head.score for trail_head in self.trailheads])
        elif part == 2:
            return sum([trail_head.pt2_score for trail_head in self.trailheads])


@timing_decorator
def main(raw, part):
    text_input = read_input(raw)
    input_parsed = [i if i else "" for i in text_input]
    puzzle = Puzzle(input_parsed)
    return puzzle.solve(part)


def run_tests():
    print(f"\nRunning Tests:")
    assert main(raw=files["test2"], part=1) == 1
    assert main(raw=files["test"], part=1) == 36
    assert main(raw=files["test"], part=2) == 81
    

    # solutions
    print(f"\nRunning Solutions:")
    assert main(raw=files["input"], part=1) == 717
    assert main(raw=files["input"], part=2) == 1686


def solve():
    print(f"\nSolving:")
    answer1 = main(raw=files["input"], part=1)
    print(f"Answer part1: {magenta_color}{answer1}{reset_color}")
    answer2 = main(raw=files["input"], part=2)
    print(f"Answer part2: {magenta_color}{answer2}{reset_color}")


if __name__ == "__main__":
    run_tests()
    solve()
