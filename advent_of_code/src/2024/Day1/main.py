from advent_of_code.utils.tools import get_txt_files, read_input, timing_decorator
from advent_of_code.utils.colors import magenta_color, reset_color

files = get_txt_files(__file__)
#########
# Start #
#########

class Puzzle:
    def __init__(self, text_input):
        self.input = text_input
        self.left, self.right = self.separate_lists()
        self.ordered_left, self.ordered_right = self.order_lists()
        self.difs = self.calculate_difs()

    def separate_lists(self):
        left = []
        right = []

        for item in self.input:
            parts = item.split()
            left.append(int(parts[0]))
            right.append(int(parts[1]))
        return left, right
    
    def order_lists(self):        
        return sorted(self.left), sorted(self.right)

    def calculate_difs(self):
        return [abs(left - right) for left, right in zip(self.ordered_left, self.ordered_right)]

    def sum_difs(self):
        return sum(self.difs)

    def calc_similarity(self):
        similarity = 0
        for left_element in self.ordered_left:
            similarity += self.ordered_right.count(left_element) * left_element
        return similarity


    def solve(self, part):
        if part == 1:
            return self.sum_difs()
        if part == 2:
            return self.calc_similarity()


@timing_decorator
def main(raw, part):
    text_input = read_input(raw)
    input_parsed = [i if i else "" for i in text_input]
    puzzle = Puzzle(input_parsed)
    puzzle.solve(part)
    return puzzle.solve(part)


def run_tests():
    print(f"\nRunning Tests:")
    assert main(raw=files["test"], part=1) == 11
    assert main(raw=files["test"], part=2) == 31

    # solutions
    print(f"\nRunning Solutions:")
    assert main(raw=files["input"], part=1) == 1319616
    assert main(raw=files["input"], part=2) == 27267728


def solve():
    print(f"\nSolving:")
    answer1 = main(raw=files["input"], part=1)
    print(f"Answer part1: {magenta_color}{answer1}{reset_color}")
    answer2 = main(raw=files["input"], part=2)
    print(f"Answer part2: {magenta_color}{answer2}{reset_color}")


if __name__ == "__main__":
    run_tests()
    solve()
