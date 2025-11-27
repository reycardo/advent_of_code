from utils.tools import get_txt_files, read_input, timing_decorator
from advent_of_code.utils.colors import magenta_color, reset_color
import re

files = get_txt_files(__file__)
#########
# Start #
#########

class Puzzle:
    def __init__(self, text_input):
        self.input = self.flatten_input(text_input)

    def flatten_input(self, text_input):
        return '\n'.join(text_input)

    def split_string(self, text, delimiters):
        pattern = '|'.join(map(re.escape, delimiters))
        parts = re.split(f'({pattern})', text)
        result = {}
        # mul instructions enabled at the beginning: delimiters[1] = do
        result[delimiters[1]] = [parts[0]]
        # parts:
        # [mul, do, mul, dont, mul]
        # [mul, don't, mul, do, mul]
        # even stuff is the delimiter
        for i in range(1, len(parts), 2):
            delimiter = parts[i]
            value = parts[i + 1] if i + 1 < len(parts) else ''
            if delimiter in result:
                result[delimiter].append(value)
            else:
                result[delimiter] = [value]
        return result



    def find_mul_patterns(self, string):
        pattern = r'mul\(\d{1,3},\d{1,3}\)'
        matches = re.findall(pattern, string)
        return matches

    def do_instructions(self, entry):
        calculations = []
        for operation in entry:
            # Extract the numbers from the operation
            numbers = re.findall(r'\d{1,3}', operation)
            x, y = map(int, numbers)
            result = x * y
            calculations.append(result)
        return calculations

    def solve(self, part):
        if part == 1:
            self.muls = self.find_mul_patterns(self.input)
            self.result = self.do_instructions(self.muls)            
            return sum(self.result)
        if part == 2:
            delimiters = ["don't()","do()"]
            self.input_delimited = self.split_string(self.input,delimiters)            
            self.do_muls = self.find_mul_patterns(self.flatten_input(self.input_delimited['do()']))
            self.result_2 = self.do_instructions(self.do_muls)
            return sum(self.result_2)


@timing_decorator
def main(raw, part):
    text_input = read_input(raw)
    puzzle = Puzzle(text_input)
    puzzle.solve(part)
    return puzzle.solve(part)


def run_tests():
    print(f"\nRunning Tests:")
    assert main(raw=files["test"], part=1) == 161
    assert main(raw=files["test2"], part=1) == 0
    assert main(raw=files["test3"], part=1) == 0
    assert main(raw=files["test4"], part=1) == 0
    assert main(raw=files["test5"], part=2) == 48

    # solutions
    print(f"\nRunning Solutions:")
    assert main(raw=files["input"], part=1) == 178886550
    assert main(raw=files["input"], part=2) == 87163705


def solve():
    print(f"\nSolving:")
    answer1 = main(raw=files["input"], part=1)
    print(f"Answer part1: {magenta_color}{answer1}{reset_color}")
    answer2 = main(raw=files["input"], part=2)
    print(f"Answer part2: {magenta_color}{answer2}{reset_color}")


if __name__ == "__main__":
    run_tests()
    solve()
