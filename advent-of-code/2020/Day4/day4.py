import re
import os
import sys
sys.path.insert(0, './')
from utils import tools

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
input_raw = os.path.join(__location__,'input.txt')
test_raw = os.path.join(__location__,'test.txt')
test_invalid_raw = os.path.join(__location__,'test_invalid.txt')
test_valid_raw = os.path.join(__location__,'test_valid.txt')

# For interactive testing
raw = r'2020\Day4\test_valid.txt'

#########
# Start #
#########

def fields_2_dict(passport):    
    return { field.split(':')[0]: field.split(':')[1] for field in passport }


def preprocess(input):
    return [group.split() for group in input]


def check_if_valid(passport,optional,expected):
    required = [x for x in expected if x not in optional]
    pp_reqs = [x for x in passport.keys() if x not in optional]    
    if sorted(pp_reqs) == sorted(required):
        return True
    else:
        return False


def check_year(value,lower,upper):    
    if int(value) >= lower and int(value) <= upper:
        return True
    else:
        return False             


def check_height(value):
    match = re.match(r"(\d+)(in|cm)",value)
    if match:
        items = match.groups()
        if items[1] == 'cm':
            if int(items[0]) >= 150 and int(items[0]) <= 193:
                return True
            else:
                return False                        
        elif items[1] == 'in':
            if int(items[0]) >= 59 and int(items[0]) <= 76:
                return True
            else:
                return False        
        else:
            return False
    else:
        return False


def check_hcl(value):    
    match = re.match(r"^#[a-fA-F0-9]{6}",value)
    if match:
        return True
    else:
        return False   


def check_ecl(value):        
    expected = ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']
    if value in expected:
        return True
    else:
        return False   


def check_pid(value):        
    match = re.match(r"(\d{9})",value)
    if match and match.groups()[0] == value:
        return True
    else:
        return False   


def main(raw,part):
    # read inputs from file
    input = preprocess(tools.read_input(raw,'\n\n'))
    input = [fields_2_dict(passport) for passport in input]
    expected = ['byr','iyr','eyr','hgt','hcl','ecl','pid','cid']
    optional = ['cid']
    if part == 1:        
        return sum([check_if_valid(passport,optional,expected) for passport in input])
    elif part == 2:
        passports_req_fields = [passport for passport in input if check_if_valid(passport,optional,expected)]
        return sum([check_year(passport['byr'],1920,2002) 
                and check_year(passport['iyr'],2010,2020) 
                and check_year(passport['eyr'],2020,2030) 
                and check_height(passport['hgt']) 
                and check_hcl(passport['hcl']) 
                and check_ecl(passport['ecl']) 
                and check_pid(passport['pid']) 
            for passport in passports_req_fields])         
    else:
        raise ValueError("part must be 1 or 2, instead of: " + part)
    

def run_tests():    
    assert main(test_raw,1) == 2    
    assert main(test_invalid_raw,2) == 0
    assert main(test_valid_raw,2) == 4
    assert check_year('2002',1920,2002) == True
    assert check_year('2003',1920,2002) == False
    assert check_height('60in') == True
    assert check_height('190cm') == True
    assert check_height('190in') == False
    assert check_height('190') == False
    assert check_hcl('#123abc') == True
    assert check_hcl('#123abz') == False
    assert check_hcl('123abc') == False
    assert check_ecl('brn') == True
    assert check_ecl('wat') == False
    assert check_pid('000000001') == True
    assert check_pid('0123456789') == False
    # solutions
    assert main(input_raw,1) == 216
    assert main(input_raw,2) == 150
    

if __name__ == '__main__':
    run_tests()
    answer1 = main(input_raw,1)    
    answer2 = main(input_raw,2)    
    print("Answer part1: {}".format(answer1))        
    print("Answer part2: {}".format(answer2))    