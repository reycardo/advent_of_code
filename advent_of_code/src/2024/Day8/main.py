from advent_of_code.utils.tools import get_txt_files, read_input, timing_decorator
from advent_of_code.utils.colors import magenta_color, reset_color
from advent_of_code.utils.tools import Grid, Point
from typing import Dict, List

files = get_txt_files(__file__)
#########
# Start #
#########


class Puzzle:
    def __init__(self, text_input, part):
        self.input = text_input
        self.input_parsed = [list(line) for line in self.input]
        self.grid = Grid(self.input_parsed)
        self.available_chars: Dict[str, List[Point]] = {}
        self.get_all_chars()
        self.find_all_antinodes(part)

    def get_all_chars(self):
        for point in self.grid._all_points:
            char = self.grid.value_at_point(point=point)
            if char != ".":
                if char in self.available_chars:
                    self.available_chars[char].append(point)
                else:
                    self.available_chars[char] = [point]

    def get_antinodes_of_point(self, current_point: Point, points: List[Point]):
        antinodes = []
        for target_point in points:
            if current_point != target_point:
                antinode = current_point + (current_point - target_point)
                if self.grid.valid_location(antinode):
                    antinodes.append(antinode)
        return antinodes

    def get_all_antinodes_of_point(self, current_point: Point, points: List[Point]):
        antinodes = []
        for target_point in points:
            if current_point != target_point:
                pos_valid = True
                neg_valid = True
                i = 0
                j = -1
                while pos_valid:
                    antinode = current_point + Point(i, i) * (
                        current_point - target_point
                    )
                    if self.grid.valid_location(antinode):
                        antinodes.append(antinode)
                        i += 1
                    else:
                        pos_valid = False
                while neg_valid:
                    antinode = current_point - Point(j, j) * (
                        current_point - target_point
                    )
                    if self.grid.valid_location(antinode):
                        antinodes.append(antinode)
                        j -= 1
                    else:
                        neg_valid = False
        return antinodes

    def find_all_antinodes(self, part):
        self.antinodes = {}
        for char, points in self.available_chars.items():
            all_antinodes = []
            for point in points:
                if part == 1:
                    point_antinodes = self.get_antinodes_of_point(
                        current_point=point, points=points
                    )
                elif part == 2:
                    point_antinodes = self.get_all_antinodes_of_point(
                        current_point=point, points=points
                    )

                all_antinodes.extend(point_antinodes)
            self.antinodes[char] = all_antinodes

    def count_unique_points(self) -> int:
        unique_points = set()
        for points in self.antinodes.values():
            unique_points.update(points)
        return len(unique_points)

    def solve(self):
        return self.count_unique_points()


@timing_decorator
def main(raw, part):
    text_input = read_input(raw)
    input_parsed = [i if i else "" for i in text_input]
    puzzle = Puzzle(input_parsed, part)
    return puzzle.solve()


def run_tests():
    print("\nRunning Tests:")
    assert main(raw=files["test"], part=1) == 14
    assert main(raw=files["test"], part=2) == 34

    # solutions
    print("\nRunning Solutions:")
    assert main(raw=files["input"], part=1) == 303
    assert main(raw=files["input"], part=2) == 1045


def solve():
    print("\nSolving:")
    answer1 = main(raw=files["input"], part=1)
    print(f"Answer part1: {magenta_color}{answer1}{reset_color}")
    answer2 = main(raw=files["input"], part=2)
    print(f"Answer part2: {magenta_color}{answer2}{reset_color}")


if __name__ == "__main__":
    run_tests()
    solve()
