from utils.tools import get_txt_files, read_input, timing_decorator
from utils.colors import magenta_color, reset_color
import re

files = get_txt_files(__file__)
#########
# Start #
#########


class Card:
    def __init__(self, card_string: str):
        self.parse_card(card_string)
        self.check_winning_numbers()
        self.get_card_points()
        self.copies = 0

    def parse_card(self, card_string: str):
        sections = card_string.split(":", 1)
        match = re.search(r"\d+", sections[0])

        if match:
            self.card_number = int(match.group())
        else:
            raise ValueError("No game number found in the input string.")

        winning_numbers, my_numbers = sections[1].split("|", 1)
        self.winning_numbers = {num for num in winning_numbers.strip().split() if num}
        self.my_numbers = {num for num in my_numbers.strip().split() if num}

    def check_winning_numbers(self):
        self.card_winning_numbers = self.my_numbers & self.winning_numbers

    def get_card_points(self):
        self.points = (
            2 ** (len(self.card_winning_numbers) - 1)
            if self.card_winning_numbers
            else 0
        )


class Scratchcards:
    def __init__(self, text_input):
        self.input = text_input
        self.scratchcards = [Card(cardstring) for cardstring in self.input]

    def parse_copies(self, card: Card):
        multiplier = card.copies + 1
        if card.card_winning_numbers:
            for x in range(1, len(card.card_winning_numbers) + 1):
                self.scratchcards[card.card_number + x - 1].copies += multiplier

    def process_card_copies(self):
        for card in self.scratchcards:
            self.parse_copies(card)

    def count_copies_and_originals(self):
        self.total_scratchcards = sum([card.copies + 1 for card in self.scratchcards])

    def solve(self, part):
        if part == 1:
            return sum([card.points for card in self.scratchcards])
        if part == 2:
            self.process_card_copies()
            self.count_copies_and_originals()
            return self.total_scratchcards


@timing_decorator
def main(raw, part):
    text_input = read_input(raw)
    input_parsed = [i if i else "" for i in text_input]
    puzzle = Scratchcards(input_parsed)
    return puzzle.solve(part)


def run_tests():
    print(f"\nRunning Tests:")
    assert main(raw=files["test"], part=1) == 13
    assert main(raw=files["test"], part=2) == 30

    # solutions
    print(f"\nRunning Solutions:")
    assert main(raw=files["input"], part=1) == 21919
    assert main(raw=files["input"], part=2) == 9881048


def solve():
    print(f"\nSolving:")
    answer1 = main(raw=files["input"], part=1)
    print(f"Answer part1: {magenta_color}{answer1}{reset_color}")
    answer2 = main(raw=files["input"], part=2)
    print(f"Answer part2: {magenta_color}{answer2}{reset_color}")


if __name__ == "__main__":
    run_tests()
    solve()
