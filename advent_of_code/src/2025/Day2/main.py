from advent_of_code.utils.tools import get_txt_files, read_input, timing_decorator
from advent_of_code.utils.colors import magenta_color, reset_color

files = get_txt_files(__file__)
#########
# Start #
#########


class Puzzle:
    def __init__(self, text_input):
        self.input = text_input
        self.input_parsed = self.parse_input()
        self.invalid_ids: dict[str, list[int]] = {}

    def parse_input(self):
        input_parsed = self.input[0].split(",")
        return input_parsed

    def run_validation(self, part):
        for id in self.input_parsed:
            lower, upper = int(id.split("-")[0]), int(id.split("-")[1])
            self.invalid_ids[id] = self.detect_invalid_ids(lower, upper, part=part)

    def next_length_number(self, n, division=2):
        n = int(n)
        length = len(str(n))
        if length % division == 0:
            return n  # Already division length
        # Next division length is 10**length
        return 10 ** length

    def detect_invalid_ids(self, range_start, range_end, part=1):
        invalid_ids = []
        if part == 1:
            divide_cap = 2
        else:
            divide_cap = len(str(range_end))
        for n in range(2, divide_cap + 1):
            id_to_check = self.next_length_number(range_start, division=n)
            self.check_sequences(invalid_ids, id_to_check, range_start, range_end, n)
        return invalid_ids

    def check_sequences(self, invalid_ids: list, id_to_check, range_start, range_end, n):
        if id_to_check > range_end:
            return
        sequence = str(id_to_check)[:len(str(id_to_check)) // n]
        candidate = int(sequence * n)
        if range_start <= candidate <= range_end:
            if candidate not in invalid_ids:
                invalid_ids.append(candidate)
        next_id = int(str(int(sequence) + 1) * n)
        self.check_sequences(invalid_ids, next_id, range_start, range_end, n)
        
    def solve(self, part):
        self.run_validation(part=part)
        return sum(sum(ids) for ids in self.invalid_ids.values())


@timing_decorator
def main(raw, part):
    text_input = read_input(raw)
    input_parsed = [i if i else "" for i in text_input]
    puzzle = Puzzle(input_parsed)    
    return puzzle.solve(part)


def run_tests():
    print("\nRunning Tests:")
    assert main(raw=files["test"], part=1) == 1227775554
    assert main(raw=files["test2"], part=1) == 0
    assert main(raw=files["test"], part=2) == 4174379265
    assert main(raw=files["test3"], part=2) == 111 + 99
    

    # solutions
    print("\nRunning Solutions:")
    assert main(raw=files["input"], part=1) == 37314786486
    assert main(raw=files["input"], part=2) == 47477053982


def solve():
    print("\nSolving:")
    answer1 = main(raw=files["input"], part=1)
    print(f"Answer part1: {magenta_color}{answer1}{reset_color}")
    answer2 = main(raw=files["input"], part=2)
    print(f"Answer part2: {magenta_color}{answer2}{reset_color}")


if __name__ == "__main__":
    run_tests()
    solve()
