from utils.tools import get_txt_files, read_input
from itertools import groupby

files = get_txt_files(__file__)
input_raw = files["input"]
test_raw = files["test"]
#########
# Start #
#########


class ElfCalories:
    def __init__(self, text_input: list):
        self.input = text_input
        self.elf_calorie_dict = self.get_elf_dict()
        self.elf_count = len(self.elf_calorie_dict)

    def get_elf_dict(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        d = {
            elf: list(sub[1])
            for elf, sub in enumerate(groupby(self.input, key=bool))
            if sub[0]
        }  # groups into an enumerated dict if key is not ''
        return {
            k: (v, sum(v)) for k, v in d.items()
        }  # returns dict where key is elf number, v is list of elf calories, sum(v) is total cals elf has

    def get_max(self, number):
        """_summary_

        Args:
            number (_type_): _description_

        Returns:
            _type_: _description_
        """
        # sorts descending, gets top number
        return sum(
            n
            for _, n in sorted(
                self.elf_calorie_dict.values(), key=lambda t: t[1], reverse=True
            )[:number]
        )


def main(raw, part):
    """_summary_

    Args:
        raw (_type_): _description_
        part (_type_): _description_

    Raises:
        ValueError: _description_

    Returns:
        _type_: _description_
    """
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
    """_summary_"""
    assert main(test_raw, 1) == 24000
    assert main(test_raw, 2) == 45000
    # solutions
    assert main(input_raw, 1) == 66616
    assert main(input_raw, 2) == 199172


if __name__ == "__main__":
    run_tests()
    answer1 = main(input_raw, 1)
    answer2 = main(input_raw, 2)
    print(f"Answer part1: {answer1}")
    print(f"Answer part2: {answer2}")
