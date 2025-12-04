from advent_of_code.utils.tools import get_txt_files, read_input, timing_decorator
from advent_of_code.utils.colors import magenta_color, reset_color

files = get_txt_files(__file__)
#########
# Start #
#########


class Puzzle:
    def __init__(self, text_input):
        self.input = text_input        
        self.largest_joltage = {}

    def turn_on_bateries(self, bank, n=2):
        original_bank = bank
        best_joltage = [jolt for jolt in bank[:n]]
        for i in range(n,0,-1):
            max_in_bank = max(bank[:-(i-1)]) if i > 1 else max(bank)
            best_joltage[n-i] = max_in_bank
            bank = bank[bank.index(best_joltage[n-i]) + 1 :]
        self.largest_joltage[original_bank] = int(''.join(best_joltage))


    def find_joltage(self, n):
        for bank in self.input:
            self.turn_on_bateries(bank=bank,n=n)

    def solve(self, part):
        if part == 1:
            self.find_joltage(n=2)
            soma = sum(ids for ids in self.largest_joltage.values())
            return soma
        if part == 2:
            self.find_joltage(n=12)
            soma = sum(ids for ids in self.largest_joltage.values())
            return soma


@timing_decorator
def main(raw, part):
    text_input = read_input(raw)
    input_parsed = [i if i else "" for i in text_input]
    puzzle = Puzzle(input_parsed)    
    return puzzle.solve(part)


def run_tests():
    print("\nRunning Tests:")
    assert main(raw=files["test"], part=1) == 357
    assert main(raw=files["test"], part=2) == 3121910778619

    # solutions
    print("\nRunning Solutions:")
    assert main(raw=files["input"], part=1) == 17412
    assert main(raw=files["input"], part=2) == 172681562473501


def solve():
    print("\nSolving:")
    answer1 = main(raw=files["input"], part=1)
    print(f"Answer part1: {magenta_color}{answer1}{reset_color}")
    answer2 = main(raw=files["input"], part=2)
    print(f"Answer part2: {magenta_color}{answer2}{reset_color}")


if __name__ == "__main__":
    run_tests()
    solve()
