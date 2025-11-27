from utils.tools import get_txt_files, read_input, timing_decorator
from advent_of_code.utils.colors import magenta_color, reset_color
from utils.tools import Grid, Point, VectorDicts
from typing import List

files = get_txt_files(__file__)
#########
# Start #
#########


class GuardMap(Grid):
    SPACE = "."
    OBSTACLE = "#"

    DIRECTIONS = "^>v<"  # Each successive direction is the result of turning right (i.e. 90 degrees)
    DIRECTIONS_MAP = {
        "^": Point(0, -1),
        ">": Point(1, 0),
        "v": Point(0, 1),
        "<": Point(-1, 0),
    }

    def __init__(self, grid_array: list):
        super().__init__(grid_array)

        self._all_obstacles = set()
        self._update_all_obstacles()

        self._guard_location = self._locate_guard()
        self._start_location = self._guard_location

        self._guard_direction = self.value_at_point(self._guard_location)
        self._directions_idx = GuardMap.DIRECTIONS.index(self._guard_direction)
        self._start_direction_idx = self._directions_idx

        self._visited_with_direction = set()
        self._visited_map = {}  # We can use this to print the route
        self._visited: list[tuple[Point, str]] = []  # To track our route, if we need it
        self._in_loop = False

        self._update_visited()

        self._pre_obstacle_added = None

    def reset(self):
        self._guard_location = self._start_location
        self._guard_direction = self.value_at_point(self._guard_location)
        self._directions_idx = self._start_direction_idx

        self._visited_with_direction = set()
        self._visited_map: dict[Point, str] = {}
        self._visited = []
        self._in_loop = False

        self._update_visited()
        self._clear_obstacle()

    def add_obstacle(self, location: Point):
        """Add an obstacle at the specified location.
        Store this location so we can clear the obstacle later."""
        self._pre_obstacle_added = (location, self.value_at_point(location))
        self.set_value_at_point(location, GuardMap.OBSTACLE)

    def _clear_obstacle(self):
        """Clear any previously set obstacle."""
        if self._pre_obstacle_added:
            self.set_value_at_point(
                self._pre_obstacle_added[0], self._pre_obstacle_added[1]
            )

    @property
    def in_loop(self) -> bool:
        """Are we stuck in a loop?"""
        return self._in_loop

    @property
    def visited(self):
        """Visited locations, as a dict of {location: direction, ...}"""
        return self._visited_map

    @property
    def distinct_visited_count(self) -> int:
        """Count of all distinct locations we've visited."""
        return len(self._visited_map)

    def _update_visited(self):
        """Update visited locations"""

        location_config = (self._guard_location, self._guard_direction)

        # Update our dict of where we've been
        self._visited_map[self._guard_location] = self._guard_direction
        self._visited.append(location_config)

        # For loop checking, we need to check if we've seen this location AND this orientation
        if location_config in self._visited_with_direction:
            self._in_loop = True  # We've done this before!
        else:
            self._visited_with_direction.add(location_config)

    def _update_all_obstacles(self):
        self._all_obstacles = set()

        for point in self._all_points:
            if self.value_at_point(point) == GuardMap.OBSTACLE:
                self._all_obstacles.add(point)

    def move(self) -> bool:
        """
        Move guard one space in current direction.
        If we can't move forward in this direction, make turn and move.
        Return True if we move, or False if we leave the map
        """
        while True:
            # Move one step in the direction the guard is pointing
            next_point = (
                self._guard_location + GuardMap.DIRECTIONS_MAP[self._guard_direction]
            )

            if not self.valid_location(next_point):  # leaving the map?
                return False

            # Are we at an obstacle? If so, rotate right and try again
            next_value = self.value_at_point(next_point)
            if next_value == GuardMap.OBSTACLE:
                # Increment the direction index
                self._directions_idx = (self._directions_idx + 1) % len(
                    GuardMap.DIRECTIONS
                )
                self._guard_direction = GuardMap.DIRECTIONS[self._directions_idx]
                continue
            else:  # No obstacle, so we can move to this location
                self._guard_location = next_point
                self._update_visited()
                break  # We've successfully moved

        return True

    def _locate_guard(self) -> Point:
        for point in self.all_points():
            if self.value_at_point(point) in GuardMap.DIRECTIONS:
                return point

    def __str__(self) -> str:
        row_strs = []
        for y, row in enumerate(self._array):
            row_list = []
            for x, char in enumerate(row):
                locn = Point(x, y)
                if locn in self._visited_map.keys():
                    row_list.extend([self._visited_map[locn]])
                else:
                    row_list.append(char)

            row_strs.append("".join(row_list))

        return "\n".join(row_strs)


def solve_p1(data):
    guard_map = GuardMap(data)
    while guard_map.move():
        pass
    return guard_map.distinct_visited_count


def solve_pt2(data):
    # Initial route
    guard_map = GuardMap(data)
    while guard_map.move():
        pass

    # Route taken, excluding starting point
    route = [locn for locn in guard_map.visited.keys()][1:]

    loop_locations = 0

    for location in route:
        guard_map.reset()
        guard_map.add_obstacle(location)
        while guard_map.move():
            if guard_map.in_loop:
                loop_locations += 1
                break

    print(f"Found {loop_locations} loop locations.")
    return loop_locations


@timing_decorator
def main(raw, part):
    text_input = read_input(raw)
    input_parsed = [i if i else "" for i in text_input]
    input_parsed = [list(line) for line in input_parsed]
    if part == 1:
        return solve_p1(input_parsed)
    if part == 2:
        return solve_pt2(input_parsed)


def run_tests():
    print(f"\nRunning Tests:")
    assert main(raw=files["test"], part=1) == 41
    assert main(raw=files["test"], part=2) == 6

    # solutions
    print(f"\nRunning Solutions:")
    assert main(raw=files["input"], part=1) == 4883
    assert main(raw=files["input"], part=2) == 1655


def solve():
    print(f"\nSolving:")
    answer1 = main(raw=files["input"], part=1)
    print(f"Answer part1: {magenta_color}{answer1}{reset_color}")
    answer2 = main(raw=files["input"], part=2)
    print(f"Answer part2: {magenta_color}{answer2}{reset_color}")


if __name__ == "__main__":
    run_tests()
    solve()
