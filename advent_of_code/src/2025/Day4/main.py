from advent_of_code.utils.tools import get_txt_files, read_input, timing_decorator, get_adjacents_with_diagonal
from advent_of_code.utils.colors import magenta_color, reset_color

files = get_txt_files(__file__)
#########
# Start #
#########

class Puzzle:
    def __init__(self, text_input):
        self.input = text_input
        self.input_parsed = self.parse_input(self.input)
        self.acessible_count = 0
        self.to_remove = []
        self.removed = 0

    def parse_input(self, input):
        return [[digit for digit in row] for row in input]

    def check_if_valid(self):        
        for row in range(len(self.input_parsed)):
            for col in range(len(self.input_parsed[0])):
                if self.input[row][col] != '@':
                    continue
                adj = get_adjacents_with_diagonal(self.input, (row, col))
                ajacents = [ajacents for ajacents in adj]
                count = 0
                for adjacent in ajacents:
                    neighbor = self.input_parsed[adjacent[0]][adjacent[1]]
                    if neighbor == '@':
                        count += 1
                if count < 4:
                    self.acessible_count += 1

    def check_if_valid_pt2(self):
        while True:
            for row in range(len(self.input_parsed)):
                for col in range(len(self.input_parsed[0])):
                    if self.input_parsed[row][col] != '@':
                        continue
                    adj = get_adjacents_with_diagonal(self.input_parsed, (row, col))
                    ajacents = [ajacents for ajacents in adj]
                    count = 0
                    for adjacent in ajacents:
                        neighbor = self.input_parsed[adjacent[0]][adjacent[1]]
                        if neighbor == '@':
                            count += 1
                    if count < 4:
                        self.acessible_count += 1                    
                        self.to_remove.append((row, col))
            if not self.to_remove:
                break
            for item in self.to_remove:
                self.input_parsed[item[0]][item[1]] = '.'
                self.removed += 1
            self.to_remove = []
        
                    

    def solve(self, part):
        if part == 1:
            self.check_if_valid()
            return self.acessible_count
        if part == 2:
            self.check_if_valid_pt2()
            return self.removed



@timing_decorator
def main(raw, part):
    text_input = read_input(raw)
    input_parsed = [i if i else "" for i in text_input]
    puzzle = Puzzle(input_parsed)    
    return puzzle.solve(part)


def run_tests():
    print("\nRunning Tests:")
    assert main(raw=files["test"], part=1) == 13
    assert main(raw=files["test"], part=2) == 43

    # solutions
    print("\nRunning Solutions:")
    assert main(raw=files["input"], part=1) == 1424
    assert main(raw=files["input"], part=2) == 8727


def solve():
    print("\nSolving:")
    answer1 = main(raw=files["input"], part=1)
    print(f"Answer part1: {magenta_color}{answer1}{reset_color}")
    answer2 = main(raw=files["input"], part=2)
    print(f"Answer part2: {magenta_color}{answer2}{reset_color}")


if __name__ == "__main__":
    run_tests()
    solve()
