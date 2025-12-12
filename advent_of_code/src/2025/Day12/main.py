from advent_of_code.utils.tools import get_txt_files, read_input, timing_decorator
from advent_of_code.utils.colors import magenta_color, reset_color
from itertools import groupby

files = get_txt_files(__file__)
#########
# Start #
#########

        

class Present:
    def __init__(self, input):
        self.id = input[0]
        self.shape = input[1:]
        self.area = 9 # checking if a 3x3 grid fits
        # self.area = self.get_area()

    def get_area(self):
        return sum(row.count('#') for row in self.shape)

    def __repr__(self):
        return f"Present(id={self.id}, shape={self.shape}), area={self.area})"


class Region:
    def __init__(self, input):
        dimensions, quantities = input.split(':')
        self.width, self.length = tuple(map(int, dimensions.split('x')))
        self.quantity_of_each_shape = list(map(int, quantities.split()[1:]))

    def __repr__(self):
        return f"Region(width={self.width}, length={self.length}, quantity_of_each_shape={self.quantity_of_each_shape})"

    def check_if_presents_area_fits(self, presents: list[Present]):
        area_available = self.width * self.length
        total_area_needed = 0
        for id, number_of_presents in enumerate(self.quantity_of_each_shape):
            present_area = presents[id].area
            total_area_needed += present_area * number_of_presents
            if total_area_needed > area_available:
                return False
        return True
            


class Puzzle:
    def __init__(self, text_input):
        self.input = text_input
        self.split_input()


    def split_input(self):                
        region_start = next(i for i, line in enumerate(self.input) if 'x' in line)
        presents_lines = self.input[:region_start]
        regions_lines = self.input[region_start:]
        
        presents = [list(group) for key, group in groupby(presents_lines, lambda x: x == "") if not key]
        self.presents = [Present(shape) for shape in presents]
        self.regions = [Region(region) for region in regions_lines if region]

    def check_fits(self):
        results = []
        for region in self.regions:
            fits = region.check_if_presents_area_fits(self.presents)
            results.append(fits)
        return results


    def solve(self, part):
        if part == 1:
            fits = self.check_fits()
            return sum(fits)


@timing_decorator
def main(raw, part):
    text_input = read_input(raw)
    input_parsed = [i if i else "" for i in text_input]
    puzzle = Puzzle(input_parsed)    
    return puzzle.solve(part)


def run_tests():
    print("\nRunning Tests:")
    # assert main(raw=files["test"], part=1) == 2    

    # solutions
    print("\nRunning Solutions:")
    assert main(raw=files["input"], part=1) == 485    


def solve():
    print("\nSolving:")
    answer1 = main(raw=files["input"], part=1)
    print(f"Answer part1: {magenta_color}{answer1}{reset_color}")


if __name__ == "__main__":
    run_tests()
    solve()
