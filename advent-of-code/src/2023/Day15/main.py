from utils.tools import get_txt_files, read_input, timing_decorator
from utils.colors import magenta_color, reset_color
import re
from typing import List

files = get_txt_files(__file__)
#########
# Start #
#########


class Lens:
    def __init__(self, label, focal_length) -> None:
        self.label = label
        self.focal_length = focal_length


class Box:
    def __init__(self, number) -> None:
        self.number = number
        self.lens: list[Lens] = []
        self.focus_power = {}

    def remove_lens(self, label: str):
        for lens in self.lens:
            if lens.label == label:
                self.lens.remove(lens)
                break

    def replace_lens(self, label: str, new_lens: Lens):
        found = False
        for i, lens in enumerate(self.lens):
            if lens.label == label:
                self.lens[i] = new_lens
                found = True
                break
        if not found:
            self.lens.append(new_lens)

    def get_focusing_power(self):
        self.focus_power = {
            lens.label: (1 + int(self.number)) * i * int(lens.focal_length)
            for i, lens in enumerate(self.lens, 1)
            if lens
        }


class Step:
    def __init__(self, step: str) -> None:
        self.step = step
        self.label = re.split("=|-", step)[0]
        self.focal_length = re.split("=|-", step)[1]
        self.current_value = 0
        self.hashed_value = self.hash(self.current_value, self.step)
        self.box = self.hash(self.current_value, self.label)

    def hash(self, value, string):
        for char in string:
            value += ord(char)
            value *= 17
            value = value % 256
        return value


class Puzzle:
    def __init__(self, text_input):
        self.input = text_input
        self.input_parsed = [Step(step=step) for step in self.input[0].split(",")]
        self.boxes: List[Box] = [Box(number=i) for i in range(0, 256)]

    def hashmap(self):
        for step in self.input_parsed:
            if step.focal_length:  # =
                self.boxes[step.box].replace_lens(
                    step.label, Lens(step.label, step.focal_length)
                )
            else:  # -
                self.boxes[step.box].remove_lens(step.label)
        for box in self.boxes:
            box.get_focusing_power()
        return sum(sum(box.focus_power.values()) for box in self.boxes)

    def solve(self, part):
        if part == 1:
            return sum([step.hashed_value for step in self.input_parsed])
        if part == 2:
            return self.hashmap()


@timing_decorator
def main(raw, part):
    text_input = read_input(raw)
    input_parsed = [i if i else "" for i in text_input]
    puzzle = Puzzle(input_parsed)
    return puzzle.solve(part)


def run_tests():
    print(f"\nRunning Tests:")
    assert main(raw=files["test"], part=1) == 1320
    assert main(raw=files["test"], part=2) == 145

    # solutions
    print(f"\nRunning Solutions:")
    assert main(raw=files["input"], part=1) == 510273
    # assert main(raw=files["input"], part=2) == 32607562


def solve():
    print(f"\nSolving:")
    answer1 = main(raw=files["input"], part=1)
    print(f"Answer part1: {magenta_color}{answer1}{reset_color}")
    answer2 = main(raw=files["input"], part=2)
    print(f"Answer part2: {magenta_color}{answer2}{reset_color}")


if __name__ == "__main__":
    run_tests()
    solve()
