import sys
sys.path.insert(0, './')
from utils import tools

input_raw = r'2020\Day1\input.txt'
test_raw = r'2020\Day1\test.txt'

def main1(raw):
    # read inputs from file
    input = tools.read_input(raw)
    
    # convert to all elements int
    input = [int(i) for i in input if i]

    # return a*b if a+b=2020 for any a,b in input
    return [a*b for a in input for b in input if a+b==2020][0]

def run_tests():
    assert main1(test_raw) == 514579

    
if __name__ == '__main__':
    run_tests()
    answer = main1(input_raw)
    print(answer)