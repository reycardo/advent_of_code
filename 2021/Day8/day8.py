import os
import sys
sys.path.insert(0, './')
from utils import tools
from collections import Counter
import copy

raw = r'2021\Day8\test.txt'

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
input_raw = os.path.join(__location__,'input.txt')
test_raw = os.path.join(__location__,'test.txt')

#########
# Start #
#########

def parse_input(input):            
    return [line.split('|') for line in input]


# match_digit_segment
mds = {
    0: list(set(['top','top_L','top_R','bot','bot_L','bot_R'])),
    1: list(set(['top_R','bot_R'])),
    2: list(set(['top','top_R','mid','bot','bot_L'])),
    3: list(set(['top','top_R','mid','bot','bot_R'])),
    4: list(set(['top_L','top_R','mid','bot_R'])),
    5: list(set(['top','top_L','mid','bot','bot_R'])),
    6: list(set(['top','top_L','mid','bot','bot_L','bot_R'])),
    7: list(set(['top','top_R','bot_R'])),
    8: list(set(['top','top_L','top_R','mid','bot','bot_L','bot_R'])),
    9: list(set(['top','top_L','top_R','mid','bot','bot_R']))
}

#signal2segment
o_sig2seg = {
    'a': "",
    'b': "",
    'c': "",
    'd': "",
    'e': "",
    'f': "",
    'g': ""
}

#signal2segment
o_seg2sig = {
    'top':   '',
    'top_L': '',
    'top_R': '',
    'mid':   '',
    'bot':   '',
    'bot_L': '',
    'bot_R': ''
}

info = {
    'top':   [0,2,3,5,6,7,8,9],
    'top_L': [0,4,5,6,8,9],
    'top_R': [0,1,2,3,4,7,8,9],
    'mid':   [2,3,4,5,6,8,9],
    'bot':   [0,2,3,5,6,8,9],
    'bot_L': [0,2,6,8],
    'bot_R': [0,1,3,4,5,6,7,8,9]
}

def find_segments(entry,sig2seg,seg2sig):
    counts = Counter(tools.flatten(entry[0].split()))
    for i in counts:
        if counts[i] == 4:
            sig2seg[i] = 'bot_L'
            seg2sig['bot_L'] = i
        elif counts[i] == 6:
            sig2seg[i] = 'top_L'
            seg2sig['top_L'] = i
        elif counts[i] == 9:
            sig2seg[i] = 'bot_R'
            seg2sig['bot_R'] = i

    #find top_R by comparing bot_R letter with letters composing number 1
    seg2sig['top_R'] = ''.join([word for word in entry[0].split() if len(word) == 2]).replace(seg2sig['bot_R'],'')
    sig2seg[seg2sig['top_R']] = 'top_R'

    #find top by comparing bot_R and top_R letters with letters composing number 7
    seg2sig['top'] = ''.join([word for word in entry[0].split() if len(word) == 3]).replace(seg2sig['bot_R'],'').replace(seg2sig['top_R'],'')
    sig2seg[seg2sig['top']] = 'top'

    #find mid by comparing bot_R, top_R and top_L letters with letters composing number 4
    seg2sig['mid'] = ''.join([word for word in entry[0].split() if len(word) == 4]).replace(seg2sig['bot_R'],'').replace(seg2sig['top_R'],'').replace(seg2sig['top_L'],'')
    sig2seg[seg2sig['mid']] = 'mid'
    
    #find bot, the last still empty
    seg2sig['bot'] = ''.join([k for k, v in sig2seg.items() if not v])
    sig2seg[seg2sig['bot']] = 'bot'            
    
    return sig2seg


def find_possible_segments(input,o_sig2seg,o_seg2sig):
    final = []    
    for entry in input:   
        sig2seg = o_sig2seg.copy()
        seg2sig = o_seg2sig.copy()
        sig2seg = find_segments(entry,sig2seg,seg2sig)
        output_value = []
        for word in entry[1].split():
            search_mds = list(set([sig2seg[letter] for letter in word]))
            output_value = output_value + ([k for k, v in mds.items() if v == search_mds])        
        final.append(int("".join(map(str,output_value))))
    return sum(final)

def count_easy_digits(input):
    output_length = [list(map(len,entry[1].split())) for entry in input]
    return len([length for length in tools.flatten(output_length) if length in [len(mds[1]),len(mds[4]),len(mds[7]),len(mds[8])]])


def main(raw,part):
    # read inputs from file
    input = tools.read_input(raw)
    input = parse_input(input)
    if part == 1:                                
        return count_easy_digits(input)
    elif part == 2:        
        return find_possible_segments(input,o_sig2seg,o_seg2sig)
    else:
        raise ValueError("part must be 1 or 2, instead of: " + str(part))


def run_tests():
    assert main(test_raw,1) == 26
    assert main(test_raw,2) == 61229
    # solutions
    assert main(input_raw,1) == 303
    assert main(input_raw,2) == 961734
    
    
if __name__ == '__main__':
    run_tests()
    answer1 = main(input_raw,1)
    answer2 = main(input_raw,2)    
    print("Answer part1: {}".format(answer1))
    print("Answer part2: {}".format(answer2))