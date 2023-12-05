from utils.tools import get_txt_files, read_input, timing_decorator
from utils.colors import magenta_color, reset_color
from typing import List, Dict, Union
import re

files = get_txt_files(__file__)
#########
# Start #
#########


class Game:
    bag = {
        "red": 12,
        "green": 13,
        "blue": 14,
    }

    def __init__(self, text_input: List[str]):
        """
        Initialize the Calibration object.

        Args:
            text_input (list): A list of strings containing input text.
        """
        self.input = text_input
        self.parse_input()

    def parse_input(self):
        self.parsed_input = [self.parse_game_string(element) for element in self.input]

    def parse_game_string(self, game_string: str) -> Dict[int, List[Dict[str, int]]]:
        sections = game_string.split(":", 1)
        match = re.search(r"\d+", sections[0])

        if match:
            game_number = int(match.group())
        else:
            # Handle the case where no game number is found
            raise ValueError("No game number found in the input string.")

        result = []

        for entry in sections[1].split(";"):
            entry_list = entry.strip().split(",")
            entry_dict = {
                color.split()[1]: int(color.split()[0]) for color in entry_list
            }
            result.append(entry_dict)

        return {game_number: result}

    def check_game(self, game: List[dict]):
        max_counts = {"red": 0, "green": 0, "blue": 0}
        for bag in game:
            for color, count in bag.items():
                max_counts[color] = max(max_counts[color], count)

        result = 1
        for value in max_counts.values():
            result *= value
        return any(max_counts[color] > self.bag[color] for color in max_counts), result

    def solve(self, part):
        if part == 1:
            result = [
                game_key
                for game_dict in self.parsed_input
                for game_key, game_values in game_dict.items()
                if not self.check_game(game_values)[0]
            ]
            return sum(result)
        if part == 2:
            result = [
                self.check_game(game_values)[1]
                for game_dict in self.parsed_input
                for _, game_values in game_dict.items()
            ]
            return sum(result)


@timing_decorator
def main(raw, part):
    text_input = read_input(raw)
    input_parsed = [i if i else "" for i in text_input]
    game = Game(input_parsed)
    return game.solve(part)


def run_tests():
    print(f"\nRunning Tests:")
    assert main(raw=files["test"], part=1) == 8
    assert main(raw=files["test"], part=2) == 2286

    # solutions
    print(f"\nRunning Solutions:")
    assert main(raw=files["input"], part=1) == 2716
    assert main(raw=files["input"], part=2) == 72227


def solve():
    print(f"\nSolving:")
    answer1 = main(raw=files["input"], part=1)
    print(f"Answer part1: {magenta_color}{answer1}{reset_color}")
    answer2 = main(raw=files["input"], part=2)
    print(f"Answer part2: {magenta_color}{answer2}{reset_color}")


if __name__ == "__main__":
    run_tests()
    solve()
