from __future__ import annotations
from advent_of_code.utils.tools import get_txt_files, read_input, timing_decorator
from advent_of_code.utils.colors import magenta_color, reset_color
from advent_of_code.utils.tools import Grid, Point, Vectors
from typing import Dict, Set, Tuple
from collections import deque
from dataclasses import dataclass

files = get_txt_files(__file__)
#########
# Start #
#########


@dataclass(frozen=True)
class Region:
    plot_type: str
    plots: Set[Point]
    perimeter: int
    perimeter_edges: dict[Point, Set[Point]]

    @property
    def area(self) -> int:
        return len(self.plots)

    @property
    def price(self) -> int:
        return self.area * self.perimeter

    @property
    def new_price(self) -> int:
        return self.area * self.sides

    @property
    def sides(self) -> int:
        return self._calculate_sides()

    def _calculate_sides(self) -> int:
        sides = 0

        # Iterate over sets for N, E, S, W...
        for (
            side
        ) in self.perimeter_edges.values():  # All plots facing a particular direction
            seen = set()

            for point in side:
                if point not in seen:
                    sides += 1  # This plot is in a new side

                    # Here we use BFS to flood fill all members of the same side
                    q = deque([point])
                    while q:
                        current = q.popleft()
                        if current in seen:
                            continue  # Stop us indefinitely queuing neighbours!

                        seen.add(current)  # Add this connected plot to seen
                        for neighbour in current.neighbours(include_diagonals=False):
                            if neighbour in side:  # Adjacent, so part of SAME side
                                q.append(neighbour)

        return sides

    def __str__(self):
        return f"Region(type={self.plot_type},area={self.area},perimeter={self.perimeter},price={self.price},sides={self.sides},new_price={self.new_price})"


class Puzzle(Grid):
    DIRECTIONS = [Vectors.N.value, Vectors.E.value, Vectors.S.value, Vectors.W.value]

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
            region_plots, perimeter, perimeter_edges = self._flood_fill_for_origin(
                point
            )
            region = Region(region_type, region_plots, perimeter, perimeter_edges)
            regions.append(region)

            allocated.update(region_plots)

        return regions

    def _flood_fill_for_origin(self, origin: Point):
        region_type = self.value_at_point(origin)

        queue: deque[Point] = deque()
        queue.append(origin)

        seen = set()
        seen.add(origin)

        plots = set()
        perimeter = 0

        perimeter_edges: Dict[Tuple[int], Set[Point]] = {}
        for dirn in Puzzle.DIRECTIONS:  # N, E, S, W
            perimeter_edges[dirn] = set()

        while queue:
            current: Point = queue.popleft()  # BFS
            current_val = self.value_at_point(current)

            if current_val == region_type:  # This plot is in our region
                plots.add(current)

            for (
                dirn
            ) in Puzzle.DIRECTIONS:  # Get the neighbours, one direction at a time
                neighbour = current + Point(*dirn)

                # If the neighbour is valid and of same type, it's in the same region so queue it
                if (
                    self.valid_location(neighbour)
                    and self.value_at_point(neighbour) == region_type
                ):
                    if neighbour not in seen:
                        queue.append(neighbour)
                        seen.add(neighbour)

                else:  # this neighbour represents a perimeter
                    perimeter += 1
                    perimeter_edges[dirn].add(
                        current
                    )  # Add the current plot as a perimeter plot

        return plots, perimeter, perimeter_edges

    def solve(self, part):
        if part == 1:
            return sum([x.price for x in self.regions])
        elif part == 2:
            return sum([x.new_price for x in self.regions])


@timing_decorator
def main(raw, part):
    text_input = read_input(raw)
    input_parsed = [i if i else "" for i in text_input]
    puzzle = Puzzle(input_parsed)
    return puzzle.solve(part)


def run_tests():
    print("\nRunning Tests:")
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
    print("\nRunning Solutions:")
    assert main(raw=files["input"], part=1) == 1464678
    assert main(raw=files["input"], part=2) == 877492


def solve():
    print("\nSolving:")
    answer1 = main(raw=files["input"], part=1)
    print(f"Answer part1: {magenta_color}{answer1}{reset_color}")
    answer2 = main(raw=files["input"], part=2)
    print(f"Answer part2: {magenta_color}{answer2}{reset_color}")


if __name__ == "__main__":
    run_tests()
    solve()
