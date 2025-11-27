from __future__ import annotations
from advent_of_code.utils.tools import get_txt_files, read_input, timing_decorator
from advent_of_code.utils.colors import magenta_color, reset_color
from typing import List
from advent_of_code.utils.tools import Grid, Point, InvertedVectors
from collections import deque, defaultdict

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
    SPACE = "."
    WALL = "#"
    START = "S"
    END = "E"
    DIRECTIONS = [
        InvertedVectors.N,
        InvertedVectors.E,
        InvertedVectors.S,
        InvertedVectors.W,
    ]

    def __init__(self, text_input, save):
        self.input: List[str] = text_input
        self.save = save
        self.grid: Grid = Grid([list(raw) for raw in self.input])
        self.find_start_and_end()
        self.saved_time = {}
        self.cheats = set()

    def find_start_and_end(self):
        found_start = False
        found_end = False
        for point in self.grid._all_points:
            if self.grid.value_at_point(point) == Puzzle.START:
                self.start = point
                found_start = True
            elif self.grid.value_at_point(point) == Puzzle.END:
                self.end = point
                found_end = True
            if found_start and found_end:
                break

    def can_move(self, grid: Grid, next_pos: Point):
        return grid.valid_location(next_pos) and (
            grid.value_at_point(next_pos) != Puzzle.WALL
        )

    def find_path(self, grid: Grid):
        frontier = deque()
        frontier.append(
            Node(
                pos=self.start,
                score=0,
                trail=[self.start],
            )
        )
        explored = defaultdict(list)
        trails = []

        while frontier:
            current_node: Node = frontier.popleft()  # Breadth-First Search

            if current_node.pos == self.end:
                trails.append((current_node.trail, current_node.score))
                continue

            if explored[current_node.pos]:
                explored[current_node.pos].append(current_node.score)
            else:
                explored[current_node.pos] = [current_node.score]

            # Explore neighbors and update distances
            for next in self.DIRECTIONS:
                next = next.value
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

        return explored, trails

    def find_cheats(self, point: Point, score_at_point: int):
        for direction in Puzzle.DIRECTIONS:
            next_point_1 = point + Point(direction.value)
            next_point_2 = next_point_1 + Point(direction.value)
            if (
                self.grid.valid_location(next_point_1)
                and self.grid.valid_location(next_point_2)
                and self.grid.value_at_point(next_point_1) == Puzzle.WALL
                and (
                    self.grid.value_at_point(next_point_2) == Puzzle.SPACE
                    or self.grid.value_at_point(next_point_2) == Puzzle.END
                )
            ):
                if next_point_1 in self.cheats:
                    continue
                self.cheats.add(next_point_1)
                score_at_point
                original_score = self.original_trail[0][0].index(next_point_2)
                new_score = (
                    score_at_point
                    + 1
                    + (len(self.original_trail[0][0]) - 1 - original_score)
                )
                time_diff = self.trail_time - new_score
                if new_score < self.trail_time:
                    new_trail = (
                        self.original_trail[0][0][:score_at_point]
                        + [next_point_1]
                        + self.original_trail[0][0][original_score:]
                    )
                    if time_diff not in self.saved_time:
                        self.saved_time[time_diff] = (1, [new_trail])
                    else:
                        count, trails = self.saved_time[time_diff]
                        self.saved_time[time_diff] = (count + 1, trails + [new_trail])
                self.grid.set_value_at_point(next_point_1, Puzzle.WALL)

    @timing_decorator
    def find_new_cheats(self, point: Point, score_at_point: int):
        for i in range(
            score_at_point, len(self.original_trail[0][0])
        ):  # might need to change len
            next_point_2: Point = self.original_trail[0][0][i]
            man_dist = next_point_2.manhattan_distance_from(point)
            if man_dist <= 20:
                # if so check if time_diff > 50
                original_score = self.original_trail[0][0].index(next_point_2)
                new_score = (
                    score_at_point
                    + man_dist
                    + (len(self.original_trail[0][0]) - 2 - original_score)
                )
                time_diff = self.trail_time - new_score
                if time_diff not in self.saved_time:
                    self.saved_time[time_diff] = 1
                else:
                    self.saved_time[time_diff] += 1

    def cheat(self, trail: List[Point], part):
        if part == 1:
            for score, point in enumerate(trail, start=1):
                self.find_cheats(point, score_at_point=score)
        elif part == 2:
            for score, point in enumerate(trail, start=1):
                print(f"finding new cheats for {point}")
                self.find_new_cheats(point, score_at_point=score)

    def paint_grid(self, grid: Grid, points_to_paint: List[Point]):
        for point in points_to_paint:
            grid.set_value_at_point(point, "o")
        print(grid)
        for point in points_to_paint:
            grid.set_value_at_point(point, ".")

    def solve(self, part):
        _, self.original_trail = self.find_path(self.grid)
        self.trail_time = min(self.original_trail, key=lambda x: x[1])[1]
        self.cheat(self.original_trail[0][0], part=part)
        if part == 1:
            return sum(
                [
                    count[0]
                    for saved_time, count in self.saved_time.items()
                    if saved_time >= self.save
                ]
            )
        elif part == 2:
            return sum(
                [
                    count
                    for saved_time, count in self.saved_time.items()
                    if saved_time >= self.save
                ]
            )


@timing_decorator
def main(raw, part, save=100):
    text_input = read_input(raw)
    input_parsed = [i if i else "" for i in text_input]
    puzzle = Puzzle(input_parsed, save)
    return puzzle.solve(part)


def run_tests():
    print("\nRunning Tests:")
    assert main(raw=files["test"], part=1, save=10) == 10
    assert (
        main(raw=files["test"], part=2, save=50)
        == 32 + 31 + 29 + 39 + 25 + 23 + 20 + 19 + 12 + 14 + 12 + 22 + 4 + 3
    )

    # solutions
    # print(f"\nRunning Solutions:")
    # assert main(raw=files["input"], part=1) == 308
    # assert main(raw=files["input"], part=2) == 662726441391898


def solve():
    print("\nSolving:")
    answer1 = main(raw=files["input"], part=1, save=100)
    print(f"Answer part1: {magenta_color}{answer1}{reset_color}")
    answer2 = main(raw=files["input"], part=2, save=100)
    print(f"Answer part2: {magenta_color}{answer2}{reset_color}")


if __name__ == "__main__":
    run_tests()
    solve()
