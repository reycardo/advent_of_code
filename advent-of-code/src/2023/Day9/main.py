from utils.tools import get_txt_files, read_input, timing_decorator
from utils.colors import magenta_color, reset_color

files = get_txt_files(__file__)
#########
# Start #
#########


class Sequence:
    def __init__(self, sequence):
        self.sequence = sequence
        self.differences = self.get_all_differences()
        self.extrapolated_sequence = self.extrapolate()

    def get_difference_step(self, sequence):
        return [sequence[i + 1] - sequence[i] for i in range(len(sequence) - 1)]

    def get_all_differences(self):
        sequence = self.sequence
        differences = [sequence]
        while not all(element == 0 for element in differences[-1]):
            sequence = self.get_difference_step(sequence)
            differences.append(sequence)
        return differences

    def extrapolate(self):
        self.differences[-1].append(0)
        for i in range(len(self.differences) - 1, 0, -1):
            self.differences[i - 1].append(
                self.differences[i][-1] + self.differences[i - 1][-1]
            )
        return self.differences[0]


class Puzzle:
    def __init__(self, text_input):
        self.input = text_input
        self.input_parsed = self.parse_input()
        self.sequences = [Sequence(seq) for seq in self.input_parsed]

    def parse_input(self):
        return [list(map(int, row.split(" "))) for row in self.input]

    def solve(self, part):
        if part == 1:
            return sum([seq.extrapolated_sequence[-1] for seq in self.sequences])
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
    assert main(raw=files["test"], part=1) == 114
    # assert main(raw=files["test"], part=2) == 71503

    # solutions
    print(f"\nRunning Solutions:")
    # assert main(raw=files["input"], part=1) == 503424
    # assert main(raw=files["input"], part=2) == 32607562


def solve():
    print(f"\nSolving:")
    answer1 = main(raw=files["input"], part=1)
    print(f"Answer part1: {magenta_color}{answer1}{reset_color}")
    # answer2 = main(raw=files["input"], part=2)
    # print(f"Answer part2: {magenta_color}{answer2}{reset_color}")


if __name__ == "__main__":
    run_tests()
    solve()
