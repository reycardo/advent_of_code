from utils.tools import get_txt_files, read_input, timing_decorator
from utils.colors import magenta_color, reset_color
from math import lcm

files = get_txt_files(__file__)
#########
# Start #
#########


class Map:
    def __init__(self, map_string: str):
        self.node = map_string.split("=")[0].strip()
        self.left = (
            map_string.split("=")[1].strip().split(",")[0].replace("(", "").strip()
        )
        self.right = (
            map_string.split("=")[1].strip().split(",")[1].replace(")", "").strip()
        )

    def follow_map(self, instruction):
        if instruction == "R":
            return self.right
        elif instruction == "L":
            return self.left
        else:
            raise Exception(f"Invalid instruction: {instruction}")


class Puzzle:
    def __init__(self, text_input):
        self.input = text_input
        self.instruction_sequence = self.input[0]
        self.maps = {Map(i).node: Map(i) for i in self.input[2:]}
        self.start_nodes = self.get_start_nodes()

    def is_end_node(self, node: Map):
        return node.node.endswith("Z")

    def is_end_node_pt1(self, node: Map):
        return node.node.endswith("ZZZ")

    def get_start_nodes(self):
        return [node for node in self.maps.values() if node.node.endswith("A")]

    def navigate_network(self, start_node):
        self.current_node = start_node
        steps = 0
        while not self.is_end_node_pt1(self.current_node):
            i = steps % len(self.instruction_sequence)
            self.current_node = self.maps[
                self.current_node.follow_map(self.instruction_sequence[i])
            ]
            steps += 1
        return steps

    def navigate_network_pt2(self, start_node):
        self.current_node = start_node
        steps = 0
        while not self.is_end_node(self.current_node):
            i = steps % len(self.instruction_sequence)
            self.current_node = self.maps[
                self.current_node.follow_map(self.instruction_sequence[i])
            ]
            steps += 1
        return steps

    def solve(self, part):
        if part == 1:
            self.end_node = self.maps["ZZZ"]
            return self.navigate_network(self.maps["AAA"])
        if part == 2:
            result = [self.navigate_network_pt2(node) for node in self.start_nodes]
            return lcm(*result)


@timing_decorator
def main(raw, part):
    text_input = read_input(raw)
    input_parsed = [i if i else "" for i in text_input]
    puzzle = Puzzle(input_parsed)
    return puzzle.solve(part)


def run_tests():
    print(f"\nRunning Tests:")
    assert main(raw=files["test"], part=1) == 2
    assert main(raw=files["test2"], part=1) == 6
    assert main(raw=files["test3"], part=2) == 6

    # solutions
    print(f"\nRunning Solutions:")
    assert main(raw=files["input"], part=1) == 17873
    assert main(raw=files["input"], part=2) == 15746133679061


def solve():
    print(f"\nSolving:")
    answer1 = main(raw=files["input"], part=1)
    print(f"Answer part1: {magenta_color}{answer1}{reset_color}")
    answer2 = main(raw=files["input"], part=2)
    print(f"Answer part2: {magenta_color}{answer2}{reset_color}")


if __name__ == "__main__":
    run_tests()
    solve()
