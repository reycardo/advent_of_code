from utils.tools import get_txt_files, read_input, timing_decorator
from advent_of_code.utils.colors import magenta_color, reset_color

files = get_txt_files(__file__)
#########
# Start #
#########


class Puzzle:
    def __init__(self, text_input):
        self.input = text_input
        self.input_parsed = self.parse_input()
        self.increases = self.get_increases()

    def parse_input(self):
        return [list(map(int, row.split())) for row in self.input]

    def compare_elements(self, report):
        return [x - y for x, y in zip(report, report[1:])]

    def get_increases(self):
        increases = []
        for report in self.input_parsed:
            increases.append((report, self.compare_elements(report)))
        return increases

    def is_safe(self, lvl_increase):
        if (
            all(x >= 1 for x in lvl_increase) and all(x <= 3 for x in lvl_increase)
        ) or (
            all(x <= -1 for x in lvl_increase) and all(x >= -3 for x in lvl_increase)
        ):
            return True
        else:
            return False

    def check_is_safe(self, part=1):
        self.safes = []
        self.unsafes = []
        for report, lvl_increase in self.increases:
            if self.is_safe(lvl_increase):
                self.safes.append((report, lvl_increase))
            else:
                self.unsafes.append((report, lvl_increase))
        if part == 2:
            for report, lvl_increase in self.unsafes:
                for i in range(len(report)):
                    new_report = report[:i] + report[i + 1 :]
                    new_lvl_increase = self.compare_elements(new_report)
                    if self.is_safe(new_lvl_increase):
                        self.safes.append((new_report, new_lvl_increase))
                        break
        return len(self.safes)

    def solve(self, part):
        if part == 1:
            return self.check_is_safe(part=1)
        if part == 2:
            return self.check_is_safe(part=2)


@timing_decorator
def main(raw, part):
    text_input = read_input(raw)
    input_parsed = [i if i else "" for i in text_input]
    puzzle = Puzzle(input_parsed)
    return puzzle.solve(part)


def run_tests():
    print("\nRunning Tests:")
    assert main(raw=files["test"], part=1) == 2
    assert main(raw=files["test"], part=2) == 4

    # solutions
    print("\nRunning Solutions:")
    assert main(raw=files["input"], part=1) == 220
    assert main(raw=files["input"], part=2) == 296


def solve():
    print("\nSolving:")
    answer1 = main(raw=files["input"], part=1)
    print(f"Answer part1: {magenta_color}{answer1}{reset_color}")
    answer2 = main(raw=files["input"], part=2)
    print(f"Answer part2: {magenta_color}{answer2}{reset_color}")


if __name__ == "__main__":
    run_tests()
    solve()
