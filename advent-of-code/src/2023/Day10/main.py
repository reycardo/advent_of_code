from utils.tools import get_txt_files, read_input, timing_decorator
from utils.colors import magenta_color, reset_color
from enum import Enum

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
            [Pipe(pipe, (x, y)) for y, pipe in enumerate(row)]
            for x, row in enumerate(self.input)
        ]
        self.starting_pipe = self.get_starting_pipe()
        self.check_start_pipe_type()
        self.connect_all_pipes()

    def get_starting_pipe(self):
        for row in self.input_parsed:
            for pipe in row:
                if pipe.pipe_type == PipeType.START:
                    return pipe

    def get_starting_pipe_neighbours(self):
        left_coords = (self.starting_pipe.coords[0] - 1, self.starting_pipe.coords[1])
        right_coords = (self.starting_pipe.coords[0] + 1, self.starting_pipe.coords[1])
        up_coords = (self.starting_pipe.coords[0], self.starting_pipe.coords[1] - 1)
        down_coords = (self.starting_pipe.coords[0], self.starting_pipe.coords[1] + 1)
        up = self.input_parsed[up_coords[1]][up_coords[0]]
        down = self.input_parsed[down_coords[1]][down_coords[0]]
        left = self.input_parsed[left_coords[1]][left_coords[0]]
        right = self.input_parsed[right_coords[1]][right_coords[0]]
        return (up, down, left, right)

    def check_start_pipe_type(self):
        up, down, left, right = self.get_starting_pipe_neighbours()
        if up.pipe_type in (
            PipeType.VERTICAL,
            PipeType.BEND_DOWN_RIGHT,
            PipeType.BEND_DOWN_LEFT,
        ) and down.pipe_type in (
            PipeType.VERTICAL,
            PipeType.BEND_UP_RIGHT,
            PipeType.BEND_UP_LEFT,
        ):
            self.starting_pipe.pipe_type = PipeType.VERTICAL
        elif left.pipe_type in (
            PipeType.HORIZONTAL,
            PipeType.BEND_UP_RIGHT,
            PipeType.BEND_DOWN_RIGHT,
        ) and right.pipe_type in (
            PipeType.HORIZONTAL,
            PipeType.BEND_UP_LEFT,
            PipeType.BEND_DOWN_LEFT,
        ):
            self.starting_pipe.pipe_type = PipeType.HORIZONTAL
        elif up.pipe_type in (
            PipeType.VERTICAL,
            PipeType.BEND_DOWN_RIGHT,
            PipeType.BEND_DOWN_LEFT,
        ) and right.pipe_type in (
            PipeType.HORIZONTAL,
            PipeType.BEND_UP_LEFT,
            PipeType.BEND_DOWN_LEFT,
        ):
            self.starting_pipe.pipe_type = PipeType.BEND_UP_RIGHT
        elif up.pipe_type in (
            PipeType.VERTICAL,
            PipeType.BEND_DOWN_RIGHT,
            PipeType.BEND_DOWN_LEFT,
        ) and left.pipe_type in (
            PipeType.HORIZONTAL,
            PipeType.BEND_UP_RIGHT,
            PipeType.BEND_DOWN_RIGHT,
        ):
            self.starting_pipe.pipe_type = PipeType.BEND_UP_LEFT
        elif down.pipe_type in (
            PipeType.VERTICAL,
            PipeType.BEND_UP_RIGHT,
            PipeType.BEND_UP_LEFT,
        ) and right.pipe_type in (
            PipeType.HORIZONTAL,
            PipeType.BEND_UP_LEFT,
            PipeType.BEND_DOWN_LEFT,
        ):
            self.starting_pipe.pipe_type = PipeType.BEND_DOWN_RIGHT
        elif down.pipe_type in (
            PipeType.VERTICAL,
            PipeType.BEND_UP_RIGHT,
            PipeType.BEND_UP_LEFT,
        ) and left.pipe_type in (
            PipeType.HORIZONTAL,
            PipeType.BEND_UP_RIGHT,
            PipeType.BEND_DOWN_RIGHT,
        ):
            self.starting_pipe.pipe_type = PipeType.BEND_DOWN_LEFT

    def connect_pipes(self, source: Pipe):
        coords = source.get_connected_pipes()
        side1 = self.input_parsed[source.coords[1] + coords[0][1]][
            source.coords[0] + coords[0][0]
        ]
        side2 = self.input_parsed[source.coords[1] + coords[1][1]][
            source.coords[0] + coords[1][0]
        ]
        return (side1, side2)

    def connect_all_pipes(self):
        source = self.starting_pipe
        side1, side2 = self.connect_pipes(source)
        steps = 1
        side1.distance = steps
        side2.distance = steps
        while side1 != side2:
            side1, _ = self.connect_pipes(side1)
            _, side2 = self.connect_pipes(side2)
            side1.distance = steps
            side2.distance = steps

    def solve(self, part):
        if part == 1:
            return max([[pipe.distance for pipe in row] for row in self.input_parsed])
        if part == 2:
            pass


@timing_decorator
def main(raw, part):
    text_input = read_input(raw)
    input_parsed = [i if i else "" for i in text_input]
    puzzle = Puzzle(input_parsed)
    return puzzle.solve(part)


def run_tests():
    print(f"\nRunning Tests:")
    # assert main(raw=files["test"], part=1) == 4
    assert main(raw=files["test2"], part=1) == 8
    # assert main(raw=files["test"], part=2) == 2

    # solutions
    print(f"\nRunning Solutions:")
    # assert main(raw=files["input"], part=1) == 2174807968
    # assert main(raw=files["input"], part=2) == 1208


def solve():
    print(f"\nSolving:")
    answer1 = main(raw=files["input"], part=1)
    print(f"Answer part1: {magenta_color}{answer1}{reset_color}")
    # answer2 = main(raw=files["input"], part=2)
    # print(f"Answer part2: {magenta_color}{answer2}{reset_color}")


if __name__ == "__main__":
    run_tests()
    solve()
