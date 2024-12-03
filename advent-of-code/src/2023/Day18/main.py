from utils.tools import get_txt_files, read_input, timing_decorator
from utils.colors import magenta_color, reset_color

files = get_txt_files(__file__)
#########
# Start #
#########


class Dig_Instruction:
    def __init__(self, instruction, part=1):
        self.instruction = instruction
        self.direction, self.amount, self.color = self.instruction.split()
        self.amount = int(self.amount)
        self.color = self.color.replace("(", "").replace(")", "")

        if part == 2:
            self.amount = int(self.color.lstrip("#")[:-1], 16)
            # 0 means R, 1 means D, 2 means L, and 3 means U.
            letters = ["R", "D", "L", "U"]
            self.direction = letters[int(self.color[-1])]

    def parse_hexadecimal(self, hex_color):
        hex_color = hex_color.lstrip("#")
        return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))

    def apply_instruction(self, pool, current_point):
        x, y = current_point
        for _ in range(self.amount):
            if self.direction == "U":
                y += 1
            elif self.direction == "D":
                y -= 1
            elif self.direction == "L":
                x -= 1
            elif self.direction == "R":
                x += 1
            pool.append(((x, y), self.color))
        current_point = (x, y)
        return pool, current_point

    def apply_instruction_p2(self, pool, current_point):
        x, y = current_point
        if self.direction == "U":
            y += self.amount
        elif self.direction == "D":
            y -= self.amount
        elif self.direction == "L":
            x -= self.amount
        elif self.direction == "R":
            x += self.amount
        pool.append(((x, y), self.color))
        current_point = (x, y)
        return pool, current_point, self.amount


class Puzzle:
    def __init__(self, text_input):
        self.input = text_input
        self.vertices = []
        self.pool = []

    def calculate_lava_capacity(self, points, edges):
        # return interior + exterior points

        n = len(points)
        area = 0

        # shoelace
        for i in range(n):
            x1, y1 = points[i]
            x2, y2 = points[(i + 1) % n]  # Wrap around to the first point
            area += x1 * y2 - x2 * y1

        area = abs(area) / 2

        # Pick's theorem

        # interior + (exterior/2) - 1 = area
        # interior + (exterior/2) = area + 1
        # interior = area + 1 - (exterior/2)

        interior = area + 1 - (edges / 2)
        return int(interior + edges)

    def solve(self, part):
        if part == 1:
            self.dig_plan = [Dig_Instruction(i, part) for i in self.input]
            current_point = (0, 0)
            for instruction in self.dig_plan:
                self.pool, current_point = instruction.apply_instruction(
                    self.pool, current_point
                )
                self.vertices.append(current_point)
            self.trench_edges = [point[0] for point in self.pool]
            lava_cap = self.calculate_lava_capacity(
                self.vertices, len(self.trench_edges)
            )
            return lava_cap
        if part == 2:
            self.dig_plan = [Dig_Instruction(i, part) for i in self.input]
            current_point = (0, 0)
            ext_points = 0
            for instruction in self.dig_plan:
                self.pool, current_point, amount = instruction.apply_instruction_p2(
                    self.pool, current_point
                )
                ext_points += amount
            self.vertices = [point[0] for point in self.pool]
            lava_cap = self.calculate_lava_capacity(self.vertices, ext_points)
            return lava_cap


@timing_decorator
def main(raw, part):
    text_input = read_input(raw)
    input_parsed = [i if i else "" for i in text_input]
    puzzle = Puzzle(input_parsed)
    return puzzle.solve(part)


def run_tests():
    print(f"\nRunning Tests:")
    assert main(raw=files["test"], part=1) == 62
    assert main(raw=files["test"], part=2) == 952408144115

    # solutions
    print(f"\nRunning Solutions:")
    assert main(raw=files["input"], part=1) == 45159
    # assert main(raw=files["input"], part=2) == 296


def solve():
    print(f"\nSolving:")
    answer1 = main(raw=files["input"], part=1)
    print(f"Answer part1: {magenta_color}{answer1}{reset_color}")
    answer2 = main(raw=files["input"], part=2)
    print(f"Answer part2: {magenta_color}{answer2}{reset_color}")


if __name__ == "__main__":
    run_tests()
    solve()
