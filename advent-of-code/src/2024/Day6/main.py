from utils.tools import get_txt_files, read_input, timing_decorator
from utils.colors import magenta_color, reset_color
from utils.tools import Grid, Point, VectorDicts
from typing import List

files = get_txt_files(__file__)
#########
# Start #
#########


class Guard:
    def __init__(self, pos: Point, front: str):
        self.pos = pos
        self.front = VectorDicts.REVERSE_ARROWS[front]
        self.count = 1
        self.count_obstructions = 0

    def turn(self):
        available_dirs = list(VectorDicts.REVERSE_ARROWS.values())
        current_index = available_dirs.index(self.front)
        self.front = available_dirs[(current_index + 1) % len(available_dirs)]

    def detect_next_stop(self, grid: Grid):
        current_point = self.pos
        direction = self.front
        previous_point = current_point
        while True:
            current_point += Point(*direction)
            if not grid.valid_location(current_point):
                return (previous_point, True)
            elif grid.value_at_point(current_point)[0] == "#":
                return (previous_point, False)
            previous_point = current_point

    def walk_to_object(self, grid: Grid, next_stop, part=1):
        current_point = self.pos
        direction = self.front
        while current_point != next_stop:
            current_point += Point(*direction)
            if part == 2:
                self.test_4_obstruction(grid=grid, current_point=current_point)
            if not grid.value_at_point(current_point)[0] == "X":
                grid.set_value_at_point(current_point, ("X", direction))
                self.count += 1
            elif (
                grid.value_at_point(current_point)[0] == "X"
                and grid.value_at_point(current_point)[1]
            ):
                old_dir = grid.value_at_point(current_point)[1]
                directions = [old_dir]
                directions.append(direction)
                grid.set_value_at_point(current_point, ("X", directions))
            self.pos = current_point

        self.turn()

    def walk_till_loop(self, grid: Grid, next_stop):
        current_point = self.pos
        direction = self.front
        while current_point != next_stop:
            current_point += Point(*direction)
            if not grid.value_at_point(current_point)[0] == "X":
                grid.set_value_at_point(current_point, ("X", [direction]))
            elif grid.value_at_point(current_point)[0] == "X":
                if grid.value_at_point(current_point)[1]:
                    if direction in grid.value_at_point(current_point)[1]:
                        self.count += 1
                        return True
                    else:
                        old_dir = grid.value_at_point(current_point)[1]
                        directions = [old_dir]
                        directions.append(direction)

            self.pos = current_point

        self.turn()
        return False

    def test_4_obstruction(self, grid: Grid, current_point):
        new_grid = Grid([row[:] for row in grid._array])  # Deep copy of the grid
        new_grid = self.add_obstacle(current_point, new_grid)
        previous_dir = self.front
        self.turn()
        loop = False
        is_done = False
        while not is_done:
            next_stop, is_done = self.detect_next_stop(grid=new_grid)
            if not is_done:
                loop = self.walk_till_loop(grid=new_grid, next_stop=next_stop)
                if loop:
                    self.count_obstructions += 1
                    break
        self.front = previous_dir

    def add_obstacle(self, location: Point, grid: Grid):
        self.new_obstacle_location = (location, grid.value_at_point(location))
        grid.set_value_at_point(location, "#")
        return grid


class Puzzle:
    def __init__(self, text_input):
        self.input = text_input
        self.grid = Grid([list(line) for line in self.input])
        self.find_guard()

    def find_guard(self):
        guard_point = next(
            (
                x
                for x in self.grid.all_points()
                if self.grid.value_at_point(x) in VectorDicts.ARROWS
            ),
            None,
        )
        if guard_point is not None:
            self.guard = Guard(guard_point, self.grid.value_at_point(guard_point))

    def solve(self, part):
        if part == 1:
            is_done = False
            self.grid.set_value_at_point(self.guard.pos, ("X", self.guard.front))
            while not is_done:
                next_stop, is_done = self.guard.detect_next_stop(grid=self.grid)
                self.guard.walk_to_object(grid=self.grid, next_stop=next_stop)
            return self.guard.count
        elif part == 2:
            is_done = False
            self.grid.set_value_at_point(self.guard.pos, ("X", self.guard.front))
            while not is_done:
                next_stop, is_done = self.guard.detect_next_stop(grid=self.grid)
                self.guard.walk_to_object(
                    grid=self.grid, next_stop=next_stop, part=part
                )
            return self.guard.count_obstructions


@timing_decorator
def main(raw, part):
    text_input = read_input(raw)
    input_parsed = [i if i else "" for i in text_input]
    puzzle = Puzzle(input_parsed)
    return puzzle.solve(part)


def run_tests():
    print(f"\nRunning Tests:")
    assert main(raw=files["test"], part=1) == 41
    assert main(raw=files["test"], part=2) == 6

    # solutions
    print(f"\nRunning Solutions:")
    assert main(raw=files["input"], part=1) == 4883
    # assert main(raw=files["input"], part=2) == 5770


def solve():
    print(f"\nSolving:")
    answer1 = main(raw=files["input"], part=1)
    print(f"Answer part1: {magenta_color}{answer1}{reset_color}")
    answer2 = main(raw=files["input"], part=2)
    print(f"Answer part2: {magenta_color}{answer2}{reset_color}")


if __name__ == "__main__":
    run_tests()
    solve()
