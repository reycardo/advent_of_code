from utils.tools import get_txt_files, read_input, timing_decorator
from utils.colors import magenta_color, reset_color
from itertools import groupby

files = get_txt_files(__file__)
#########
# Start #
#########

class Puzzle:
    def __init__(self, text_input):
        self.input = text_input        
        self.input_parsed = [[point for point in row] for row in self.input]

    def get_column(self, matrix, column_nr):
        return [row[column_nr] for row in matrix]

    def get_row(self, matrix, row_nr):
        return matrix[row_nr]

    def tilt(self, line: list, direction):
        if all(x == '#' for x in line):
            return line
        round_rocks = line.count('O')
        if direction == "l":            
            new_line = ['O'] * round_rocks + ['.'] * (len(line) - round_rocks)
        if direction == "r":            
            new_line = ['.'] * (len(line) - round_rocks) + ['O'] * round_rocks
        return new_line
        
    def split_list(self, line, separator='#'):
        return [list(group) for _, group in groupby(line, lambda x: x == separator)]

    def tilt_all(self, matrix, direction):
        tilted = []
        matrix_len = len(matrix)
        matrix_0_len = len(matrix[0])        
        if direction == 'north':
            for i in range(matrix_0_len):
                line = self.get_column(matrix, i)
                splitted_lines = self.split_list(line, separator='#')
                result = [item for sublist in splitted_lines for item in self.tilt(sublist, 'l')]
                tilted.append(result)
                tilted_final = list(map(list, zip(*tilted)))                
        elif direction == 'south':
            for i in range(matrix_0_len):
                line = self.get_column(matrix, i)
                splitted_lines = self.split_list(line, separator='#')
                result = [item for sublist in splitted_lines for item in self.tilt(sublist, 'r')]
                tilted.append(result)
                tilted_final = list(map(list, zip(*tilted)))     
        elif direction == 'east':
            for i in range(matrix_len):
                line = self.get_row(matrix, i)
                splitted_lines = self.split_list(line, separator='#')
                result = [item for sublist in splitted_lines for item in self.tilt(sublist, 'r')]
                tilted.append(result)
                tilted_final = tilted
        elif direction == 'west':
            for i in range(matrix_len):
                line = self.get_row(matrix, i)
                splitted_lines = self.split_list(line, separator='#')
                result = [item for sublist in splitted_lines for item in self.tilt(sublist, 'l')]
                tilted.append(result)
                tilted_final = tilted
        else:
            raise ValueError("invalid direction: " + direction)
        return tilted_final

    def cycle(self, iterations):
        matrix = self.input_parsed
        seen = {str(matrix): 0}  # Keep track of when each state was seen
        for i in range(1, iterations + 1):
            matrix = self.tilt_all(matrix=matrix, direction='north')
            matrix = self.tilt_all(matrix=matrix, direction='west')
            matrix = self.tilt_all(matrix=matrix, direction='south')
            matrix = self.tilt_all(matrix=matrix, direction='east')
            matrix_str = str(matrix)
            if matrix_str in seen:
                cycle_length = i - seen[matrix_str]
                remaining_iterations = (iterations - i) % cycle_length
                for _ in range(remaining_iterations):
                    matrix = self.tilt_all(matrix=matrix, direction='north')
                    matrix = self.tilt_all(matrix=matrix, direction='west')
                    matrix = self.tilt_all(matrix=matrix, direction='south')
                    matrix = self.tilt_all(matrix=matrix, direction='east')
                break 
            seen[matrix_str] = i
        return matrix

    def solve(self, part):
        if part == 1:
            self.tilted = self.tilt_all(matrix=self.input_parsed, direction='north')        
        if part == 2:
            self.tilted = self.cycle(1000000000)
        if part == 3:
            self.tilted = self.cycle(3)            
        return sum([row.count('O') * (len(self.tilted)-i) for i, row in enumerate(self.tilted)])


@timing_decorator
def main(raw, part):
    text_input = read_input(raw)
    input_parsed = [i if i else "" for i in text_input]
    puzzle = Puzzle(input_parsed)
    return puzzle.solve(part)


def run_tests():
    print(f"\nRunning Tests:")
    assert main(raw=files["test"], part=1) == 136
    assert main(raw=files["test"], part=3) == 69
    assert main(raw=files["test"], part=2) == 64

    # solutions
    print(f"\nRunning Solutions:")
    assert main(raw=files["input"], part=1) == 109939
    # assert main(raw=files["input"], part=2) == 32607562


def solve():
    print(f"\nSolving:")
    answer1 = main(raw=files["input"], part=1)
    print(f"Answer part1: {magenta_color}{answer1}{reset_color}")
    answer2 = main(raw=files["input"], part=2)
    print(f"Answer part2: {magenta_color}{answer2}{reset_color}")


if __name__ == "__main__":
    run_tests()
    solve()
