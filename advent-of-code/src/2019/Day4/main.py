from utils.tools import get_txt_files, read_input, timing_decorator
from utils.colors import magenta_color, reset_color
import re

files = get_txt_files(__file__)
#########
# Start #
#########


class Puzzle:
    def __init__(self, text_input):
        self.input = text_input
        self.range = self.parse_input()        

    
    def parse_input(self):
        return list(map(int, self.input[0].split("-")))

    def solve(self, part):
        result = 0
        for number in range(self.range[0], self.range[1]):
            password = [int(digit) for digit in str(number)]
            if password != sorted(password):
                continue

            for digit in password:           
                if part == 1:
                    if password.count(digit) >= 2:
                        result += 1
                        break
                elif part == 2:
                    if password.count(digit) == 2:
                        result += 1
                        break
        return result


@timing_decorator
def main(raw, part):
    text_input = read_input(raw)
    input_parsed = [i if i else "" for i in text_input]
    puzzle = Puzzle(input_parsed)    
    return puzzle.solve(part)


def run_tests():
    print(f"\nRunning Tests:")
    print(f"\nNO TESTS")

    # solutions
    print(f"\nRunning Solutions:")
    # assert main(raw=files["input"], part=1) == 960
    # assert main(raw=files["input"], part=2) == 296


def solve():
    print(f"\nSolving:")
    answer1 = main(raw=files["input"], part=1)
    print(f"Answer part1: {magenta_color}{answer1}{reset_color}")
    answer2 = main(raw=files["input"], part=2)
    print(f"Answer part2: {magenta_color}{answer2}{reset_color}")


if __name__ == "__main__":
    run_tests()
    solve()
