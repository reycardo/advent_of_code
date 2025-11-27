import sys

sys.path.insert(0, "./")
from utils import tools
import os

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
input_raw = os.path.join(__location__, "input.txt")
test_raw = os.path.join(__location__, "test.txt")
test_raw_2 = os.path.join(__location__, "test2.txt")

#########
# Start #
#########


class Rope_Motion:
    def __init__(self, input: list[str], part: int):
        self.input = input
        self.parsed = self.parse_input()
        self.create_knots(part)
        self.move_rope(part)
        self.answer = len(set(self.tail.occupied))

    def create_knots(self, part: int):
        self.head = Rope_Head()
        if part == 2:
            self.create_middle_knots()
            self.tail = Rope_Tail(self.middles[-1])
        else:
            self.tail = Rope_Tail(self.head)

    def create_middle_knots(self):
        self.middles = [Rope_Tail(self.head)]
        for _ in range(7):
            self.middles.append(Rope_Tail(self.middles[-1]))

    def parse_input(self):
        parsed = []
        for order in self.input:
            splited = order.split(" ")
            parsed.append([splited[0], int(splited[1])])
        return parsed

    def move_rope(self, part):
        for command in self.parsed:
            for _ in range(command[1]):
                self.head.move(command[0])
                if part == 2:
                    [middle.move() for middle in self.middles]
                self.tail.move()


class Rope_Knot:
    def __init__(self):
        self.start = (0, 0)
        self.occupied = [self.start]
        self.pos = self.start


class Rope_Head(Rope_Knot):
    def __init__(self):
        super().__init__()

    def move(self, command):
        self.occupied.append(self.pos)
        if command == "L":
            self.pos = self.pos[0] - 1, self.pos[1]
        elif command == "R":
            self.pos = self.pos[0] + 1, self.pos[1]
        elif command == "U":
            self.pos = self.pos[0], self.pos[1] + 1
        elif command == "D":
            self.pos = self.pos[0], self.pos[1] - 1


class Rope_Tail(Rope_Knot):
    def __init__(self, head: Rope_Head):
        super().__init__()
        self.head = head

    def get_vector(self):
        distance = [self.head.pos[0] - self.pos[0], self.head.pos[1] - self.pos[1]]
        return [distance[0], distance[1]]

    def move(self):
        vector = self.get_vector()
        if abs(vector[0]) <= 1 and abs(vector[1]) <= 1:
            should_move = False
        else:
            should_move = True

        if should_move:
            if vector[0] < -1:
                vector[0] = -1
            elif vector[0] > 1:
                vector[0] = 1

            if vector[1] < -1:
                vector[1] = -1
            elif vector[1] > 1:
                vector[1] = 1
            self.pos = tuple(map(sum, zip(self.pos, vector)))
            self.occupied.append(self.pos)


def main(raw, part):
    input = tools.read_input(raw)
    if part == 1:
        rope = Rope_Motion(input=input, part=1)
        return rope.answer
    elif part == 2:
        rope = Rope_Motion(input=input, part=2)
        return rope.answer
    else:
        raise ValueError("part must be 1 or 2, instead of: " + part)


def run_tests():
    assert main(test_raw, 1) == 13
    assert main(test_raw, 2) == 1
    assert main(test_raw_2, 2) == 36

    # solutions
    assert main(input_raw, 1) == 5858
    assert main(input_raw, 2) == 2602


if __name__ == "__main__":
    run_tests()
    answer1 = main(input_raw, 1)
    answer2 = main(input_raw, 2)
    print("Answer part1: {}".format(answer1))
    print("Answer part2: {}".format(answer2))
