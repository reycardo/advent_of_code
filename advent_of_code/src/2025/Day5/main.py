from advent_of_code.utils.tools import get_txt_files, read_input, timing_decorator
from advent_of_code.utils.colors import magenta_color, reset_color

files = get_txt_files(__file__)
#########
# Start #
#########

class Puzzle:
    def __init__(self, text_input):
        self.input = text_input
        self.split_input()        

    def split_input(self):
        separator_index = self.input.index("")
        self.ranges = [[int(ranges.split('-')[0]), int(ranges.split('-')[1])] for ranges in self.input[:separator_index]]
        self.ids = [int(ids) for ids in self.input[separator_index + 1 :]]                    

    def check_if_id_is_fresh(self, id):
        for range in self.ranges:
            if range[0] <= id <= range[1]:
                return True
        return False
    
    def check_fresh_ids(self):
        fresh_ids = 0
        for id in self.ids:
            if self.check_if_id_is_fresh(id):
                fresh_ids += 1
        return fresh_ids

    def count_distinct_ids_in_ranges(self):
        self.sorted_ranges = sorted(self.ranges, key=lambda x: x[0])

        # loop over i and i+1
        for i in range(len(self.sorted_ranges) - 1):
            current_range = self.sorted_ranges[i]
            next_range = self.sorted_ranges[i + 1]
            # if the next range start is less than or equal to the current range end, merge them
            if next_range[0] <= current_range[1]:
                merged_range = [current_range[0], max(current_range[1], next_range[1])]
                self.sorted_ranges[i + 1] = merged_range
                self.sorted_ranges[i] = None
        
        # filter Nones
        self.merged_ranges = [r for r in self.sorted_ranges if r is not None]
        distinct_ids = 0
        for range_ in self.merged_ranges:
            distinct_ids += range_[1] - range_[0] + 1 # (3,5) -> 3 , 4 , 5 => 5 - 3 + 1
        return distinct_ids

    def solve(self, part):
        if part == 1:
            return self.check_fresh_ids()
        if part == 2:
            return self.count_distinct_ids_in_ranges()



@timing_decorator
def main(raw, part):
    text_input = read_input(raw)
    input_parsed = [i if i else "" for i in text_input]
    puzzle = Puzzle(input_parsed)    
    return puzzle.solve(part)


def run_tests():
    print("\nRunning Tests:")
    assert main(raw=files["test"], part=1) == 3
    assert main(raw=files["test"], part=2) == 14

    # solutions
    print("\nRunning Solutions:")
    assert main(raw=files["input"], part=1) == 638
    assert main(raw=files["input"], part=2) == 352946349407338


def solve():
    print("\nSolving:")
    answer1 = main(raw=files["input"], part=1)
    print(f"Answer part1: {magenta_color}{answer1}{reset_color}")
    answer2 = main(raw=files["input"], part=2)
    print(f"Answer part2: {magenta_color}{answer2}{reset_color}")


if __name__ == "__main__":
    run_tests()
    solve()
