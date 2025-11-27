import os
import sys

sys.path.insert(0, "./")
from utils import tools

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
input_raw = os.path.join(__location__, "input.txt")
test_raw = os.path.join(__location__, "test.txt")

# For interactive testing
raw = r"2020\Day6\test.txt"

#########
# Start #
#########


def count_any_yes(group):
    return len(set("".join(group)))


def count_everyone_yes(group):
    people = len(group)
    all_chars = "".join(group)
    distinct_chars = list(set("".join(group)))
    return len([x for x in distinct_chars if all_chars.count(x) == people])


def main(raw, part):
    # read inputs from file
    input = tools.read_input_blank_separator(raw)
    if part == 1:
        return sum([count_any_yes(group) for group in input])
    elif part == 2:
        return sum([count_everyone_yes(group) for group in input])
    else:
        raise ValueError("part must be 1 or 2, instead of: " + part)


def run_tests():
    assert main(test_raw, 1) == 11
    test_input = tools.read_input_blank_separator(raw)
    assert count_everyone_yes(test_input[0]) == 3
    assert count_everyone_yes(test_input[1]) == 0
    assert count_everyone_yes(test_input[2]) == 1
    assert count_everyone_yes(test_input[3]) == 1
    assert count_everyone_yes(test_input[4]) == 1
    assert main(test_raw, 2) == 6


if __name__ == "__main__":
    run_tests()
    answer1 = main(input_raw, 1)
    answer2 = main(input_raw, 2)
    print("Answer part1: {}".format(answer1))
    print("Answer part2: {}".format(answer2))
