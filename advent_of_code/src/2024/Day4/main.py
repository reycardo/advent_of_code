from utils.tools import get_txt_files, read_input, timing_decorator
from advent_of_code.utils.colors import magenta_color, reset_color
from utils.tools import Point, Grid, Vectors

files = get_txt_files(__file__)
#########
# Start #
#########

class Puzzle:
    def __init__(self, text_input, part):
        self.input = text_input
        self.grid = Grid(self.input)
        self.word_to_match = "XMAS"
        self.directions = self.set_directions(part=part)

    def find_all(self, char_to_match):
        for x in self.grid.all_points():
            if self.grid.value_at_point(x) == char_to_match:
                yield x

    def get_all(self, char_to_match):
        return list(self.find_all(char_to_match))

    def set_directions(self, part):
        if part == 1:
            dirs = Vectors
        else:
            specific_directions = {'NE', 'SE', 'SW', 'NW'}                    
            dirs = [vector for vector in Vectors if vector.name in specific_directions]            
        return dirs
    
    def get_neighbours(self, point: Point, include_self: bool = False, scalar: int = 3):
        neighbours = []
        for i in range(1,scalar+1):
            neighbours.append(point.get_scaled_neighbours(directions=self.directions, scalar=i))        
        transposed_neighbours = list(map(list, zip(*neighbours)))        
        
        if include_self:
            for neighbour_list in transposed_neighbours:
                neighbour_list.insert(0, point)          
        
        return {cardinal: neighbours for cardinal, neighbours in zip(self.directions,transposed_neighbours)}        
            
    def find_xmas(self):
        self.xmas_count = 0
        self.words = {}
        for x in self.get_all(self.word_to_match[0]):
            self.words[x] = self.get_neighbours(x,include_self=True, scalar=3)
            for cardinal in self.directions:
                test = [self.grid.value_at_point(point) for point in self.words[x][cardinal] if self.grid.valid_location(point)]
                if self.word_to_match in "".join(test):
                    self.xmas_count += 1

    def find_x_mas(self):
        self.x_mas_count = 0
        self.words = {}        
        for x in self.get_all(self.word_to_match[2]):
            self.words[x] = self.get_neighbours(x,include_self=False, scalar=1)
            test = ''
            for cardinal in self.directions:
                test += ''.join([self.grid.value_at_point(point) for point in self.words[x][cardinal] if self.grid.valid_location(point)])
            if test in ('SSMM', 'MMSS','MSSM','SMMS'):
                self.x_mas_count += 1

    def solve(self, part):
        if part == 1:
            self.find_xmas()
            return self.xmas_count
        if part == 2:
            self.find_x_mas()
            return self.x_mas_count


@timing_decorator
def main(raw, part):
    text_input = read_input(raw)
    input_parsed = [i if i else "" for i in text_input]
    puzzle = Puzzle(input_parsed, part=part)
    return puzzle.solve(part)


def run_tests():
    print(f"\nRunning Tests:")
    assert main(raw=files["test"], part=1) == 18
    assert main(raw=files["test"], part=2) == 9

    # solutions
    print(f"\nRunning Solutions:")
    assert main(raw=files["input"], part=1) == 2547
    assert main(raw=files["input"], part=2) == 1939


def solve():
    print(f"\nSolving:")
    answer1 = main(raw=files["input"], part=1)
    print(f"Answer part1: {magenta_color}{answer1}{reset_color}")
    answer2 = main(raw=files["input"], part=2)
    print(f"Answer part2: {magenta_color}{answer2}{reset_color}")


if __name__ == "__main__":
    run_tests()
    solve()
