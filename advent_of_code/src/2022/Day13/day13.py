import sys

sys.path.insert(0, "./")
import os
from utils import tools
from itertools import groupby, zip_longest
from functools import cmp_to_key
import json


__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
input_raw = os.path.join(__location__, "input.txt")
test_raw = os.path.join(__location__, "test.txt")

#########
# Start #
#########


class Distress_Signal:
    def __init__(self, input):
        self.input = input
        self.parsed = self.parse_input()
        self.parsed2 = self.parse_input_pt2()
        self.parsed2.extend([[[2]], [[6]]])

    def parse_input_pt2(self):
        return [
            json.loads(sub) for sub in self.input if sub
        ]  # split packet pairs into dict where key is pair indice and value lists

    def parse_input(self):
        _dict = {
            id // 2 + 1: list(sub[1])
            for id, sub in enumerate(groupby(self.input, key=bool))
            if sub[0]
        }  # split packet pairs into dict where key is pair indice and value lists
        return {
            key: {"left": json.loads(val[0]), "right": json.loads(val[1])}
            for key, val in _dict.items()
        }  # separate vals into left and right

    def comparation(self, left, right):
        # ran out of items
        if left is None:
            return -1
        elif right is None:
            return 1

        # conver other int to list
        if isinstance(left, list) and isinstance(right, int):
            right = [right]
        elif isinstance(left, int) and isinstance(right, list):
            left = [left]

        # compare ints
        if isinstance(left, int) and isinstance(right, int):
            if left < right:
                return -1
            elif left > right:
                return 1

        # compare inner list
        elif isinstance(left, list) and isinstance(right, list):
            for inner_left, inner_right in zip_longest(left, right):
                found = self.comparation(
                    inner_left, inner_right
                )  # compares left[0] with right[0] and so on
                if found is not None:
                    break  # breaks for loop to return found
            if right or left:  # same as if 2 empty lists continue
                return found

    def run(self, part):
        if part == 1:
            self.pocket_pairs = {
                k: self.comparation(value["left"], value["right"])
                for k, value in self.parsed.items()
            }
        else:
            self.pocket_pairs = sorted(
                self.parsed2, key=cmp_to_key(lambda x, y: self.comparation(x, y))
            )

    def get_answer(self, part):
        if part == 1:
            return sum(
                [key for key, val in self.pocket_pairs.items() if val == -1]
            )  # sums all indices if vals returned True
        else:
            return (self.pocket_pairs.index([[2]]) + 1) * (
                self.pocket_pairs.index([[6]]) + 1
            )


def main(raw, part):
    input = tools.read_input(raw)
    distress_signal = Distress_Signal(input=input)
    if part in (1, 2):
        distress_signal.run(part)
        return distress_signal.get_answer(part)
    else:
        raise ValueError("part must be 1 or 2, instead of: " + part)


def run_tests():
    assert main(test_raw, 1) == 13
    assert main(test_raw, 2) == 140

    # solutions
    assert main(input_raw, 1) == 5529
    # assert main(input_raw, 2) == 480


if __name__ == "__main__":
    run_tests()
    answer1 = main(input_raw, 1)
    answer2 = main(input_raw, 2)
    print("Answer part1: {}".format(answer1))
    print("Answer part2: {}".format(answer2))
