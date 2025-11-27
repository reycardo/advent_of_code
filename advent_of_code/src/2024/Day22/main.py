from __future__ import annotations
from advent_of_code.utils.tools import get_txt_files, read_input, timing_decorator
from advent_of_code.utils.colors import magenta_color, reset_color
from typing import List
import itertools

files = get_txt_files(__file__)
#########
# Start #
#########


class Puzzle:
    def __init__(self, text_input):
        self.input: List[str] = text_input
        self.input_parsed: List[int] = list(map(int, self.input))

    def calc_secret_number_1(self, secret_number: int) -> int:
        return self.prune_number(self.mix_number(secret_number * (2**6), secret_number))

    def calc_secret_number_2(self, secret_number: int) -> int:
        return self.prune_number(
            self.mix_number(secret_number // (2**5), secret_number)
        )

    def calc_secret_number_3(self, secret_number: int) -> int:
        return self.prune_number(
            self.mix_number(secret_number * (2**11), secret_number)
        )

    def mix_number(self, number: int, secret_number: int) -> int:
        return number ^ secret_number

    def prune_number(self, secret_number: int) -> int:
        return secret_number % (2**24)

    def create_secret_number(self, secret_number: int) -> int:
        return self.calc_secret_number_3(
            self.calc_secret_number_2(self.calc_secret_number_1(secret_number))
        )

    def run_create_secret_number_n_times(self, secret_number: int, n: int) -> int:
        result = secret_number
        secret_digits = [result % 10]
        for _ in range(n):
            result = self.create_secret_number(result)
            secret_digits.append(result % 10)
        return result, secret_digits

    def calculate_differences(self, lst):
        return [b - a for a, b in itertools.pairwise(lst)]

    def create_rolling_window_dict(self, a, b, window_size=4):
        result = {}
        for i in range(len(a) - window_size + 1):
            window = tuple(a[i : i + window_size])
            if window not in result:
                value = b[i + window_size] if i + window_size < len(b) else None
                result[window] = value
        return result

    def aggregate_rolling_window_values(self, rolling_windows):
        aggregated_result = {}
        for window_dict in rolling_windows:
            for key, value in window_dict.items():
                if key not in aggregated_result:
                    aggregated_result[key] = 0
                if value is not None:
                    aggregated_result[key] += value
        return aggregated_result

    def solve(self, part):
        if part == 1:
            result = [
                self.run_create_secret_number_n_times(secret_number, 2000)[0]
                for secret_number in self.input_parsed
            ]
            return sum(result)
        elif part == 2:
            result = [
                self.run_create_secret_number_n_times(secret_number, 2000)[1]
                for secret_number in self.input_parsed
            ]
            differences = [
                self.calculate_differences(buyer_prices) for buyer_prices in result
            ]
            rolling_windows = [
                self.create_rolling_window_dict(buyer_difference, buyer_price)
                for buyer_difference, buyer_price in zip(differences, result)
            ]
            aggregated_result = self.aggregate_rolling_window_values(rolling_windows)
            return max(aggregated_result.values())


@timing_decorator
def main(raw, part):
    text_input = read_input(raw)
    input_parsed = [i if i else "" for i in text_input]
    puzzle = Puzzle(input_parsed)
    return puzzle.solve(part)


def run_tests():
    print("\nRunning Tests:")
    assert main(raw=files["test"], part=1) == 37327623
    assert main(raw=files["test2"], part=2) == 23

    # solutions
    print("\nRunning Solutions:")
    assert main(raw=files["input"], part=1) == 16619522798
    # assert main(raw=files["input"], part=2) == 662726441391898


def solve():
    print("\nSolving:")
    answer1 = main(raw=files["input"], part=1)
    print(f"Answer part1: {magenta_color}{answer1}{reset_color}")
    answer2 = main(raw=files["input"], part=2)
    print(f"Answer part2: {magenta_color}{answer2}{reset_color}")


if __name__ == "__main__":
    run_tests()
    solve()
