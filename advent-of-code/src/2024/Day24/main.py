from __future__ import annotations
from utils.tools import get_txt_files, read_input, timing_decorator
from utils.colors import magenta_color, reset_color
from typing import List, Tuple, Dict
import operator

files = get_txt_files(__file__)
#########
# Start #
#########

class Wire:
    def __init__(self, raw: str):                
        self.raw = raw
        self.name, val = raw.split(":")
        self.val = int(val.strip())

class Gate:
    OPERATORS = {
        "XOR": operator.xor,
        "AND": operator.and_,
        "OR": operator.or_,
    }

    def __init__(self, raw: str):        
        self.raw = raw
        parts = self.raw.split()
        self.inputs = (parts[0], parts[2])
        self.output = parts[-1]
        self.operation = self.OPERATORS.get(parts[1])

    def solve(self, wires: Dict[str, int]):
        wires[self.output] = self.operation(wires[self.inputs[0]],wires[self.inputs[1]])
        return wires

class Puzzle:
    def __init__(self, text_input):
        self.input: List[str] = text_input
        self.split_wires_from_gates()

    def split_wires_from_gates(self):
        separator_index = self.input.index("")        
        self.wires = {wire.name: wire.val for wire in (Wire(raw) for raw in self.input[:separator_index])}
        self.gates = [Gate(raw) for raw in self.input[separator_index + 1 :]]

    def solve(self, part):
        if part == 1:
            pass
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
    assert main(raw=files["test"], part=1) == 4
    assert main(raw=files["test2"], part=1) == 2024    

    # solutions
    # print(f"\nRunning Solutions:")
    # assert main(raw=files["input"], part=1) == 1476
    # assert main(raw=files["input"], part=2) == 662726441391898


def solve():
    print(f"\nSolving:")
    answer1 = main(raw=files["input"], part=1)
    print(f"Answer part1: {magenta_color}{answer1}{reset_color}")
    # answer2 = main(raw=files["input"], part=2)
    # print(f"Answer part2: {magenta_color}{answer2}{reset_color}")


if __name__ == "__main__":
    run_tests()
    solve()
