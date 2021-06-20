def read_input(file):
    with open(file, "r") as tf:        
        return tf.read().split()

def read_input_new_line_sep(file):
    with open(file, "r") as tf:        
        input = tf.read().split('\n')
        return [x for x in input if x]

def read_input_blank_separator(file):
    with open(file, "r") as tf:        
        input = tf.read().split('\n\n')
        return [group.split() for group in input]

def flatten(t):
    return [item for sublist in t for item in sublist]