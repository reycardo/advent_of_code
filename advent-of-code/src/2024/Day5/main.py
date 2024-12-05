from utils.tools import get_txt_files, read_input, timing_decorator
from utils.colors import magenta_color, reset_color
from collections import defaultdict

files = get_txt_files(__file__)
#########
# Start #
#########

class Rule:
    def __init__(self, raw):
        self.parse_raw(raw)


    def parse_raw(self, raw):
        self.order = raw.split("|")
        self.lower = int(self.order[0])
        self.upper = int(self.order[1])

class Update:
    def __init__(self, raw):
        self.parse_raw(raw)        

    def get_midle(self):
        return self.pages[int((len(self.pages) - 1)/2)]

    def parse_raw(self, raw):
        self.pages = list(map(int,raw.split(",")))


class Puzzle:
    def __init__(self, text_input):
        self.input = text_input
        self.split_input()
        self.setup_page_boundaries()
        self.valids = []
        self.invalids = []

    def split_input(self):
        separator_index = self.input.index("")
        self.rules = [Rule(raw) for raw in self.input[:separator_index]]
        self.updates = [Update(raw) for raw in self.input[separator_index + 1 :]]

    def setup_page_boundaries(self):
        self.page_uppers = defaultdict(list)
        self.page_lowers = defaultdict(list)
        
        for rule in self.rules:
            self.page_uppers[rule.lower].append(rule.upper)
            self.page_lowers[rule.upper].append(rule.lower)
            
    def validate_update(self, update):
        for page in update.pages:
            pages_to_the_right = update.pages[update.pages.index(page) + 1:]
            pages_to_the_left = update.pages[:update.pages.index(page)]

            # check if there is a page to the right that should be to the left
            for right_page in pages_to_the_right:
                if right_page in self.page_lowers[page]:
                    return False
            
            # check if there is a page to the left that should be to the right
            for left_page in pages_to_the_left:
                if left_page in self.page_uppers[page]:
                    return False
        return True

    def order_invalid_update(self, update):
        for page in update.pages:
            pages_to_the_right = update.pages[update.pages.index(page) + 1:]
            pages_to_the_left = update.pages[:update.pages.index(page)]

            # check if there is a page to the right that should be to the left
            for right_page in pages_to_the_right:
                if right_page in self.page_lowers[page]:
                    # put right_page to the left of page
                    update.pages[update.pages.index(right_page)] = page
                    update.pages[update.pages.index(page)] = right_page
                    update = self.order_invalid_update(update)
            
            # check if there is a page to the left that should be to the right
            for left_page in pages_to_the_left:
                if left_page in self.page_uppers[page]:
                    # put left_page to the right of page
                    update.pages[update.pages.index(left_page)] = page
                    update.pages[update.pages.index(page)] = left_page
                    update = self.order_invalid_update(update)
        return update

    def validate_updates(self):
        for update in self.updates:
            if self.validate_update(update):
                self.valids.append(update)
            else:
                self.invalids.append(update)


    def solve(self, part):                
        self.validate_updates()
        if part == 1:            
            self.midles = [update.get_midle() for update in self.valids]            
        elif part == 2:
            self.ordered_invalids = [self.order_invalid_update(update) for update in self.updates if update not in self.valids]
            self.midles = [update.get_midle() for update in self.ordered_invalids]
        return sum(self.midles)
            


@timing_decorator
def main(raw, part):
    text_input = read_input(raw)
    input_parsed = [i if i else "" for i in text_input]
    puzzle = Puzzle(input_parsed)
    return puzzle.solve(part)


def run_tests():
    print(f"\nRunning Tests:")
    assert main(raw=files["test"], part=1) == 143
    assert main(raw=files["test"], part=2) == 123

    # solutions
    print(f"\nRunning Solutions:")
    assert main(raw=files["input"], part=1) == 7365
    assert main(raw=files["input"], part=2) == 5770


def solve():
    print(f"\nSolving:")
    answer1 = main(raw=files["input"], part=1)
    print(f"Answer part1: {magenta_color}{answer1}{reset_color}")
    answer2 = main(raw=files["input"], part=2)
    print(f"Answer part2: {magenta_color}{answer2}{reset_color}")


if __name__ == "__main__":
    run_tests()
    solve()
