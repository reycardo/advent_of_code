from __future__ import annotations
import os
import time
from typing import Any, Callable, Union, Tuple
from datetime import timedelta
from utils.colors import green_color, cyan_color, reset_color
from itertools import product
from enum import Enum
from dataclasses import asdict, dataclass


def read_input(file, sep: str = "\n"):
    with open(file, "r") as tf:
        return tf.read().strip().split(sep)


def flatten(t):
    return [item for sublist in t for item in sublist]


def is_inside(matrix, coords: tuple):
    if all(
        (
            coords[0] >= 0,
            coords[0] < len(matrix[0]),
            coords[1] >= 0,
            coords[1] < len(matrix),
        )
    ):
        return True
    else:
        return False


def get_adjacents(matrix, coords: tuple):
    for r_offset, c_offset in product(range(-1, 2), range(-1, 2)):  # get all offsets
        if not (r_offset == 0 and c_offset == 0) and (
            c_offset == 0 or r_offset == 0
        ):  # if not own and not diagonal
            adjacent = (coords[0] + r_offset, coords[1] + c_offset)
            if is_inside(matrix, adjacent):
                yield adjacent


def get_txt_files(current_script_path):
    data_paths = {}
    # Get the path of the current script file
    current_dir = os.path.dirname(current_script_path)
    # For each .txt file in the current directory and its subdirectories
    for root, _, files in os.walk(current_dir):
        for file in files:
            if file.endswith(".txt"):
                data_type = file.split(".")[0]
                data_paths[data_type] = os.path.join(root, file)
    return data_paths


def timing_decorator(func: Callable[..., Any]) -> Callable[..., Any]:
    """
    Decorator to measure the execution time of a function.

    Parameters:
        func (callable): The function to be timed.

    Returns:
        callable: The wrapped function.

    Example:
        @timing_decorator
        def example_function():
            # Your function code here
            time.sleep(2)
            print("Function executed.")
    """

    def wrapper(*args, **kwargs) -> Any:
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time
        readable_time = format_elapsed_time(elapsed_time)

        # Get the value of the 'raw' parameter
        raw_value = kwargs.get("raw", None)

        # If 'raw' is present and is a file path, truncate it to the file name
        if raw_value and os.path.isfile(raw_value):
            kwargs["raw"] = os.path.basename(raw_value)

        # Get the parameter names and values
        param_names = func.__code__.co_varnames[: func.__code__.co_argcount]
        param_values = args + tuple(f"{key}={value}" for key, value in kwargs.items())

        # Print the function name, elapsed time, and parameter values
        print(
            f"{green_color}{func.__name__}({', '.join(f'{value}' for value in param_values)}){reset_color} "
            f"took {cyan_color}{readable_time}{reset_color} to run."
        )
        return result

    return wrapper


def format_elapsed_time(seconds: float) -> str:
    """
    Format elapsed time in a human-readable format.

    Parameters:
        seconds (float): Elapsed time in seconds.

    Returns:
        str: Human-readable elapsed time.
    """
    delta = timedelta(seconds=seconds)

    # Extract components
    days = delta.days
    hours, remainder = divmod(delta.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    ms = delta.microseconds / 1000

    # Format as a string
    if days > 0:
        return f"{days}d, {hours}h, {minutes}m, {seconds}s, {ms}ms"
    elif hours > 0:
        return f"{hours}h, {minutes}m, {seconds}s, {ms}ms"
    elif minutes > 0:
        return f"{minutes}m, {seconds}s, {ms}ms"
    elif seconds > 0:
        return f"{seconds}s, {ms}ms"
    else:
        return f"{ms}ms"


@dataclass(frozen=True)
class Point:
    """Class for storing a point x,y coordinate"""

    x: int
    y: int

    def __init__(self, x: Union[int, Tuple[int, int]], y: int = None):
        if isinstance(x, tuple):
            object.__setattr__(self, 'x', x[0])
            object.__setattr__(self, 'y', x[1])
        else:
            object.__setattr__(self, 'x', x)
            object.__setattr__(self, 'y', y)

    def __add__(self, other: Point):
        return Point(self.x + other.x, self.y + other.y)

    def __mul__(self, other: Point):
        """(x, y) * (a, b) = (xa, yb)"""
        return Point(self.x * other.x, self.y * other.y)

    def __mul__(self, other: Union['Point', int]):
        """Multiply by another Point or a scalar
        (x, y) * (a, b) = (xa, yb)
        or
        (x, y) * a = (xa, ya)
        """
        if isinstance(other, Point):
            return Point(self.x * other.x, self.y * other.y)
        elif isinstance(other, int):
            return Point(self.x * other, self.y * other)
        else:
            return NotImplemented

    def __sub__(self, other: Point):
        return self + Point(-other.x, -other.y)

    def __lt__(self, other):
        # Arbitrary comparison logic
        return (self.x, self.y) < (other.x, other.y)

    def yield_neighbours(self, include_diagonals=True, include_self=False):
        """Generator to yield neighbouring Points"""

        deltas: list
        if not include_diagonals:
            deltas = [
                vector.value
                for vector in Vectors
                if abs(vector.value[0]) != abs(vector.value[1])
            ]
        else:
            deltas = [vector.value for vector in Vectors]

        if include_self:
            deltas.append((0, 0))

        for delta in deltas:
            yield Point(self.x + delta[0], self.y + delta[1])

    def neighbours(self, include_diagonals=True, include_self=False) -> list[Point]:
        """Return all the neighbours, with specified constraints.
        It wraps the generator with a list."""
        return list(self.yield_neighbours(include_diagonals, include_self))

    def get_specific_neighbours(self, directions: list[Vectors]) -> list[Point]:
        """Get neighbours, given a specific list of allowed locations"""
        return [(self + Point(*vector.value)) for vector in list(directions)]

    def get_scaled_neighbours(
        self, directions: list[Vectors], scalar: int
    ) -> list[Point]:
        """Get neighbours, given a specific list of allowed locations, scaled by a scalar"""
        return [
            (self + Point(vector.value[0] * scalar, vector.value[1] * scalar))
            for vector in directions
        ]

    @staticmethod
    def manhattan_distance(a_point: Point) -> int:
        """Return the Manhattan distance value of this vector"""
        return sum(abs(coord) for coord in asdict(a_point).values())

    def manhattan_distance_from(self, other: Point) -> int:
        """Manhattan distance between this Vector and another Vector"""
        diff = self - other
        return Point.manhattan_distance(diff)

    def __repr__(self):
        return f"P({self.x},{self.y})"


class Vectors(Enum):
    """Enumeration of 8 directions.
    Note: y axis increments in the North direction, i.e. N = (0, 1)"""

    N = (0, 1)
    NE = (1, 1)
    E = (1, 0)
    SE = (1, -1)
    S = (0, -1)
    SW = (-1, -1)
    W = (-1, 0)
    NW = (-1, 1)

    @property
    def y_inverted(self):
        """Return vector, but with y-axis inverted. I.e. N = (0, -1)"""
        x, y = self.value
        return (x, -y)

class InvertedVectors(Enum):
    """Enumeration of 8 directions.
    Note: y axis increments in the South direction, i.e. N = (0, -1)"""

    N = (0, -1)
    NE = (1, -1)
    E = (1, 0)
    SE = (1, 1)
    S = (0, 1)
    SW = (-1, 1)
    W = (-1, 0)
    NW = (-1, -1)

    @property
    def y_inverted(self):
        """Return vector, but with y-axis inverted. I.e. N = (0, 1)"""
        x, y = self.value
        return (x, -y)

class VectorDicts:
    """Contains constants for Vectors"""

    ARROWS = {
        "^": Vectors.N.value,
        ">": Vectors.E.value,
        "v": Vectors.S.value,
        "<": Vectors.W.value,
    }

    REVERSE_ARROWS = {
        "^": Vectors.S.value,
        ">": Vectors.E.value,
        "v": Vectors.N.value,
        "<": Vectors.W.value,
    }

    DIRS = {
        "U": Vectors.N.value,
        "R": Vectors.E.value,
        "D": Vectors.S.value,
        "L": Vectors.W.value,
    }

    NINE_BOX: dict[str, tuple[int, int]] = {
        # x, y vector for adjacent locations
        "tr": (1, 1),
        "mr": (1, 0),
        "br": (1, -1),
        "bm": (0, -1),
        "bl": (-1, -1),
        "ml": (-1, 0),
        "tl": (-1, 1),
        "tm": (0, 1),
    }


class Grid:
    """2D grid of point values."""

    def __init__(self, grid_array: list) -> None:
        self._array = grid_array
        self._width = len(self._array[0])
        self._height = len(self._array)
        self._all_points = [
            Point(x, y) for y in range(self._height) for x in range(self._width)
        ]

    def value_at_point(self, point: Point) -> int:
        """The value at this point"""
        return self._array[point.y][point.x]

    def set_value_at_point(self, point: Point, value):
        self._array[point.y][point.x] = value

    def valid_location(self, point: Point) -> bool:
        """Check if a location is within the grid"""
        if 0 <= point.x < self._width and 0 <= point.y < self._height:
            return True

        return False

    @property
    def width(self):
        """Array width (cols)"""
        return self._width

    @property
    def height(self):
        """Array height (rows)"""
        return self._height

    def all_points(self) -> list[Point]:
        return self._all_points

    def rows_as_str(self):
        """Return the grid"""
        return ["".join(str(char) for char in row) for row in self._array]

    def cols_as_str(self):
        """Render columns as str. Returns: list of str"""
        cols_list = list(zip(*self._array))
        return ["".join(str(char) for char in col) for col in cols_list]

    def __repr__(self) -> str:
        return f"Grid(size={self.width}*{self.height})"

    def __str__(self) -> str:
        return "\n".join("".join(map(str, row)) for row in self._array)
