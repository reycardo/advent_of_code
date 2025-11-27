from utils.tools import get_txt_files, read_input, timing_decorator
from advent_of_code.utils.colors import magenta_color, reset_color
from typing import List
import copy

files = get_txt_files(__file__)
#########
# Start #
#########


class Tile:
    def __init__(self, tile, pos) -> None:
        self.tile = tile
        self.pos = pos
        self.energized = False
        self.laser_dir = None


class Laser:
    def __init__(self, start, direction, tiles) -> None:
        self.start = start
        self.current_direction = direction
        self.sublasers: List[Laser] = []
        self.stop = False
        self.tiles: List[Tile] = tiles

    def parse_tile(self, tile: Tile):
        if tile.laser_dir == self.current_direction:
            self.stop = True
            return
        tile.laser_dir = self.current_direction
        tile.energized = True

        if tile.tile == ".":
            return

        elif tile.tile == "/" and self.current_direction == (1, 0):  # right
            self.current_direction = (0, -1)  # up
        elif tile.tile == "/" and self.current_direction == (0, 1):  # down
            self.current_direction = (-1, 0)  # left
        elif tile.tile == "/" and self.current_direction == (-1, 0):  # left
            self.current_direction = (0, 1)  # down
        elif tile.tile == "/" and self.current_direction == (0, -1):  # up
            self.current_direction = (1, 0)  # right

        elif tile.tile == "\\" and self.current_direction == (1, 0):  # right
            self.current_direction = (0, 1)  # down
        elif tile.tile == "\\" and self.current_direction == (0, 1):  # down
            self.current_direction = (1, 0)  # right
        elif tile.tile == "\\" and self.current_direction == (-1, 0):  # left
            self.current_direction = (0, -1)  # up
        elif tile.tile == "\\" and self.current_direction == (0, -1):  # up
            self.current_direction = (-1, 0)  # left

        elif tile.tile == "|" and self.current_direction in [
            (1, 0),
            (-1, 0),
        ]:  # right or left
            if self.start[1] + 1 <= len(self.tiles) - 1:
                self.sublasers.append(
                    Laser(
                        start=(self.start[0], self.start[1] + 1),
                        direction=(0, 1),
                        tiles=self.tiles,
                    )
                )
            if self.start[1] - 1 >= 0:
                self.sublasers.append(
                    Laser(
                        start=(self.start[0], self.start[1] - 1),
                        direction=(0, -1),
                        tiles=self.tiles,
                    )
                )

            self.stop = True
        elif tile.tile == "-" and self.current_direction in [
            (0, 1),
            (0, -1),
        ]:  # down or up
            if self.start[0] + 1 <= len(self.tiles[0]) - 1:
                self.sublasers.append(
                    Laser(
                        start=(self.start[0] + 1, self.start[1]),
                        direction=(1, 0),
                        tiles=self.tiles,
                    )
                )

            if self.start[0] - 1 >= 0:
                self.sublasers.append(
                    Laser(
                        start=(self.start[0] - 1, self.start[1]),
                        direction=(-1, 0),
                        tiles=self.tiles,
                    )
                )
            self.stop = True

    def check_end_tile(self):
        if self.current_direction == (1, 0) and self.start[0] == len(self.tiles[0]) - 1:
            self.stop = True
        elif self.current_direction == (0, 1) and self.start[1] == len(self.tiles) - 1:
            self.stop = True
        elif self.current_direction == (-1, 0) and self.start[0] == 0:
            self.stop = True
        elif self.current_direction == (0, -1) and self.start[1] == 0:
            self.stop = True
        else:
            self.start = (
                self.start[0] + self.current_direction[0],
                self.start[1] + self.current_direction[1],
            )

    def run(self):
        while not self.stop:
            self.parse_tile(self.tiles[self.start[1]][self.start[0]])
            if self.stop:
                break
            self.check_end_tile()
        for sublaser in self.sublasers:
            sublaser.run()


class Puzzle:
    def __init__(self, text_input):
        self.input = text_input
        self.input_parsed = [
            [Tile(point, (x, y)) for x, point in enumerate(row)]
            for y, row in enumerate(self.input)
        ]

    def run_lasers(self):
        max_energized = 0
        for i in range(len(self.input_parsed)):
            laser = Laser(
                start=(0, i), direction=(1, 0), tiles=copy.deepcopy(self.input_parsed)
            )
            laser.run()
            max_energized = max(
                max_energized,
                sum(1 for row in laser.tiles for tile in row if tile.energized),
            )
            del laser

            laser = Laser(
                start=(len(self.input_parsed[0]) - 1, i),
                direction=(-1, 0),
                tiles=copy.deepcopy(self.input_parsed),
            )
            laser.run()
            max_energized = max(
                max_energized,
                sum(1 for row in laser.tiles for tile in row if tile.energized),
            )
            del laser

        for i in range(len(self.input_parsed[0])):
            laser = Laser(
                start=(i, 0), direction=(0, 1), tiles=copy.deepcopy(self.input_parsed)
            )
            laser.run()
            max_energized = max(
                max_energized,
                sum(1 for row in laser.tiles for tile in row if tile.energized),
            )
            del laser

            laser = Laser(
                start=(i, len(self.input_parsed) - 1),
                direction=(0, -1),
                tiles=copy.deepcopy(self.input_parsed),
            )
            laser.run()
            max_energized = max(
                max_energized,
                sum(1 for row in laser.tiles for tile in row if tile.energized),
            )
            del laser

        return max_energized

    def solve(self, part):
        if part == 1:
            self.laser = Laser(start=(0, 0), direction=(1, 0), tiles=self.input_parsed)
            self.laser.run()
            return sum(1 for row in self.input_parsed for tile in row if tile.energized)
        if part == 2:
            return self.run_lasers()


@timing_decorator
def main(raw, part):
    text_input = read_input(raw)
    input_parsed = [i if i else "" for i in text_input]
    puzzle = Puzzle(input_parsed)
    return puzzle.solve(part)


def run_tests():
    print("\nRunning Tests:")
    assert main(raw=files["test"], part=1) == 46
    assert main(raw=files["test"], part=2) == 51

    # solutions
    print("\nRunning Solutions:")
    assert main(raw=files["input"], part=1) == 6978
    assert main(raw=files["input"], part=2) == 7315  # 33s


def solve():
    print("\nSolving:")
    answer1 = main(raw=files["input"], part=1)
    print(f"Answer part1: {magenta_color}{answer1}{reset_color}")
    answer2 = main(raw=files["input"], part=2)
    print(f"Answer part2: {magenta_color}{answer2}{reset_color}")


if __name__ == "__main__":
    run_tests()
    solve()
