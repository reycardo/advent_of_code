from __future__ import annotations
from utils.tools import get_txt_files, read_input, timing_decorator
from utils.colors import magenta_color, reset_color
from utils.tools import Grid, Point
from typing import List
from collections import deque
from dataclasses import dataclass

files = get_txt_files(__file__)
#########
# Start #
#########


@dataclass(frozen=True)
class Region:
    plot_type: str
    plots: set[Point]
    perimeter: int

    @property
    def area(self) -> int:
        return len(self.plots)

    @property
    def price(self) -> int:
        return self.area * self.perimeter

    def __str__(self):
        return f"Region(type={self.plot_type},area={self.area},perimeter={self.perimeter},price={self.price})"


class Garden(Grid):
    def __init__(self, grid_array):
        super().__init__(grid_array)

        self._regions = self._find_regions()

    @property
    def regions(self):
        return self._regions

    def _find_regions(self):
        regions: list[Region] = []
        allocated = set()

        for point in self._all_points:
            if point in allocated:
                continue  # We've done this one

            region_type = self.value_at_point(point)
            region_plots, perimeter = self._flood_fill_for_origin(point)
            region = Region(region_type, region_plots, perimeter)
            regions.append(region)

            allocated.update(region_plots)

        return regions

    def _flood_fill_for_origin(self, origin: Point):
        region_type = self.value_at_point(origin)

        frontier: deque[Point] = deque()  # Very efficient for FIFO queueing
        frontier.append(origin)

        seen = set()
        seen.add(origin)

        plots = set()
        perimeter = 0

        while frontier:
            current: Point = frontier.popleft()  # BFS
            current_val = self.value_at_point(current)

            if current_val == region_type:
                plots.add(current)

            # Get valid neighbours
            neighbours = [
                neighbour
                for neighbour in current.neighbours(include_diagonals=False)
                if (
                    self.valid_location(neighbour)
                    and self.value_at_point(neighbour) == region_type
                )
            ]

            # For every neighbour that isn't valid, we have established a perimeter unit
            perimeter += 4 - len(neighbours)

            for next in neighbours:
                if next not in seen:
                    frontier.append(next)
                    seen.add(next)

        return plots, perimeter

    def solve(self, part):
        if part == 1:
            return sum([x.price for x in self.regions])
        elif part == 2:
            pass


@timing_decorator
def main(raw, part):
    text_input = read_input(raw)
    input_parsed = [i if i else "" for i in text_input]
    puzzle = Garden(input_parsed)
    return puzzle.solve(part)


def run_tests():
    print(f"\nRunning Tests:")
    assert main(raw=files["test"], part=1) == 140
    assert main(raw=files["test2"], part=1) == 772
    assert main(raw=files["test3"], part=1) == 1930
    assert main(raw=files["test4"], part=1) == 280
    assert main(raw=files["test5"], part=1) == 426452
    assert main(raw=files["test6"], part=1) == 1202
    assert main(raw=files["test7"], part=1) == 2566

    assert main(raw=files["test"], part=2) == 80
    assert main(raw=files["test2"], part=2) == 436
    assert main(raw=files["p2_test"], part=2) == 236
    assert main(raw=files["p2_test2"], part=2) == 368
    assert main(raw=files["test3"], part=2) == 1206

    # solutions
    print(f"\nRunning Solutions:")
    assert main(raw=files["input"], part=1) == 1464678
    # assert main(raw=files["input"], part=2) == 1686


def solve():
    print(f"\nSolving:")
    answer1 = main(raw=files["input"], part=1)
    print(f"Answer part1: {magenta_color}{answer1}{reset_color}")
    answer2 = main(raw=files["input"], part=2)
    print(f"Answer part2: {magenta_color}{answer2}{reset_color}")


if __name__ == "__main__":
    run_tests()
    solve()
