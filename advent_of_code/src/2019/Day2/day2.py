from utils.tools import get_txt_files, read_input, timing_decorator, flatten
from advent_of_code.utils.colors import magenta_color, reset_color
from typing import List
import copy

files = get_txt_files(__file__)

#########
# Start #
#########


class Intcode:
    """
    A simple Intcode computer that can execute a given program.

    Parameters:
    - text_input (List[int]): The initial Intcode program.

    Attributes:
    - input (List[int]): The current state of the Intcode program.
    - current_opcode_pos (int): The current position of the opcode in the program.
    - halt (bool): Flag indicating whether the program has halted.

    Methods:
    - move_opcode(): Move to the next opcode position.
    - do_opcode(): Execute the current opcode.
    - run_program(part: int) -> int: Run the Intcode program with optional modifications for part 1.
    """

    def __init__(self, text_input: List[int]):
        """
        Initialize the Intcode computer with the given program.

        Parameters:
        - text_input (List[int]): The initial Intcode program.
        """
        self.input = text_input
        self.initial_input = copy.deepcopy(text_input)
        self.current_opcode_pos = 0
        self.halt = False
        self.expected_result = 19690720

    def move_opcode(self):
        """
        Move to the next opcode position.
        """
        self.current_opcode_pos += 4

    def do_opcode(self):
        """
        Execute the current opcode.
        """
        if self.input[self.current_opcode_pos] == 1:
            self.input[self.input[self.current_opcode_pos + 3]] = (
                self.input[self.input[self.current_opcode_pos + 1]]
                + self.input[self.input[self.current_opcode_pos + 2]]
            )
        elif self.input[self.current_opcode_pos] == 2:
            self.input[self.input[self.current_opcode_pos + 3]] = (
                self.input[self.input[self.current_opcode_pos + 1]]
                * self.input[self.input[self.current_opcode_pos + 2]]
            )
        elif self.input[self.current_opcode_pos] == 99:
            self.halt = True
        else:
            raise ValueError(
                f"Wrong opcode value: {self.input[self.current_opcode_pos]}"
            )

    def test_noun_verb(self):
        result = next(
            100 * noun + verb
            for noun in range(100)
            for verb in range(100)
            if self.run_program(2, noun, verb) == self.expected_result
        )
        return result

    def reset_computer(self):
        self.input = copy.deepcopy(self.initial_input)
        self.current_opcode_pos = 0
        self.halt = False

    def run_program(self, part: int, noun: int = 12, verb: int = 2) -> int:
        """
        Run the Intcode program with optional modifications for part 1.

        Parameters:
        - part (int): Part of the puzzle (1 or 2).

        Returns:
        - int: The result of the program after execution.
        """
        self.reset_computer()
        if part != 0:
            self.input[1] = noun
            self.input[2] = verb

        while not self.halt:
            self.do_opcode()
            self.move_opcode()

        return self.input[0]


@timing_decorator
def main(raw, part):
    text_input = read_input(raw, sep=",")
    input_parsed = [int(i) if i else "" for i in text_input]
    computer = Intcode(input_parsed)
    if part in (0, 1):
        return computer.run_program(part)
    elif part == 2:
        return computer.test_noun_verb()

    else:
        raise ValueError("part must be 1 or 2, instead of: " + part)


def run_tests():
    print(f"\nRunning Tests:")
    assert main(files["test1_1"], 0) == 3500
    assert main(files["test1_2"], 0) == 2
    assert main(files["test1_3"], 0) == 2
    assert main(files["test1_4"], 0) == 2
    assert main(files["test1_5"], 0) == 30

    # solutions
    assert main(files["input"], 1) == 4462686
    assert main(files["input"], 2) == 5936


def run_solution():
    print(f"\nRunning Solutions:")
    answer1 = main(files["input"], 1)
    print(f"Answer part1: {magenta_color}{answer1}{reset_color}")
    answer2 = main(files["input"], 2)
    print(f"Answer part2: {magenta_color}{answer2}{reset_color}")


if __name__ == "__main__":
    run_tests()
    run_solution()
