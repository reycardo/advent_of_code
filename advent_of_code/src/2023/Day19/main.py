from __future__ import annotations
from advent_of_code.utils.tools import get_txt_files, read_input, timing_decorator
from advent_of_code.utils.colors import magenta_color, reset_color
from typing import List


files = get_txt_files(__file__)
#########
# Start #
#########


class Part:
    def __init__(self, raw):
        self.parse_raw_part(raw)
        self._outcome = None
        self.xmas_rating = self.x + self.m + self.a + self.s

    def parse_raw_part(self, raw):
        self.part = raw[1:-1].split(",")
        self.x, self.m, self.a, self.s = [int(category[2:]) for category in self.part]

    @property
    def outcome(self):
        return self._outcome

    @outcome.setter
    def outcome(self, value):
        self._outcome = value


class Step:
    def __init__(self, raw):
        self.parse_raw_step(raw)

    def parse_raw_step(self, raw):
        splitted_raw = raw.split(":")
        if len(splitted_raw) == 1:
            self.condition = None
            self.output = splitted_raw[0]
        else:
            self.condition = splitted_raw[0]
            self.output = splitted_raw[1]

    def compare(self, a, b):
        if self.condition[1] == ">":
            return a > b
        elif self.condition[1] == "<":
            return a < b

    def solve(self, part: Part):
        if self.condition:
            condition_map = {"x": part.x, "m": part.m, "a": part.a, "s": part.s}
            category = condition_map.get(self.condition[0])
            if category is not None:
                if eval(f"{category} {self.condition[1]} {int(self.condition[2:])}"):
                    part.outcome = self.output
        else:
            part.outcome = self.output

    # WIP
    def solve_ranged(self, range: dict, total=0):
        if self.condition:
            category, operation, value = (
                self.condition[0],
                self.condition[1],
                int(self.condition[2:]),
            )
            low, high = range[category]
            true_split = (low, value - 1) if operation == "<" else (value + 1, high)
            false_split = (low, value) if operation == ">" else (value, high)

            if true_split[0] <= true_split[1]:  # workflow solved go to next
                ranges_copy = dict(range)
                ranges_copy[category] = true_split

            if false_split[0] <= false_split[1]:  # move to next rule
                range = dict(range)
                range[category] = false_split

        else:
            pass


class Workflow:
    def __init__(self, raw):
        self.parse_raw_workflow(raw)

    def parse_raw_workflow(self, raw):
        self.name = raw.split("{")[0]
        self.steps = raw.split("{")[1].replace("}", "").split(",")
        self.steps = [Step(raw) for raw in self.steps]

    def solve_workflow(self, part: Part, workflows: List[Workflow]):
        workflow_map = {workflow.name: workflow for workflow in workflows}

        for step in self.steps:
            step.solve(part)
            if part.outcome:
                break

        if part.outcome in ("A", "R"):
            return part.outcome

        if part.outcome in workflow_map:
            workflow = workflow_map[part.outcome]
            part.outcome = None
            return workflow.solve_workflow(part=part, workflows=workflows)

        return part.outcome

    def solve_ranged_workflow(self, range: dict, workflows: List[Workflow]):
        # workflow_map = {workflow.name: workflow for workflow in workflows}

        for step in self.steps:
            step.solve_ranged(range)

        return


class Puzzle:
    def __init__(self, text_input):
        self.input = text_input
        self.split_workflow_from_parts()
        self.start_workflow: Workflow = self.find_workflow_by_name("in")
        self.range = {key: (1, 4000) for key in ["x", "m", "a", "s"]}

    def split_workflow_from_parts(self):
        separator_index = self.input.index("")
        self.workflows = [Workflow(raw) for raw in self.input[:separator_index]]
        self.parts = [Part(raw) for raw in self.input[separator_index + 1 :]]

    def find_workflow_by_name(self, name):
        for workflow in self.workflows:
            if workflow.name == name:
                return workflow
        return None

    def solve(self, part):
        if part == 1:
            for part in self.parts:
                _ = self.start_workflow.solve_workflow(
                    part=part, workflows=self.workflows
                )
            return sum([part.xmas_rating for part in self.parts if part.outcome == "A"])

        if part == 2:
            self.start_workflow.solve_ranged_workflow(
                range=self.range, workflows=self.workflows
            )


@timing_decorator
def main(raw, part):
    text_input = read_input(raw)
    input_parsed = [i if i else "" for i in text_input]
    puzzle = Puzzle(input_parsed)
    return puzzle.solve(part)


def run_tests():
    print("\nRunning Tests:")
    assert main(raw=files["test"], part=1) == 19114
    # assert main(raw=files["test"], part=2) == 167409079868000

    # solutions
    print("\nRunning Solutions:")
    assert main(raw=files["input"], part=1) == 509597
    # assert main(raw=files["input"], part=2) == 296


def solve():
    print("\nSolving:")
    answer1 = main(raw=files["input"], part=1)
    print(f"Answer part1: {magenta_color}{answer1}{reset_color}")
    answer2 = main(raw=files["input"], part=2)
    print(f"Answer part2: {magenta_color}{answer2}{reset_color}")


if __name__ == "__main__":
    run_tests()
    solve()
