import sys
sys.path.insert(0, './')
import os
from utils import tools
from math import prod, lcm

__location__ = os.path.realpath(os.path.join(
    os.getcwd(), os.path.dirname(__file__)))
input_raw = os.path.join(__location__, 'input.txt')
test_raw = os.path.join(__location__, 'test.txt')

#########
# Start #
#########

class Monkey():

    def __init__(self, number, start_items: list[int], operation: str, test, if_true, if_false, send_to):
        self.number = number
        self.start_items = start_items
        self.operation = operation
        self.test = test
        self.if_true = if_true
        self.if_false = if_false
        self.send_to = send_to

        self.current_items = start_items
        self.activity = 0

    def do_monkey_turn(self, part):
        for item in self.current_items:
            self.inspect_item(item, part)
        self.current_items = []

    def inspect_item(self, item, part):
        item = self.do_operation(item)
        item = self.no_damage(item, part)
        if self.do_test(item):
            self.send_to(item,self.if_true)
        else:
            self.send_to(item,self.if_false)
        self.activity += 1

    def do_test(self, item):
        return item % self.test == 0

    def no_damage(self, item, part):
        if part == 1:
            return item // 3
        else:
            if item > self.lcm:
                return item % self.lcm
            else:
                return item


    def do_operation(self, old):
        number_list = [int(s) for s in self.operation.split() if s.isdigit()]
        if not number_list:
            number = old
        else:
            number = number_list[0]

        if '*' in self.operation:
            return old * number
        elif '+' in self.operation:
            return old + number


class Keep_Away():

    def __init__(self, input: list[str]):
        self.input = input
        self.parsed = self.parse_input()
        self.monkeys = self.create_monkeys()
        self.give_lcm_to_monkeys()
        self.round = 1

    def parse_input(self):
        parsed = [[]]
        for i in self.input:
            if not i:
                parsed.append([])
            else:
                parsed[-1].append(i)
        return parsed

    def get_monkey_info(self, monkey):
        number = [int(s) for s in monkey[0] if s.isdigit()][0]
        start_items = [int(s) for s in monkey[1].replace(',','').split() if s.isdigit()]
        operation = monkey[2].split('= ')[1]
        test = int(monkey[3].split('by ')[1])
        if_true = [int(s) for s in monkey[4] if s.isdigit()][0]
        if_false = [int(s) for s in monkey[5] if s.isdigit()][0]
        return number, start_items, operation, test, if_true, if_false

    def create_monkeys(self) -> list[Monkey]:
        return [Monkey(*self.get_monkey_info(monkey), send_to= self.send_to) for monkey in self.parsed]

    def send_to(self, item, receiver):
        self.monkeys[receiver].current_items.append(item)

    def run_round(self, part):
        for monkey in self.monkeys:
            monkey.do_monkey_turn(part)

    def play(self, n: int, part: int):
        # play n rounds
        for _ in range(n):
            self.run_round(part)
            self.round += 1

    def get_monkey_business(self):
        monkeys_activity = sorted(self.monkeys, key=lambda x: x.activity)
        return prod([monkey.activity for monkey in monkeys_activity[-2:]])

    def give_lcm_to_monkeys(self):
        monkeys_lcm = lcm(*[monkey.test for monkey in self.monkeys])
        for monkey in self.monkeys:
            monkey.lcm = monkeys_lcm



def main(raw, part):
    input = tools.read_input(raw)
    shenanigans = Keep_Away(input=input)
    if part == 1:
        shenanigans.play(20, part)
        return shenanigans.get_monkey_business()
    elif part == 2:
        shenanigans.play(10000, part)
        return shenanigans.get_monkey_business()
    else:
        raise ValueError("part must be 1 or 2, instead of: " + part)


def run_tests():
    assert main(test_raw, 1) == 10605
    assert main(test_raw, 2) == 2713310158

    # solutions
    assert main(input_raw, 1) == 50172
    assert main(input_raw, 2) == 11614682178


if __name__ == '__main__':
    run_tests()
    answer1 = main(input_raw, 1)
    answer2 = main(input_raw, 2)
    print("Answer part1: {}".format(answer1))
    print("Answer part2: {}".format(answer2))
