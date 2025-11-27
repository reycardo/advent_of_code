from advent_of_code.utils.tools import get_txt_files, read_input, timing_decorator
from advent_of_code.utils.colors import magenta_color, reset_color
from functools import reduce

files = get_txt_files(__file__)
#########
# Start #
#########


class Puzzle:
    def __init__(self, text_input):
        self.input = text_input
        self.input_parsed, self.input_parsed2 = self.parse_input()

    def parse_input(self):
        parsed_time = [
            int(x) for x in self.input[0].split(":")[1].strip().split(" ") if x
        ]
        parsed_distance = [
            int(x) for x in self.input[1].split(":")[1].strip().split(" ") if x
        ]
        parsed_input_1 = list(zip(parsed_time, parsed_distance))
        parsed_input_2 = [
            (
                int("".join(map(str, parsed_time))),
                int("".join(map(str, parsed_distance))),
            )
        ]
        return parsed_input_1, parsed_input_2

    def get_distance(self, time_pressed, max_time):
        time_remaining = max_time - time_pressed
        distance = time_remaining * time_pressed
        return distance

    def run_all_distances(self, max_time):
        return [
            self.get_distance(time_pressed, max_time)
            for time_pressed in range(max_time)
        ]

    def run_pt2_distances(self):
        record_passed = False
        time_pressed = 0
        while not record_passed:
            if (
                self.get_distance(time_pressed, self.input_parsed2[0][0])
                > self.input_parsed2[0][1]
            ):
                record_passed = True
                return time_pressed
            time_pressed += 1

    def check_records(self, input):
        ways_2_beat = []
        for race in input:
            distances = self.run_all_distances(race[0])
            records = [distance for distance in distances if distance > race[1]]
            ways_2_beat.append(len(records))
        return ways_2_beat

    def solve(self, part):
        if part == 1:
            return reduce(lambda x, y: x * y, self.check_records(self.input_parsed))
        if part == 2:
            answer = self.input_parsed2[0][0] - 2 * self.run_pt2_distances() + 1
            return answer
        # self.check_records(self.input_parsed2)[0]


@timing_decorator
def main(raw, part):
    text_input = read_input(raw)
    input_parsed = [i if i else "" for i in text_input]
    puzzle = Puzzle(input_parsed)
    return puzzle.solve(part)


def run_tests():
    print("\nRunning Tests:")
    assert main(raw=files["test"], part=1) == 288
    assert main(raw=files["test"], part=2) == 71503

    # solutions
    print("\nRunning Solutions:")
    assert main(raw=files["input"], part=1) == 503424
    assert main(raw=files["input"], part=2) == 32607562


def solve():
    print("\nSolving:")
    answer1 = main(raw=files["input"], part=1)
    print(f"Answer part1: {magenta_color}{answer1}{reset_color}")
    answer2 = main(raw=files["input"], part=2)
    print(f"Answer part2: {magenta_color}{answer2}{reset_color}")


if __name__ == "__main__":
    run_tests()
    solve()
