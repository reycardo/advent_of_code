from __future__ import annotations
from utils.tools import get_txt_files, read_input, timing_decorator
from utils.colors import magenta_color, reset_color
from typing import List
from utils.tools import Grid, Point, VectorDicts
from collections import deque, defaultdict
from functools import cache

files = get_txt_files(__file__)
#########
# Start #
#########

class Node:
    def __init__(self, pos: Point, score: int, trail: List[Point]):
        self.pos = pos
        self.score = score
        self.trail = trail

class Puzzle:
    DIRECTIONS = VectorDicts.REVERSE_ARROWS

    def __init__(self, text_input):
        self.input: List[str] = text_input
        self.numeric_keypad = [["7","8","9"],["4","5","6"],["1","2","3"],["#","0","A"]]
        self.directional_keypad = [['#','^','A'],['<','v','>']]
        self.numeric_keypad_grid = Grid(self.numeric_keypad)
        self.directional_keypad_grid = Grid(self.directional_keypad)

    def can_move(self, grid: Grid, next_pos: Point):
        return grid.valid_location(next_pos) and (grid.value_at_point(next_pos) != "#")

    def get_point_with_value(self, grid: Grid, value):
        for point in grid._all_points:
            if grid.value_at_point(point) == value:
                return point

    @cache
    def shortest_path_to_keypad(self, grid: Grid, start: Point, end: Point):
        frontier = deque()
        frontier.append(
            Node(
                pos=start,
                score=0,
                trail=[start],
            )
        )
        explored = defaultdict(list)
        trails = []
        while frontier:
            current_node: Node = frontier.popleft()  # Breadth-First Search

            if current_node.pos == end:
                trails.append((current_node.trail, current_node.score))
                continue

            if explored[current_node.pos]:
                explored[current_node.pos].append(current_node.score)
            else:
                explored[current_node.pos] = [current_node.score]

            # Explore neighbors and update distances
            for next in self.DIRECTIONS.values():
                neighbour = current_node.pos + Point(next)
                if self.can_move(grid=grid, next_pos=neighbour):
                    new_score = current_node.score + 1

                    if neighbour not in explored or new_score <= min(
                        explored[current_node.pos]
                    ):
                        new_trail = current_node.trail + [neighbour]
                        frontier.append(
                            Node(
                                pos=neighbour,
                                score=new_score,
                                trail=new_trail,
                            )
                        )

        return trails

    @cache
    def get_shortest_paths_in_keypad(self, grid: Grid, start: str, end: str):
        start_point = self.get_point_with_value(grid, start)
        end_point = self.get_point_with_value(grid, end)
        trails = self.shortest_path_to_keypad(grid, start_point, end_point)
        min_score = min([trail[1] for trail in trails])
        min_trails = [trail[0] for trail in trails if trail[1] == min_score]
        return min_trails

    

    def solve(self, part):
        if part==1:            
            pass
        elif part==2:
            pass


@timing_decorator
def main(raw, part):
    text_input = read_input(raw)
    input_parsed = [i if i else "" for i in text_input]
    puzzle = Puzzle(input_parsed)
    return puzzle.solve(part)


def run_tests():
    print(f"\nRunning Tests:")
    assert main(raw=files["test"], part=1) == 126384
    # assert main(raw=files["test"], part=2) == 20

    # solutions
    # print(f"\nRunning Solutions:")
    # assert main(raw=files["input"], part=1) == 308
    # assert main(raw=files["input"], part=2) == 662726441391898


def solve():
    print(f"\nSolving:")
    answer1 = main(raw=files["input"], part=1)
    print(f"Answer part1: {magenta_color}{answer1}{reset_color}")
    # answer2 = main(raw=files["input"], part=2)
    # print(f"Answer part2: {magenta_color}{answer2}{reset_color}")


if __name__ == "__main__":
    run_tests()
    solve()
