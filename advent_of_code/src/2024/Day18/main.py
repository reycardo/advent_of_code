from __future__ import annotations
from utils.tools import get_txt_files, read_input, timing_decorator
from advent_of_code.utils.colors import magenta_color, reset_color
from utils.tools import Point, Grid, InvertedVectors
from typing import List
import heapq

files = get_txt_files(__file__)
#########
# Start #
#########

class Robot:
    def __init__(self, pos: Point):
        self.pos = pos
        self.score = 0

    def set_robot_at_pos(self, pos: Point, grid: Grid):        
        self.pos = pos
        grid.set_value_at_point(pos, Puzzle.ROBOT)

    def can_move(self, grid: Grid, next_pos: Point):        
        return grid.valid_location(next_pos) and (grid.value_at_point(next_pos) != Puzzle.WALL)


class Puzzle:
    SPACE = "."
    WALL = "#"
    ROBOT = "@"
    DIRECTIONS = [
        InvertedVectors.N,
        InvertedVectors.E,
        InvertedVectors.S,
        InvertedVectors.W,
    ]

    def __init__(self, text_input, size, kb):
        self.input: List[str] = text_input
        self.input_parsed = self.parse_input()
        self.size = size + 1
        self.start = Point(0,0)
        self.end = Point(size,size)
        self.setup_grid()
        self.robot = Robot(self.start)
        self.kb = kb

    def parse_input(self):
        return [Point(*map(int, line.split(','))) for line in self.input]
    

    def setup_grid(self):        
        empty_grid = [['.' for _ in range(self.size)] for _ in range(self.size)]
        self.grid = Grid([list(raw) for raw in empty_grid])

    def populate_grid(self):
        for point in self.input_parsed[:self.kb]:
            self.grid.set_value_at_point(point=point,value=Puzzle.WALL)

    def find_path(self, weight=1):        
        # Initialize distances with infinity for all vertices except the start vertex
        distances = {vertex: float('inf') for vertex in self.grid._all_points}
        distances[self.start] = 0
        priority_queue = [(0, self.start, [self.start])] # score, pos, trail
        trails =[]
        
        while priority_queue:
            current_distance, current_vertex, trail = heapq.heappop(priority_queue)
            # Ignore processing if we've found a shorter path to the current vertex already
            if current_distance > distances[current_vertex]:
                continue

            if current_vertex == self.end:
                trails.append((trail, current_distance))
                continue
                    
            # Explore neighbors and update distances
            for next in self.DIRECTIONS:
                next = next.value
                neighbour = current_vertex + Point(next)
                if self.robot.can_move(grid=self.grid, next_pos=neighbour):
                    distance = current_distance + weight
                    # Update distance if a shorter path is found
                    if distance < distances[neighbour]:
                        distances[neighbour] = distance
                        trail += [neighbour]
                        heapq.heappush(priority_queue, (distance, neighbour, trail))
    
        return distances, trails

    def solve(self, part):
        if part == 1:
            self.populate_grid()
            self.distances, self.trails = self.find_path()
            min_value = min(trail[1] for trail in self.trails)
            return min_value
        elif part == 2:            
            self.populate_grid()
            while True:                                
                self.grid.set_value_at_point(point=self.input_parsed[self.kb], value=Puzzle.WALL)                
                self.distances, self.trails = self.find_path()
                if self.distances[self.end] == float('inf'):
                    found = self.input_parsed[self.kb]
                    break
                self.kb +=1
            return found

@timing_decorator
def main(raw, part, size, kb):
    text_input = read_input(raw)
    input_parsed = [i if i else "" for i in text_input]
    puzzle = Puzzle(input_parsed, size, kb)
    return puzzle.solve(part)


def run_tests():
    print(f"\nRunning Tests:")
    assert main(raw=files["test"], part=1, size=6, kb=12) == 22
    assert main(raw=files["test"], part=2, size=6, kb=12) == Point(6,1)

    # solutions
    print(f"\nRunning Solutions:")
    assert main(raw=files["input"], part=1, size=70, kb=1024) == 312
    # assert main(raw=files["input"], part=2) == 1509724


def solve():
    print(f"\nSolving:")
    answer1 = main(raw=files["input"], part=1, size=70, kb=1024)    
    print(f"Answer part1: {magenta_color}{answer1}{reset_color}")
    answer2 = main(raw=files["input"], part=2, size=70, kb=1024)
    print(f"Answer part2: {magenta_color}{answer2}{reset_color}")


if __name__ == "__main__":
    run_tests()
    solve()
