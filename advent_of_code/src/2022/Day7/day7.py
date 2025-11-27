import os
import sys

sys.path.insert(0, "./")
from utils import tools
import networkx as nx


__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
input_raw = os.path.join(__location__, "input.txt")
test_raw = os.path.join(__location__, "test.txt")

#########
# Start #
#########


class Browse:
    def __init__(self, input: list):
        self.input = input
        self.G = self.init_graph()
        self.current_node = self.G.nodes["/"]

    def run(self):
        for rule in self.input:
            self.apply_command(rule)

    def init_graph(self) -> nx.DiGraph:
        G = nx.DiGraph()
        G.add_node("/", size=0, directory=True)
        return G

    def apply_command(self, string: str):
        if string.startswith("$ cd /"):
            self.current_node = "/"

        elif string == "$ cd ..":
            self.current_node = list(self.G.predecessors(self.current_node))[0]

        elif string.startswith("$ cd "):
            self.current_node = self.current_node + string[5:] + "/"

        elif string.startswith("dir "):
            new_dir = self.current_node + string[4:] + "/"
            self.G.add_edge(self.current_node, new_dir)
            nx.set_node_attributes(self.G, {new_dir: 0}, name="size")
            nx.set_node_attributes(self.G, {new_dir: True}, name="directory")

        elif string[0].isdigit():
            separated = string.split(" ")
            size, name = int(separated[0]), separated[1]
            self.G.add_edge(self.current_node, name)
            nx.set_node_attributes(
                self.G, {name: size}, name="size"
            )  # add size to file
            nx.set_node_attributes(
                self.G,
                {self.current_node: self.G.nodes[self.current_node]["size"] + size},
                name="size",
            )  # add size to current dir
            for parent in nx.ancestors(self.G, self.current_node):
                nx.set_node_attributes(
                    self.G, {parent: self.G.nodes[parent]["size"] + size}, name="size"
                )  # add size to parent dirs
            nx.set_node_attributes(self.G, {name: False}, name="directory")

    def get_dir_size_pt1(self):
        val = 0
        for node, data in self.G.nodes.data():
            if data["directory"]:
                if data["size"] <= 100000:
                    val += data["size"]
        return val

    def get_dir_size_pt2(self):
        total = 70000000
        need = 30000000
        used = self.G.nodes["/"]["size"]
        unused = total - used
        to_delete = need - unused
        return min(
            [
                data["size"]
                for _, data in self.G.nodes.data()
                if data["directory"] and data["size"] >= to_delete
            ]
        )


def main(raw, part):
    input = tools.read_input(raw)
    filesystem = Browse(input=input)
    filesystem.run()
    if part == 1:
        return filesystem.get_dir_size_pt1()
    elif part == 2:
        return filesystem.get_dir_size_pt2()
    else:
        raise ValueError("part must be 1 or 2, instead of: " + part)


def run_tests():
    assert main(test_raw, 1) == 95437
    assert main(test_raw, 2) == 24933642

    # solutions
    assert main(input_raw, 1) == 1642503
    assert main(input_raw, 2) == 6999588


if __name__ == "__main__":
    run_tests()
    answer1 = main(input_raw, 1)
    answer2 = main(input_raw, 2)
    print("Answer part1: {}".format(answer1))
    print("Answer part2: {}".format(answer2))
