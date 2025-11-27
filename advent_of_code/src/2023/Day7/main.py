from utils.tools import get_txt_files, read_input, timing_decorator
from advent_of_code.utils.colors import magenta_color, reset_color
from typing import List
from collections import Counter
from functools import cmp_to_key

files = get_txt_files(__file__)
#########
# Start #
#########


class Hand:
    def __init__(self, row, part):
        self.hand: str = row[0]
        self.bid = int(row[1])
        self.hand_counts = Counter(self.hand)
        self.check_hand_type(part)

    def parse_jokers(self):
        self.jokers = self.hand_counts.get("J", 0)
        if self.jokers > 0:
            # Remove 'J' from hand_counts
            del self.hand_counts["J"]

        # Find the character with the max count
        max_char = (
            max(self.hand_counts, key=self.hand_counts.get) if self.hand_counts else "J"
        )

        # Replace 'J' with max_char in the hand
        self.hand_wild = self.hand.replace("J", max_char)

        # Recalculate hand_counts
        self.hand_counts = Counter(self.hand_wild)

    def check_hand_type(self, part=1):
        if part == 2:
            self.parse_jokers()

        if max(self.hand_counts.values()) == 5:
            self.hand_type = "Five of a Kind"
        elif max(self.hand_counts.values()) == 4:
            self.hand_type = "Four of a Kind"
        elif (
            max(self.hand_counts.values()) == 3 and min(self.hand_counts.values()) == 2
        ):
            self.hand_type = "Full House"
        elif max(self.hand_counts.values()) == 3:
            self.hand_type = "Three of a Kind"
        elif max(self.hand_counts.values()) == 2 and len(self.hand_counts) == 3:
            self.hand_type = "Two Pair"
        elif max(self.hand_counts.values()) == 2:
            self.hand_type = "One Pair"
        else:
            self.hand_type = "High Card"

    def get_hand_winnings(self):
        return self.bid * self.rank


class Puzzle:
    card_order = {
        "A": 1,
        "K": 2,
        "Q": 3,
        "J": 4,
        "T": 5,
        "9": 6,
        "8": 7,
        "7": 8,
        "6": 9,
        "5": 10,
        "4": 11,
        "3": 12,
        "2": 13,
    }
    new_card_order = {
        "A": 1,
        "K": 2,
        "Q": 3,
        "T": 4,
        "9": 5,
        "8": 6,
        "7": 7,
        "6": 8,
        "5": 9,
        "4": 10,
        "3": 11,
        "2": 12,
        "J": 13,
    }
    hand_types = [
        "Five of a Kind",
        "Four of a Kind",
        "Full House",
        "Three of a Kind",
        "Two Pair",
        "One Pair",
        "High Card",
    ]

    def __init__(self, text_input, part):
        self.input = text_input
        self.input_parsed = self.parse_input(part)
        self.organize_hands()
        self.sort_hands_by_rank(part)
        self.order_all_hands()
        self.give_ranks_to_cards()

    def parse_input(self, part):
        return [Hand(row, part) for row in (item.split(" ") for item in self.input)]

    def order_all_hands(self):
        self.ordered_hands: List[Hand] = (
            self.HIGH_CARD
            + self.ONE_PAIR
            + self.TWO_PAIR
            + self.THREE_OF_A_KIND
            + self.FULL_HOUSE
            + self.FOUR_OF_A_KIND
            + self.FIVE_OF_A_KIND
        )

    def give_ranks_to_cards(self):
        for hand in self.ordered_hands:
            hand.rank = self.ordered_hands.index(hand) + 1

    def get_total_winnings(self):
        return sum([hand.get_hand_winnings() for hand in self.ordered_hands])

    def organize_hands(self):
        self.FIVE_OF_A_KIND = []
        self.FOUR_OF_A_KIND = []
        self.FULL_HOUSE = []
        self.THREE_OF_A_KIND = []
        self.TWO_PAIR = []
        self.ONE_PAIR = []
        self.HIGH_CARD = []

        for hand in self.input_parsed:
            if hand.hand_type == "Five of a Kind":
                self.FIVE_OF_A_KIND.append(hand)
            elif hand.hand_type == "Four of a Kind":
                self.FOUR_OF_A_KIND.append(hand)
            elif hand.hand_type == "Full House":
                self.FULL_HOUSE.append(hand)
            elif hand.hand_type == "Three of a Kind":
                self.THREE_OF_A_KIND.append(hand)
            elif hand.hand_type == "Two Pair":
                self.TWO_PAIR.append(hand)
            elif hand.hand_type == "One Pair":
                self.ONE_PAIR.append(hand)
            elif hand.hand_type == "High Card":
                self.HIGH_CARD.append(hand)

    def compare_hands(self, hand1: Hand, hand2: Hand):
        for character1, character2 in zip(hand1.hand, hand2.hand):
            if self.card_order[character1] < self.card_order[character2]:
                return 1
            elif self.card_order[character1] > self.card_order[character2]:
                return -1
        return 0

    def compare_hands_new_order(self, hand1: Hand, hand2: Hand):
        for character1, character2 in zip(hand1.hand, hand2.hand):
            if self.new_card_order[character1] < self.new_card_order[character2]:
                return 1
            elif self.new_card_order[character1] > self.new_card_order[character2]:
                return -1
        return 0

    def sort_hands(self, hand_list, comparison_method):
        return sorted(hand_list, key=cmp_to_key(comparison_method))

    def sort_hands_by_rank(self, part):
        if part == 1:
            compare_method = self.compare_hands
        elif part == 2:
            compare_method = self.compare_hands_new_order
        self.FIVE_OF_A_KIND = self.sort_hands(self.FIVE_OF_A_KIND, compare_method)
        self.FOUR_OF_A_KIND = self.sort_hands(self.FOUR_OF_A_KIND, compare_method)
        self.FULL_HOUSE = self.sort_hands(self.FULL_HOUSE, compare_method)
        self.THREE_OF_A_KIND = self.sort_hands(self.THREE_OF_A_KIND, compare_method)
        self.TWO_PAIR = self.sort_hands(self.TWO_PAIR, compare_method)
        self.ONE_PAIR = self.sort_hands(self.ONE_PAIR, compare_method)
        self.HIGH_CARD = self.sort_hands(self.HIGH_CARD, compare_method)

    def solve(self, part):
        return self.get_total_winnings()


@timing_decorator
def main(raw, part):
    text_input = read_input(raw)
    input_parsed = [i if i else "" for i in text_input]
    puzzle = Puzzle(input_parsed, part)
    return puzzle.solve(part)


def run_tests():
    print(f"\nRunning Tests:")
    assert main(raw=files["test"], part=1) == 6440
    assert main(raw=files["test"], part=2) == 5905
    assert main(raw=files["test2"], part=2) == 78
    assert main(raw=files["test3"], part=2) == 6839

    # solutions
    print(f"\nRunning Solutions:")
    assert main(raw=files["input"], part=1) == 253954294
    assert main(raw=files["input"], part=2) == 254837398


def solve():
    print(f"\nSolving:")
    answer1 = main(raw=files["input"], part=1)
    print(f"Answer part1: {magenta_color}{answer1}{reset_color}")
    answer2 = main(raw=files["input"], part=2)
    print(f"Answer part2: {magenta_color}{answer2}{reset_color}")


if __name__ == "__main__":
    run_tests()
    solve()
