from advent_of_code.utils.tools import get_txt_files, read_input, timing_decorator
from advent_of_code.utils.colors import magenta_color, reset_color
from collections import deque
import pulp

files = get_txt_files(__file__)

class Button:
    def __init__(self, *positions):
        self.positions = positions

    def __repr__(self):
        return f"Button{self.positions}"

    def press(self, machine_state):
        state_list = list(machine_state)
        for pos in self.positions:
            state_list[pos] = '#' if state_list[pos] == '.' else '.'
        return ''.join(state_list)

    def increase_joltage(self, machine_joltage: list):
        state_list = machine_joltage
        for pos in self.positions:
            state_list[pos] += 1
        return state_list

class Machine:
    def __init__(self, instructions):
        self.indicator_light_diagram = instructions[0][1:-1]
        self.buttons = [Button(*map(int, s[1:-1].split(','))) for s in instructions[1:-1]]
        self.joltage_requirements = list(map(int, instructions[-1][1:-1].split(',')))
        self.state = '.' * len(instructions[0][1:-1])
        self.joltage_state = [0] * len(self.joltage_requirements)
        self.presses = 0

    def turn_on_machine(self):    

        target = self.indicator_light_diagram
        visited = set()
        queue = deque([(self.state, 0)])  # (current_state, presses)

        while queue:
            state, presses = queue.popleft()
            if state == target:
                return presses
            if state in visited:
                continue
            visited.add(state)
            for button in self.buttons:
                next_state = button.press(state)
                if next_state not in visited:
                    queue.append((next_state, presses + 1))
        raise Exception("impossible")

    def meet_joltage_reqs(self):
        n = len(self.joltage_requirements)
        m = len(self.buttons)
        # Build coefficient matrix
        A = [[0]*m for _ in range(n)]
        for j, button in enumerate(self.buttons):
            for pos in button.positions:
                A[pos][j] = 1
        b = self.joltage_requirements

        # Define LP problem
        prob = pulp.LpProblem("ButtonPresses", pulp.LpMinimize)
        x = [pulp.LpVariable(f"x{j}", lowBound=0, cat="Integer") for j in range(m)]
        # Objective: minimize total presses
        prob += pulp.lpSum(x)
        # Constraints: match joltage requirements
        for i in range(n):
            prob += pulp.lpSum(A[i][j] * x[j] for j in range(m)) == b[i]

        # Solve        
        result = prob.solve(pulp.PULP_CBC_CMD(msg=False))
        if result != pulp.LpStatusOptimal:
            raise Exception("impossible")
        return int(sum(var.value() for var in x))

class Puzzle:
    def __init__(self, text_input):
        self.input = text_input
        self.machines = self.parse_input()

    def parse_input(self):
        return [Machine(row.split()) for row in self.input]

    def solve(self, part):
        if part == 1:
            for machine in self.machines:
                machine.presses = machine.turn_on_machine()
            return sum(machine.presses for machine in self.machines)
        if part == 2:
            for machine in self.machines:
                machine.presses = machine.meet_joltage_reqs()
            return sum(machine.presses for machine in self.machines)


@timing_decorator
def main(raw, part):
    text_input = read_input(raw)
    input_parsed = [i if i else "" for i in text_input]
    puzzle = Puzzle(input_parsed)    
    return puzzle.solve(part)


def run_tests():
    print("\nRunning Tests:")
    assert main(raw=files["test"], part=1) == 7
    assert main(raw=files["test"], part=2) == 33

    # solutions
    print("\nRunning Solutions:")
    assert main(raw=files["input"], part=1) == 434
    assert main(raw=files["input"], part=2) == 15132


def solve():
    print("\nSolving:")
    answer1 = main(raw=files["input"], part=1)
    print(f"Answer part1: {magenta_color}{answer1}{reset_color}")
    answer2 = main(raw=files["input"], part=2)
    print(f"Answer part2: {magenta_color}{answer2}{reset_color}")


if __name__ == "__main__":
    run_tests()
    solve()
