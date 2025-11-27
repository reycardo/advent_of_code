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


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i : i + n]


def separate_compartments(string):
    return string[: len(string) // 2], string[len(string) // 2 :]


def find_common(first: str, second: str):
    return list(set(first).intersection(second))


def find_common_pt2(first: str, second: str, third: str):
    return list(set(first).intersection(second).intersection(third))


class Rucksacks:
    def __init__(self, input: list):
        self.input = input
        self.compartments = self.get_compartments()
        self.answer1 = self.sum_priorities()
        self.elf_groups = list(chunks(self.input, 3))
        self.answer2 = self.sum_priorities_pt2()

    def get_compartments(self):
        return [separate_compartments(string) for string in self.input]

    def get_priority(self, letter):
        if letter.isupper():
            return ord(letter) - 38
        return ord(letter) - 96

    def sum_priorities(self):
        commons = [find_common(i[0], i[1]) for i in self.compartments]
        priorities = [self.get_priority(letter_list[0]) for letter_list in commons]
        return sum(priorities)

    def sum_priorities_pt2(self):
        commons = [find_common_pt2(i[0], i[1], i[2]) for i in self.elf_groups]
        priorities = [self.get_priority(letter_list[0]) for letter_list in commons]
        return sum(priorities)


def main(raw, part):
    input = tools.read_input(raw)
    rucksacks = Rucksacks(input)
    if part == 1:
        return rucksacks.answer1
    elif part == 2:
        return rucksacks.answer2
    else:
        raise ValueError("part must be 1 or 2, instead of: " + part)


def run_tests():
    assert main(test_raw, 1) == 157
    assert main(test_raw, 2) == 70
    # solutions
    assert main(input_raw, 1) == 8401
    assert main(input_raw, 2) == 2641


if __name__ == "__main__":
    run_tests()
    answer1 = main(input_raw, 1)
    answer2 = main(input_raw, 2)
    print("Answer part1: {}".format(answer1))
    print("Answer part2: {}".format(answer2))
