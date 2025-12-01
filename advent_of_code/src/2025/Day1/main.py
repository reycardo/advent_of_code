from advent_of_code.utils.tools import get_txt_files, read_input, timing_decorator
from advent_of_code.utils.colors import magenta_color, reset_color

files = get_txt_files(__file__)
#########
# Start #
#########


class Puzzle:
    def __init__(self, text_input):
        self.input = text_input
        self.init_state = 50
        self.total_clicks = 100
        self.current_state = self.init_state
        self.count_of_zeros = 0

    def run_rotations(self):
        for rotation in self.input:            
            lr = rotation[0]
            distance = int(rotation[1:])
            self.current_state += distance if lr == "R" else -distance
            self.current_state %= 100
            if self.current_state == 0:
                self.count_of_zeros += 1

    def run_rotations_pt2(self):
        for rotation in self.input:
            lr = rotation[0]
            distance = int(rotation[1:])
            new_state = self.current_state + distance if lr == "R" else self.current_state - distance
            previous_state = self.current_state
            self.current_state = new_state % 100
            if previous_state == 0:
                self.count_of_zeros += abs(new_state) // 100
            else:                
                if lr == "R":
                    crosses = new_state // 100
                    self.count_of_zeros += crosses
                else:  
                    # Moving left                    
                    self.count_of_zeros += abs(new_state // 100)
                    
                    # Special case when we land exactly on 0 going left (not taken into account by %)
                    if self.current_state == 0:
                        self.count_of_zeros += 1


    def solve(self, part):
        if part == 1:
            self.run_rotations()
            return self.count_of_zeros
        if part == 2:
            self.run_rotations_pt2()
            return self.count_of_zeros


@timing_decorator
def main(raw, part):
    text_input = read_input(raw)
    input_parsed = [i if i else "" for i in text_input]
    puzzle = Puzzle(input_parsed)    
    return puzzle.solve(part)


def run_tests():
    print("\nRunning Tests:")
    assert main(raw=files["test"], part=1) == 3
    assert main(raw=files["test5"], part=2) == 2 # test left twice over zero
    assert main(raw=files["test4"], part=2) == 1 # test left on top of zero once
    assert main(raw=files["test3"], part=2) == 1 # test left once over zero
    assert main(raw=files["test2"], part=2) == 2 # test hit zero, then loop right
    assert main(raw=files["test"], part=2) == 6

    # solutions
    print("\nRunning Solutions:")
    assert main(raw=files["input"], part=1) == 1036
    assert main(raw=files["input"], part=2) == 6228


def solve():
    print("\nSolving:")
    answer1 = main(raw=files["input"], part=1)
    print(f"Answer part1: {magenta_color}{answer1}{reset_color}")
    answer2 = main(raw=files["input"], part=2)
    print(f"Answer part2: {magenta_color}{answer2}{reset_color}")


if __name__ == "__main__":
    run_tests()
    solve()
