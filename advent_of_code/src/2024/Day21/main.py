from __future__ import annotations
from utils.tools import get_txt_files, read_input, timing_decorator
from advent_of_code.utils.colors import magenta_color, reset_color
from typing import List
from utils.tools import Grid, Point, VectorDicts
from collections import deque, defaultdict
from functools import cache, lru_cache
import itertools

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

    def __init__(self, text_input, num_robots):
        self.input: List[str] = text_input
        self.numeric_keypad = [
            ["7", "8", "9"],
            ["4", "5", "6"],
            ["1", "2", "3"],
            ["#", "0", "A"],
        ]
        self.directional_keypad = [["#", "^", "A"], ["<", "v", ">"]]
        self.numeric_keypad_grid = Grid(self.numeric_keypad)
        self.directional_keypad_grid = Grid(self.directional_keypad)
        self.robot_pos = ["A"] * num_robots

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

    def translate_path_to_directions(self, path: List[Point]):
        directions = ""
        for i in range(len(path) - 1):
            current = path[i]
            next = path[i + 1]
            # get direction where self.DIRECTIONS value = next - current
            direction = [
                key
                for key, value in self.DIRECTIONS.items()
                if Point(value) == next - current
            ][0]
            directions += direction
        return directions

    def press_buttons(self, num_robots: int):
        self.final_sequences = {}

        @lru_cache(maxsize=None)
        def recursive_expand(sequence, robot):
            if robot >= num_robots:
                return [sequence]

            expanded_path = self.do_sequence(
                sequence, grid=self.directional_keypad_grid, robot=robot
            )
            possible_sequences = [
                "".join(seq) for seq in itertools.product(*expanded_path)
            ]

            all_sequences = []
            for seq in possible_sequences:
                all_sequences.extend(recursive_expand(seq, robot + 1))

            return all_sequences

        for button_sequence in self.input:
            expanded_path = self.do_sequence(
                button_sequence, grid=self.numeric_keypad_grid, robot=0
            )
            possible_sequences_0 = [
                "".join(sequence) for sequence in itertools.product(*expanded_path)
            ]

            all_sequences = []
            for sequence in possible_sequences_0:
                all_sequences.extend(recursive_expand(sequence, 1))

            self.final_sequences[button_sequence] = all_sequences

    def get_minimum_string_length(self, sequences: List[str]) -> int:
        # Flatten the list of lists into a single list of strings
        # Find the string with the minimum length
        min_length_string = min(sequences, key=len)
        # Return the length of the minimum length string
        return len(min_length_string)

    def get_complexity(self):
        complexity = []
        for k, v in self.final_sequences.items():
            len_of_shortest_seq = self.get_minimum_string_length(v)
            numeric_part_of_code = int(k[:-1])
            complexity.append(len_of_shortest_seq * numeric_part_of_code)
        return sum(complexity)

    def do_sequence(self, sequence, grid: Grid, robot):
        expanded_path = []
        for i in range(len(sequence)):
            current_button = self.robot_pos[robot]
            end = sequence[i]
            paths = self.get_shortest_paths_in_keypad(
                grid, start=current_button, end=end
            )
            self.robot_pos[robot] = sequence[i]
            dir_path = []
            for path in paths:
                dir_path.append(self.translate_path_to_directions(path) + "A")
            expanded_path.append(dir_path)
        return expanded_path

    def solve(self, part):
        if part == 1:
            self.press_buttons(3)
            return self.get_complexity()
        elif part == 2:
            self.press_buttons(26)
            return self.get_complexity()


@timing_decorator
def main(raw, part, num_robots):
    text_input = read_input(raw)
    input_parsed = [i if i else "" for i in text_input]
    puzzle = Puzzle(input_parsed, num_robots)
    return puzzle.solve(part)


def run_tests():
    print("\nRunning Tests:")
    assert main(raw=files["test"], part=1, num_robots=3) == 126384
    # assert main(raw=files["test"], part=2) == 20

    # solutions
    print("\nRunning Solutions:")
    assert main(raw=files["input"], part=1, num_robots=3) == 134120
    # assert main(raw=files["input"], part=2) == 662726441391898


def solve():
    print("\nSolving:")
    answer1 = main(raw=files["input"], part=1, num_robots=3)
    print(f"Answer part1: {magenta_color}{answer1}{reset_color}")
    answer2 = main(raw=files["input"], part=2, num_robots=26)
    print(f"Answer part2: {magenta_color}{answer2}{reset_color}")


if __name__ == "__main__":
    run_tests()
    solve()
