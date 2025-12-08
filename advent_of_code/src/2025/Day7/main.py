from advent_of_code.utils.tools import get_txt_files, read_input, timing_decorator, is_inside
from advent_of_code.utils.colors import magenta_color, reset_color
from functools import cache

files = get_txt_files(__file__)
#########
# Start #
#########

split_positions = []

class Tachyon:
    def __init__(self, position):
        self.position = position
        self.velocity = (1, 0)

    def move(self, grid):        
        if not is_inside(grid, self.position):
            return
        self.new_position = (self.position[0] + self.velocity[0], self.position[1] + self.velocity[1])
        if grid[self.new_position[0]][self.new_position[1]] == '^':
            self.split(self.new_position, grid)
        elif grid[self.new_position[0]][self.new_position[1]] == '|':            
            return
        else:
            grid[self.new_position[0]][self.new_position[1]] = '|'
            self.position = self.new_position
            self.move(grid)


    def split(self, position, grid):               
        if position in split_positions:
            return
        split_positions.append(position)
        left_tachyon_pos = (position[0], position[1] - 1)
        right_tachyon_pos = (position[0], position[1] + 1)
        if is_inside(grid, right_tachyon_pos) and grid[right_tachyon_pos[0]][right_tachyon_pos[1]] != '|':
            grid[right_tachyon_pos[0]][right_tachyon_pos[1]] = '|'
            Tachyon(right_tachyon_pos).move(grid)
        if is_inside(grid, left_tachyon_pos) and grid[left_tachyon_pos[0]][left_tachyon_pos[1]] != '|':
            grid[left_tachyon_pos[0]][left_tachyon_pos[1]] = '|'
            Tachyon(left_tachyon_pos).move(grid)



class Puzzle:
    def __init__(self, text_input):
        self.input = text_input
        self.parse_input()
        self.start = (0,self.input_parsed[0].index('S'))
        self.tachyons = [Tachyon(self.start)]

    def move_tachyons(self):
        for tachyon in self.tachyons:
            tachyon.move(self.input_parsed)

    def parse_input(self):
        self.input_parsed = [[char for char in row] for row in self.input]

    @cache
    def count_timelines(self, position):
        if not is_inside(self.input_parsed, position):
            return 1
        if self.input_parsed[position[0]][position[1]] == '^':
            return self.count_timelines((position[0], position[1] - 1)) + self.count_timelines((position[0], position[1] + 1))
        else:
            return self.count_timelines((position[0] + 1, position[1]))
        

    def solve(self, part):
        if part == 1:
            self.move_tachyons()
            return len(set(split_positions))

        if part == 2:
            count = self.count_timelines(self.start)
            return count

@timing_decorator
def main(raw, part):
    text_input = read_input(raw)
    input_parsed = [i if i else "" for i in text_input]
    puzzle = Puzzle(input_parsed)
    return puzzle.solve(part)


def run_tests():
    print("\nRunning Tests:")
    assert main(raw=files["test"], part=1) == 21
    assert main(raw=files["test"], part=2) == 40

    # solutions
    print("\nRunning Solutions:")
    assert main(raw=files["input"], part=1) == 1566
    assert main(raw=files["input"], part=2) == 5921061943075


def solve():
    print("\nSolving:")
    answer1 = main(raw=files["input"], part=1)
    print(f"Answer part1: {magenta_color}{answer1}{reset_color}")
    answer2 = main(raw=files["input"], part=2)
    print(f"Answer part2: {magenta_color}{answer2}{reset_color}")


if __name__ == "__main__":
    run_tests()
    solve()
