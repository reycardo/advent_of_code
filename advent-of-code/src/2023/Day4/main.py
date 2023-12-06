from utils.tools import get_txt_files, read_input, timing_decorator
from utils.colors import magenta_color, reset_color
import re

files = get_txt_files(__file__)
#########
# Start #
#########


class Scratchcard:
    def __init__(self, text_input):
        self.input = text_input
        self.input_parsed = [self.parse_card(card) for card in self.input ]
        a=1

    def solve(self):
        pass

    def parse_card(self, card_string: str):
        sections = card_string.split(":", 1)
        match = re.search(r"\d+", sections[0])

        if match:
            card_number = int(match.group())
        else:
            raise ValueError("No game number found in the input string.")

        winning_numbers, my_numbers = sections[1].split("|", 1)        
        winning_numbers = [num for num in winning_numbers.strip().split() if num]
        my_numbers = [num for num in my_numbers.strip().split() if num]
        return {card_number: (winning_numbers, my_numbers)}

@timing_decorator
def main(raw, part):
    text_input = read_input(raw)
    input_parsed = [i if i else "" for i in text_input]
    scratchcard = Scratchcard(input_parsed)
    return scratchcard.solve(part)


def run_tests():
    print(f"\nRunning Tests:")
    assert main(raw=files["test"], part=1) == 13
    #assert main(raw=files["test"], part=2) == 467835

    # solutions
    print(f"\nRunning Solutions:")
    #assert main(raw=files["input"], part=1) == 544664
    #assert main(raw=files["input"], part=2) == 84495585


def solve():
    print(f"\nSolving:")
    answer1 = main(raw=files["input"], part=1)
    print(f"Answer part1: {magenta_color}{answer1}{reset_color}")
    #answer2 = main(raw=files["input"], part=2)
    #print(f"Answer part2: {magenta_color}{answer2}{reset_color}")


if __name__ == "__main__":
    run_tests()
    solve()
