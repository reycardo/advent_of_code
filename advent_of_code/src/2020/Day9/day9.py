import os
import sys

sys.path.insert(0, "./")
from utils import tools

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
input_raw = os.path.join(__location__, "input.txt")
test_raw = os.path.join(__location__, "test.txt")

# For interactive testing
raw = r"2020\Day9\test.txt"

#########
# Start #
#########


def check_valid_numbers(my_list):
    return list(set([a + b for a in my_list for b in my_list if a != b]))


def validate_number(number, valids):
    return number in valids


def validate_data(my_list, preamble):
    invalids = []
    for i in range(len(my_list) - preamble):
        cur_pos = preamble + i
        valids = check_valid_numbers(my_list[i:cur_pos])
        if not validate_number(my_list[cur_pos], valids):
            invalids.append(my_list[cur_pos])
    return invalids


def encryption_weakness(my_list):
    return min(my_list) + max(my_list)


def find_encryption_weakness(my_list, invalid):
    return [
        encryption_weakness(my_list[a:b])
        for a in range(len(my_list) - 1)
        for b in range(a, len(my_list) - 1)
        if sum(my_list[a:b]) == invalid and a < b
    ]


def main(raw, part, preamble):
    input = tools.read_input(raw)
    # convert all elements to int
    input = [int(i) for i in input if i]

    if part == 1:
        return validate_data(input, preamble)[0]
    elif part == 2:
        invalid = validate_data(input, preamble)[0]
        return find_encryption_weakness(input, invalid)[0]
    else:
        raise ValueError("part must be 1 or 2, instead of: " + part)


def run_tests():
    assert main(test_raw, 1, 5) == 127
    assert main(test_raw, 2, 5) == 62
    # solutions
    assert main(input_raw, 1, 25) == 50047984
    assert main(input_raw, 2, 25) == 5407707


if __name__ == "__main__":
    run_tests()
    answer1 = main(input_raw, 1, 25)
    answer2 = main(input_raw, 2, 25)
    print("Answer part1: {}".format(answer1))
    print("Answer part2: {}".format(answer2))
