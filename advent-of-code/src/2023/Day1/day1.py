from utils.tools import get_txt_files, read_input, timing_decorator
from utils.colors import magenta_color, reset_color
from itertools import groupby

files = get_txt_files(__file__)
#########
# Start #
#########


class ElfCalories:
    def __init__(self, text_input: list):
        self.input = text_input
        self.elf_calorie_dict = self.get_elf_dict()
        self.elf_count = len(self.elf_calorie_dict)

    def get_elf_dict(self):
        d = {
            elf: list(sub[1])
            for elf, sub in enumerate(groupby(self.input, key=bool))
            if sub[0]
        }  # groups into an enumerated dict if key is not ''
        return {
            k: (v, sum(v)) for k, v in d.items()
        }  # returns dict where key is elf number, v is list of elf calories, sum(v) is total cals elf has

    def get_max(self, number):
        # sorts descending, gets top number
        return sum(
            n
            for _, n in sorted(
                self.elf_calorie_dict.values(), key=lambda t: t[1], reverse=True
            )[:number]
        )


@timing_decorator
def main(raw, part):
    text_input = read_input(raw)
    input_parsed = [int(i) if i else "" for i in text_input]
    elf_cals = ElfCalories(input_parsed)
    if part == 1:
        return elf_cals.get_max(1)
    elif part == 2:
        return elf_cals.get_max(3)
    else:
        raise ValueError("part must be 1 or 2, instead of: " + part)


def run_tests():
    print(f"\nRunning Tests:")
    assert main(files["test"], 1) == 24000
    assert main(files["test"], 2) == 45000

    # solutions
    assert main(files["input"], 1) == 66616
    assert main(files["input"], 2) == 199172


def run_solution():
    print(f"\nRunning Solutions:")
    answer1 = main(files["input"], 1)
    print(f"Answer part1: {magenta_color}{answer1}{reset_color}")
    answer2 = main(files["input"], 2)
    print(f"Answer part2: {magenta_color}{answer2}{reset_color}")


if __name__ == "__main__":
    run_tests()
    run_solution()
