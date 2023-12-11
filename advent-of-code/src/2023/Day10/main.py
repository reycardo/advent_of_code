from utils.tools import get_txt_files, read_input, timing_decorator
from utils.colors import magenta_color, reset_color
from enum import Enum
from typing import Tuple
import matplotlib.path as mplPath


files = get_txt_files(__file__)
#########
# Start #
#########


class PipeType(Enum):
    GROUND = "."
    VERTICAL = "|"
    HORIZONTAL = "-"
    BEND_UP_RIGHT = "L"
    BEND_UP_LEFT = "J"
    BEND_DOWN_LEFT = "7"
    BEND_DOWN_RIGHT = "F"
    START = "S"


class Pipe:
    def __init__(self, pipe, coords) -> None:
        self.pipe = pipe
        self.coords = coords
        self.assign_pipe_type()
        self.distance = None

    def assign_pipe_type(self):
        for pipe_type in PipeType:
            if self.pipe == pipe_type.value:
                self.pipe_type = pipe_type
                break

    def get_connected_pipes(self):
        if self.pipe_type == PipeType.GROUND:
            return None
        elif self.pipe_type == PipeType.VERTICAL:
            return ((0, 1), (0, -1))
        elif self.pipe_type == PipeType.HORIZONTAL:
            return ((1, 0), (-1, 0))
        elif self.pipe_type == PipeType.BEND_UP_RIGHT:
            return ((1, 0), (0, -1))
        elif self.pipe_type == PipeType.BEND_UP_LEFT:
            return ((-1, 0), (0, -1))
        elif self.pipe_type == PipeType.BEND_DOWN_LEFT:
            return ((-1, 0), (0, 1))
        elif self.pipe_type == PipeType.BEND_DOWN_RIGHT:
            return ((1, 0), (0, 1))
        elif self.pipe_type == PipeType.START:
            return None


class Puzzle:
    def __init__(self, text_input):
        self.input = text_input
        self.input_parsed = [
            [Pipe(pipe, (y, x)) for y, pipe in enumerate(row)]
            for x, row in enumerate(self.input)
        ]
        self.starting_pipe = self.get_starting_pipe()
        self.check_start_pipe_type()
        self.make_loop()

    def get_starting_pipe(self):
        for row in self.input_parsed:
            for pipe in row:
                if pipe.pipe_type == PipeType.START:
                    return pipe

    def is_inside(self, coords: tuple):
        if all(
            (
                coords[0] >= 0,
                coords[0] < len(self.input_parsed[0]),
                coords[1] >= 0,
                coords[1] < len(self.input_parsed),
            )
        ):
            return True
        else:
            return False

    def get_starting_pipe_neighbours(self):
        directions = {"up": (0, -1), "down": (0, 1), "left": (-1, 0), "right": (1, 0)}
        neighbours = {}

        for direction, (dx, dy) in directions.items():
            new_coords = (
                self.starting_pipe.coords[0] + dx,
                self.starting_pipe.coords[1] + dy,
            )
            if self.is_inside(new_coords):
                neighbours[direction] = self.input_parsed[new_coords[1]][new_coords[0]]
            else:
                neighbours[direction] = None

        return neighbours

    def check_start_pipe_type(self):
        neighbours = self.get_starting_pipe_neighbours()
        conditions = {
            PipeType.VERTICAL: (
                {
                    "up": (
                        PipeType.VERTICAL,
                        PipeType.BEND_DOWN_RIGHT,
                        PipeType.BEND_DOWN_LEFT,
                    ),
                    "down": (
                        PipeType.VERTICAL,
                        PipeType.BEND_UP_RIGHT,
                        PipeType.BEND_UP_LEFT,
                    ),
                }
            ),
            PipeType.HORIZONTAL: (
                {
                    "left": (
                        PipeType.HORIZONTAL,
                        PipeType.BEND_UP_RIGHT,
                        PipeType.BEND_DOWN_RIGHT,
                    ),
                    "right": (
                        PipeType.HORIZONTAL,
                        PipeType.BEND_UP_LEFT,
                        PipeType.BEND_DOWN_LEFT,
                    ),
                }
            ),
            PipeType.BEND_UP_RIGHT: (
                {
                    "up": (
                        PipeType.VERTICAL,
                        PipeType.BEND_DOWN_RIGHT,
                        PipeType.BEND_DOWN_LEFT,
                    ),
                    "right": (
                        PipeType.HORIZONTAL,
                        PipeType.BEND_UP_LEFT,
                        PipeType.BEND_DOWN_LEFT,
                    ),
                }
            ),
            PipeType.BEND_UP_LEFT: (
                {
                    "up": (
                        PipeType.VERTICAL,
                        PipeType.BEND_DOWN_RIGHT,
                        PipeType.BEND_DOWN_LEFT,
                    ),
                    "left": (
                        PipeType.HORIZONTAL,
                        PipeType.BEND_UP_RIGHT,
                        PipeType.BEND_DOWN_RIGHT,
                    ),
                }
            ),
            PipeType.BEND_DOWN_RIGHT: (
                {
                    "down": (
                        PipeType.VERTICAL,
                        PipeType.BEND_UP_RIGHT,
                        PipeType.BEND_UP_LEFT,
                    ),
                    "right": (
                        PipeType.HORIZONTAL,
                        PipeType.BEND_UP_LEFT,
                        PipeType.BEND_DOWN_LEFT,
                    ),
                }
            ),
            PipeType.BEND_DOWN_LEFT: (
                {
                    "down": (
                        PipeType.VERTICAL,
                        PipeType.BEND_UP_RIGHT,
                        PipeType.BEND_UP_LEFT,
                    ),
                    "left": (
                        PipeType.HORIZONTAL,
                        PipeType.BEND_UP_RIGHT,
                        PipeType.BEND_DOWN_RIGHT,
                    ),
                }
            ),
        }

        for pipe_type, condition in conditions.items():
            if all(
                neighbours[direction]
                and neighbours[direction].pipe_type in condition[direction]
                for direction in condition
            ):
                self.starting_pipe.pipe_type = pipe_type
                break

    def connect_pipes(self, source: Pipe) -> Tuple[Pipe, Pipe]:
        coords = source.get_connected_pipes()
        side1 = self.input_parsed[source.coords[1] + coords[0][1]][
            source.coords[0] + coords[0][0]
        ]
        side2 = self.input_parsed[source.coords[1] + coords[1][1]][
            source.coords[0] + coords[1][0]
        ]
        return (side1, side2)

    def make_loop(self):
        source = self.starting_pipe
        source.distance = 0
        self.loop = [source]
        side1, side2 = self.connect_pipes(source)
        steps = 1
        side1.distance = side2.distance = steps
        previous_side1 = previous_side2 = source
        self.loop.extend([side1, side2])
        while side1 != side2:
            new_side1_1, new_side1_2 = self.connect_pipes(side1)
            new_side2_1, new_side2_2 = self.connect_pipes(side2)
            steps += 1
            picked_side1 = new_side1_1 if new_side1_1 != previous_side1 else new_side1_2
            picked_side2 = new_side2_1 if new_side2_1 != previous_side2 else new_side2_2
            previous_side1 = side1
            previous_side2 = side2
            side1 = picked_side1
            side2 = picked_side2
            side1.distance = side2.distance = steps
            self.loop.extend([side1, side2] if side1 != side2 else [side1])

    def get_inside_points(self):
        polygon = [(pipe.coords[0], pipe.coords[1]) for pipe in self.loop]
        path = mplPath.Path(polygon)
        boundaries = [pipe.coords for pipe in self.loop]
        result = [
            [
                path.contains_point(pipe.coords)
                for pipe in row
                if pipe.coords not in boundaries
            ]
            for row in self.input_parsed
        ]
        return sum(value for sublist in result for value in sublist)

    def solve(self, part):
        if part == 1:
            return max([pipe.distance for pipe in self.loop])
        if part == 2:
            return self.get_inside_points()


@timing_decorator
def main(raw, part):
    text_input = read_input(raw)
    input_parsed = [i if i else "" for i in text_input]
    puzzle = Puzzle(input_parsed)
    return puzzle.solve(part)


def run_tests():
    print(f"\nRunning Tests:")
    assert main(raw=files["test"], part=1) == 4
    assert main(raw=files["test2"], part=1) == 8
    assert main(raw=files["test"], part=2) == 1
    assert main(raw=files["test2"], part=2) == 1
    assert main(raw=files["test3"], part=2) == 4
    assert main(raw=files["test4"], part=2) == 8
    assert main(raw=files["test5"], part=2) == 10

    # solutions
    print(f"\nRunning Solutions:")
    assert main(raw=files["input"], part=1) == 6786
    # assert main(raw=files["input"], part=2) == 1208


def solve():
    print(f"\nSolving:")
    answer1 = main(raw=files["input"], part=1)
    print(f"Answer part1: {magenta_color}{answer1}{reset_color}")
    answer2 = main(raw=files["input"], part=2)
    print(f"Answer part2: {magenta_color}{answer2}{reset_color}")


if __name__ == "__main__":
    run_tests()
    solve()
