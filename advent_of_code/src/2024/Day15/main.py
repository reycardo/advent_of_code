from __future__ import annotations
from advent_of_code.utils.tools import get_txt_files, read_input, timing_decorator
from advent_of_code.utils.colors import magenta_color, reset_color
from advent_of_code.utils.tools import Point, Grid, VectorDicts
from typing import List


files = get_txt_files(__file__)
#########
# Start #
#########


class Robot:
    def __init__(self, pos: Point, moves: str):
        self.pos = pos
        self.moves = moves

    def set_robot_at_pos(self, pos: Point, grid: Grid):
        grid.set_value_at_point(self.pos, Puzzle.SPACE)
        self.pos = pos
        grid.set_value_at_point(pos, Puzzle.ROBOT)

    def move(self, grid: Grid, part):
        current_pos = self.pos
        for move in self.moves:
            direction = Point(*Puzzle.DIRECTIONS[move])
            new_pos = current_pos + direction
            if grid.value_at_point(new_pos) == Puzzle.SPACE:
                current_pos = new_pos
                self.set_robot_at_pos(new_pos, grid=grid)
            elif grid.value_at_point(new_pos) == Puzzle.WALL:
                continue
            elif part == 1 or direction.x:
                look_ahead = new_pos
                while grid.value_at_point(look_ahead) in "O[]":
                    look_ahead += direction
                if grid.value_at_point(look_ahead) == Puzzle.WALL:
                    continue
                while look_ahead != new_pos:
                    grid.set_value_at_point(
                        look_ahead, grid.value_at_point(look_ahead - direction)
                    )
                    look_ahead -= direction
                grid.set_value_at_point(new_pos, Puzzle.SPACE)
                current_pos = new_pos
                self.set_robot_at_pos(new_pos, grid=grid)
            elif self.can_vertical_push(new_pos, direction, grid=grid):
                self.do_vertical_push(new_pos, direction, grid=grid)
                current_pos = new_pos
                self.set_robot_at_pos(new_pos, grid=grid)

    def can_vertical_push(self, pos: Point, dir: Point, grid: Grid):
        adj_pos = (
            Puzzle.DIRECTIONS[">"]
            if grid.value_at_point(pos) == "["
            else Puzzle.DIRECTIONS["<"]
        )
        adj_pos = Point(*adj_pos)
        new_pos = pos + dir
        if (
            grid.value_at_point(new_pos) == "#"
            or grid.value_at_point(new_pos + adj_pos) == "#"
        ):
            return False

        if grid.value_at_point(new_pos) in "[]" and not self.can_vertical_push(
            new_pos, dir, grid=grid
        ):
            return False

        if grid.value_at_point(
            new_pos + adj_pos
        ) in "[]" and not self.can_vertical_push(new_pos + adj_pos, dir, grid=grid):
            return False
        return True

    def do_vertical_push(self, pos: Point, dir: Point, grid: Grid):
        adj_pos = (
            Puzzle.DIRECTIONS[">"]
            if grid.value_at_point(pos) == Puzzle.BIGBOX_LEFT
            else Puzzle.DIRECTIONS["<"]
        )
        adj_pos = Point(*adj_pos)
        new_pos = pos + dir
        if grid.value_at_point(new_pos) in (Puzzle.BIGBOX_LEFT, Puzzle.BIGBOX_RIGHT):
            self.do_vertical_push(new_pos, dir, grid=grid)

        if grid.value_at_point(new_pos + adj_pos) in (
            Puzzle.BIGBOX_LEFT,
            Puzzle.BIGBOX_RIGHT,
        ):
            self.do_vertical_push(new_pos + adj_pos, dir, grid=grid)

        grid.set_value_at_point(new_pos, grid.value_at_point(pos))
        grid.set_value_at_point(new_pos + adj_pos, grid.value_at_point(pos + adj_pos))
        grid.set_value_at_point(pos, Puzzle.SPACE)
        grid.set_value_at_point(pos + adj_pos, Puzzle.SPACE)


class Puzzle:
    SPACE = "."
    WALL = "#"
    ROBOT = "@"
    BOX = "O"
    BIGBOX_LEFT = "["
    BIGBOX_RIGHT = "]"
    DIRECTIONS = VectorDicts.REVERSE_ARROWS

    def __init__(self, text_input):
        self.input: List[str] = text_input
        self.split_grid_from_moves()
        self.expand_grid()

    def split_grid_from_moves(self):
        separator_index = self.input.index("")
        self.grid = Grid([list(raw) for raw in self.input[:separator_index]])
        self.moves = "".join([raw for raw in self.input[separator_index + 1 :]])

    def find_robot(self, grid: Grid):
        for point in grid._all_points:
            if grid.value_at_point(point) == Puzzle.ROBOT:
                self.robot = Robot(point, self.moves)
                break

    def get_gps_coordinates(self, grid: Grid):
        self.gps_coordinates = []
        for point in grid._all_points:
            if grid.value_at_point(point) in (Puzzle.BOX, Puzzle.BIGBOX_LEFT):
                self.gps_coordinates.append(point.x + point.y * 100)

    def expand_grid(self):
        expansion_map = {"#": "##", ".": "..", "O": "[]", "@": "@."}

        expanded_arrays = [
            [char for e in array for char in expansion_map.get(e, e)]
            for array in self.grid._array
        ]

        self.expanded_grid = Grid(expanded_arrays)

    def solve(self, part):
        if part == 1:
            self.find_robot(self.grid)
            self.robot.move(self.grid, part=1)
            self.get_gps_coordinates(grid=self.grid)
            return sum(self.gps_coordinates)
        elif part == 2:
            self.find_robot(self.expanded_grid)
            self.robot.move(self.expanded_grid, part=2)
            self.get_gps_coordinates(grid=self.expanded_grid)
            return sum(self.gps_coordinates)


@timing_decorator
def main(raw, part):
    text_input = read_input(raw)
    input_parsed = [i if i else "" for i in text_input]
    puzzle = Puzzle(input_parsed)
    return puzzle.solve(part)


def run_tests():
    print("\nRunning Tests:")
    assert main(raw=files["test"], part=1) == 10092
    assert main(raw=files["test2"], part=1) == 2028
    assert main(raw=files["test3"], part=2) == 105 + 207 + 306
    assert main(raw=files["test"], part=2) == 9021

    # solutions
    print("\nRunning Solutions:")
    assert main(raw=files["input"], part=1) == 1475249
    assert main(raw=files["input"], part=2) == 1509724


def solve():
    print("\nSolving:")
    answer1 = main(raw=files["input"], part=1)
    print(f"Answer part1: {magenta_color}{answer1}{reset_color}")
    answer2 = main(raw=files["input"], part=2)
    print(f"Answer part2: {magenta_color}{answer2}{reset_color}")


if __name__ == "__main__":
    run_tests()
    solve()
