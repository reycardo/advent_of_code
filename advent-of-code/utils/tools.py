import os
import time
from typing import Any, Callable
from datetime import timedelta
from utils.colors import green_color, cyan_color, reset_color
from itertools import product


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
