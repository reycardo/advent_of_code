from __future__ import annotations
from utils.tools import get_txt_files, read_input, timing_decorator
from utils.colors import magenta_color, reset_color
from utils.tools import Point, Grid, VectorDicts
from typing import Tuple, List
from collections import deque


files = get_txt_files(__file__)
#########
# Start #
#########


class Robot:
    def __init__(self, pos: Point, moves: str):
        self.pos = pos
        self.moves = moves

    # TODO: move by directions: left right uses old move
    # TODO: move by directions: up down uses new move
    # TODO: fix deque: going up or down checks available spaces above each box
    def move(self, grid: Grid):
        for move in self.moves:
            """can not move if between the next wall and the robot there is no space
            get all points between the robot and the next wall
            check if there is a space between them
            if there is a space move the robot"""
            points_between = self.get_points_between_robot_and_wall(
                grid=grid, move=move
            )
            # find first space between robot and wall
            space_index = next(
                (
                    i
                    for i, point in enumerate(points_between)
                    if point[1] == Puzzle.SPACE
                ),
                None,
            )
            if space_index is not None:
                # move everything until space_index
                grid.set_value_at_point(
                    points_between[0][0], Puzzle.SPACE
                )  # set robot to space
                self.pos = points_between[1][0]  # set robot to next position
                for i in range(space_index):
                    grid.set_value_at_point(
                        points_between[i + 1][0], points_between[i][1]
                    )

    def move_p2(self, grid: Grid):
        for move in self.moves:
            """can only move if between the next wall and the robot is available space
            for each box that would get moved along with the robot
            check if there is a space between them
            if there is a space move the robot"""
            points_between = self.get_points_between_X_and_wall_p2(grid=grid, move=move)
            # find first space between robot and wall
            space_index = next(
                (
                    i
                    for i, point in enumerate(points_between)
                    if point[1] == Puzzle.SPACE
                ),
                None,
            )
            if space_index is not None:
                # move everything until space_index
                grid.set_value_at_point(
                    points_between[0][0], Puzzle.SPACE
                )  # set robot to space
                self.pos = points_between[1][0]  # set robot to next position
                for i in range(space_index):
                    grid.set_value_at_point(
                        points_between[i + 1][0], points_between[i][1]
                    )

    def get_points_between_robot_and_wall(self, grid: Grid, move: str):
        points_between = [(self.pos, grid.value_at_point(self.pos))]
        next_pos = self.pos + Point(*Puzzle.DIRECTIONS[move])
        while grid.value_at_point(next_pos) != Puzzle.WALL:
            points_between.append((next_pos, grid.value_at_point(next_pos)))
            next_pos = next_pos + Point(*Puzzle.DIRECTIONS[move])
        return points_between

    def get_points_between_X_and_wall_p2(self, grid: Grid, move: str, X_pos: Point):
        points_between = [(X_pos, grid.value_at_point(X_pos))]
        next_pos = X_pos + Point(*Puzzle.DIRECTIONS[move])
        # check if there is a BIGBOX in the way
        # if there is a BIGBOX in the way, also check the points between the BIGBOX and the next wall
        if grid.value_at_point(next_pos) == Puzzle.BIGBOX_LEFT:
            points_between.extend(
                self.get_points_between_X_and_wall_p2(
                    grid=grid, move=move, next_pos=(next_pos)
                )
            )
        while grid.value_at_point(next_pos) != Puzzle.WALL:
            points_between.append((next_pos, grid.value_at_point(next_pos)))
            next_pos = next_pos + Point(*Puzzle.DIRECTIONS[move])
        return points_between


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

    def find_robot(self):
        for point in self.grid._all_points:
            if self.grid.value_at_point(point) == Puzzle.ROBOT:
                self.robot = Robot(point, self.moves)
                break

    def get_gps_coordinates(self):
        self.gps_coordinates = []
        for point in self.grid._all_points:
            if self.grid.value_at_point(point) == Puzzle.BOX:
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
            self.find_robot()
            self.robot.move(self.grid)
            self.get_gps_coordinates()
            return sum(self.gps_coordinates)
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
    assert main(raw=files["test3"], part=2) == 9021
    assert main(raw=files["test2"], part=1) == 2028
    assert main(raw=files["test"], part=1) == 10092

    # solutions
    print(f"\nRunning Solutions:")
    assert main(raw=files["input"], part=1) == 1475249
    # assert main(raw=files["input"], part=2) == 6398


def solve():
    print(f"\nSolving:")
    answer1 = main(raw=files["input"], part=1)
    print(f"Answer part1: {magenta_color}{answer1}{reset_color}")
    answer2 = main(raw=files["input"], part=2)
    print(f"Answer part2: {magenta_color}{answer2}{reset_color}")


if __name__ == "__main__":
    run_tests()
    solve()
