from __future__ import annotations
from utils.tools import get_txt_files, read_input, timing_decorator
from utils.colors import magenta_color, reset_color
from typing import List


files = get_txt_files(__file__)
#########
# Start #
#########


class Puzzle:
    def __init__(self, text_input):
        self.input: List[str] = text_input
        self.register_A = int(self.input[0].split(" ")[-1])
        self.register_B = int(self.input[1].split(" ")[-1])
        self.register_C = int(self.input[2].split(" ")[-1])

        self.program = list(map(int, self.input[4].split(" ")[1].split(",")))

        self.instruction_pointer = 0
        self.jumped = False
        self.halt = False

        self.output = []

        self.combo_operand_map = {
            0: 0,
            1: 1,
            2: 2,
            3: 3,
            4: lambda: self.register_A,
            5: lambda: self.register_B,
            6: lambda: self.register_C,
            7: None,
        }

        self.initial_setup = (self.register_A, self.register_B, self.register_C)
        self.increment = 1

    def run(self, opcode, operand):
        combo_operand = (
            self.combo_operand_map[operand]()
            if callable(self.combo_operand_map[operand])
            else self.combo_operand_map[operand]
        )

        match opcode:
            case 0:  # adv
                self.register_A = self.register_A // (2**combo_operand)

            case 1:  # bxl
                self.register_B = self.register_B ^ operand

            case 2:  # bst
                self.register_B = combo_operand % 8

            case 3:  # jnz
                if self.register_A != 0:
                    self.instruction_pointer = operand
                    self.jumped = True

            case 4:  # bxc
                self.register_B = self.register_B ^ self.register_C

            case 5:  # out
                self.output.append(str(combo_operand % 8))

            case 6:  # bdv
                self.register_B = self.register_A // (2**combo_operand)

            case 7:  # cdv
                self.register_C = self.register_A // (2**combo_operand)

    def run_all_instructions(self):
        while not self.halt:
            self.jumped = False
            self.run(
                opcode=self.program[self.instruction_pointer],
                operand=self.program[self.instruction_pointer + 1],
            )
            if not self.jumped:
                self.instruction_pointer += 2

            if self.instruction_pointer >= len(self.program):
                self.halt = True

    def solve(self, part):
        if part == 1:
            self.run_all_instructions()
            return ",".join(self.output)
        elif part == 2:
            pass


@timing_decorator
def main(raw, part):
    text_input = read_input(raw)
    input_parsed = [i if i else "" for i in text_input]
    puzzle = Puzzle(input_parsed)
    return puzzle.solve(part)


def run_tests():
    print(f"\nRunning Tests:")
    assert main(raw=files["test2"], part=2) == 117440

    assert main(raw=files["test"], part=1) == "4,6,3,5,6,3,5,2,1,0"
    assert main(raw=files["small_test1"], part=1) == ""
    assert main(raw=files["small_test2"], part=1) == "0,1,2"
    assert main(raw=files["small_test3"], part=1) == "4,2,5,6,7,7,7,7,3,1,0"
    assert main(raw=files["small_test4"], part=1) == ""
    assert main(raw=files["small_test5"], part=1) == ""

    # solutions
    # print(f"\nRunning Solutions:")
    # assert main(raw=files["input"], part=1) == 1475249
    # assert main(raw=files["input"], part=2) == 1509724


def solve():
    print(f"\nSolving:")
    answer1 = main(raw=files["input"], part=1)
    print(f"Answer part1: {magenta_color}{answer1}{reset_color}")
    answer2 = main(raw=files["input"], part=2)
    print(f"Answer part2: {magenta_color}{answer2}{reset_color}")


if __name__ == "__main__":
    run_tests()
    solve()
