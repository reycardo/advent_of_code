from utils.tools import get_txt_files, read_input, timing_decorator
from utils.colors import magenta_color, reset_color
from typing import List

files = get_txt_files(__file__)
#########
# Start #
#########


class FileBlocks:
    def __init__(self, id: int, amount: int, position: int):
        self.id = id
        self.amount = amount
        self.position = position
        self.seen = False


class FreeSpaces:
    def __init__(self, amount: int, position: int):
        self.files: List[FileBlocks] = []
        self.amount = amount
        self.position = position

    def add_file(self, file: FileBlocks):
        if file.amount <= self.amount:
            self.files.append(FileBlocks(file.id, file.amount, position=self.position))
            self.amount -= file.amount
            self.position += file.amount
            file.amount -= file.amount
        else:
            passing_amount = file.amount - self.amount
            if passing_amount > self.amount:
                passing_amount = self.amount
            self.files.append(
                FileBlocks(file.id, passing_amount, position=self.position)
            )
            self.amount -= passing_amount
            self.position += passing_amount
            file.amount -= passing_amount


class Puzzle:
    def __init__(self, text_input):
        self.input = text_input[0]
        self.initialize_disk()
        self.checksum = 0
        self.remove_empties()

    def remove_empties(self):
        for i in self.disk:
            if isinstance(i, FreeSpaces):
                if i.amount == 0:
                    self.disk.remove(i)

    def initialize_disk(self):
        self.disk = []
        pos = 0
        for i in range(0, len(self.input), 2):
            self.disk.append(FileBlocks(int(i) // 2, int(self.input[i]), pos))
            pos += int(self.input[i])
            if i + 1 < len(self.input):
                self.disk.append(FreeSpaces(int(self.input[i + 1]), pos))
                pos += int(self.input[i + 1])

    def get_first_free_space(self):
        for i in self.disk:
            if isinstance(i, FreeSpaces):
                if i.amount > 0:
                    return i

    def get_first_free_space_that_fits(self, size):
        for i in self.disk:
            if isinstance(i, FreeSpaces):
                if i.amount >= size:
                    return i
        return None

    def move_file(self, file: FileBlocks):
        # moves this file from self.disk to the first available FreeSpace on self.disk

        while file.amount > 0:
            # find the first FreeSpace
            free_space = self.get_first_free_space()

            if free_space.position > file.position:
                return False
            # move the file to the first FreeSpace
            free_space.add_file(file)
        return True

    def move_file_blocks(self, file: FileBlocks):
        # moves this file from self.disk to the first available FreeSpace on self.disk

        # find the first FreeSpace
        free_space = self.get_first_free_space_that_fits(file.amount)
        if isinstance(free_space, FreeSpaces):
            # move the file to the first FreeSpace
            if free_space.position < file.position:
                free_space.add_file(file)
                self.disk.remove(file)
        file.seen = True

    def get_last_file_block(self):
        for i in self.disk[::-1]:
            if isinstance(i, FileBlocks):
                if i.amount > 0:
                    return i

    def get_unseen_file_block(self):
        for i in self.disk[::-1]:
            if isinstance(i, FileBlocks):
                if not i.seen:
                    return i
        return None

    def fragment_disk(self):
        available_free_spaces = True
        while available_free_spaces:
            file = self.get_last_file_block()
            available_free_spaces = self.move_file(file=file)

    def fragment_disk_new(self):
        while True:
            file = self.get_unseen_file_block()
            if not file:
                break
            self.move_file_blocks(file=file)

    def calculate_checksum(self):
        for block in self.disk:
            if isinstance(block, FreeSpaces):
                for file in block.files:
                    for i in range(file.amount):
                        self.checksum += file.id * (file.position + i)
            if isinstance(block, FileBlocks):
                for i in range(block.amount):
                    self.checksum += block.id * (block.position + i)

    def solve(self, part):
        if part == 1:
            self.fragment_disk()
            self.calculate_checksum()
            return self.checksum
        elif part == 2:
            self.fragment_disk_new()
            self.calculate_checksum()
            return self.checksum


@timing_decorator
def main(raw, part):
    text_input = read_input(raw)
    input_parsed = [i if i else "" for i in text_input]
    puzzle = Puzzle(input_parsed)
    return puzzle.solve(part)


def run_tests():
    print(f"\nRunning Tests:")
    assert main(raw=files["test"], part=1) == 1928
    assert main(raw=files["test"], part=2) == 2858
    assert main(raw=files["test2"], part=2) == 132

    # solutions
    print(f"\nRunning Solutions:")
    assert main(raw=files["input"], part=1) == 6259790630969
    assert main(raw=files["input"], part=2) == 6289564433984


def solve():
    print(f"\nSolving:")
    answer1 = main(raw=files["input"], part=1)
    print(f"Answer part1: {magenta_color}{answer1}{reset_color}")
    answer2 = main(raw=files["input"], part=2)
    print(f"Answer part2: {magenta_color}{answer2}{reset_color}")


if __name__ == "__main__":
    run_tests()
    solve()
