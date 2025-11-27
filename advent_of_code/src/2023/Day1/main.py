from utils.tools import get_txt_files, read_input, timing_decorator
from advent_of_code.utils.colors import magenta_color, reset_color
from typing import List, Tuple, Union

files = get_txt_files(__file__)
#########
# Start #
#########


class Calibration:
    digits = [str(digit) for digit in range(1, 10)]
    digits_str = [
        "one",
        "two",
        "three",
        "four",
        "five",
        "six",
        "seven",
        "eight",
        "nine",
    ]

    def __init__(self, text_input: List[str]):
        """
        Initialize the Calibration object.

        Args:
            text_input (list): A list of strings containing input text.
        """
        self.input = text_input

    def get_calib_values(
        self, input_string: str
    ) -> Tuple[Union[int, str, None], Union[int, str, None]]:
        """
        Extract the first and last digits from the input string.

        Args:
            input_string (str): The input string.

        Returns:
            Tuple[int, int]: A tuple containing the first and last digits.
        """
        # Find the first digit
        first_digit = next((char for char in input_string if char.isdigit()), None)

        # Find the last digit
        reversed_string = input_string[::-1]
        last_digit = next((char for char in reversed_string if char.isdigit()), None)

        return first_digit, last_digit

    def get_spelled_digits(
        self, input_string: str
    ) -> Tuple[Union[int, str], Union[int, str]]:
        """
        Extract the first and last spelled-out digits from the input string.

        Args:
            input_string (str): The input string.

        Returns:
            Tuple[Union[int, str], Union[int, str]]: A tuple containing the first and last spelled-out digits.
        """
        numbers_location_dict = {
            number: (input_string.find(number), input_string.rfind(number))
            for number in self.digits_str + self.digits
            if number in input_string
        }
        first_element = min(
            numbers_location_dict, key=lambda key: numbers_location_dict[key][0]
        )
        last_element = max(
            numbers_location_dict, key=lambda key: numbers_location_dict[key][1]
        )
        first_element = self.get_number(first_element)
        last_element = self.get_number(last_element)
        return first_element, last_element

    def get_number(self, occurrence):
        """
        Convert a digit occurrence to its corresponding integer value.

        Args:
            occurrence (str): The digit occurrence.

        Returns:
            Union[int, str]: The corresponding integer value.
        """
        if occurrence.isdigit():
            return int(occurrence)
        else:
            return self.digits_str.index(occurrence) + 1

    def join_into_number(self, first_digit, last_digit) -> int:
        """
        Combine the first and last digits into a single integer.

        Args:
            first_digit (Union[int, str]): The first digit.
            last_digit (Union[int, str]): The last digit.

        Returns:
            int: The combined integer value.
        """
        return int(str(first_digit) + str(last_digit))

    def solve(self, part: int) -> int:
        """
        Get the calibration document value for a given part.

        Args:
            part (int): The part number (1 or 2).

        Returns:
            int: The calibration document value.
        """
        if part == 1:
            doc = [
                self.join_into_number(*self.get_calib_values(element))
                for element in self.input
            ]
        elif part == 2:
            doc = [
                self.join_into_number(*self.get_spelled_digits(element))
                for element in self.input
            ]
        else:
            raise ValueError("Invalid part number. Use 1 or 2.")
        return sum(doc)


@timing_decorator
def main(raw, part):
    text_input = read_input(raw)
    input_parsed = [i if i else "" for i in text_input]
    puzzle = Calibration(input_parsed)
    return puzzle.solve(part)


def run_tests():
    print(f"\nRunning Tests:")
    assert main(raw=files["test"], part=1) == 142
    assert main(raw=files["test2"], part=2) == 281
    assert main(raw=files["test3"], part=2) == 33

    # solutions
    print(f"\nRunning Solutions:")
    assert main(raw=files["input"], part=1) == 55971
    assert main(raw=files["input"], part=2) == 54719


def solve():
    print(f"\nSolving:")
    answer1 = main(raw=files["input"], part=1)
    print(f"Answer part1: {magenta_color}{answer1}{reset_color}")
    answer2 = main(raw=files["input"], part=2)
    print(f"Answer part2: {magenta_color}{answer2}{reset_color}")


if __name__ == "__main__":
    run_tests()
    solve()
