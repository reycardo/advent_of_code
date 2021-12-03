import os
import sys
sys.path.insert(0, './')
from utils import tools
import pandas as pd
import numpy as np

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
input_raw = os.path.join(__location__,'input.txt')
test_raw = os.path.join(__location__,'test.txt')

#########
# Start #
#########

def parse_input(input):                     
    return pd.DataFrame([[*x] for x in input if x])

def get_gamma(df):
    return ''.join(df.mode(axis='rows').values.tolist()[0])

def get_epsilon(gamma):
    return gamma.replace('1', '2').replace('0', '1').replace('2', '0')

def get_oxygen(df):
    columns = df.columns
    for i in columns:
        val_counts = df[i].value_counts()
        if len(val_counts) == 1:
            mode = df[i].values.tolist()[0]            
        elif val_counts['0'] > val_counts['1']:
            mode = '0'
        else:
            mode = '1'
        df = df.loc[df[i] == mode]
    return ''.join(df.values[0])

def get_CO2(df):
    columns = df.columns
    for i in columns:
        val_counts = df[i].value_counts()
        if len(val_counts) == 1:
            mode = df[i].values.tolist()[0]            
        elif val_counts['1'] < val_counts['0']:
            mode = '1'
        else:
            mode = '0'        
        df = df.loc[df[i] == mode]
    return ''.join(df.values[0])

def main(raw,part):
    # read inputs from file
    input = tools.read_input(raw)
        
    input = parse_input(input)
    if part == 1:        
        gamma = get_gamma(input)
        epsilon = get_epsilon(gamma)
        return int(gamma,2) * int(epsilon,2)
    elif part == 2:        
        oxygen = get_oxygen(input)
        CO2 = get_CO2(input)
        return int(oxygen,2) * int(CO2,2)
    else:
        raise ValueError("part must be 1 or 2, instead of: " + part)


def run_tests():
    assert main(test_raw,1) == 198
    assert main(test_raw,2) == 230
    # solutions
    assert main(input_raw,1) == 3813416
    assert main(input_raw,2) == 2990784
    

    
if __name__ == '__main__':
    run_tests()
    answer1 = main(input_raw,1)
    answer2 = main(input_raw,2)    
    print("Answer part1: {}".format(answer1))
    print("Answer part2: {}".format(answer2))