from utils.tools import get_txt_files, read_input, timing_decorator
from utils.colors import magenta_color, reset_color
from typing import List

files = get_txt_files(__file__)
#########
# Start #
#########


class Correspondence:
    def __init__(self, source, destination, range) -> None:
        self.source = source
        self.destination = destination
        self.range = range

    def correspond_mapping(self, number):
        if self.source <= number <= self.source + self.range:
            difference = number - self.source
            return self.destination + difference
        else:
            return None


class Map:
    def __init__(self, correspondence_list: List[Correspondence]):
        self.correspondences = correspondence_list

    def find_correspondence(self, number):
        for correspondence in self.correspondences:
            if correspondence.correspond_mapping(number):
                return correspondence.correspond_mapping(number)
        return number


class Almanac:
    def __init__(self, text_input):
        self.input = text_input
        self.seeds = [
            int(seed) for seed in self.input[0].split(":")[1].strip().split(" ")
        ]
        self.seed_soil_map = self.parse_map(
            "seed-to-soil map:", "soil-to-fertilizer map:"
        )
        self.soil_fertilizer_map = self.parse_map(
            "soil-to-fertilizer map:", "fertilizer-to-water map:"
        )
        self.fertilizer_water_map = self.parse_map(
            "fertilizer-to-water map:", "water-to-light map:"
        )
        self.water_light_map = self.parse_map(
            "water-to-light map:", "light-to-temperature map:"
        )
        self.light_temperature_map = self.parse_map(
            "light-to-temperature map:", "temperature-to-humidity map:"
        )
        self.temperature_humidity_map = self.parse_map(
            "temperature-to-humidity map:", "humidity-to-location map:"
        )
        self.humidity_location_map = self.parse_map("humidity-to-location map:", "")

    def parse_map(self, start_key, end_key):
        if end_key == "":
            map_data = self.input[self.input.index(start_key) + 1 :]
        else:
            map_data = self.input[
                self.input.index(start_key) + 1 : self.input.index(end_key) - 1
            ]
        map_data = [list(map(int, row.split(" "))) for row in map_data]
        return Map(
            [
                Correspondence(source=row[1], destination=row[0], range=row[2])
                for row in map_data
            ]
        )

    def get_location_from_seed(self, seed):
        soil = self.seed_soil_map.find_correspondence(seed)
        fertilizer = self.soil_fertilizer_map.find_correspondence(soil)
        water = self.fertilizer_water_map.find_correspondence(fertilizer)
        light = self.water_light_map.find_correspondence(water)
        temperature = self.light_temperature_map.find_correspondence(light)
        humidity = self.temperature_humidity_map.find_correspondence(temperature)
        location = self.humidity_location_map.find_correspondence(humidity)
        return location

    def test_all_seeds(self):
        self.locations = []
        for i in range(0, len(self.seeds), 2):
            self.locations.extend(
                map(
                    self.get_location_from_seed,
                    range(self.seeds[i], self.seeds[i] + self.seeds[i + 1] + 1),
                )
            )
        return min(self.locations)

    def check_seed(self, seed):
        for i in range(0, len(self.seeds), 2):
            if self.seeds[i] <= seed <= self.seeds[i] + self.seeds[i + 1] - 1:
                return True
        return False

    def solve(self, part):
        if part == 1:
            self.locations = list(map(self.get_location_from_seed, self.seeds))
            return min(self.locations)
        if part == 2:
            pass
            # return self.test_all_seeds() # NOT DOING THIS


@timing_decorator
def main(raw, part):
    text_input = read_input(raw)
    input_parsed = [i if i else "" for i in text_input]
    puzzle = Almanac(input_parsed)
    return puzzle.solve(part)


def run_tests():
    print(f"\nRunning Tests:")
    assert main(raw=files["test"], part=1) == 35
    assert main(raw=files["test"], part=2) == 46

    # solutions
    print(f"\nRunning Solutions:")
    assert main(raw=files["input"], part=1) == 265018614
    # assert main(raw=files["input"], part=2) ==


def solve():
    print(f"\nSolving:")
    answer1 = main(raw=files["input"], part=1)
    print(f"Answer part1: {magenta_color}{answer1}{reset_color}")
    # answer2 = main(raw=files["input"], part=2)
    # print(f"Answer part2: {magenta_color}{answer2}{reset_color}")


if __name__ == "__main__":
    run_tests()
    solve()
