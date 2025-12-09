from typing import NamedTuple
from advent_of_code.utils.tools import get_txt_files, read_input, timing_decorator
from advent_of_code.utils.colors import magenta_color, reset_color

files = get_txt_files(__file__)

class RedTile(NamedTuple):
    x: int
    y: int

class Puzzle:
    def __init__(self, text_input):
        self.input = text_input
        self.red_tiles = [RedTile(*map(int, row.split(','))) for row in self.input]
        self.n = len(self.red_tiles)
        self.poly_edges = [
            (self.red_tiles[i], self.red_tiles[(i + 1) % self.n])
            for i in range(self.n)
        ]

    def rectangle_edges(self, rt1, rt2):
        # Returns the four edges of the rectangle defined by rt1 and rt2 as opposite corners
        min_x, max_x = sorted([rt1.x, rt2.x])
        min_y, max_y = sorted([rt1.y, rt2.y])
        return [
            (RedTile(min_x, min_y), RedTile(max_x, min_y)),  # bottom edge
            (RedTile(max_x, min_y), RedTile(max_x, max_y)),  # right edge
            (RedTile(max_x, max_y), RedTile(min_x, max_y)),  # top edge
            (RedTile(min_x, max_y), RedTile(min_x, min_y)),  # left edge
        ]

    def point_in_polygon(self, pt):
        # Ray casting algorithm for point-in-polygon test (works for any simple polygon)
        # Returns True if pt is inside or on the boundary of the polygon
        x, y = pt.x, pt.y
        count = 0
        for i in range(self.n):
            rt1 = self.red_tiles[i]
            rt2 = self.red_tiles[(i + 1) % self.n]
            if rt1.y == rt2.y:  # horizontal edge
                if y == rt1.y and min(rt1.x, rt2.x) <= x <= max(rt1.x, rt2.x):
                    return True  # On boundary
            # Count crossings of a ray to the right from (x, y)
            if ((rt1.y > y) != (rt2.y > y)):
                x_intersect = (rt2.x - rt1.x) * (y - rt1.y) / (rt2.y - rt1.y) + rt1.x
                if x_intersect > x:
                    count += 1
        return count % 2 == 1

    def segments_intersect(self, a1, a2, b1, b2):
        # Checks if two axis-aligned segments cross (not just touch or overlap)
        # Only returns True if the intersection is strictly inside both segments
        if a1.x == a2.x and b1.y == b2.y:
            # a is vertical, b is horizontal
            if (min(b1.x, b2.x) < a1.x < max(b1.x, b2.x) and
                min(a1.y, a2.y) < b1.y < max(a1.y, a2.y)):
                return True
            return False
        if a1.y == a2.y and b1.x == b2.x:
            # a is horizontal, b is vertical
            if (min(a1.x, a2.x) < b1.x < max(a1.x, a2.x) and
                min(b1.y, b2.y) < a1.y < max(b1.y, b2.y)):
                return True
            return False
        return False

    def rectangle_has_intersection(self, rt1, rt2):
        # Returns True if any edge of the rectangle crosses any edge of the polygon
        rect_edges = self.rectangle_edges(rt1, rt2)
        for re1, re2 in rect_edges:
            for pe1, pe2 in self.poly_edges:
                if self.segments_intersect(re1, re2, pe1, pe2):
                    return True
        return False

    def get_max_area(self):
        # Part 1: largest rectangle defined by any two red tiles (no containment check)
        max_area = 0
        for i in range(self.n):
            for j in range(i + 1, self.n):
                rt1 = self.red_tiles[i]
                rt2 = self.red_tiles[j]
                area = (abs(rt1.x - rt2.x) + 1) * (abs(rt1.y - rt2.y) + 1)
                if area > max_area:
                    max_area = area
        return max_area

    def get_max_area_pt2(self):
        # Part 2: largest rectangle fully inside polygon
        # For each pair of red tiles, check if the rectangle is fully inside the polygon
        max_area = 0
        max_rect = None
        for i in range(self.n):
            for j in range(i + 1, self.n):
                rt1 = self.red_tiles[i]
                rt2 = self.red_tiles[j]
                # Skip rectangles that cross the polygon boundary
                if self.rectangle_has_intersection(rt1, rt2):
                    continue
                min_x, max_x = sorted([rt1.x, rt2.x])
                min_y, max_y = sorted([rt1.y, rt2.y])
                # Check all four corners are inside or on the boundary
                corners = [
                    RedTile(min_x, min_y),
                    RedTile(min_x, max_y),
                    RedTile(max_x, min_y),
                    RedTile(max_x, max_y)
                ]
                if all(self.point_in_polygon(corner) for corner in corners):
                    area = (max_x - min_x + 1) * (max_y - min_y + 1)
                    if area > max_area:
                        max_area = area
                        max_rect = {'rt1': rt1, 'rt2': rt2, 'area': area}
        return max_rect

    def solve(self, part):
        if part == 1:
            return self.get_max_area()
        if part == 2:
            return self.get_max_area_pt2()["area"]

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