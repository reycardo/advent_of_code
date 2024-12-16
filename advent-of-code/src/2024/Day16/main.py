from __future__ import annotations
from utils.tools import get_txt_files, read_input, timing_decorator
from utils.colors import magenta_color, reset_color
from utils.tools import Point, Grid, InvertedVectors
from typing import List
from collections import deque, defaultdict


files = get_txt_files(__file__)
#########
# Start #
#########


class Reindeer:
    def __init__(self, pos: Point):
        self.pos = pos
        self._facing = Point(InvertedVectors.E.value)
        self._directions_idx = Puzzle.DIRECTIONS.index(InvertedVectors.E)
        self._start_direction_idx = self._directions_idx
        self.score = 0
        self.last_rotation = None

    def rotate_cw(self, count: bool = True):
        self._directions_idx = (self._directions_idx + 1) % len(Puzzle.DIRECTIONS)
        self._facing = Point(Puzzle.DIRECTIONS[self._directions_idx].value)
        if count:
            self.score += 1000
            self.last_rotation = "cw"

    def rotate_ccw(self, count: bool = True):
        self._directions_idx = (self._directions_idx - 1) % len(Puzzle.DIRECTIONS)
        self._facing = Point(Puzzle.DIRECTIONS[self._directions_idx].value)
        if count:
            self.score += 1000
            self.last_rotation = "ccw"

    def move(self):
        self.pos = self.pos + self._facing
        self.score += 1

    def can_move(self, grid: Grid):
        next_pos = self.pos + self._facing
        return grid.value_at_point(next_pos) != Puzzle.WALL

    def move_back(self):
        self.pos = self.pos - self._facing
        self.score -= 1
        # revert rotation if it rotated previously
        if self.last_rotation == "cw":
            self.rotate_ccw(count=False)
            self.last_rotation = None
            self.score -= 1000
        elif self.last_rotation == "ccw":
            self.rotate_cw(count=False)
            self.last_rotation = None
            self.score -= 1000

    def restore_state(self, node: Node):
        self.pos = node.pos
        self.score = node.score
        self._facing = node.facing
        self._directions_idx = next(
            i
            for i, direction in enumerate(Puzzle.DIRECTIONS)
            if direction.value == (node.facing.x, node.facing.y)
        )

    def available_options(self, grid: Grid):
        """the options are move forward facing self._facing, rotate cw and move forward or rotate ccw and move forward
        can only move if the next position is not a wall"""

        options = []

        # Test if can move forward
        if self.can_move(grid=grid):
            options.append([self.move])

        # Test if can move right
        self.rotate_cw(count=False)
        if self.can_move(grid=grid):
            options.append([self.rotate_cw, self.move])
        self.rotate_ccw(count=False)

        # Test if can move left
        self.rotate_ccw(count=False)
        if self.can_move(grid=grid):
            options.append([self.rotate_ccw, self.move])
        self.rotate_cw(count=False)
        return options


class Node:
    def __init__(self, pos: Point, score: int, facing: Point, trail: List[Point]):
        self.pos = pos
        self.score = score
        self.facing = facing
        self.trail = trail


# TODO: Implement Stack frontier then compare all paths what has lowest score
class Puzzle:
    SPACE = "."
    WALL = "#"
    START = "S"
    END = "E"
    DIRECTIONS = [
        InvertedVectors.N,
        InvertedVectors.E,
        InvertedVectors.S,
        InvertedVectors.W,
    ]

    def __init__(self, text_input):
        self.input: List[str] = text_input
        self.grid: Grid = Grid([list(raw) for raw in self.input])

    def find_reindeer(self, grid: Grid):
        for point in grid._all_points:
            if grid.value_at_point(point) == Puzzle.START:
                self.reindeer = Reindeer(point)
                break

    def find_end(self, grid: Grid):
        for point in grid._all_points:
            if grid.value_at_point(point) == Puzzle.END:
                self.end = point
                break

    def find_path(self, grid: Grid, debug=False):
        frontier = deque()
        frontier.append(
            Node(
                pos=self.reindeer.pos,
                score=self.reindeer.score,
                facing=self.reindeer._facing,
                trail=[self.reindeer.pos],
            )
        )
        explored = defaultdict(list)
        trails = []

        while frontier:
            current_node: Node = frontier.popleft()  # Depth-First search

            # Restore the reindeer's state
            self.reindeer.restore_state(current_node)

            if current_node.pos == self.end:
                trails.append((current_node.trail, current_node.score))
                continue

            if explored[self.reindeer.pos]:
                explored[self.reindeer.pos].append(self.reindeer.score)
            else:
                explored[self.reindeer.pos] = [self.reindeer.score]
            pass

            if debug == True:
                print(f"{self.reindeer.score=}")
                self.paint_grid(grid, current_node.trail)
                print(f"{self.reindeer.pos} = {explored[self.reindeer.pos]=}")

            for next in self.reindeer.available_options(grid=grid):
                for action in next:
                    action()
                if self.reindeer.pos not in explored or self.reindeer.score <= min(
                    explored[self.reindeer.pos]
                ):
                    new_trail = current_node.trail + [self.reindeer.pos]
                    frontier.append(
                        Node(
                            pos=self.reindeer.pos,
                            score=self.reindeer.score,
                            facing=self.reindeer._facing,
                            trail=new_trail,
                        )
                    )
                self.reindeer.move_back()

        return explored, trails

    def paint_grid(self, grid: Grid, points_to_paint: List[Point]):
        for point in points_to_paint:
            grid.set_value_at_point(point, "X")
        print(grid)
        for point in points_to_paint:
            grid.set_value_at_point(point, ".")

    def find_distinct_seats(self):
        seats = [seat for trail in self.best_trails for seat in trail[0]]
        self.seats = list(set(seats))
        return len(self.seats)

    def solve(self, part):
        self.find_reindeer(self.grid)
        self.find_end(self.grid)
        self.explored, self.trails = self.find_path(self.grid)

        min_value = min(trail[1] for trail in self.trails)
        if part == 1:
            return min_value
        elif part == 2:
            self.best_trails = [trail for trail in self.trails if trail[1] == min_value]
            return self.find_distinct_seats()


@timing_decorator
def main(raw, part):
    text_input = read_input(raw)
    input_parsed = [i if i else "" for i in text_input]
    puzzle = Puzzle(input_parsed)
    return puzzle.solve(part)


def run_tests():
    print(f"\nRunning Tests:")
    assert main(raw=files["test"], part=1) == 7036
    assert main(raw=files["test2"], part=1) == 11048
    assert main(raw=files["test3"], part=1) == 21148
    assert main(raw=files["test4"], part=1) == 1004
    assert main(raw=files["test5"], part=1) == 4013
    assert main(raw=files["test"], part=2) == 45
    assert main(raw=files["test2"], part=2) == 64

    # solutions
    print(f"\nRunning Solutions:")
    assert main(raw=files["input"], part=1) == 85480
    assert main(raw=files["input"], part=2) == 518


def solve():
    print(f"\nSolving:")
    answer1 = main(raw=files["input"], part=1)
    print(f"Answer part1: {magenta_color}{answer1}{reset_color}")
    answer2 = main(raw=files["input"], part=2)
    print(f"Answer part2: {magenta_color}{answer2}{reset_color}")


if __name__ == "__main__":
    run_tests()
    solve()
