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
        self.solved = False

    def solve(self, wires: Dict[str, Wire]) -> Dict[str, Wire]:
        if self.inputs[0] in wires and self.inputs[1] in wires:
            result = self.operation(
                wires[self.inputs[0]].val, wires[self.inputs[1]].val
            )
            wires[self.output] = Wire(f"{self.output}: {result}")
            self.solved = True
        return wires


class Puzzle:
    def __init__(self, text_input):
        self.input: List[str] = text_input
        self.split_wires_from_gates()

    def split_wires_from_gates(self):
        separator_index = self.input.index("")
        self.wires: Dict[str, Wire] = {
            wire.name: wire
            for wire in (Wire(raw) for raw in self.input[:separator_index])
        }
        self.gates = [Gate(raw) for raw in self.input[separator_index + 1 :]]

    def convert_binary_to_decimal(self, binary: str) -> int:
        return int(binary, 2)

    def get_solution(self):
        sorted_zs = sorted(
            [
                (wire.name, wire.val)
                for wire in self.wires.values()
                if wire.name.startswith("z")
            ],
            reverse=True,
        )
        return self.convert_binary_to_decimal(
            "".join(list(map(str, [t[1] for t in sorted_zs])))
        )

    def get_solution_pt2(self):
        sorted_zs = sorted(
            [
                (wire.name, wire.val)
                for wire in self.wires.values()
                if wire.name.startswith("z")
            ],
            reverse=True,
        )
        sorted_xs = sorted(
            [
                (wire.name, wire.val)
                for wire in self.wires.values()
                if wire.name.startswith("x")
            ],
            reverse=True,
        )
        sorted_ys = sorted(
            [
                (wire.name, wire.val)
                for wire in self.wires.values()
                if wire.name.startswith("y")
            ],
            reverse=True,
        )
        z = "".join(list(map(str, [t[1] for t in sorted_zs])))

        x = "".join(list(map(str, [t[1] for t in sorted_xs])))

        y = "".join(list(map(str, [t[1] for t in sorted_ys])))
        bin_sum = bin(int(x, 2) + int(y, 2))[2:]
        return x, y, z, bin_sum

    # TODO: check what bits are wrong, swap only the wires that appear on the list that reach to those bits?

    def solve(self, part):
        if part == 1:
            # solve all gates until all are solved
            while not all(gate.solved for gate in self.gates):
                for gate in self.gates:
                    self.wires = gate.solve(self.wires)
            return self.get_solution()
        elif part == 2:
            while not all(gate.solved for gate in self.gates):
                for gate in self.gates:
                    self.wires = gate.solve(self.wires)
            cenas = self.get_solution_pt2()
            pass
            return


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
    assert main(raw=files["test3"], part=2) == 2024

    # solutions
    print(f"\nRunning Solutions:")
    assert main(raw=files["input"], part=1) == 53258032898766
    # assert main(raw=files["input"], part=2) == 662726441391898


def solve():
    print(f"\nSolving:")
    answer1 = main(raw=files["input"], part=1)
    print(f"Answer part1: {magenta_color}{answer1}{reset_color}")
    answer2 = main(raw=files["input"], part=2)
    print(f"Answer part2: {magenta_color}{answer2}{reset_color}")


if __name__ == "__main__":
    run_tests()
    solve()
