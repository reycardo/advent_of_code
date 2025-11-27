from advent_of_code.utils.tools import get_txt_files, read_input, timing_decorator
from advent_of_code.utils.colors import magenta_color, reset_color

files = get_txt_files(__file__)
#########
# Start #
#########


class Puzzle:
    def __init__(self, text_input):
        self.input = text_input
        self.parse_input()
        self.wire1_path = self.wire_path(self.wire1)
        self.wire2_path = self.wire_path(self.wire2)
        self.intersections = self.find_intersections()

    def parse_input(self):
        self.wire1 = self.input[0].split(",")
        self.wire2 = self.input[1].split(",")

    def wire_path(self, wire):
        path = []
        x, y = 0, 0
        for i in wire:
            direction = i[0]
            distance = int(i[1:])
            for _ in range(distance):
                if direction == "U":
                    y += 1
                elif direction == "D":
                    y -= 1
                elif direction == "L":
                    x -= 1
                elif direction == "R":
                    x += 1
                path.append((x, y))
        return path

    def find_intersections(self):
        return set(self.wire1_path).intersection(self.wire2_path)

    def find_steps_to_intersection(self):
        return {
            intersection: self.wire1_path.index(intersection)
            + self.wire2_path.index(intersection)
            + 2
            for intersection in self.intersections
        }

    def closest_intersection_to_origin(self):
        return min([abs(x) + abs(y) for x, y in self.intersections])

    def solve(self, part):
        if part == 1:
            return self.closest_intersection_to_origin()
        if part == 2:
            return min(self.find_steps_to_intersection().values())


@timing_decorator
def main(raw, part):
    text_input = read_input(raw)
    input_parsed = [i if i else "" for i in text_input]
    puzzle = Puzzle(input_parsed)
    puzzle.solve(part)
    return puzzle.solve(part)


def run_tests():
    print("\nRunning Tests:")
    assert main(raw=files["test"], part=1) == 6
    assert main(raw=files["test2"], part=1) == 159
    assert main(raw=files["test3"], part=1) == 135
    assert main(raw=files["test"], part=2) == 30
    assert main(raw=files["test2"], part=2) == 610
    assert main(raw=files["test3"], part=2) == 410

    # solutions
    print("\nRunning Solutions:")
    assert main(raw=files["input"], part=1) == 227
    # assert main(raw=files["input"], part=2) == 296


def solve():
    print("\nSolving:")
    answer1 = main(raw=files["input"], part=1)
    print(f"Answer part1: {magenta_color}{answer1}{reset_color}")
    answer2 = main(raw=files["input"], part=2)
    print(f"Answer part2: {magenta_color}{answer2}{reset_color}")


if __name__ == "__main__":
    run_tests()
    solve()
