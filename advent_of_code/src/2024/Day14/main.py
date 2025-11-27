from advent_of_code.utils.tools import get_txt_files, read_input, timing_decorator
from advent_of_code.utils.colors import magenta_color, reset_color
from advent_of_code.utils.tools import Point, Grid
from typing import Tuple, List
import re
from functools import reduce
import operator
import numpy as np

files = get_txt_files(__file__)
#########
# Start #
#########


class Robot:
    def __init__(self, pos: Point, velocity: Tuple[int, int]):
        self.pos = pos
        self.velocity = velocity

    def move(self, seconds: int, size: Tuple[int, int]):
        new_posx = (self.pos.x + (self.velocity[0] * seconds)) % size[0]
        new_posy = (self.pos.y + (self.velocity[1] * seconds)) % size[1]

        self.pos = Point(new_posx, new_posy)


class Puzzle:
    def __init__(self, text_input, size):
        self.input = text_input
        self.size = size
        self.parse_robots()
        self.setup_quadrants()
        self.seconds = 0

    def setup_quadrants(self):
        self.quadrants = {
            1: ((0, self.size[0] // 2 - 1), (0, self.size[1] // 2 - 1)),
            2: ((self.size[0] // 2 + 1, self.size[0]), (0, self.size[1] // 2 - 1)),
            3: ((0, self.size[0] // 2 - 1), (self.size[1] // 2 + 1, self.size[1])),
            4: (
                (self.size[0] // 2 + 1, self.size[0]),
                (self.size[1] // 2 + 1, self.size[1]),
            ),
        }

    def parse_robots(self):
        self.robots: List[Robot] = []
        for robot_raw in self.input:
            pos_match = re.search(r"p=(-?\d+),(-?\d+)", robot_raw)
            vel_match = re.search(r"v=(-?\d+),(-?\d+)", robot_raw)

            if pos_match and vel_match:
                pos = (int(pos_match.group(1)), int(pos_match.group(2)))
                velocity = (int(vel_match.group(1)), int(vel_match.group(2)))
                self.robots.append(Robot(Point(*pos), velocity))

    def move_robots(self, seconds):
        for robot in self.robots:
            robot.move(seconds, self.size)
        self.grid: Grid = self.create_grid()

    def create_grid(self):
        # Initialize the grid with "."
        grid = [["." for _ in range(self.size[0])] for _ in range(self.size[1])]

        # Mark the robot positions with "X"
        for robot in self.robots:
            x, y = robot.pos.x, robot.pos.y
            grid[y][x] = "X"

        return Grid(grid)

    def count_robots_in_quadrants(self):
        counts = {1: 0, 2: 0, 3: 0, 4: 0}

        for robot in self.robots:
            x, y = robot.pos.x, robot.pos.y

            for quadrant, ((x_min, x_max), (y_min, y_max)) in self.quadrants.items():
                if x_min <= x <= x_max and y_min <= y <= y_max:
                    counts[quadrant] += 1
                    break

        return counts

    def calculate_variance(self):
        # calculate the variance between all robot positions
        positions = [(robot.pos.x, robot.pos.y) for robot in self.robots]
        positions_array = np.array(positions)
        mean_position = np.mean(positions_array, axis=0)
        variance = np.mean(np.sum((positions_array - mean_position) ** 2, axis=1))

        return variance

    def solve(self, part):
        if part == 1:
            self.move_robots(seconds=100)
            counts = self.count_robots_in_quadrants()
            return reduce(operator.mul, counts.values(), 1)
        elif part == 2:
            variance = [9e10, 0]  # [var,seconds]
            for _ in range(int(1e4)):
                self.move_robots(seconds=1)
                self.seconds += 1
                new_var = self.calculate_variance()
                if new_var < variance[0]:
                    variance = [new_var, self.seconds]
            return variance[1]
        elif part == 3:
            self.move_robots(seconds=6398)
            print(self.grid)


@timing_decorator
def main(raw, part, size):
    text_input = read_input(raw)
    input_parsed = [i if i else "" for i in text_input]
    puzzle = Puzzle(input_parsed, size)
    return puzzle.solve(part)


def run_tests():
    print("\nRunning Tests:")
    assert main(raw=files["test"], part=1, size=(11, 7)) == 12

    # solutions
    print("\nRunning Solutions:")
    assert main(raw=files["input"], part=1, size=(101, 103)) == 219512160
    # assert main(raw=files["input"], part=2, size=(101,103)) == 6398


def solve():
    print("\nSolving:")
    answer1 = main(raw=files["input"], part=1, size=(101, 103))
    print(f"Answer part1: {magenta_color}{answer1}{reset_color}")
    answer2 = main(raw=files["input"], part=3, size=(101, 103))
    print(f"Printing tree: {magenta_color}{answer2}{reset_color}")
    answer2 = main(raw=files["input"], part=2, size=(101, 103))
    print(f"Answer part2: {magenta_color}{answer2}{reset_color}")


if __name__ == "__main__":
    run_tests()
    solve()
