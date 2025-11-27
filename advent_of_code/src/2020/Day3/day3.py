import math
import os
import sys

sys.path.insert(0, "./")
from utils import tools

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
input_raw = os.path.join(__location__, "input.txt")
test_raw = os.path.join(__location__, "test.txt")

#########
# Start #
#########


def repeat_pattern(my_list, pattern, times):
    # concats element-wise a my_list and the patern $times times
    for _ in range(times):
        my_list = [a + b for a, b in zip(my_list, pattern)]
    return my_list


def hit_or_open(char):
    if char == ".":
        return "O"
    elif char == "#":
        return "X"
    else:
        raise ValueError("wrong char: " + char)


def tree_counter(trees, open_spaces, destination):
    if destination == "X":
        return trees + 1, open_spaces
    elif destination == "O":
        return trees, open_spaces + 1
    else:
        raise ValueError("wrong destination: " + destination)


def slope(my_list, h, v, start):
    # slides h horizontally and v vertically across my_list
    cur_pos = start
    trees = 0
    open_spaces = 0
    input = my_list
    # loops until hits bottom
    for _ in range(int(math.floor((len(my_list) - 1) / v))):
        # updates current position
        cur_pos = [sum(x) for x in zip(cur_pos, (h, v))]
        # repeats pattern if reaching right side
        if cur_pos[0] >= len(my_list[0]):
            my_list = repeat_pattern(my_list, input, 1)
        # checks if it hit a tree or open spot
        destination = hit_or_open(my_list[cur_pos[1]][cur_pos[0]])
        # updates position with O if open, X if tree
        my_list[cur_pos[1]] = (
            my_list[cur_pos[1]][: cur_pos[0]]
            + destination
            + my_list[cur_pos[1]][cur_pos[0] + 1 :]
        )
        # updates counters
        trees, open_spaces = tree_counter(trees, open_spaces, destination)
    return my_list, trees, open_spaces


def main(raw, part):
    # read inputs from file
    input = tools.read_input(raw)
    if part == 1:
        start = (0, 0)
        h = 3
        v = 1
        my_list, trees, open_spaces = slope(input, h, v, start)
        return trees
    elif part == 2:
        start = (0, 0)
        slope_list = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
        trees_list = []
        for h, v in slope_list:
            my_list, trees, open_spaces = slope(input, h, v, start)
            trees_list.append(trees)
        return math.prod(trees_list)
    else:
        raise ValueError("part must be 1 or 2, instead of: " + part)


def run_tests():
    assert main(test_raw, 1) == 7
    assert main(test_raw, 2) == 336
    # solutions
    assert main(input_raw, 1) == 145
    assert main(input_raw, 2) == 3424528800


if __name__ == "__main__":
    run_tests()
    answer1 = main(input_raw, 1)
    answer2 = main(input_raw, 2)
    print("Answer part1: {}".format(answer1))
    print("Answer part2: {}".format(answer2))
