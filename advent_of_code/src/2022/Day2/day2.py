import os
import sys

sys.path.insert(0, "./")
from utils import tools

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
input_raw = os.path.join(__location__, "input.txt")
test_raw = os.path.join(__location__, "test.txt")

#########
# Start #
#########


def parse_input(input):
    return [x.split(" ") for x in input if x]


class Strategy:
    shape_selected_score = {"X": 1, "Y": 2, "Z": 3}
    outcome_score = {"won": 6, "draw": 3, "lost": 0}

    def __init__(self, input: list):
        self.input = input
        self.round_scores = [self.round_score(round) for round in input]
        self.score = sum(self.round_scores)
        self.round_scores_pt2 = [self.round_score_pt2(round) for round in input]
        self.score_pt2 = sum(self.round_scores_pt2)

    def round_score(self, round: list):
        match (round[0], round[1]):
            case ("A", "X"):  # rock vs rock
                return self.outcome_score["draw"] + self.shape_selected_score["X"]
            case ("A", "Y"):  # rock vs paper
                return self.outcome_score["won"] + self.shape_selected_score["Y"]
            case ("A", "Z"):  # rock vs scissors
                return self.outcome_score["lost"] + self.shape_selected_score["Z"]
            case ("B", "X"):  # paper vs rock
                return self.outcome_score["lost"] + self.shape_selected_score["X"]
            case ("B", "Y"):  # paper vs paper
                return self.outcome_score["draw"] + self.shape_selected_score["Y"]
            case ("B", "Z"):  # paper vs scissors
                return self.outcome_score["won"] + self.shape_selected_score["Z"]
            case ("C", "X"):  # scissors vs rock
                return self.outcome_score["won"] + self.shape_selected_score["X"]
            case ("C", "Y"):  # scissors vs paper
                return self.outcome_score["lost"] + self.shape_selected_score["Y"]
            case ("C", "Z"):  # scissors vs scissors
                return self.outcome_score["draw"] + self.shape_selected_score["Z"]

    def round_score_pt2(self, round: list):
        match (round[0], round[1]):
            case ("A", "X"):  # rock vs lost
                return self.outcome_score["lost"] + self.shape_selected_score["Z"]
            case ("A", "Y"):  # rock vs draw
                return self.outcome_score["draw"] + self.shape_selected_score["X"]
            case ("A", "Z"):  # rock vs won
                return self.outcome_score["won"] + self.shape_selected_score["Y"]
            case ("B", "X"):  # paper vs lost
                return self.outcome_score["lost"] + self.shape_selected_score["X"]
            case ("B", "Y"):  # paper vs draw
                return self.outcome_score["draw"] + self.shape_selected_score["Y"]
            case ("B", "Z"):  # paper vs won
                return self.outcome_score["won"] + self.shape_selected_score["Z"]
            case ("C", "X"):  # scissors vs lost
                return self.outcome_score["lost"] + self.shape_selected_score["Y"]
            case ("C", "Y"):  # scissors vs draw
                return self.outcome_score["draw"] + self.shape_selected_score["Z"]
            case ("C", "Z"):  # scissors vs won
                return self.outcome_score["won"] + self.shape_selected_score["X"]


def main(raw, part):
    input = tools.read_input(raw)
    input = parse_input(input)
    strategy = Strategy(input=input)
    if part == 1:
        return strategy.score
    elif part == 2:
        return strategy.score_pt2
    else:
        raise ValueError("part must be 1 or 2, instead of: " + part)


def run_tests():
    assert main(test_raw, 1) == 15
    assert main(test_raw, 2) == 12
    # solutions
    assert main(input_raw, 1) == 10816
    assert main(input_raw, 2) == 11657


if __name__ == "__main__":
    run_tests()
    answer1 = main(input_raw, 1)
    answer2 = main(input_raw, 2)
    print("Answer part1: {}".format(answer1))
    print("Answer part2: {}".format(answer2))
