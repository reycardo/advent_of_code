from __future__ import annotations
from utils.tools import get_txt_files, read_input, timing_decorator
from utils.colors import magenta_color, reset_color
from utils.tools import Point, Grid, Vectors
from typing import List


files = get_txt_files(__file__)
#########
# Start #
#########


class Reindeer:
    def __init__(self, pos: Point):
        self.pos = pos
        self._facing = Point(Vectors.E)
        self._directions_idx = Puzzle.DIRECTIONS.index(self._facing)
        self._start_direction_idx = self._directions_idx
        self.score = 0

    def rotate_cw(self):
        self._directions_idx = (self._directions_idx + 1) % len(
            Puzzle.DIRECTIONS
        )
        self._facing = Point(Puzzle.DIRECTIONS[self._directions_idx])
        self.score += 1000
        
    def rotate_ccw(self):
        self._directions_idx = (self._directions_idx - 1) % len(
            Puzzle.DIRECTIONS
        )
        self._facing = Point(Puzzle.DIRECTIONS[self._directions_idx])
        self.score += 1000

    def move(self):
        self.pos = self.pos + self._facing
        self.score += 1

    def can_move(self, grid: Grid):
        next_pos = self.pos + self._facing
        return grid.value_at_point(next_pos) != Puzzle.WALL

class Puzzle:
    SPACE = "."
    WALL = "#"
    START = "S"
    END = "E"
    DIRECTIONS = [Vectors.N, Vectors.E, Vectors.S, Vectors.W]

    def __init__(self, text_input):
        self.input: List[str] = text_input
        self.grid: Grid = Grid([list(raw) for raw in self.input])

    def find_reindeer(self, grid: Grid):
        for point in grid._all_points:
            if grid.value_at_point(point) == Puzzle.START:
                self.reindeer = Reindeer(point)
                break

    def solve(self, part):
        if part == 1:
            self.find_reindeer(self.grid)
            pass
        elif part == 2:
            pass

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

    # solutions
    # print(f"\nRunning Solutions:")
    # assert main(raw=files["input"], part=1) == 1475249
    # assert main(raw=files["input"], part=2) == 1509724


def solve():
    print(f"\nSolving:")
    answer1 = main(raw=files["input"], part=1)
    print(f"Answer part1: {magenta_color}{answer1}{reset_color}")
    # answer2 = main(raw=files["input"], part=2)
    # print(f"Answer part2: {magenta_color}{answer2}{reset_color}")


if __name__ == "__main__":
    run_tests()
    solve()
