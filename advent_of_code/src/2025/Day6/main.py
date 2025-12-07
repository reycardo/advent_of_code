from advent_of_code.utils.tools import get_txt_files, timing_decorator
from advent_of_code.utils.colors import magenta_color, reset_color
import math

files = get_txt_files(__file__)
#########
# Start #
#########

class Puzzle:
    def __init__(self, text_input):
        self.input = text_input
        self.parse_input()
        self.replace_spaces()
        self.alignments = self.count_spaces()
        self.transposed_replaced = list(zip(*self.input_replaced))
        self.total = 0

    def count_spaces_after_each_char(self, s):
        result = []
        i = 0
        while i < len(s):
            if s[i] != ' ':
                count = 0
                j = i + 1
                while j < len(s) and s[j] == ' ':
                    count += 1
                    j += 1
                result.append(count)
            i += 1
        return result

    def replace_spaces(self):
        self.input_replaced = [row.replace(' ', '_') for row in self.input]

    def count_spaces(self):
        spaces = self.count_spaces_after_each_char(self.input[-1])
        natural_space_removed = spaces[:-1] + [spaces[-1] + 1]
        cumulative = []
        total = 0
        for n in natural_space_removed:
            total += n
            cumulative.append(total)
        return cumulative


    def parse_input(self):
        self.input_parsed = [row.split() for row in self.input if row]
        self.transposed_input = list(zip(*self.input_parsed))

    def apply_operation(self):
        for problem in self.transposed_input:
            operation = problem[-1]
            numbers = list(map(int, problem[:-1]))
            if operation == "+":
                self.total += sum(numbers)
            elif operation == "*":
                self.total += math.prod(numbers)

    def apply_operation_pt2(self):
        numbers = [self.tuple_to_int(problem[:-1]) for problem in self.transposed_replaced if problem != ('_',)*len(problem)]
        operations = [problem[-1] for problem in self.transposed_input if problem != ('_',)*len(problem)]
        start = 0
        for i, end in enumerate(self.alignments):
            if operations[i] == "+":
                self.total += sum(numbers[start:end])
            elif operations[i] == "*":
                self.total += math.prod(numbers[start:end])
            start = end


    def tuple_to_int(self, t):
        return int(''.join(c for c in t if c.isdigit()))

    def solve(self, part):
        if part == 1:
            self.apply_operation()
            return self.total
        if part == 2:
            self.apply_operation_pt2()
            return self.total

def read_input(file, sep: str = "\n"):
    with open(file, "r") as tf:
        return tf.read().split(sep)

@timing_decorator
def main(raw, part):
    text_input = read_input(raw)
    input_parsed = [i if i else "" for i in text_input]
    puzzle = Puzzle(input_parsed)
    return puzzle.solve(part)


def run_tests():
    print("\nRunning Tests:")
    assert main(raw=files["test"], part=1) == 4277556
    assert main(raw=files["test"], part=2) == 3263827

    # solutions
    print("\nRunning Solutions:")
    assert main(raw=files["input"], part=1) == 5060053676136
    assert main(raw=files["input"], part=2) == 9695042567249


def solve():
    print("\nSolving:")
    answer1 = main(raw=files["input"], part=1)
    print(f"Answer part1: {magenta_color}{answer1}{reset_color}")
    answer2 = main(raw=files["input"], part=2)
    print(f"Answer part2: {magenta_color}{answer2}{reset_color}")


if __name__ == "__main__":
    run_tests()
    solve()
