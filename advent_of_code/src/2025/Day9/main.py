
from itertools import combinations
from shapely.geometry import Polygon, box
from advent_of_code.utils.tools import get_txt_files, read_input, timing_decorator
from advent_of_code.utils.colors import magenta_color, reset_color

files = get_txt_files(__file__)

class Rectangle:
    # Represented by two opposite corners
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        self.min_x = min(p1[0], p2[0])
        self.max_x = max(p1[0], p2[0])
        self.min_y = min(p1[1], p2[1])
        self.max_y = max(p1[1], p2[1])
        self.area = (self.max_x - self.min_x + 1) * (self.max_y - self.min_y + 1)
    
    def __getitem__(self, key):
        return getattr(self, key)
    
    def __repr__(self):
        return f"Rectangle(({self.min_x}, {self.min_y}), ({self.max_x}, {self.max_y}), area={self.area})"

class Puzzle:
    def __init__(self, text_input):
        self.input = text_input
        self.red_tiles = [tuple(map(int, row.split(','))) for row in self.input]        
        self.polygon = Polygon(self.red_tiles)

    def get_max_area(self):
        # Part 1: largest rectangle defined by any two red tiles (no containment check)
        rects = [
            Rectangle(p1, p2)
            for p1, p2 in combinations(self.red_tiles, 2)
        ]
        return max(rect.area for rect in rects)

    def get_max_area_pt2(self):
        # Part 2: largest rectangle fully inside polygon
        rects = [
            Rectangle(p1, p2)
            for p1, p2 in combinations(self.red_tiles, 2)
        ]
        valid_rects = [
            rect for rect in rects
            if self.polygon.covers(box(rect.min_x, rect.min_y, rect.max_x, rect.max_y))
        ]
        return max(valid_rects, key=lambda r: r.area, default=None).area if valid_rects else None

    def solve(self, part):
        if part == 1:
            return self.get_max_area()
        if part == 2:
            return self.get_max_area_pt2()
            

@timing_decorator
def main(raw, part):
    text_input = read_input(raw)
    input_parsed = [i if i else "" for i in text_input]
    puzzle = Puzzle(input_parsed)
    return puzzle.solve(part)

def run_tests():
    print("\nRunning Tests:")
    assert main(raw=files["test"], part=1) == 50
    assert main(raw=files["test"], part=2) == 24

    # solutions
    print("\nRunning Solutions:")
    assert main(raw=files["input"], part=1) == 4772103936
    assert main(raw=files["input"], part=2) == 1529675217

def solve():
    print("\nSolving:")
    answer1 = main(raw=files["input"], part=1)
    print(f"Answer part1: {magenta_color}{answer1}{reset_color}")
    answer2 = main(raw=files["input"], part=2)
    print(f"Answer part2: {magenta_color}{answer2}{reset_color}")

if __name__ == "__main__":
    run_tests()
    solve()