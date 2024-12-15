from utils.tools import get_txt_files, read_input, timing_decorator
from utils.colors import magenta_color, reset_color
from utils.tools import Point, Grid, VectorDicts
from typing import Tuple, List


files = get_txt_files(__file__)
#########
# Start #
#########


class Robot:
    def __init__(self, pos: Point):
        self.pos = pos

    def move(self):
        pass


class Moves:
    def __init__(self, raw: str):
        self.moves = "\n".join(raw)


class Puzzle:
    def __init__(self, text_input):
        self.input: List[str] = text_input
        self.split_grid_from_moves()
        self.find_robot()

    def split_grid_from_moves(self):
        separator_index = self.input.index("")
        self.grid = Grid([raw for raw in self.input[:separator_index]])
        self.moves = Moves([raw for raw in self.input[separator_index + 1 :]])

    def find_robot(self):
        for point in self.grid._all_points:
            if self.grid.value_at_point(point) == "@":
                self.robot = Robot(point)
                break

    def solve(self, part):
        if part == 1:
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
    assert main(raw=files["test2"], part=1) == 2028
    assert main(raw=files["test"], part=1) == 10092

    # solutions
    print(f"\nRunning Solutions:")
    # assert main(raw=files["input"], part=1) == 219512160
    # assert main(raw=files["input"], part=2) == 6398


def solve():
    print(f"\nSolving:")
    answer1 = main(raw=files["input"], part=1)
    print(f"Answer part1: {magenta_color}{answer1}{reset_color}")
    # answer2 = main(raw=files["input"], part=2)
    # print(f"Answer part2: {magenta_color}{answer2}{reset_color}")


if __name__ == "__main__":
    run_tests()
    solve()
